"""FastAPI entry point."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.config import Settings, get_settings
from app.kb import load_articles
from app.llm import LLMError, LLMProvider, OpenAICompatibleProvider
from app.prompting import PROMPT_VERSION
from app.ratelimit import DailyBudget, SlidingWindowRateLimiter
from app.retrieval import BM25Retriever
from app.schemas import DemoReason, Sample, TicketIn, TriageResponse
from app.triage import TriageService

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("triage.api")

EVAL_RESULTS_FILE = Path(__file__).resolve().parent.parent / "eval" / "results.json"


def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def build_provider(settings: Settings) -> LLMProvider | None:
    if not settings.llm_enabled:
        return None
    return OpenAICompatibleProvider(
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        timeout=settings.llm_timeout_seconds,
        extra_body=settings.llm_extra_body_dict,
    )


def create_app(
    settings: Settings | None = None,
    provider: LLMProvider | None = None,
    service: TriageService | None = None,
) -> FastAPI:
    settings = settings or get_settings()
    articles = load_articles()
    retriever = BM25Retriever(articles)
    provider = provider if provider is not None else build_provider(settings)
    service = service or TriageService(retriever, settings, provider=provider)
    limiter = SlidingWindowRateLimiter(
        settings.rate_limit_requests, settings.rate_limit_window_seconds
    )
    budget = DailyBudget(settings.daily_llm_budget)

    app = FastAPI(
        title="TriageAI API",
        version=__version__,
        description=(
            "Classifies IT help desk tickets (category, priority, level, sentiment), retrieves "
            "knowledge base articles with BM25 and drafts a cited reply. Without an API key, or "
            "when the rate limit is reached, it answers in demo mode."
        ),
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )
    app.state.service = service
    app.state.limiter = limiter

    @app.get("/api/health", tags=["meta"])
    def health() -> dict:
        return {
            "status": "ok",
            "version": __version__,
            "llm_enabled": service.provider is not None,
            "model": service.provider.model if service.provider else None,
            "prompt_version": PROMPT_VERSION,
            "kb_articles": len(articles),
            "demo_results": len(service.demo_results),
            "rate_limit": {
                "requests": settings.rate_limit_requests,
                "window_seconds": settings.rate_limit_window_seconds,
            },
            "max_ticket_chars": settings.max_ticket_chars,
        }

    @app.get("/api/samples", response_model=list[Sample], tags=["triage"])
    def samples() -> list[Sample]:
        return service.samples

    @app.get("/api/kb", tags=["knowledge base"])
    def kb() -> list[dict]:
        return [
            {
                "id": a.id,
                "title": a.title,
                "category": a.category,
                "level": a.level,
                "url": a.url(settings.kb_site_url),
            }
            for a in articles
        ]

    @app.post("/api/triage", response_model=TriageResponse, tags=["triage"])
    def triage(ticket: TicketIn, request: Request, response: Response) -> TriageResponse:
        text = ticket.text.strip()
        if len(text) > settings.max_ticket_chars:
            raise HTTPException(
                status_code=422,
                detail=f"Ticket is too long ({len(text)} characters). "
                f"The limit is {settings.max_ticket_chars}.",
            )
        ip = client_ip(request)
        reason: DemoReason | None = None
        if service.provider is None:
            reason = "no_api_key"
        elif not limiter.allow(ip):
            reason = "rate_limited"
        elif not budget.allow():
            reason = "daily_budget"

        result: TriageResponse
        if reason is None:
            try:
                result = service.run_live(text)
            except LLMError as exc:
                log.warning("llm error: %s", exc)
                reason = "llm_error"
        if reason is not None:
            result = service.run_demo(text, reason)

        response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_requests)
        response.headers["X-RateLimit-Remaining"] = str(limiter.remaining(ip))
        log.info(
            json.dumps(
                {
                    "event": "triage",
                    "mode": result.mode,
                    "demo_reason": result.demo_reason,
                    "chars": len(text),
                    "category": result.classification.category if result.classification else None,
                    "priority": result.classification.priority if result.classification else None,
                    "tokens": result.usage.total_tokens if result.usage else 0,
                    "latency_ms": result.latency_ms,
                    "flags": result.flags,
                }
            )
        )
        return result

    @app.get("/api/eval", tags=["evaluation"])
    def evaluation() -> dict:
        if not EVAL_RESULTS_FILE.exists():
            raise HTTPException(status_code=404, detail="No evaluation results yet.")
        return json.loads(EVAL_RESULTS_FILE.read_text(encoding="utf-8"))

    return app


app = create_app()
