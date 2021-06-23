from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.database import get_db
from app.db.queries import memos
from app.models import models
from app.models.schemas.memos import MemoInResponce, MemoCreate


router = APIRouter()


@router.get(
    "",
    response_model=List[MemoInResponce],
    name="memos:get-own-memos"
)
def read_memos_for_current_user(
    skip: int = 0, limit: int = 100,
    current_user: models.User = Depends(get_current_user),
) -> list[MemoInResponce]:
    return current_user.memos[skip:limit]


@router.get("/{memo_id}", response_model=MemoInResponce)
def read_memo(
    memo_id: int, db: Session = Depends(get_db)
) -> MemoInResponce:
    return memos.get_memo(db=db, memo_id=memo_id)


@router.post("", response_model=MemoInResponce)
def create_memo_for_user(
    memo: MemoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> MemoInResponce:
    return memos.create_memo_for_user(
        db=db,
        memo=memo,
        user_id=current_user.id
    )
