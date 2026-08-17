from __future__ import annotations

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models.flashcard import FlashcardReview, ReviewResult
from app.models.vocabulary import Vocabulary


class FlashcardRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_review(self, review: FlashcardReview) -> FlashcardReview:
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def count_total(self) -> int:
        stmt = select(func.count()).select_from(FlashcardReview)
        return self.db.execute(stmt).scalar_one()

    def all_review_dates(self) -> list[date]:
        """
        Every calendar date that had at least one review. SQLite and Postgres
        both support func.date() to truncate a datetime column, so this stays
        portable across the DB swap described in the architecture doc.
        """
        stmt = select(func.date(FlashcardReview.reviewed_at)).distinct()
        rows = self.db.execute(stmt).scalars().all()
        return [d if isinstance(d, date) else date.fromisoformat(d) for d in rows]

    def recently_learned_vocabulary(
        self, results: tuple[ReviewResult, ...], limit: int
    ) -> list[Vocabulary]:
        """
        Most recent distinct words whose review result was in `results`
        (i.e. mastery increased — see PROGRESS_RESULTS in dashboard_service.py).
        Dedupes by vocabulary, keeping only the most recent qualifying review
        per word.
        """
        stmt = (
            select(FlashcardReview)
            .options(joinedload(FlashcardReview.vocabulary))
            .where(FlashcardReview.result.in_(results))
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
