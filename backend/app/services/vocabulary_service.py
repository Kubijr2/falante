from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.vocabulary import Vocabulary
from app.repositories.vocabulary_repository import VocabularyRepository
from app.schemas.vocabulary import VocabularyCreate, VocabularyUpdate


class VocabularyService:
    def __init__(self, repo: VocabularyRepository):
        self.repo = repo

    def list(self, category: str | None, search: str | None) -> list[Vocabulary]:
        return self.repo.list(category=category, search=search)

    def get_or_404(self, vocabulary_id: int) -> Vocabulary:
        vocab = self.repo.get(vocabulary_id)
        if vocab is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vocabulary {vocabulary_id} not found",
            )
        return vocab

    def create(self, data: VocabularyCreate) -> Vocabulary:
        vocab = Vocabulary(
            portuguese=data.portuguese,
            english=data.english,
            example_sentence=data.example_sentence,
            notes=data.notes,
            category=data.category,
            difficulty=data.difficulty,
            next_review_at=datetime.now(timezone.utc),
        )
        vocab.tags = data.tags
        return self.repo.create(vocab)

    def update(self, vocabulary_id: int, data: VocabularyUpdate) -> Vocabulary:
        vocab = self.get_or_404(vocabulary_id)
        updates = data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(vocab, field, value)  # `tags` setter handles JSON encoding
        return self.repo.update(vocab)

    def delete(self, vocabulary_id: int) -> None:
        vocab = self.get_or_404(vocabulary_id)
        self.repo.delete(vocab)
