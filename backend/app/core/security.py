"""
Our own session tokens — issued after a successful Google sign-in, unrelated
to Google's ID token (which we verify once and then discard). Keeping our
own token means the frontend never needs to talk to Google again after the
initial login; every subsequent request just carries this token.
"""
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings

ALGORITHM = settings.jwt_algorithm


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int | None:
    """Returns the user id encoded in the token, or None if it's invalid/expired."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        return None
