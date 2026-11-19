"""Triage pipeline: retrieve KB articles -> one structured LLM call -> validated response.

Demo mode (no API key, rate limit reached, daily budget spent or provider error) serves
precomputed results for the sample tickets, or retrieval-only results for other tickets.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path

from app.config import Settings
from app.kb import DATA_DIR
from app.llm import LLMProvider, complete_structured
from app.priority import compute_priority
from app.prompting import PROMPT_VERSION, build_messages, looks_like_injection
from app.retrieval import RetrievedArticle, Retriever
from app.schemas import (
    ArticleRef,
    Classification,
    DemoReason,
    LLMTriageOutput,
    Sample,
    TriageResponse,
)

log = logging.getLogger("triage")

SAMPLES_FILE = DATA_DIR / "samples.json"
DEMO_RESULTS_FILE = DATA_DIR / "demo_results.json"

DEMO_NOTICES: dict[str, str] = {
    "no_api_key": "Live AI is not configured on this server.",
    "rate_limited": "You reached the live AI limit for this hour.",
    "daily_budget": "The daily live AI budget for this demo is spent.",
    "llm_error": "The AI provider did not answer correctly.",
}


def _normalize(text: str) -> str:
    return " ".join(text.split()).lower()


def load_samples(path: Path = SAMPLES_FILE) -> list[Sample]:
    return [Sample.model_validate(s) for s in json.loads(path.read_text(encoding="utf-8"))]


def load_demo_results(path: Path = DEMO_RESULTS_FILE) -> dict[str, dict]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


class TriageService:
    def __init__(
        self,
        retriever: Retriever,
        settings: Settings,
        provider: LLMProvider | None = None,
        samples: list[Sample] | None = None,
        demo_results: dict[str, dict] | None = None,
    ) -> None:
        self.retriever = retriever
        self.settings = settings
        self.provider = provider
        self.samples = samples if samples is not None else load_samples()
        self.demo_results = demo_results if demo_results is not None else load_demo_results()
        self._sample_by_text = {_normalize(s.text): s.id for s in self.samples}

    # ---- helpers -------------------------------------------------------------------------
    def _refs(self, results: list[RetrievedArticle], cited: set[str]) -> list[ArticleRef]:
        site = self.settings.kb_site_url
        return [
            ArticleRef(
                id=r.article.id,
                title=r.article.title,
                category=r.article.category,
                level=r.article.level,
                url=r.article.url(site),
                score=r.score,
                section=r.best_section,
                cited=r.article.id in cited,
            )
            for r in results
        ]

    def sample_id_for(self, text: str) -> str | None:
        return self._sample_by_text.get(_normalize(text))

    # ---- live ----------------------------------------------------------------------------
    def run_live(self, text: str) -> TriageResponse:
        if self.provider is None:
            raise RuntimeError("no LLM provider configured")
        start = time.perf_counter()
        results = self.retriever.search(text, top_k=self.settings.retrieval_top_k)
        messages = build_messages(text, results)
        out, usage, attempts = complete_structured(
            self.provider, messages, LLMTriageOutput, max_tokens=self.settings.llm_max_tokens
        )
        retrieved_ids = {r.article.id for r in results}
        # Never surface a citation that was not in the retrieved context.
        cited = [i for i in out.cited_article_ids if i in retrieved_ids]

        flags: list[str] = []
        if looks_like_injection(text) or out.injection_detected:
            flags.append("possible_prompt_injection")
        if not out.is_support_request:
            flags.append("out_of_scope")
        if attempts > 1:
            flags.append("json_retry")
        if len(cited) < len(out.cited_article_ids):
            flags.append("dropped_unknown_citation")

        classification = Classification(
            category=out.category,
            priority=compute_priority(out.impact, out.urgency, out.category),
            impact=out.impact,
            urgency=out.urgency,
            level=out.level,
            sentiment=out.sentiment,
            confidence=round(out.confidence, 2),
            language=out.language,
            summary=out.summary,
            priority_reason=out.priority_reason,
            is_support_request=out.is_support_request,
            injection_detected=out.injection_detected or "possible_prompt_injection" in flags,
        )
        return TriageResponse(
            mode="live",
            classification=classification,
            articles=self._refs(results, set(cited)),
            reply=out.reply,
            usage=usage,
            latency_ms=int((time.perf_counter() - start) * 1000),
            model=self.provider.model,
            prompt_version=PROMPT_VERSION,
            flags=flags,
        )

    # ---- demo ----------------------------------------------------------------------------
    def run_demo(self, text: str, reason: DemoReason) -> TriageResponse:
        start = time.perf_counter()
        sample_id = self.sample_id_for(text)
        recorded = self.demo_results.get(sample_id) if sample_id else None
        if recorded:
            response = TriageResponse.model_validate(recorded["response"])
            return response.model_copy(
                update={
                    "mode": "demo",
                    "demo_reason": reason,
                    "notice": f"{DEMO_NOTICES[reason]} Showing a precomputed result recorded "
                    f"with {recorded['model']} on {recorded['recorded_at']}.",
                }
            )

        results = self.retriever.search(text, top_k=self.settings.retrieval_top_k)
        flags = ["retrieval_only"]
        if looks_like_injection(text):
            flags.append("possible_prompt_injection")
        return TriageResponse(
            mode="demo",
            demo_reason=reason,
            notice=f"{DEMO_NOTICES[reason]} Showing the knowledge base search only. "
            "Load one of the sample tickets to see a full AI result.",
            classification=None,
            articles=self._refs(results, set()),
            reply=None,
            latency_ms=int((time.perf_counter() - start) * 1000),
            prompt_version=PROMPT_VERSION,
            flags=flags,
        )
