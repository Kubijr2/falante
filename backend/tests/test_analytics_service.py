import json
from datetime import date, datetime, timezone

import pytest

from app.models.flashcard import FlashcardReview, ReviewResult
from app.models.vocabulary import Vocabulary
from app.models.writing import WritingSubmission
from app.repositories.flashcard_repository import FlashcardRepository
from app.repositories.vocabulary_repository import VocabularyRepository
from app.repositories.writing_repository import WritingSubmissionRepository
from app.services.analytics_service import AnalyticsService, InvalidRangeError, parse_range


def _dt(y, m, d):
    return datetime(y, m, d, 12, 0, tzinfo=timezone.utc)


@pytest.fixture()
def service(db_session, test_user):
    return AnalyticsService(
        VocabularyRepository(db_session, test_user.id),
        FlashcardRepository(db_session, test_user.id),
        WritingSubmissionRepository(db_session, test_user.id),
    )


def _make_vocab(db_session, user_id, portuguese, created_at):
    v = Vocabulary(
        portuguese=portuguese, english="x", user_id=user_id, created_at=created_at, updated_at=created_at
    )
    v.tags = []
    db_session.add(v)
    db_session.commit()
    db_session.refresh(v)
    return v


def _make_review(db_session, user_id, vocab_id, result, reviewed_at):
    r = FlashcardReview(
        user_id=user_id,
        vocabulary_id=vocab_id,
        result=result,
        reviewed_at=reviewed_at,
        interval_days_before=0,
        interval_days_after=1,
    )
    db_session.add(r)
    db_session.commit()
    return r


class TestParseRange:
    def test_all_returns_none(self):
        assert parse_range("all") is None

    def test_7d_returns_a_date(self):
        assert isinstance(parse_range("7d"), date)

    def test_invalid_range_raises(self):
        with pytest.raises(InvalidRangeError):
            parse_range("bogus")


class TestVocabularyGrowth:
    def test_counts_and_cumulative_totals(self, db_session, test_user, service):
        _make_vocab(db_session, test_user.id, "falar", _dt(2026, 1, 1))
        _make_vocab(db_session, test_user.id, "comer", _dt(2026, 1, 1))
        _make_vocab(db_session, test_user.id, "beber", _dt(2026, 1, 2))

        result = service._vocabulary_growth(None)

        assert result == [
            {"date": "2026-01-01", "count": 2, "cumulative": 2},
            {"date": "2026-01-02", "count": 1, "cumulative": 3},
        ]

    def test_range_filter_keeps_correct_baseline(self, db_session, test_user, service):
        _make_vocab(db_session, test_user.id, "falar", _dt(2026, 1, 1))
        _make_vocab(db_session, test_user.id, "comer", _dt(2026, 1, 10))

        # Filtering to start on the 5th should still count the word from
        # the 1st in the running total, not restart from zero.
        result = service._vocabulary_growth(date(2026, 1, 5))

        assert result == [{"date": "2026-01-10", "count": 1, "cumulative": 2}]


class TestReviewActivityAndQuality:
    def test_activity_counts_per_day(self, db_session, test_user, service):
        v = _make_vocab(db_session, test_user.id, "falar", _dt(2026, 1, 1))
        _make_review(db_session, test_user.id, v.id, ReviewResult.easy, _dt(2026, 1, 2))
        _make_review(db_session, test_user.id, v.id, ReviewResult.hard, _dt(2026, 1, 2))
        _make_review(db_session, test_user.id, v.id, ReviewResult.easy, _dt(2026, 1, 3))

        result = service._review_activity(None)

        assert result == [{"date": "2026-01-02", "count": 2}, {"date": "2026-01-03", "count": 1}]

    def test_quality_breaks_down_by_result(self, db_session, test_user, service):
        v = _make_vocab(db_session, test_user.id, "falar", _dt(2026, 1, 1))
        _make_review(db_session, test_user.id, v.id, ReviewResult.easy, _dt(2026, 1, 2))
        _make_review(db_session, test_user.id, v.id, ReviewResult.again, _dt(2026, 1, 2))

        result = service._review_quality(None)

        assert result == [
            {"date": "2026-01-02", "again": 1, "hard": 0, "medium": 0, "easy": 1}
        ]


