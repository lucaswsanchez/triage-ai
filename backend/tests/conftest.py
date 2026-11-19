import json

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.llm import LLMError, LLMResult
from app.main import create_app
from app.schemas import Usage

VALID_OUTPUT = {
    "is_support_request": True,
    "injection_detected": False,
    "language": "en",
    "category": "Network",
    "impact": "Low",
    "urgency": "High",
    "level": "L1",
    "sentiment": "frustrated",
    "confidence": 0.8,
    "summary": "VPN fails from a hotel network.",
    "priority_reason": "One user blocked before a deadline.",
    "cited_article_ids": ["KB-009", "KB-099"],
    "reply": "Hi, please accept the hotel login page first [KB-009].\n\nService Desk",
}


class FakeProvider:
    model = "fake-model"

    def __init__(self, contents=None, error=False):
        self.contents = list(contents or [json.dumps(VALID_OUTPUT)])
        self.error = error
        self.calls = 0

    def complete_json(self, messages, max_tokens):
        self.calls += 1
        if self.error:
            raise LLMError("boom")
        content = self.contents[min(self.calls - 1, len(self.contents) - 1)]
        return LLMResult(
            content=content,
            usage=Usage(prompt_tokens=900, completion_tokens=200, total_tokens=1100),
        )


def make_settings(**overrides) -> Settings:
    base = {"llm_api_key": "", "rate_limit_requests": 10, "daily_llm_budget": 300}
    base.update(overrides)
    return Settings(_env_file=None, **base)


@pytest.fixture
def demo_client():
    return TestClient(create_app(settings=make_settings()))


@pytest.fixture
def fake_provider():
    return FakeProvider()


@pytest.fixture
def live_client(fake_provider):
    app = create_app(settings=make_settings(llm_api_key="test"), provider=fake_provider)
    return TestClient(app)
