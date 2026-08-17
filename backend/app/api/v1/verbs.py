from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.verb_repository import VerbRepository
from app.schemas.verb import VerbDetail, VerbListItem
from app.services.verb_service import VerbService

router = APIRouter(prefix="/verbs", tags=["verbs"])


def get_service(db: Session = Depends(get_db)) -> VerbService:
    return VerbService(VerbRepository(db))


@router.get("", response_model=list[VerbListItem])
def list_verbs(search: str | None = None, service: VerbService = Depends(get_service)):
    return service.list(search=search)


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
