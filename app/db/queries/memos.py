from datetime import datetime

from sqlalchemy.orm import Session

from app.models import models
from app.models.schemas.memos import MemoInCreate, MemoInUpdate


def get_memo(db: Session, memo_id: int) -> models.Memo:
    return db.query(models.Memo).filter(models.Memo.id == memo_id).one()


def get_memos(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.Memo]:
    return db.query(models.Memo).offset(skip).limit(limit).all()


def create_memo_for_user(
    db: Session, memo: MemoInCreate, user_id: int
) -> models.Memo:
    now = datetime.now()
    db_memo = models.Memo(**memo.dict(), owner_id=user_id, datetime=now)
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo


def update_memo(
    memo_id: int, db: Session, memo_update: MemoInUpdate,
) -> MemoInUpdate:
    memo_update.datetime = datetime.now()
    db.query(models.Memo).filter(
        models.Memo.id == memo_id
    ).update(memo_update.dict())
    db.commit()

    return memo_update
