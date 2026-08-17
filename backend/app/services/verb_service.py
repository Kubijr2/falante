from __future__ import annotations

import json

from fastapi import HTTPException, status

from app.models.verb import Verb
from app.repositories.verb_repository import VerbRepository
from app.services.conjugation_engine import TENSE_LABELS, Tense, conjugate_regular

# Fixed display order for tenses — Python dict order is preserved through
# Pydantic/FastAPI's JSON serialization, so this also controls the order the
# frontend receives them in.
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
        """
        Irregular verbs: parse the stored JSON blob.
        Regular verbs: compute on the fly via the conjugation engine —
        nothing about a regular verb's forms is ever stored in the DB.
        """
        if verb.is_irregular:
            if not verb.irregular_conjugations:
                raise ValueError(
                    f"Verb '{verb.infinitive}' is marked irregular but has no stored conjugations"
                )
            stored = json.loads(verb.irregular_conjugations)
            return {tense.value: stored[tense.value] for tense in TENSE_ORDER}

        computed = conjugate_regular(verb.infinitive)
        return {tense.value: computed[tense].as_list() for tense in TENSE_ORDER}
