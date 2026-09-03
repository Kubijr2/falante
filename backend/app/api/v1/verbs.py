from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.verb_repository import VerbRepository
from app.schemas.verb import (
    VerbDetail,
    VerbFormLookupRequest,
    VerbFormLookupResponse,
    VerbFormLookupResult,
    VerbListItem,
)
from app.services.verb_service import VerbService

router = APIRouter(prefix="/verbs", tags=["verbs"])


def get_service(db: Session = Depends(get_db)) -> VerbService:
    return VerbService(VerbRepository(db))


@router.get("", response_model=list[VerbListItem])
def list_verbs(search: str | None = None, service: VerbService = Depends(get_service)):
    return service.list(search=search)


@router.post("/lookup-batch", response_model=VerbFormLookupResponse)
def lookup_verb_forms(payload: VerbFormLookupRequest, service: VerbService = Depends(get_service)):
    """
    Given a batch of raw word forms (e.g. tokens pulled out of a pasted
    reading passage), returns which ones are conjugated forms of a known
    verb, and what that verb's infinitive + translation are. Forms with no
    match are simply absent from the response rather than erroring — most
    words in any given passage won't be verb forms at all, and that's
    expected, not exceptional.
    """
    matches = service.find_verbs_for_forms(payload.forms)
    return VerbFormLookupResponse(
        matches={
            form: VerbFormLookupResult(infinitive=verb.infinitive, translation=verb.translation)
            for form, verb in matches.items()
        }
    )


@router.get("/{infinitive}", response_model=VerbDetail)
def get_verb(infinitive: str, service: VerbService = Depends(get_service)):
    verb = service.get_or_404(infinitive)
    conjugations = service.get_conjugations(verb)
    return VerbDetail(
        id=verb.id,
        infinitive=verb.infinitive,
        translation=verb.translation,
        is_irregular=verb.is_irregular,
        conjugations=conjugations,
    )
