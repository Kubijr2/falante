import pytest

from app.services.conjugation_engine import Tense, conjugate_regular, get_conjugation_class


def test_ar_verb_full_paradigm_falar():
    forms = conjugate_regular("falar")
    assert forms[Tense.PRESENT].as_list() == ["falo", "fala", "falamos", "falam"]
    assert forms[Tense.PRETERITO_PERFEITO].as_list() == ["falei", "falou", "falamos", "falaram"]
    assert forms[Tense.PRETERITO_IMPERFEITO].as_list() == [
        "falava",
        "falava",
        "falávamos",
        "falavam",
    ]
    assert forms[Tense.FUTURE].as_list() == ["falarei", "falará", "falaremos", "falarão"]
    assert forms[Tense.CONDITIONAL].as_list() == ["falaria", "falaria", "falaríamos", "falariam"]
    assert forms[Tense.SUBJUNCTIVE_PRESENT].as_list() == ["fale", "fale", "falemos", "falem"]


def test_er_verb_full_paradigm_comer():
    forms = conjugate_regular("comer")
    assert forms[Tense.PRESENT].as_list() == ["como", "come", "comemos", "comem"]
    assert forms[Tense.PRETERITO_PERFEITO].as_list() == ["comi", "comeu", "comemos", "comeram"]
    assert forms[Tense.PRETERITO_IMPERFEITO].as_list() == ["comia", "comia", "comíamos", "comiam"]
    assert forms[Tense.FUTURE].as_list() == ["comerei", "comerá", "comeremos", "comerão"]
    assert forms[Tense.CONDITIONAL].as_list() == ["comeria", "comeria", "comeríamos", "comeriam"]
    assert forms[Tense.SUBJUNCTIVE_PRESENT].as_list() == ["coma", "coma", "comamos", "comam"]


def test_ir_verb_full_paradigm_partir():
    forms = conjugate_regular("partir")
    assert forms[Tense.PRESENT].as_list() == ["parto", "parte", "partimos", "partem"]
    assert forms[Tense.PRETERITO_PERFEITO].as_list() == ["parti", "partiu", "partimos", "partiram"]
    assert forms[Tense.PRETERITO_IMPERFEITO].as_list() == [
        "partia",
        "partia",
        "partíamos",
        "partiam",
    ]
    assert forms[Tense.FUTURE].as_list() == ["partirei", "partirá", "partiremos", "partirão"]
    assert forms[Tense.CONDITIONAL].as_list() == [
        "partiria",
        "partiria",
        "partiríamos",
        "partiriam",
    ]
    assert forms[Tense.SUBJUNCTIVE_PRESENT].as_list() == ["parta", "parta", "partamos", "partam"]


def test_all_six_tenses_present_for_every_class():
    for infinitive in ("morar", "beber", "abrir"):
        forms = conjugate_regular(infinitive)
        assert set(forms.keys()) == set(Tense)


def test_conjugation_class_detection():
    assert get_conjugation_class("falar").value == "ar"
    assert get_conjugation_class("comer").value == "er"
    assert get_conjugation_class("partir").value == "ir"


def test_ar_preterito_eu_orthography_c_to_qu():
    forms = conjugate_regular("ficar")
    assert forms[Tense.PRETERITO_PERFEITO].eu == "fiquei"
    assert forms[Tense.PRETERITO_PERFEITO].ele_ela_voce == "ficou"  # unaffected


def test_ar_preterito_eu_orthography_g_to_gu():
    forms = conjugate_regular("chegar")
    assert forms[Tense.PRETERITO_PERFEITO].eu == "cheguei"


def test_ar_preterito_eu_orthography_c_cedilha_to_c():
    forms = conjugate_regular("começar")
    assert forms[Tense.PRETERITO_PERFEITO].eu == "comecei"


def test_invalid_infinitive_raises():
    # Note: this engine has no way to know a verb is *irregular* — that's a
    # decision made one layer up, in VerbService, based on the `is_irregular`
    # flag on the Verb model. This only tests the one thing the engine can
    # actually detect: an ending it doesn't recognize at all.
    with pytest.raises(ValueError):
        conjugate_regular("xyz")
