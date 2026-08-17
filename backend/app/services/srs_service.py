"""
Spaced-repetition scheduling.

Deliberately kept as pure functions with no DB or FastAPI dependency, so it
can be unit tested in isolation (see tests/test_srs_service.py) and swapped
out later for a smarter algorithm (e.g. SM-2, or the "adaptive ML" idea in
the roadmap) without touching the API or repository layers.
"""
from app.models.flashcard import ReviewResult

# Interval, in days, to schedule the next review to, keyed by result.
# "again" means the card was forgotten — resets progress rather than
# advancing it, which is standard SRS behavior (Anki, SuperMemo, etc.)
_INTERVAL_BY_RESULT: dict[ReviewResult, int] = {
    ReviewResult.again: 0,  # due again same day
    ReviewResult.hard: 1,
    ReviewResult.medium: 3,
    ReviewResult.easy: 7,
}

# Mastery level (0-5) change per result.
_MASTERY_DELTA: dict[ReviewResult, int] = {
    ReviewResult.again: -1,
    ReviewResult.hard: 0,
    ReviewResult.medium: 1,
    ReviewResult.easy: 1,
}

MIN_MASTERY = 0
MAX_MASTERY = 5


def next_interval_days(current_mastery: int, result: ReviewResult) -> int:
    """
    Base interval scales with mastery: a word at mastery 4 that's marked
    "easy" gets a longer gap than a brand-new word marked "easy". This is a
    deliberately simple multiplier — swap this function out for a real SM-2
    implementation later without touching anything else.
    """
    base = _INTERVAL_BY_RESULT[result]
    if result in (ReviewResult.medium, ReviewResult.easy):
        multiplier = 1 + (current_mastery * 0.5)
        return max(base, round(base * multiplier))
    return base


def next_mastery_level(current_mastery: int, result: ReviewResult) -> int:
    new_level = current_mastery + _MASTERY_DELTA[result]
    return min(MAX_MASTERY, max(MIN_MASTERY, new_level))
