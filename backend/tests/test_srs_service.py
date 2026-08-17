from app.models.flashcard import ReviewResult
from app.services import srs_service


def test_again_resets_interval_to_zero():
    assert srs_service.next_interval_days(current_mastery=3, result=ReviewResult.again) == 0


def test_easy_interval_grows_with_mastery():
    low_mastery = srs_service.next_interval_days(current_mastery=0, result=ReviewResult.easy)
    high_mastery = srs_service.next_interval_days(current_mastery=4, result=ReviewResult.easy)
    assert high_mastery > low_mastery


def test_mastery_level_clamped_between_min_and_max():
    assert srs_service.next_mastery_level(0, ReviewResult.again) == 0  # can't go below 0
    assert srs_service.next_mastery_level(5, ReviewResult.easy) == 5  # can't exceed 5


def test_mastery_increases_on_medium_and_easy():
    assert srs_service.next_mastery_level(2, ReviewResult.medium) == 3
    assert srs_service.next_mastery_level(2, ReviewResult.easy) == 3


def test_mastery_unchanged_on_hard():
    assert srs_service.next_mastery_level(2, ReviewResult.hard) == 2
