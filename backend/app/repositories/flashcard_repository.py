from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models.flashcard import FlashcardReview, ReviewResult
from app.models.vocabulary import Vocabulary


class FlashcardRepository:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    def create_review(self, review: FlashcardReview) -> FlashcardReview:
        review.user_id = self.user_id
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def count_total(self) -> int:
        stmt = (
            select(func.count())
            .select_from(FlashcardReview)
            .where(FlashcardReview.user_id == self.user_id)
        )
        return self.db.execute(stmt).scalar_one()

    def all_review_dates(self) -> list[date]:
        stmt = (
            select(func.date(FlashcardReview.reviewed_at))
            .where(FlashcardReview.user_id == self.user_id)
            .distinct()
        )
        rows = self.db.execute(stmt).scalars().all()
        return [d if isinstance(d, date) else date.fromisoformat(d) for d in rows]

    def recently_learned_vocabulary(
        self, results: tuple[ReviewResult, ...], limit: int
    ) -> list[Vocabulary]:
        stmt = (
            select(FlashcardReview)
            .options(joinedload(FlashcardReview.vocabulary))
            .where(FlashcardReview.result.in_(results), FlashcardReview.user_id == self.user_id)
            .order_by(FlashcardReview.reviewed_at.desc())
        )
        reviews = self.db.execute(stmt).scalars().all()

        seen_vocab_ids: set[int] = set()
        recently_learned: list[Vocabulary] = []
        for review in reviews:
            if review.vocabulary_id in seen_vocab_ids:
                continue
            seen_vocab_ids.add(review.vocabulary_id)
            recently_learned.append(review.vocabulary)
            if len(recently_learned) >= limit:
                break
        return recently_learned
