from __future__ import annotations

import json
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone

from app.repositories.flashcard_repository import FlashcardRepository
from app.repositories.vocabulary_repository import VocabularyRepository
from app.repositories.writing_repository import WritingSubmissionRepository
from app.services import srs_service

VALID_RANGES = ("7d", "30d", "90d", "all")

VALID_WIDGET_IDS = (
    "vocabulary_growth",
    "review_activity",
    "review_quality",
    "mastery_trend",
    "writing_insights",
)


class InvalidRangeError(Exception):
    pass


def parse_range(range_param: str) -> date | None:
    """Returns the start date a range string implies, or None for "all" (no lower bound)."""
    # created_at/reviewed_at are stored in UTC, so the "today" boundary here
    # must be UTC too — local date.today() can be a day behind UTC (e.g. any
    # evening in a UTC-negative timezone), which silently drops same-day
    # activity from every range filter and from the mastery trend below.
    today = datetime.now(timezone.utc).date()
    if range_param == "7d":
        return today - timedelta(days=7)
    if range_param == "30d":
        return today - timedelta(days=30)
    if range_param == "90d":
        return today - timedelta(days=90)
    if range_param == "all":
        return None
    raise InvalidRangeError(
        f"'{range_param}' isn't a valid range. Use one of: {', '.join(VALID_RANGES)}."
    )


class AnalyticsService:
    def __init__(
        self,
        vocabulary_repo: VocabularyRepository,
        flashcard_repo: FlashcardRepository,
        writing_repo: WritingSubmissionRepository,
    ):
        self.vocabulary_repo = vocabulary_repo
        self.flashcard_repo = flashcard_repo
        self.writing_repo = writing_repo

    def get_summary(self, range_param: str) -> dict:
        start_date = parse_range(range_param)
        return {
            "vocabulary_growth": self._vocabulary_growth(start_date),
            "review_activity": self._review_activity(start_date),
            "review_quality": self._review_quality(start_date),
            "mastery_trend": self._mastery_trend(start_date),
            "writing_insights": self._writing_insights(start_date),
        }

    def _vocabulary_growth(self, start_date: date | None) -> list[dict]:
        baseline = self.vocabulary_repo.count_before(start_date) if start_date else 0
        rows = self.vocabulary_repo.count_by_day(start_date)

        cumulative = baseline
        result = []
        for day_str, count in rows:
            cumulative += count
            result.append({"date": day_str, "count": count, "cumulative": cumulative})
        return result

    def _review_activity(self, start_date: date | None) -> list[dict]:
        rows = self.flashcard_repo.counts_by_day(start_date)
        return [{"date": day_str, "count": count} for day_str, count in rows]

    def _review_quality(self, start_date: date | None) -> list[dict]:
        rows = self.flashcard_repo.counts_by_day_and_result(start_date)
        by_date: dict[str, dict[str, int]] = defaultdict(
            lambda: {"again": 0, "hard": 0, "medium": 0, "easy": 0}
        )
        for day_str, result, count in rows:
            by_date[day_str][result.value] = count
        return [{"date": day_str, **counts} for day_str, counts in sorted(by_date.items())]

    def _mastery_trend(self, start_date: date | None) -> list[dict]:
        """
        There's no stored history of mastery levels over time — only the
        current value. This reconstructs it by replaying every review in
        chronological order (using the exact same delta rules
        srs_service.py applies live) and recording a distribution snapshot
        for each day in the requested window.

        Always replays from a word's actual creation date and the very
        first review, regardless of the requested range — a "last 7 days"
        view still needs to know the correct mastery levels *entering*
        that window, not start everyone over at level 0.
        """
        vocab_created = self.vocabulary_repo.list_id_and_created_date()
        if not vocab_created:
            return []

        reviews = self.flashcard_repo.all_reviews_ordered()

        vocab_created_by_date: dict[date, list[int]] = defaultdict(list)
        for vocab_id, created_date in vocab_created:
            vocab_created_by_date[created_date].append(vocab_id)

        reviews_by_date: dict[date, list[tuple[int, object]]] = defaultdict(list)
        for vocab_id, reviewed_date, result in reviews:
            reviews_by_date[reviewed_date].append((vocab_id, result))

        first_day = min(vocab_created_by_date.keys())
        last_day = datetime.now(timezone.utc).date()

        mastery: dict[int, int] = {}
        result: list[dict] = []
        current = first_day
        while current <= last_day:
            for vocab_id in vocab_created_by_date.get(current, []):
                mastery[vocab_id] = 0
            for vocab_id, review_result in reviews_by_date.get(current, []):
                mastery[vocab_id] = srs_service.next_mastery_level(
                    mastery.get(vocab_id, 0), review_result
                )

            if start_date is None or current >= start_date:
                distribution = {i: 0 for i in range(6)}
                for level in mastery.values():
                    distribution[level] += 1
                result.append(
                    {
                        "date": current.isoformat(),
                        **{f"level_{i}": distribution[i] for i in range(6)},
                    }
                )

            current += timedelta(days=1)

        return result

    def _writing_insights(self, start_date: date | None) -> list[dict]:
        rows = self.writing_repo.list_dates_and_corrections(start_date)
        by_date: dict[str, dict[str, int]] = defaultdict(lambda: {"grammar": 0, "wording": 0})
        for day, corrections_raw in rows:
            day_str = day.isoformat()
            corrections = json.loads(corrections_raw) if corrections_raw else []
            for correction in corrections:
                correction_type = correction.get("type")
                if correction_type in ("grammar", "wording"):
                    by_date[day_str][correction_type] += 1
        return [{"date": day_str, **counts} for day_str, counts in sorted(by_date.items())]
