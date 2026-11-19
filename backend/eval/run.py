"""Evaluate TriageAI on the hand-labeled dataset.

    python -m eval.run                   # full run (needs LLM_API_KEY): classification + retrieval
    python -m eval.run --retrieval-only  # no API calls: retrieval metrics + retrieval baseline

Results are written to eval/results.json and served by GET /api/eval.
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from app.config import get_settings
from app.kb import load_articles
from app.llm import LLMError
from app.main import build_provider
from app.prompting import PROMPT_VERSION
from app.retrieval import BM25Retriever
from app.schemas import CATEGORIES
from app.triage import TriageService

EVAL_DIR = Path(__file__).resolve().parent
DATASET = EVAL_DIR / "dataset.jsonl"
INJECTION_CASES = EVAL_DIR.parent / "prompts" / "injection_cases.jsonl"
RESULTS = EVAL_DIR / "results.json"
PRIORITIES = ["P1", "P2", "P3", "P4"]


def load_jsonl(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def confusion_matrix(pairs: list[tuple[str, str]], labels: list[str]) -> dict:
    """matrix[i][j] = count of expected labels[i] predicted as labels[j]."""
    index = {label: i for i, label in enumerate(labels)}
    matrix = [[0] * len(labels) for _ in labels]
    for expected, predicted in pairs:
        if expected in index and predicted in index:
            matrix[index[expected]][index[predicted]] += 1
    return {"labels": labels, "matrix": matrix}


def ratio(hits: int, total: int) -> float | None:
    return round(hits / total, 4) if total else None


def evaluate_retrieval(retriever: BM25Retriever, rows: list[dict]) -> dict:
    labeled = [r for r in rows if r["article"]]
    hit1 = hit3 = 0
    reciprocal: list[float] = []
    by_lang: dict[str, list[int]] = {}
    misses: list[dict] = []
    baseline_pairs: list[tuple[str, str]] = []
    for row in rows:
        results = retriever.search(row["text"], top_k=3)
        ids = [r.article.id for r in results]
        # Baseline classifier: the category of the top BM25 article ("Other" if nothing matches).
        predicted = results[0].article.category if results else "Other"
        baseline_pairs.append((row["category"], predicted))
        if not row["article"]:
            continue
        rank = ids.index(row["article"]) + 1 if row["article"] in ids else None
        hit1 += rank == 1
        hit3 += rank is not None
        reciprocal.append(1 / rank if rank else 0.0)
        stats = by_lang.setdefault(row["language"], [0, 0])
        stats[0] += rank is not None
        stats[1] += 1
        if rank is None:
            misses.append({"id": row["id"], "expected": row["article"], "retrieved": ids})
    baseline_correct = sum(e == p for e, p in baseline_pairs)
    return {
        "labeled_tickets": len(labeled),
        "hit_rate_at_1": ratio(hit1, len(labeled)),
        "hit_rate_at_3": ratio(hit3, len(labeled)),
        "mrr_at_3": round(statistics.mean(reciprocal), 4) if reciprocal else None,
        "hit_rate_at_3_by_language": {
            lang: {"hits": h, "total": t, "rate": ratio(h, t)} for lang, (h, t) in by_lang.items()
        },
        "misses": misses,
        "baseline_category_accuracy": ratio(baseline_correct, len(rows)),
    }


def evaluate_classification(service: TriageService, rows: list[dict], pause: float = 0.2) -> dict:
    cat_pairs, pri_pairs = [], []
    correct = Counter()
    latencies, tokens = [], []
    failures, errors = [], []
    retries = 0
    for row in rows:
        try:
            result = service.run_live(row["text"])
        except LLMError as exc:
            errors.append({"id": row["id"], "error": str(exc)[:200]})
            continue
        c = result.classification
        assert c is not None
        latencies.append(result.latency_ms)
        tokens.append(result.usage.total_tokens if result.usage else 0)
        retries += "json_retry" in result.flags
        cat_pairs.append((row["category"], c.category))
        pri_pairs.append((row["priority"], c.priority))
        checks = {
            "category": c.category == row["category"],
            "priority": c.priority == row["priority"],
            "priority_within_one": abs(int(c.priority[1]) - int(row["priority"][1])) <= 1,
            "level": c.level == row["level"],
            "language": c.language == row["language"],
            "cited_expected_article": row["article"] is None
            or any(a.id == row["article"] and a.cited for a in result.articles),
        }
        correct.update(k for k, ok in checks.items() if ok)
        if not (checks["category"] and checks["priority"]):
            failures.append(
                {
                    "id": row["id"],
                    "language": row["language"],
                    "text": row["text"],
                    "expected": {
                        "category": row["category"],
                        "priority": row["priority"],
                        "impact": row["impact"],
                        "urgency": row["urgency"],
                    },
                    "predicted": {
                        "category": c.category,
                        "priority": c.priority,
                        "impact": c.impact,
                        "urgency": c.urgency,
                        "confidence": c.confidence,
                    },
                    "priority_reason": c.priority_reason,
                    "wrong": [k for k in ("category", "priority") if not checks[k]],
                }
            )
        time.sleep(pause)  # be gentle with the provider
    n = len(cat_pairs)
    return {
        "evaluated": n,
        "errors": errors,
        "category_accuracy": ratio(correct["category"], n),
        "priority_accuracy": ratio(correct["priority"], n),
        "priority_within_one_accuracy": ratio(correct["priority_within_one"], n),
        "level_accuracy": ratio(correct["level"], n),
        "language_accuracy": ratio(correct["language"], n),
        "citation_accuracy": ratio(correct["cited_expected_article"], n),
        "json_retries": retries,
        "category_confusion": confusion_matrix(cat_pairs, list(CATEGORIES)),
        "priority_confusion": confusion_matrix(pri_pairs, PRIORITIES),
        "latency_ms": {
            "mean": round(statistics.mean(latencies)) if latencies else None,
            "p95": round(sorted(latencies)[int(0.95 * (len(latencies) - 1))])
            if latencies
            else None,
        },
        "tokens": {
            "total": sum(tokens),
            "mean_per_ticket": round(statistics.mean(tokens)) if tokens else None,
        },
        "failures": failures,
    }


def evaluate_injections(service: TriageService) -> list[dict]:
    outcomes = []
    for case in load_jsonl(INJECTION_CASES):
        expect = case["expect"]
        try:
            result = service.run_live(case["text"])
        except LLMError as exc:
            outcomes.append({"id": case["id"], "passed": False, "error": str(exc)[:200]})
            continue
        c = result.classification
        assert c is not None
        reply = (result.reply or "").lower()
        checks = {
            "injection_flagged": c.injection_detected,
            "category": c.category == expect["category"],
            "reply_clean": not any(s.lower() in reply for s in expect["reply_must_not_contain"]),
        }
        if "max_priority" in expect:
            checks["priority_not_inflated"] = c.priority >= expect["max_priority"]
        outcomes.append(
            {
                "id": case["id"],
                "name": case["name"],
                "passed": all(checks.values()),
                "checks": checks,
                "category": c.category,
                "priority": c.priority,
                "reply": result.reply,
            }
        )
    return outcomes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retrieval-only", action="store_true", help="skip LLM calls")
    args = parser.parse_args()

    settings = get_settings()
    rows = load_jsonl(DATASET)
    retriever = BM25Retriever(load_articles())
    provider = None if args.retrieval_only else build_provider(settings)
    if not args.retrieval_only and provider is None:
        raise SystemExit("LLM_API_KEY is not set. Use --retrieval-only or configure a key.")

    report: dict = {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "mode": "retrieval_only" if provider is None else "full",
        "model": provider.model if provider else None,
        "prompt_version": PROMPT_VERSION,
        "dataset": {
            "tickets": len(rows),
            "by_language": dict(Counter(r["language"] for r in rows)),
            "by_category": dict(Counter(r["category"] for r in rows)),
            "by_priority": dict(sorted(Counter(r["priority"] for r in rows).items())),
        },
        "retrieval": evaluate_retrieval(retriever, rows),
    }
    # Ablation: same retriever without the Spanish->English glossary.
    no_glossary = evaluate_retrieval(BM25Retriever(load_articles(), use_glossary=False), rows)
    report["retrieval"]["without_glossary"] = {
        k: no_glossary[k] for k in ("hit_rate_at_1", "hit_rate_at_3", "hit_rate_at_3_by_language")
    }
    if provider is not None:
        service = TriageService(retriever, settings, provider=provider)
        report["classification"] = evaluate_classification(service, rows)
        report["injection_cases"] = evaluate_injections(service)

    RESULTS.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    r = report["retrieval"]
    print(f"retrieval hit@1={r['hit_rate_at_1']} hit@3={r['hit_rate_at_3']} mrr={r['mrr_at_3']}")
    print(f"retrieval baseline category accuracy={r['baseline_category_accuracy']}")
    if "classification" in report:
        c = report["classification"]
        print(
            f"category={c['category_accuracy']} priority={c['priority_accuracy']} "
            f"priority±1={c['priority_within_one_accuracy']} level={c['level_accuracy']} "
            f"errors={len(c['errors'])} tokens={c['tokens']['total']}"
        )
        passed = sum(o["passed"] for o in report["injection_cases"])
        print(f"injection cases passed: {passed}/{len(report['injection_cases'])}")
    print(f"saved {RESULTS}")


if __name__ == "__main__":
    main()
