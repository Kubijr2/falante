from __future__ import annotations

import logging

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

from app.core.config import settings
from app.models.user import User
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class InvalidGoogleTokenError(Exception):
    """Raised when the Google ID token fails verification for any reason."""


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def verify_google_id_token(self, raw_token: str) -> dict:
        """
        Verifies the token's signature against Google's public keys and
        checks it was actually issued for this app (the audience check) —
        without that check, an ID token meant for a completely different
        Google Sign-In-using app would also be accepted here.
        """
        if not settings.google_client_id:
            raise InvalidGoogleTokenError(
                "Google sign-in isn't configured on this server (GOOGLE_CLIENT_ID is unset)."
            )
        try:
            claims = google_id_token.verify_oauth2_token(
                raw_token, google_requests.Request(), settings.google_client_id
            )
        except ValueError as exc:
            # Covers the "expected" failure modes: bad signature, expired
            # token, wrong audience (Client ID mismatch between the frontend
            # and backend .env files is the single most common cause here).
            raise InvalidGoogleTokenError(f"Invalid Google token: {exc}") from exc
        except Exception as exc:
            # Deliberately broad: verifying with Google also involves a real
            # network call to fetch Google's public keys, which can fail in
            # ways that aren't a ValueError (DNS/connectivity issues from
            # inside the container, TLS problems, etc.). Without this, those
            # failures surfaced as a raw unhandled 500 with no detail — the
            # frontend showed a generic "couldn't sign in" and nobody could
            # tell why. Logging the real exception server-side (visible via
            # `docker compose logs backend`) while returning a clean 401 to
            # the client is what actually makes this debuggable.
            logger.exception("Unexpected error verifying Google ID token")
            raise InvalidGoogleTokenError(f"Couldn't verify with Google: {exc}") from exc

        if "email" not in claims or "sub" not in claims:
            raise InvalidGoogleTokenError("Google token is missing required claims.")
        return claims

    def get_or_create_user(self, claims: dict) -> User:
        existing = self.user_repo.get_by_google_sub(claims["sub"])
        if existing:
            return existing

        user = User(
            email=claims["email"],
            google_sub=claims["sub"],
            name=claims.get("name", claims["email"]),
            picture_url=claims.get("picture"),
        )
        return self.user_repo.create(user)
