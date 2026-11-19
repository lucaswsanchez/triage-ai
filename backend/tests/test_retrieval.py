import pytest

from app.kb import clean_markdown, load_articles, parse_article
from app.retrieval import BM25Retriever, tokenize

SAMPLE = """---
id: KB-999
title: Sample Article
category: Network
level: L1
tags: [vpn, wifi]
estimated_time: 5 min
last_reviewed: 2026-11-17
---

# Sample Article

## Summary

Short **summary** with a [link](other.md).

## Resolution

1. Press ++ctrl+alt+del++.

## Related articles

- [KB-001](kb-001.md)
"""


@pytest.fixture(scope="module")
def retriever():
    return BM25Retriever(load_articles())


def test_parse_article_front_matter_and_sections():
    article = parse_article(SAMPLE, "kb-999-sample")
    assert article.id == "KB-999"
    assert article.tags == ("vpn", "wifi")
    assert [c.section for c in article.chunks] == ["Summary", "Resolution"]
    assert article.summary == "Short summary with a link."
    assert article.url("https://example.org/site/") == "https://example.org/site/kb/kb-999-sample/"


def test_parse_article_requires_front_matter():
    with pytest.raises(ValueError):
        parse_article("# No front matter", "kb-000")


def test_clean_markdown_strips_admonitions_and_keys():
    text = clean_markdown('!!! warning "Careful"\n    Press ++ctrl+l++ and see <https://x.org>')
    assert "!!!" not in text and "++" not in text
    assert "Careful" in text and "ctrl+l" in text and "https://x.org" in text


def test_all_kb_articles_load():
    articles = load_articles()
    assert len(articles) == 21
    assert len({a.id for a in articles}) == 21
    assert all(a.chunks for a in articles)


def test_tokenize_folds_accents_and_translates_spanish():
    tokens = tokenize("Olvidé mi contraseña y la impresora no imprime")
    assert "password" in tokens
    assert "printer" in tokens
    assert "mi" not in tokens


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("VPN will not connect from the hotel, says gateway timed out", "KB-009"),
        ("My printer shows offline and jobs are stuck in the queue", "KB-012"),
        ("I clicked a link in a suspicious email and typed my password", "KB-018"),
        ("BitLocker is asking for a recovery key after BIOS update", "KB-014"),
        ("Se me bloqueó la cuenta después de cambiar la contraseña", "KB-003"),
    ],
)
def test_search_finds_expected_article_in_top3(retriever, query, expected):
    ids = [r.article.id for r in retriever.search(query, top_k=3)]
    assert expected in ids


def test_search_returns_nothing_for_stopword_query(retriever):
    assert retriever.search("") == []
    assert retriever.search("the and of") == []


def test_search_results_are_sorted_and_limited(retriever):
    results = retriever.search("outlook email not syncing", top_k=2)
    assert len(results) == 2
    assert results[0].score >= results[1].score
