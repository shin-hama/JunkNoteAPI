from sqlalchemy.orm import Session

from app.models import models, schemas


def get_memo(db: Session, memo_id: int):
    return db.query(models.Memo).filter(models.Memo.id == memo_id).first()


def get_memos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Memo).offset(skip).limit(limit).all()


def create_memo(db: Session, memo: schemas.MemoCreate, user_id: int):
    db_memo = models.Memo(**memo.dict(), owner_id=user_id)
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo
