from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.current_user import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.flashcard_repository import FlashcardRepository
from app.repositories.vocabulary_repository import VocabularyRepository
from app.schemas.flashcard import ReviewSubmit
from app.schemas.vocabulary import VocabularyRead
from app.services.flashcard_service import FlashcardService
from app.services.vocabulary_service import VocabularyService

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


def get_service(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> FlashcardService:
    return FlashcardService(
        VocabularyRepository(db, current_user.id), FlashcardRepository(db, current_user.id)
    )


def get_vocab_service(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> VocabularyService:
    return VocabularyService(VocabularyRepository(db, current_user.id))


@router.get("/due", response_model=list[VocabularyRead])
def get_due_cards(service: FlashcardService = Depends(get_service)):
    return service.due_cards()


@router.post("/{vocabulary_id}/review", response_model=VocabularyRead)
def submit_review(
    vocabulary_id: int,
    data: ReviewSubmit,
    service: FlashcardService = Depends(get_service),
    vocab_service: VocabularyService = Depends(get_vocab_service),
):
    vocabulary = vocab_service.get_or_404(vocabulary_id)
    return service.submit_review(vocabulary, data.result)
