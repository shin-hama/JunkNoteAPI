from sqlalchemy.orm import Session

from app.models import models, schemas


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_memo_for_user(
    db: Session, memo: schemas.MemoCreate, user_id: int
) -> models.Memo:
    db_memo = models.Memo(**memo.dict(), owner_id=user_id)
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo
