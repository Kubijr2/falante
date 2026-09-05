"""
A single shared slowapi Limiter, keyed by client IP address.

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
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
