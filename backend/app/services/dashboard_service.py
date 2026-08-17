"""
Dashboard aggregation logic.

`compute_streak` is kept pure (no DB, no datetime.now() inside it) for the
same reason app/services/srs_service.py is pure — easy to unit test every
edge case (gap on day 1, gap in the middle, empty history) without touching
a database.
"""
from datetime import date, timedelta

from app.models.flashcard import ReviewResult
from app.repositories.flashcard_repository import FlashcardRepository
from app.repositories.vocabulary_repository import VocabularyRepository

# Reviews with these results are the ones that actually increase mastery —
# see _MASTERY_DELTA in srs_service.py. "recently learned" tracks these.
PROGRESS_RESULTS = (ReviewResult.medium, ReviewResult.easy)

RECENTLY_LEARNED_LIMIT = 5


def compute_streak(review_dates: list[date], today: date) -> int:
    """
    Consecutive-day streak, Duolingo-style: a review today OR yesterday keeps
    the streak alive (you get today to keep it going before it breaks), but
    a review only two-or-more days ago means the streak already broke.
    """
    if not review_dates:
        return 0

    distinct_dates = sorted(set(review_dates), reverse=True)
    most_recent = distinct_dates[0]

    if most_recent < today - timedelta(days=1):
        return 0  # most recent activity was more than a day ago — streak's broken

    streak = 1
    cursor = most_recent
    for d in distinct_dates[1:]:
        if d == cursor - timedelta(days=1):
            streak += 1
            cursor = d
        elif d == cursor:
            continue  # duplicate/same-day guard, shouldn't happen post-dedupe
        else:
            break
    return streak


class DashboardService:
    def __init__(self, vocab_repo: VocabularyRepository, review_repo: FlashcardRepository):
        self.vocab_repo = vocab_repo
        self.review_repo = review_repo

    def get_summary(self, today: date):
        review_dates = self.review_repo.all_review_dates()
        streak = compute_streak(review_dates, today)

        return {
            "streak": streak,
            "total_words": self.vocab_repo.count_total(),
            "due_today": len(self.vocab_repo.due_for_review(_end_of_day_utc(today))),
            "total_reviews": self.review_repo.count_total(),
            "mastery_distribution": self.vocab_repo.mastery_distribution(),
            "recently_learned": self.review_repo.recently_learned_vocabulary(
                results=PROGRESS_RESULTS, limit=RECENTLY_LEARNED_LIMIT
            ),
        }


def _end_of_day_utc(d: date):
    from datetime import datetime, timezone

    return datetime.combine(d, datetime.max.time(), tzinfo=timezone.utc)
