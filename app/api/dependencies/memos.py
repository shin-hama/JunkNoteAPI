from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.db.queries import memos
from app.models import models


def check_owner_is_collect(
    memo_id: int, db: Session, owner: models.User
) -> bool:
    memo = get_memo_by_id(db=db, id=memo_id)

    return memo.owner == owner


def get_memo_by_id(db: Session, id: int) -> models.Memo:
    try:
        memo = memos.get_memo(db=db, memo_id=id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your requested id does not exist."
        )

    return memo
