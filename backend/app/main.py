from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.api.v1 import (
    analytics,
    auth,
    dashboard,
    flashcards,
    grammar,
    study_assistant,
    tutor,
    verbs,
    vocabulary,
    writing,
)
from app.core.config import settings
from app.core.rate_limit import limiter

app = FastAPI(title=settings.app_name)

app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "detail": (
                "You've reached today's limit for AI features on this demo "
                f"({settings.ai_rate_limit_per_day} requests/day per visitor). "
                "It resets tomorrow — or clone the repo and run it locally with "
                "your own API key for unlimited use."
            )
        },
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(vocabulary.router, prefix=settings.api_v1_prefix)
app.include_router(flashcards.router, prefix=settings.api_v1_prefix)
app.include_router(dashboard.router, prefix=settings.api_v1_prefix)
app.include_router(grammar.router, prefix=settings.api_v1_prefix)
app.include_router(verbs.router, prefix=settings.api_v1_prefix)
app.include_router(tutor.router, prefix=settings.api_v1_prefix)
app.include_router(writing.router, prefix=settings.api_v1_prefix)
app.include_router(analytics.router, prefix=settings.api_v1_prefix)
app.include_router(study_assistant.router, prefix=settings.api_v1_prefix)


@app.get("/health")
def health_check():
    return {"status": "ok"}