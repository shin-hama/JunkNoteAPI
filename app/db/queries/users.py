from datetime import datetime

from sqlalchemy.orm import Session

from app.models.schemas.users import UserInCreate
from app.models.schemas.memos import MemoCreate
from app.models import models


def create_user(db: Session, user: UserInCreate) -> models.User:
    now = datetime.now()
    db_user = models.User(**user.dict(), created_at=now)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_memo_for_user(
    db: Session, memo: MemoCreate, user_id: int
) -> models.Memo:
    db_memo = models.Memo(**memo.dict(), owner_id=user_id)
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo
