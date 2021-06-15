from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.db.queries import memos
from app.models import schemas


router = APIRouter()


@router.get("/", response_model=List[schemas.Memo])
def read_memos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[schemas.Memo]:
    return memos.get_memos(db=db, skip=skip, limit=limit)


@router.get("/{memo_id}", response_model=schemas.Memo)
def read_memo(
    memo_id: int, db: Session = Depends(get_db)
) -> schemas.Memo:
    return memos.get_memo(db=db, memo_id=memo_id)
