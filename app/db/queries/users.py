from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.schemas.users import UserInDB
from app.models.schemas.memos import MemoCreate
from app.models import models


def create_user(db: Session, user: UserInDB) -> models.User:
    now = datetime.now()
    db_user = models.User(**user.dict(), created_at=now)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session,
    user: UserInDB,
    username: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
) -> UserInDB:
    org_email = user.email
    user.username = username or user.username
    user.email = email or user.email
    if password:
        user.change_password(password)

    db.query(models.User).filter(
        models.User.email == org_email
    ).update(user.dict())
    db.commit()

    return user


def create_memo_for_user(
    db: Session, memo: MemoCreate, user_id: int
) -> models.Memo:
    db_memo = models.Memo(**memo.dict(), owner_id=user_id)
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    db_user = db.query(models.User).filter(
        models.User.username == username
    ).first()
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    db_user = db.query(models.User).filter(
        models.User.email == email
    ).first()
    return db_user
