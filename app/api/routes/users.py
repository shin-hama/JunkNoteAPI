from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.db import SessionLocal, engine
from app.db import users
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


@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return users.create_user(db=db, user=user)


@router.post("/{user_id}/memos")
def create_memo_for_user(
    user_id: int, memo: schemas.MemoCreate, db: Session = Depends(get_db)
):
    return users.create_memo_for_user(db=db, memo=memo, user_id=user_id)
