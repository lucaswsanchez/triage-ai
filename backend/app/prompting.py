"""Builds the chat messages from the versioned prompt files in `prompts/`."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

from app.retrieval import RetrievedArticle

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
PROMPT_VERSION = "v1"

# Heuristic detector, used as a second layer next to the model's own judgement.
_INJECTION_PATTERNS = [
    r"\bignore\b.{0,30}\b(instructions?|rules|prompt)\b",
    r"\bdisregard\b.{0,30}\b(instructions?|rules|above)\b",
    r"\b(system|developer)\s+prompt\b",
    r"\byou are now\b",
    r"\bact as\b",
    r"\bjailbreak\b|\bdan mode\b|\bdeveloper mode\b",
    r"\b(reveal|print|show)\b.{0,30}\b(prompt|instructions)\b",
    r"\bignor[aáe]\w*\b.{0,30}\binstrucciones\b",
    r"\bolvid[aáe]\w*\b.{0,30}\b(instrucciones|reglas)\b",
    r"\bprompt de sistema\b",
    r"\bahora sos\b|\bahora eres\b",
    r"</?\s*(ticket|system|assistant)\s*>",
]
_INJECTION_RE = re.compile("|".join(_INJECTION_PATTERNS), re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"</?\s*ticket\s*>", re.IGNORECASE)


def looks_like_injection(text: str) -> bool:
    return bool(_INJECTION_RE.search(text))


def sanitize_ticket(text: str) -> str:
    """Neutralize delimiter tags so the ticket cannot close its own <ticket> block."""
    return _TAG_RE.sub("[ticket-tag removed]", text).strip()


@lru_cache
def load_system_prompt(version: str = PROMPT_VERSION) -> str:
    return (PROMPTS_DIR / version / "system.md").read_text(encoding="utf-8")


@lru_cache
def load_few_shot(version: str = PROMPT_VERSION) -> tuple[dict, ...]:
    return tuple(json.loads((PROMPTS_DIR / version / "few_shot.json").read_text(encoding="utf-8")))


def _articles_block(articles: list[dict]) -> str:
    if not articles:
        return "KB articles found by search: none."
    lines = ["KB articles found by search (may be irrelevant):"]
    for a in articles:
        lines.append(
            f"- [{a['id']}] {a['title']} (category: {a['category']}, level: {a['level']})\n"
            f"  Best matching section '{a['section']}': {a['snippet']}"
        )
    return "\n".join(lines)


def _user_message(articles: list[dict], ticket: str) -> str:
    return f"{_articles_block(articles)}\n\n<ticket>\n{sanitize_ticket(ticket)}\n</ticket>"


def article_context(results: list[RetrievedArticle]) -> list[dict]:
    return [
        {
            "id": r.article.id,
            "title": r.article.title,
            "category": r.article.category,
            "level": r.article.level,
            "section": r.best_section,
            "snippet": " ".join(r.snippet.split())[:500],
        }
        for r in results
    ]


def build_messages(
    ticket: str, results: list[RetrievedArticle], version: str = PROMPT_VERSION
) -> list[dict[str, str]]:
    messages = [{"role": "system", "content": load_system_prompt(version)}]
    for example in load_few_shot(version):
        messages.append(
            {"role": "user", "content": _user_message(example["articles"], example["ticket"])}
        )
        messages.append(
            {"role": "assistant", "content": json.dumps(example["answer"], ensure_ascii=False)}
        )
    messages.append({"role": "user", "content": _user_message(article_context(results), ticket)})
    return messages
