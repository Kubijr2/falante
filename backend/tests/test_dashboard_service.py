from datetime import date, timedelta

from app.services.dashboard_service import compute_streak

TODAY = date(2026, 8, 5)


def test_no_reviews_gives_zero_streak():
    assert compute_streak([], TODAY) == 0


def test_review_today_only_gives_streak_of_one():
    assert compute_streak([TODAY], TODAY) == 1


def test_review_yesterday_but_not_today_still_counts():
    yesterday = TODAY - timedelta(days=1)
    assert compute_streak([yesterday], TODAY) == 1


def test_review_two_days_ago_breaks_streak():
    two_days_ago = TODAY - timedelta(days=2)
    assert compute_streak([two_days_ago], TODAY) == 0


def test_consecutive_days_count_correctly():
    dates = [TODAY - timedelta(days=i) for i in range(5)]  # today, -1, -2, -3, -4
    assert compute_streak(dates, TODAY) == 5


def test_gap_in_history_stops_the_count():
    dates = [TODAY, TODAY - timedelta(days=1), TODAY - timedelta(days=3)]  # gap at -2
    assert compute_streak(dates, TODAY) == 2


def test_duplicate_dates_dont_inflate_streak():
    dates = [TODAY, TODAY, TODAY - timedelta(days=1)]
    assert compute_streak(dates, TODAY) == 2
