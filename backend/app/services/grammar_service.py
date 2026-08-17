from __future__ import annotations

from fastapi import HTTPException, status

from app.models.grammar import GrammarTopic
from app.repositories.grammar_repository import GrammarRepository


class GrammarService:
    def __init__(self, repo: GrammarRepository):
        self.repo = repo

    def list(self, category: str | None, search: str | None) -> list[GrammarTopic]:
        return self.repo.list(category=category, search=search)

    def get_by_slug_or_404(self, slug: str) -> GrammarTopic:
        topic = self.repo.get_by_slug(slug)
        if topic is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grammar topic '{slug}' not found",
            )
        return topic

    def list_categories(self) -> list[str]:
        return self.repo.list_categories()
