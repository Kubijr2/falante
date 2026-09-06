"""
Application configuration.

Everything environment-specific lives here and nowhere else. The rest of
the app imports `settings` and never reads os.environ directly — this is
what makes it trivial to swap SQLite for Postgres later: change
DATABASE_URL in .env, and nothing else in the codebase needs to change.
"""
import json
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # extra="ignore" is the important part here: without it, pydantic-
    # settings rejects the *entire* .env file if it contains even one key
    # that isn't a declared field — including a harmless typo in an unused
    # variable (this is exactly what happened with a mistyped
    # GOOGLE_CLIENT_SECRET, which crashed the whole backend rather than
    # just being ignored). A config file should tolerate stray or
    # future-use variables without taking the app down.
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Defaults to a local SQLite file — zero setup required to start developing.
    # Swap to a Postgres URL (postgresql://user:pass@host:port/dbname) for
    # production; verified to work end-to-end against real Postgres 16,
    # including the dialect-sensitive func.date() call in dashboard_service.py.
    database_url: str = "sqlite:///./falante.db"

    # AI features (Milestone 5+). The app runs fully without these set —
    # ai_api_key being empty is what get_ai_provider() checks to decide
    # whether AI features are enabled at all.
    ai_provider: str = "openai"
    ai_api_key: str | None = None
    ai_model: str = "gpt-4o-mini"

    # How many AI requests (Tutor + Writing Coach combined) a single visitor
    # (identified by IP — there's no login system) can make per day. Exists
    # so a public deployment can't run up an unbounded OpenAI bill. Bump
    # this via .env / the hosting platform's env vars — no code change
    # needed. 10/day is intentionally conservative for an initial deploy.
    ai_rate_limit_per_day: int = 10

    # Kept as a plain string field — NOT list[str] — on purpose. Pydantic-
    # settings tries to JSON-decode the raw env value for any list-typed
    # field before any custom validator gets a chance to run, so a plain
    # comma-separated value like "https://a.com,https://b.com" (invalid
    # JSON) crashes the app at startup, before main.py even runs. Storing
    # the raw string here and parsing it in the `cors_origins` property
    # below sidesteps pydantic-settings' complex-type handling entirely.
    # Accepts either a JSON list ('["https://a.com","https://b.com"]') or a
    # plain comma-separated string — most hosting platforms' env-var UIs
    # make the comma-separated form much easier to set than JSON.
    cors_origins_env: str = Field(default="http://localhost:5173", validation_alias="CORS_ORIGINS")

    @property
    def cors_origins(self) -> list[str]:
        stripped = self.cors_origins_env.strip()
        if stripped.startswith("["):
            return json.loads(stripped)
        return [origin.strip() for origin in stripped.split(",") if origin.strip()]

    app_name: str = "Falante API"
    api_v1_prefix: str = "/api/v1"

    # Auth (Milestone 10). Google Sign-In only — the backend verifies the ID
    # token Google issues client-side and never sees or stores a password.
    # google_client_id must match the OAuth Client ID from Google Cloud
    # Console; it's used to check the token was actually issued for *this*
    # app, not some other app that also uses Google Sign-In.
    google_client_id: str | None = None

    # Signs the app's own session tokens (issued after a successful Google
    # sign-in). MUST be overridden with a real random secret outside local
    # dev — this default is intentionally obvious/insecure so it's never
    # mistaken for a safe production value. Generate one with, e.g.:
    # python3 -c "import secrets; print(secrets.token_hex(32))"
    jwt_secret_key: str = "dev-only-insecure-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 30  # 30 days


@lru_cache
def get_settings() -> Settings:
    """Cached so we don't re-parse the .env file on every request."""
    return Settings()


settings = get_settings()
