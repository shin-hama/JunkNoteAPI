from datetime import datetime

from sqlalchemy.orm import Session

from app.models import models
from app.models.schemas.memos import MemoCreate


def get_memo(db: Session, memo_id: int) -> models.Memo:
    return db.query(models.Memo).filter(models.Memo.id == memo_id).first()


def get_memos(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.Memo]:
    return db.query(models.Memo).offset(skip).limit(limit).all()


def create_memo_for_user(
    db: Session, memo: MemoCreate, user_id: int
) -> models.Memo:
    now = datetime.now()
    db_memo = models.Memo(**memo.dict(), owner_id=user_id, datetime=now)
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo
