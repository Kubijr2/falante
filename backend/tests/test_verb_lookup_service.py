from app.repositories.verb_repository import VerbRepository
from app.services.verb_service import VerbService


def test_find_verbs_for_forms_matches_regular_conjugated_form(db_session):
    service = VerbService(VerbRepository(db_session))
    matches = service.find_verbs_for_forms(["falo"])
    assert matches["falo"].infinitive == "falar"


def test_find_verbs_for_forms_matches_irregular_conjugated_form(db_session):
    service = VerbService(VerbRepository(db_session))
    matches = service.find_verbs_for_forms(["sou"])
    assert matches["sou"].infinitive == "ser"


def test_find_verbs_for_forms_matches_infinitive_itself(db_session):
    service = VerbService(VerbRepository(db_session))
    matches = service.find_verbs_for_forms(["falar"])
    assert matches["falar"].infinitive == "falar"


def test_find_verbs_for_forms_is_case_insensitive(db_session):
    service = VerbService(VerbRepository(db_session))
    matches = service.find_verbs_for_forms(["FALO", "Sou"])
    assert matches["FALO"].infinitive == "falar"
    assert matches["Sou"].infinitive == "ser"


def test_find_verbs_for_forms_no_match_is_simply_absent(db_session):
    service = VerbService(VerbRepository(db_session))
    matches = service.find_verbs_for_forms(["xyznonword", "pizza"])
    assert matches == {}


def test_find_verbs_for_forms_handles_a_mixed_batch(db_session):
    service = VerbService(VerbRepository(db_session))
    matches = service.find_verbs_for_forms(["falo", "pizza", "comi", "sou", "xyz"])
    assert set(matches.keys()) == {"falo", "comi", "sou"}
    assert matches["comi"].infinitive == "comer"


def test_find_verbs_for_forms_handles_orthographic_change_forms(db_session):
    # "fiquei" (I stayed) — the ficar orthographic c->qu case from the
    # conjugation engine's preterito perfeito eu-form fix.
    service = VerbService(VerbRepository(db_session))
    matches = service.find_verbs_for_forms(["fiquei"])
    assert matches["fiquei"].infinitive == "ficar"


def test_find_verbs_for_forms_empty_and_blank_forms_are_skipped(db_session):
    service = VerbService(VerbRepository(db_session))
    matches = service.find_verbs_for_forms(["", "   ", "falo"])
    assert set(matches.keys()) == {"falo"}
