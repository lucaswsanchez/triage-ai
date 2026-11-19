"""Record real LLM results for the 6 sample tickets into data/demo_results.json.

Needs LLM_API_KEY (in backend/.env or the environment). Run from backend/:

    python -m scripts.build_demo
"""

import json
from datetime import UTC, datetime

from app.config import get_settings
from app.kb import load_articles
from app.main import build_provider
from app.retrieval import BM25Retriever
from app.triage import DEMO_RESULTS_FILE, TriageService


def main() -> None:
    settings = get_settings()
    provider = build_provider(settings)
    if provider is None:
        raise SystemExit("LLM_API_KEY is not set: cannot record demo results.")
    service = TriageService(BM25Retriever(load_articles()), settings, provider=provider)
    today = datetime.now(UTC).date().isoformat()
    recorded: dict[str, dict] = {}
    for sample in service.samples:
        result = service.run_live(sample.text)
        recorded[sample.id] = {
            "model": provider.model,
            "recorded_at": today,
            "response": result.model_dump(),
        }
        c = result.classification
        print(f"{sample.id}: {c.category if c else '-'} {c.priority if c else ''} {result.flags}")
    DEMO_RESULTS_FILE.write_text(
        json.dumps(recorded, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"saved {len(recorded)} results to {DEMO_RESULTS_FILE}")


if __name__ == "__main__":
    main()
