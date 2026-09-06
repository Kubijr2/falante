"""
A single shared slowapi Limiter, now keyed by authenticated user rather
than IP address (Milestone 10: both AI endpoints require login, so a real
user identity is always available — user-based limiting is strictly more
correct than IP-based, since a shared IP, like a university network or a
household behind one router, would otherwise share a single quota).

slowapi's key function only receives the raw Starlette `Request` — it runs
outside FastAPI's dependency-injection system, so it can't just receive the
already-resolved `current_user` the route handler gets via `Depends`. This
decodes the JWT directly from the Authorization header for that reason.
Falls back to IP if a request somehow reaches here without a valid token —
shouldn't happen in practice, since the route itself also requires
authentication and would reject the request before slowapi even needs a
key, but it's a safe default rather than an error.

Deliberately in-memory rather than Redis-backed: this app runs as a single
process on a single instance (see docker-compose.yml / DEPLOYMENT.md), so an
in-memory counter is enough and avoids needing a separate piece of
infrastructure just to rate-limit two endpoints. If this ever needs to run
as multiple instances behind a load balancer, swap the storage_uri here for
a Redis URL — slowapi supports that as a one-line change.

Only applied to the AI-calling endpoints (Tutor, Writing Coach) — the rest
of the API is cheap DB reads/writes with no per-request external cost, so
there's nothing to protect there.
"""
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.security import decode_access_token


def get_user_or_ip_key(request: Request) -> str:
    authorization = request.headers.get("authorization", "")
    if authorization.startswith("Bearer "):
        token = authorization.removeprefix("Bearer ").strip()
        user_id = decode_access_token(token)
        if user_id is not None:
            return f"user:{user_id}"
    return get_remote_address(request)


limiter = Limiter(key_func=get_user_or_ip_key)
