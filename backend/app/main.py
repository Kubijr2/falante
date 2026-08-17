from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import dashboard, flashcards, grammar, tutor, verbs, vocabulary
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vocabulary.router, prefix=settings.api_v1_prefix)
app.include_router(flashcards.router, prefix=settings.api_v1_prefix)
app.include_router(dashboard.router, prefix=settings.api_v1_prefix)
app.include_router(grammar.router, prefix=settings.api_v1_prefix)
app.include_router(verbs.router, prefix=settings.api_v1_prefix)
app.include_router(tutor.router, prefix=settings.api_v1_prefix)


@app.get("/health")
def health_check():
    return {"status": "ok"}
