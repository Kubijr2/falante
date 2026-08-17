from datetime import datetime, timedelta, timezone

from app.models.flashcard import FlashcardReview, ReviewResult
from app.models.vocabulary import Vocabulary
from app.repositories.flashcard_repository import FlashcardRepository
from app.repositories.vocabulary_repository import VocabularyRepository
from app.services import srs_service


class FlashcardService:
    def __init__(self, vocab_repo: VocabularyRepository, review_repo: FlashcardRepository):
        self.vocab_repo = vocab_repo
        self.review_repo = review_repo

    def due_cards(self) -> list[Vocabulary]:
        return self.vocab_repo.due_for_review(datetime.now(timezone.utc))

    def submit_review(self, vocabulary: Vocabulary, result: ReviewResult) -> Vocabulary:
        interval_before = (vocabulary.next_review_at - vocabulary.updated_at).days
        interval_before = max(interval_before, 0)

        new_mastery = srs_service.next_mastery_level(vocabulary.mastery_level, result)
        interval_after = srs_service.next_interval_days(vocabulary.mastery_level, result)

        vocabulary.mastery_level = new_mastery
        vocabulary.next_review_at = datetime.now(timezone.utc) + timedelta(days=interval_after)
        self.vocab_repo.update(vocabulary)

        review = FlashcardReview(
            vocabulary_id=vocabulary.id,
            result=result,
            interval_days_before=interval_before,
            interval_days_after=interval_after,
        )
        self.review_repo.create_review(review)
        return vocabulary
