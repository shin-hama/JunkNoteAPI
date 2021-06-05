from sqlalchemy.orm import Session

from app.models import models


def get_memo(db: Session, memo_id: int):
    return db.query(models.Memo).filter(models.Memo.id == memo_id).first()


def get_memos(
    db: Session, skip: int = 0, limit: int = 100
):
    return db.query(models.Memo).offset(skip).limit(limit).all()
