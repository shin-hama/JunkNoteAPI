from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.db.queries import users
from app.models import schemas


router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    return users.create_user(db=db, user=user)


@router.post("/{user_id}/memos", response_model=schemas.Memo)
def create_memo_for_user(
    user_id: int, memo: schemas.MemoCreate, db: Session = Depends(get_db)
) -> schemas.Memo:
    return users.create_memo_for_user(db=db, memo=memo, user_id=user_id)
