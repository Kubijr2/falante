"""
Regular verb conjugation engine.

Kept pure (no DB, no FastAPI) for the same reason srs_service.py and
dashboard_service.py are pure — this is the piece most worth unit testing
exhaustively, and it's testable in isolation because it has no side effects.

Person forms are collapsed to the 4 distinct verb forms actually used in
everyday Brazilian Portuguese (no "tu", no "vós" — both are either archaic
or regional): "eu", "ele/ela/você", "nós", "eles/elas/vocês". "você" and
"ele/ela" always share a form, so grouping them avoids a redundant 6-row
table without losing anything a learner needs.
"""
from dataclasses import dataclass
from enum import Enum


class ConjugationClass(str, Enum):
    AR = "ar"
    ER = "er"
    IR = "ir"


class Tense(str, Enum):
    PRESENT = "present"
    PRETERITO_PERFEITO = "preterito_perfeito"
    PRETERITO_IMPERFEITO = "preterito_imperfeito"
    FUTURE = "future"
    CONDITIONAL = "conditional"
    SUBJUNCTIVE_PRESENT = "subjunctive_present"


# Human-readable labels + display order, single source of truth for both the
# API (which just returns tense keys) and anywhere that needs a friendly name.
TENSE_LABELS: dict[Tense, str] = {
    Tense.PRESENT: "Present",
    Tense.PRETERITO_PERFEITO: "Preterito Perfeito",
    Tense.PRETERITO_IMPERFEITO: "Preterito Imperfeito",
    Tense.FUTURE: "Future",
    Tense.CONDITIONAL: "Conditional",
    Tense.SUBJUNCTIVE_PRESENT: "Subjunctive (Present)",
}

PERSON_LABELS = ["eu", "ele/ela/você", "nós", "eles/elas/vocês"]


@dataclass(frozen=True)
class ConjugationForm:
    eu: str
    ele_ela_voce: str
    nos: str
    eles_elas_voces: str

    def as_list(self) -> list[str]:
        return [self.eu, self.ele_ela_voce, self.nos, self.eles_elas_voces]


# Endings keyed by [tense][conjugation_class] -> (eu, ele/ela/você, nós, eles/elas/vocês)
# Future and Conditional endings are identical across all three classes and
# are appended to the *whole infinitive*, not a stem — handled separately
# below rather than duplicated three times in this table.
_STEM_ENDINGS: dict[Tense, dict[ConjugationClass, tuple[str, str, str, str]]] = {
    Tense.PRESENT: {
        ConjugationClass.AR: ("o", "a", "amos", "am"),
        ConjugationClass.ER: ("o", "e", "emos", "em"),
        ConjugationClass.IR: ("o", "e", "imos", "em"),
    },
    Tense.PRETERITO_PERFEITO: {
        ConjugationClass.AR: ("ei", "ou", "amos", "aram"),
        ConjugationClass.ER: ("i", "eu", "emos", "eram"),
        ConjugationClass.IR: ("i", "iu", "imos", "iram"),
    },
    Tense.PRETERITO_IMPERFEITO: {
        ConjugationClass.AR: ("ava", "ava", "ávamos", "avam"),
        ConjugationClass.ER: ("ia", "ia", "íamos", "iam"),
        ConjugationClass.IR: ("ia", "ia", "íamos", "iam"),
    },
    Tense.SUBJUNCTIVE_PRESENT: {
        ConjugationClass.AR: ("e", "e", "emos", "em"),
        ConjugationClass.ER: ("a", "a", "amos", "am"),
        ConjugationClass.IR: ("a", "a", "amos", "am"),
    },
}

_INFINITIVE_ENDINGS: dict[Tense, tuple[str, str, str, str]] = {
    Tense.FUTURE: ("ei", "á", "emos", "ão"),
    Tense.CONDITIONAL: ("ia", "ia", "íamos", "iam"),
}


def _ar_preterito_eu_orthography(stem: str, plain_eu_form: str) -> str:
    """
    Regular -ar verbs whose stem ends in c/g/ç need a spelling adjustment in
    the preterito perfeito "eu" form to preserve the hard/soft consonant
    sound (ficar -> fiquei, not "ficei"; chegar -> cheguei; começar ->
    comecei). This is the one orthographic exception common enough among
    everyday -ar verbs to be worth handling in the engine rather than just
    excluding those verbs from the seed list.
    """
    if stem.endswith("c"):
        return stem[:-1] + "quei"
    if stem.endswith("g"):
        return stem[:-1] + "guei"
    if stem.endswith("ç"):
        return stem[:-1] + "cei"
    return plain_eu_form


def get_conjugation_class(infinitive: str) -> ConjugationClass:
    suffix = infinitive[-2:]
    try:
        return ConjugationClass(suffix)
    except ValueError as exc:
        raise ValueError(
            f"'{infinitive}' doesn't end in -ar, -er, or -ir — not a regular verb this engine can conjugate."
        ) from exc


def conjugate_regular(infinitive: str) -> dict[Tense, ConjugationForm]:
    """
    Conjugate a regular -ar/-er/-ir verb across all six tenses.
    Raises ValueError for anything that isn't a plain -ar/-er/-ir infinitive —
    irregular verbs are handled entirely separately (see verb_service.py),
    this function should never be called on one.
    """
    conj_class = get_conjugation_class(infinitive)
    stem = infinitive[:-2]

    result: dict[Tense, ConjugationForm] = {}

    for tense, endings_by_class in _STEM_ENDINGS.items():
        endings = endings_by_class[conj_class]
        result[tense] = ConjugationForm(*(stem + ending for ending in endings))

    if conj_class == ConjugationClass.AR:
        perfeito = result[Tense.PRETERITO_PERFEITO]
        corrected_eu = _ar_preterito_eu_orthography(stem, perfeito.eu)
        result[Tense.PRETERITO_PERFEITO] = ConjugationForm(
            eu=corrected_eu,
            ele_ela_voce=perfeito.ele_ela_voce,
            nos=perfeito.nos,
            eles_elas_voces=perfeito.eles_elas_voces,
        )

    for tense, endings in _INFINITIVE_ENDINGS.items():
        result[tense] = ConjugationForm(*(infinitive + ending for ending in endings))

    return result
