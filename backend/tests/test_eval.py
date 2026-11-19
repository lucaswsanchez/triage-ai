import json

from app.kb import load_articles
from app.retrieval import BM25Retriever
from app.schemas import CATEGORIES
from app.triage import TriageService
from eval.run import (
    DATASET,
    confusion_matrix,
    evaluate_classification,
    evaluate_retrieval,
    load_jsonl,
)
from tests.conftest import VALID_OUTPUT, FakeProvider, make_settings

ROWS = load_jsonl(DATASET)


def test_dataset_has_50_valid_labeled_tickets():
    assert len(ROWS) == 50
    assert len({r["id"] for r in ROWS}) == 50
    assert {r["language"] for r in ROWS} == {"en", "es"}
    article_ids = {a.id for a in load_articles()}
    for r in ROWS:
        assert r["category"] in CATEGORIES
        assert r["priority"] in {"P1", "P2", "P3", "P4"}
        assert r["article"] is None or r["article"] in article_ids


def test_confusion_matrix_counts():
    cm = confusion_matrix([("a", "a"), ("a", "b"), ("b", "b"), ("x", "a")], ["a", "b"])
    assert cm["matrix"] == [[1, 1], [0, 1]]


def test_retrieval_regression_guard():
    # Guard against regressions in the tokenizer or chunking (real value is in eval/results.json).
    report = evaluate_retrieval(BM25Retriever(load_articles()), ROWS)
    assert report["labeled_tickets"] == 46
    assert report["hit_rate_at_3"] >= 0.9


def test_classification_metrics_with_fake_provider():
    rows = [r for r in ROWS if r["id"] in {"T17", "T19", "T01"}]  # Network, Network, Accounts
    out = {**VALID_OUTPUT, "cited_article_ids": ["KB-009"]}
    service = TriageService(
        BM25Retriever(load_articles()),
        make_settings(),
        provider=FakeProvider([json.dumps(out)]),
    )
    report = evaluate_classification(service, rows, pause=0)
    assert report["evaluated"] == 3
    assert report["category_accuracy"] == round(2 / 3, 4)
    assert report["priority_accuracy"] == 1.0  # all three are Low x High = P3
    assert [f["id"] for f in report["failures"]] == ["T01"]
    assert sum(map(sum, report["category_confusion"]["matrix"])) == 3
