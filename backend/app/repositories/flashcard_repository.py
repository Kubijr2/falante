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

    def counts_by_day(self, start_date: date | None) -> list[tuple[str, int]]:
        """Reviews per day — raw material for the review-activity heatmap."""
        stmt = select(func.date(FlashcardReview.reviewed_at), func.count()).where(
            FlashcardReview.user_id == self.user_id
        )
        if start_date is not None:
            stmt = stmt.where(FlashcardReview.reviewed_at >= start_date)
        stmt = stmt.group_by(func.date(FlashcardReview.reviewed_at)).order_by(
            func.date(FlashcardReview.reviewed_at)
        )
        return list(self.db.execute(stmt).all())

    def counts_by_day_and_result(
        self, start_date: date | None
    ) -> list[tuple[str, ReviewResult, int]]:
        """Reviews per day, broken down by result — raw material for the review-quality trend."""
        stmt = select(
            func.date(FlashcardReview.reviewed_at), FlashcardReview.result, func.count()
        ).where(FlashcardReview.user_id == self.user_id)
        if start_date is not None:
            stmt = stmt.where(FlashcardReview.reviewed_at >= start_date)
        stmt = stmt.group_by(func.date(FlashcardReview.reviewed_at), FlashcardReview.result)
        return list(self.db.execute(stmt).all())

    def all_reviews_ordered(self) -> list[tuple[int, date, ReviewResult]]:
        """
        Every review (vocabulary_id, date, result), full history in
        chronological order — needed to replay mastery-level changes for
        the mastery trend chart. Always full history regardless of any
        display range, for the same reason list_id_and_created_date() is:
        an accurate trend for a filtered window still needs to know the
        correct starting state going into that window.
        """
        stmt = (
            select(
                FlashcardReview.vocabulary_id,
                func.date(FlashcardReview.reviewed_at),
                FlashcardReview.result,
            )
            .where(FlashcardReview.user_id == self.user_id)
            .order_by(FlashcardReview.reviewed_at)
        )
        rows = self.db.execute(stmt).all()
        return [
            (vid, d if isinstance(d, date) else date.fromisoformat(d), result)
            for vid, d, result in rows
        ]
