"""Load help desk KB articles (Markdown + YAML front matter) and split them into sections."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
KB_DIR = DATA_DIR / "kb"

_FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_AUTOLINK = re.compile(r"<(https?://[^>]+)>")
_KEYS = re.compile(r"\+\+(.+?)\+\+")
_ADMONITION = re.compile(r'^!!!\s+\w+\s*(?:"([^"]*)")?\s*$', re.MULTILINE)
_EMPHASIS = re.compile(r"[*_`]{1,3}")

# Sections that add little signal for retrieval.
SKIPPED_SECTIONS = {"Related articles", "Last reviewed"}


@dataclass(frozen=True)
class Chunk:
    article_id: str
    section: str
    text: str


@dataclass(frozen=True)
class Article:
    id: str
    title: str
    category: str
    level: str
    tags: tuple[str, ...]
    slug: str
    summary: str
    chunks: tuple[Chunk, ...] = field(default_factory=tuple)

    def url(self, site_url: str) -> str:
        return f"{site_url.rstrip('/')}/kb/{self.slug}/"


def clean_markdown(text: str) -> str:
    """Strip MkDocs/Markdown syntax that does not help retrieval or the prompt."""
    text = _ADMONITION.sub(lambda m: m.group(1) or "", text)
    text = _LINK.sub(r"\1", text)
    text = _AUTOLINK.sub(r"\1", text)
    text = _KEYS.sub(r"\1", text)
    text = _EMPHASIS.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_article(raw: str, slug: str) -> Article:
    match = _FRONT_MATTER.match(raw)
    if not match:
        raise ValueError(f"{slug}: missing YAML front matter")
    meta = yaml.safe_load(match.group(1)) or {}
    for key in ("id", "title", "category", "level"):
        if key not in meta:
            raise ValueError(f"{slug}: front matter is missing '{key}'")
    body = raw[match.end() :]

    sections: list[tuple[str, str]] = []
    for part in re.split(r"^## ", body, flags=re.MULTILINE)[1:]:
        heading, _, content = part.partition("\n")
        sections.append((heading.strip(), clean_markdown(content)))

    article_id = str(meta["id"])
    chunks = tuple(
        Chunk(article_id=article_id, section=heading, text=content)
        for heading, content in sections
        if heading not in SKIPPED_SECTIONS and content
    )
    summary = next((c for h, c in sections if h == "Summary"), "")
    return Article(
        id=article_id,
        title=str(meta["title"]),
        category=str(meta["category"]),
        level=str(meta["level"]),
        tags=tuple(str(t) for t in meta.get("tags") or []),
        slug=slug,
        summary=summary,
        chunks=chunks,
    )


def load_articles(kb_dir: Path = KB_DIR) -> list[Article]:
    files = sorted(kb_dir.glob("kb-*.md"))
    if not files:
        raise FileNotFoundError(f"No KB articles found in {kb_dir}")
    return [parse_article(f.read_text(encoding="utf-8"), f.stem) for f in files]
