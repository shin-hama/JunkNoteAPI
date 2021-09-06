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
    db_memo = models.Memo(**memo.dict(), owner_id=user_id)
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo


def update_memo(
    db: Session, memo_id: int, memo_update: MemoInUpdate,
) -> models.Memo:
    db_memo = db.query(models.Memo).filter(
        models.Memo.id == memo_id
    ).one()
    db_memo.contents = memo_update.contents
    db_memo.reference = memo_update.reference
    db_memo.is_removed = memo_update.is_removed
    db.commit()
    print(db_memo)

    return db_memo


def delete_memo_by_id(db: Session, memo_id: int) -> bool:
    memo_rows = db.query(models.Memo).filter(
        models.Memo.id == memo_id
    ).delete()
    if memo_rows == 1:
        db.commit()
        return True
    else:
        return False
