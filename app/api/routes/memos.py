from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.db import SessionLocal, engine
from app.db import memos
from app.models import models, schemas


models.Base.metadata.create_all(bind=engine)

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Memo])
def read_memos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return memos.get_memos(db=db, skip=skip, limit=limit)


@router.get("/{memo_id}", response_model=schemas.Memo)
def read_memo(
    memo_id: int, db: Session = Depends(get_db)
):
    return memos.get_memo(db=db, memo_id=memo_id)
