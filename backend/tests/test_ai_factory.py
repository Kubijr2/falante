import pytest

from app.core.config import settings
from app.services.ai.factory import AIFeatureDisabledError, get_ai_provider
from app.services.ai.openai_provider import OpenAIProvider


def test_no_api_key_raises_feature_disabled(monkeypatch):
    monkeypatch.setattr(settings, "ai_api_key", None)
    with pytest.raises(AIFeatureDisabledError):
        get_ai_provider()


def test_configured_openai_returns_provider_instance(monkeypatch):
    monkeypatch.setattr(settings, "ai_api_key", "fake-test-key")
    monkeypatch.setattr(settings, "ai_provider", "openai")
    provider = get_ai_provider()
    assert isinstance(provider, OpenAIProvider)


def test_unsupported_provider_raises_feature_disabled(monkeypatch):
    monkeypatch.setattr(settings, "ai_api_key", "fake-test-key")
    monkeypatch.setattr(settings, "ai_provider", "some-future-provider")
    with pytest.raises(AIFeatureDisabledError):
        get_ai_provider()
