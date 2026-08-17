"""
Application configuration.

Everything environment-specific lives here and nowhere else. The rest of the
app imports `settings` and never reads os.environ directly — this is what
makes it trivial to swap SQLite for Postgres later: change DATABASE_URL in
.env, and nothing else in the codebase needs to change.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Defaults to a local SQLite file — zero setup required to start developing.
    database_url: str = "sqlite:///./falante.db"

    # AI features (Milestone 5+). The app runs fully without these set —
    # ai_api_key being empty is what get_ai_provider() checks to decide
    # whether AI features are enabled at all.
    ai_provider: str = "openai"
    ai_api_key: str | None = None
    ai_model: str = "gpt-4o-mini"

    # CORS: the Vite dev server's default origin.
    cors_origins: list[str] = ["http://localhost:5173"]

    app_name: str = "Falante API"
    api_v1_prefix: str = "/api/v1"


@lru_cache
def get_settings() -> Settings:
    """Cached so we don't re-parse the .env file on every request."""
    return Settings()


settings = get_settings()
