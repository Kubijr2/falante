from __future__ import annotations

import json

from fastapi import HTTPException, status

from app.models.verb import Verb
from app.repositories.verb_repository import VerbRepository
from app.services.conjugation_engine import TENSE_LABELS, Tense, conjugate_regular

TENSE_ORDER: list[Tense] = list(TENSE_LABELS.keys())


class VerbService:
    def __init__(self, repo: VerbRepository):
        self.repo = repo

    def list(self, search: str | None) -> list[Verb]:
        return self.repo.list(search=search)

    def get_or_404(self, infinitive: str) -> Verb:
        verb = self.repo.get_by_infinitive(infinitive)
        if verb is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Verb '{infinitive}' not found",
            )
        return verb

    def get_conjugations(self, verb: Verb) -> dict[str, list[str]]:
        if verb.is_irregular:
            if not verb.irregular_conjugations:
                raise ValueError(
                    f"Verb '{verb.infinitive}' is marked irregular but has no stored conjugations"
                )
            stored = json.loads(verb.irregular_conjugations)
            return {tense.value: stored[tense.value] for tense in TENSE_ORDER}

        computed = conjugate_regular(verb.infinitive)
        return {tense.value: computed[tense].as_list() for tense in TENSE_ORDER}

    def find_verbs_for_forms(self, forms: list[str]) -> dict[str, Verb]:
        """
        Reverse lookup: given raw word forms as they might appear in a
        learner's own writing or reading ("falo", "somos"), find which verb
        (if any) each one is a conjugated form of.

        Builds one reverse map (every known form -> its verb) per call
        rather than re-conjugating for every requested form — with ~85
        verbs this is cheap, and it means looking up 100 words costs the
        same map-build as looking up 1.
        """
        reverse_map = self._build_reverse_form_map()

        result: dict[str, Verb] = {}
        for form in forms:
            normalized = form.strip().lower()
            if not normalized:
                continue
            verb = reverse_map.get(normalized)
            if verb is not None:
                result[form] = verb
        return result

    def _build_reverse_form_map(self) -> dict[str, Verb]:
        reverse: dict[str, Verb] = {}
        for verb in self.repo.list():
            # The infinitive itself always counts as a "form" of the verb.
            reverse.setdefault(verb.infinitive.lower(), verb)

            if verb.is_irregular:
                if not verb.irregular_conjugations:
                    continue
                stored = json.loads(verb.irregular_conjugations)
                for forms in stored.values():
                    for f in forms:
                        reverse.setdefault(f.lower(), verb)
            else:
                try:
                    computed = conjugate_regular(verb.infinitive)
                except ValueError:
                    continue
                for conj_form in computed.values():
                    for f in conj_form.as_list():
                        reverse.setdefault(f.lower(), verb)
        return reverse
