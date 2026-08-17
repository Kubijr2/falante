from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.grammar_repository import GrammarRepository
from app.schemas.grammar import GrammarTopicDetail, GrammarTopicListItem
from app.services.grammar_service import GrammarService

router = APIRouter(prefix="/grammar", tags=["grammar"])


def get_service(db: Session = Depends(get_db)) -> GrammarService:
    return GrammarService(GrammarRepository(db))


@router.get("", response_model=list[GrammarTopicListItem])
def list_topics(
    category: str | None = None,
    search: str | None = None,
    service: GrammarService = Depends(get_service),
):
    return service.list(category=category, search=search)


@router.get("/categories", response_model=list[str])
def list_categories(service: GrammarService = Depends(get_service)):
    return service.list_categories()


@router.get("/{slug}", response_model=GrammarTopicDetail)
def get_topic(slug: str, service: GrammarService = Depends(get_service)):
    return service.get_by_slug_or_404(slug)
