from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.vocabulary_repository import VocabularyRepository
from app.schemas.vocabulary import VocabularyCreate, VocabularyRead, VocabularyUpdate
from app.services.vocabulary_service import VocabularyService

router = APIRouter(prefix="/vocabulary", tags=["vocabulary"])


def get_service(db: Session = Depends(get_db)) -> VocabularyService:
    return VocabularyService(VocabularyRepository(db))


@router.get("", response_model=list[VocabularyRead])
def list_vocabulary(
    category: str | None = None,
    search: str | None = None,
    service: VocabularyService = Depends(get_service),
):
    return service.list(category=category, search=search)


@router.post("", response_model=VocabularyRead, status_code=status.HTTP_201_CREATED)
def create_vocabulary(
    data: VocabularyCreate,
    service: VocabularyService = Depends(get_service),
):
    return service.create(data)


@router.get("/{vocabulary_id}", response_model=VocabularyRead)
def get_vocabulary(vocabulary_id: int, service: VocabularyService = Depends(get_service)):
    return service.get_or_404(vocabulary_id)


@router.patch("/{vocabulary_id}", response_model=VocabularyRead)
def update_vocabulary(
    vocabulary_id: int,
    data: VocabularyUpdate,
    service: VocabularyService = Depends(get_service),
):
    return service.update(vocabulary_id, data)


@router.delete("/{vocabulary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vocabulary(vocabulary_id: int, service: VocabularyService = Depends(get_service)):
    service.delete(vocabulary_id)
