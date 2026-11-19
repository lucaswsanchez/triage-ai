import json

import pytest

from app.llm import LLMError, LLMResult, complete_structured, parse_json_object
from app.priority import compute_priority
from app.schemas import LLMTriageOutput, Usage

VALID = {
    "is_support_request": True,
    "injection_detected": False,
    "language": "en",
    "category": "Network",
    "impact": "Low",
    "urgency": "High",
    "level": "L1",
    "sentiment": "frustrated",
    "confidence": 0.82,
    "summary": "VPN fails from a hotel network.",
    "priority_reason": "One user, blocked before a client meeting.",
    "cited_article_ids": ["kb-009 "],
    "reply": "Hi, please accept the hotel login page first (KB-009).",
}


class FakeProvider:
    model = "fake-model"

    def __init__(self, contents: list[str]) -> None:
        self._contents = list(contents)
        self.calls: list[list[dict[str, str]]] = []

    def complete_json(self, messages, max_tokens):
        self.calls.append(messages)
        return LLMResult(
            content=self._contents.pop(0),
            usage=Usage(prompt_tokens=100, completion_tokens=50, total_tokens=150),
        )


MESSAGES = [{"role": "system", "content": "json"}, {"role": "user", "content": "ticket"}]


def test_parse_json_object_handles_fences():
    assert parse_json_object('```json\n{"a": 1}\n```') == {"a": 1}


@pytest.mark.parametrize("bad", ["", "   ", "[1, 2]", "not json"])
def test_parse_json_object_rejects_invalid(bad):
    with pytest.raises(ValueError):
        parse_json_object(bad)


def test_complete_structured_valid_first_try():
    provider = FakeProvider([json.dumps(VALID)])
    out, usage, attempts = complete_structured(provider, MESSAGES, LLMTriageOutput, 500)
    assert attempts == 1
    assert out.category == "Network"
    assert out.cited_article_ids == ["KB-009"]
    assert usage.total_tokens == 150


def test_complete_structured_retries_once_with_error_feedback():
    provider = FakeProvider(["   ", json.dumps(VALID)])
    out, usage, attempts = complete_structured(provider, MESSAGES, LLMTriageOutput, 500)
    assert attempts == 2
    assert usage.total_tokens == 300
    assert "not valid JSON" in provider.calls[1][-1]["content"]
    assert out.level == "L1"


def test_complete_structured_rejects_values_outside_schema():
    bad = {**VALID, "category": "Plumbing"}
    provider = FakeProvider([json.dumps(bad), json.dumps({**VALID, "confidence": 7})])
    with pytest.raises(LLMError):
        complete_structured(provider, MESSAGES, LLMTriageOutput, 500)


@pytest.mark.parametrize(
    ("impact", "urgency", "category", "expected"),
    [
        ("High", "High", "Microsoft 365", "P1"),
        ("Medium", "High", "Hardware & Printing", "P2"),
        ("Low", "Medium", "Microsoft 365", "P4"),
        ("Medium", "Low", "Hardware & Printing", "P4"),
        ("Low", "High", "Security", "P2"),  # security: one user counts as Medium impact
        ("Low", "High", "Network", "P3"),
    ],
)
def test_priority_matrix(impact, urgency, category, expected):
    assert compute_priority(impact, urgency, category) == expected