class TestMasteryTrend:
    def test_replays_mastery_changes_chronologically(self, db_session, test_user, service):
        # Day 1: word A created (starts at mastery 0)
        a = _make_vocab(db_session, test_user.id, "falar", _dt(2026, 1, 1))
        # Day 2: A reviewed "easy" -> mastery 1
        _make_review(db_session, test_user.id, a.id, ReviewResult.easy, _dt(2026, 1, 2))
        # Day 3: word B created (starts at mastery 0)
        b = _make_vocab(db_session, test_user.id, "comer", _dt(2026, 1, 3))
        # Day 4: A reviewed "easy" again -> mastery 2; B reviewed "medium" -> mastery 1
        _make_review(db_session, test_user.id, a.id, ReviewResult.easy, _dt(2026, 1, 4))
        _make_review(db_session, test_user.id, b.id, ReviewResult.medium, _dt(2026, 1, 4))

        result = service._mastery_trend(None)
        by_date = {row["date"]: row for row in result}

        # Day 1: only A exists, at level 0
        assert by_date["2026-01-01"]["level_0"] == 1
        assert sum(v for k, v in by_date["2026-01-01"].items() if k.startswith("level_")) == 1

        # Day 2: A moved to level 1
        assert by_date["2026-01-02"]["level_1"] == 1
        assert by_date["2026-01-02"]["level_0"] == 0

        # Day 3: B now exists at level 0, A still at level 1
        assert by_date["2026-01-03"]["level_0"] == 1
        assert by_date["2026-01-03"]["level_1"] == 1

        # Day 4: A at level 2, B at level 1
        assert by_date["2026-01-04"]["level_2"] == 1
        assert by_date["2026-01-04"]["level_1"] == 1
        assert by_date["2026-01-04"]["level_0"] == 0

    def test_range_filter_still_reflects_correct_starting_state(self, db_session, test_user, service):
        a = _make_vocab(db_session, test_user.id, "falar", _dt(2026, 1, 1))
        _make_review(db_session, test_user.id, a.id, ReviewResult.easy, _dt(2026, 1, 2))
        _make_review(db_session, test_user.id, a.id, ReviewResult.easy, _dt(2026, 1, 3))

        # Filter starting on day 3 — should still show A already at level 2
        # (from days 1-2), not restart the replay from level 0.
        result = service._mastery_trend(date(2026, 1, 3))
        first_row = result[0]

        assert first_row["date"] == "2026-01-03"
        assert first_row["level_2"] == 1

    def test_empty_history_returns_empty_list(self, service):
        assert service._mastery_trend(None) == []


class TestWritingInsights:
    def test_tallies_correction_types_per_day(self, db_session, test_user, service):
        submission = WritingSubmission(
            user_id=test_user.id,
            original_text="x",
            overall_feedback="ok",
            created_at=_dt(2026, 1, 1),
        )
        submission.corrections = [
            {"type": "grammar", "original": "a", "corrected": "b", "explanation": "c"},
            {"type": "grammar", "original": "d", "corrected": "e", "explanation": "f"},
            {"type": "wording", "original": "g", "corrected": "h", "explanation": "i"},
        ]
        submission.vocabulary_suggestions = []
        db_session.add(submission)
        db_session.commit()

        result = service._writing_insights(None)

        assert result == [{"date": "2026-01-01", "grammar": 2, "wording": 1}]


class TestGetSummary:
    def test_returns_all_five_datasets(self, service):
        summary = service.get_summary("all")
        assert set(summary.keys()) == {
            "vocabulary_growth",
            "review_activity",
            "review_quality",
            "mastery_trend",
            "writing_insights",
        }

    def test_invalid_range_raises(self, service):
        with pytest.raises(InvalidRangeError):
            service.get_summary("not-a-range")
