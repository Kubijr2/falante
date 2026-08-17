from app.core.config import settings
from app.services.ai.base import AIProvider
from app.services.ai.openai_provider import OpenAIProvider


class AIFeatureDisabledError(Exception):
    """
    Raised whenever an AI feature is requested but no provider is usable —
    either no API key is set, or AI_PROVIDER names a provider that isn't
    implemented yet. Routes catch this and return 503 with the message as-is,
    since it's already written to be shown to the person, not just logged.

    This is the mechanism behind the hard requirement that the app works
    fully without AI: every AI feature is reachable but degrades to this
    error instead of crashing when no key is configured.
    """


def get_ai_provider() -> AIProvider:
    if not settings.ai_api_key:
        raise AIFeatureDisabledError(
            "AI features aren't configured yet. Add AI_API_KEY to backend/.env and restart the server to enable them."
        )

    if settings.ai_provider == "openai":
        return OpenAIProvider(api_key=settings.ai_api_key, model=settings.ai_model)

    raise AIFeatureDisabledError(
        f"AI_PROVIDER '{settings.ai_provider}' isn't supported yet. Supported providers: openai."
    )
