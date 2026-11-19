"""Pydantic models: the LLM's structured output and the public API contract."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

Category = Literal[
    "Accounts & Identity",
    "Microsoft 365",
    "Network",
    "Hardware & Printing",
    "Software",
    "Security",
    "Onboarding & Offboarding",
    "Other",
]
CATEGORIES: tuple[str, ...] = Category.__args__  # type: ignore[attr-defined]

Level3 = Literal["High", "Medium", "Low"]
Priority = Literal["P1", "P2", "P3", "P4"]
SupportLevel = Literal["L1", "L2"]
Sentiment = Literal["positive", "neutral", "frustrated", "angry"]
Language = Literal["en", "es"]


class LLMTriageOutput(BaseModel):
    """Exactly what the model must return (validated before anything reaches the UI)."""

    is_support_request: bool
    injection_detected: bool = False
    language: Language
    category: Category
    impact: Level3
    urgency: Level3
    level: SupportLevel
    sentiment: Sentiment
    confidence: float = Field(ge=0, le=1)
    summary: str = Field(min_length=1, max_length=300)
    priority_reason: str = Field(min_length=1, max_length=400)
    cited_article_ids: list[str] = Field(default_factory=list, max_length=3)
    reply: str = Field(min_length=1, max_length=4000)

    @field_validator("cited_article_ids")
    @classmethod
    def _normalize_ids(cls, ids: list[str]) -> list[str]:
        return [i.strip().upper() for i in ids if i.strip()]


class Classification(BaseModel):
    category: Category
    priority: Priority
    impact: Level3
    urgency: Level3
    level: SupportLevel
    sentiment: Sentiment
    confidence: float
    language: Language
    summary: str
    priority_reason: str
    is_support_request: bool
    injection_detected: bool


class ArticleRef(BaseModel):
    id: str
    title: str
    category: str
    level: str
    url: str
    score: float
    section: str
    cited: bool = False


class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


DemoReason = Literal["no_api_key", "rate_limited", "daily_budget", "llm_error"]


class TicketIn(BaseModel):
    text: str = Field(min_length=10, description="Ticket or email text pasted by the agent.")


class TriageResponse(BaseModel):
    mode: Literal["live", "demo"]
    demo_reason: DemoReason | None = None
    notice: str | None = None
    classification: Classification | None
    articles: list[ArticleRef]
    reply: str | None
    usage: Usage | None = None
    latency_ms: int
    model: str | None = None
    prompt_version: str
    flags: list[str] = Field(default_factory=list)


class Sample(BaseModel):
    id: str
    title: str
    language: Language
    text: str
