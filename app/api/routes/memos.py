from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.database import get_db
from app.db.queries import memos
from app.models import models
from app.models.schemas.memos import MemoInResponce, MemoInCreate, MemoInUpdate


router = APIRouter()


@router.get(
    "",
    response_model=List[MemoInResponce],
    name="memos:get-own-memos",
)
def read_memos_for_current_user(
    skip: int = 0, limit: int = 100,
    current_user: models.User = Depends(get_current_user),
) -> list[MemoInResponce]:
    return current_user.memos[skip:limit]


@router.get("/{memo_id}", response_model=MemoInResponce)
def read_memo(
    memo_id: int, db: Session = Depends(get_db)
) -> MemoInResponce:
    return memos.get_memo(db=db, memo_id=memo_id)


@router.post("", response_model=MemoInResponce, name="memos:create-own-memo")
def create_memo_for_user(
    memo: MemoInCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> MemoInResponce:
    return memos.create_memo_for_user(
        db=db,
        memo=memo,
        user_id=current_user.id
    )


@router.put("/{memo_id}", response_model=MemoInResponce, name="memos:update")
def update_memo(
    memo_id: int,
    memo_update: MemoInUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> MemoInResponce:
    """ Update memo that the current user has.
    """
    try:
        memo = memos.get_memo(db=db, memo_id=memo_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your requested id does not exist."
        )

    if memo.owner != current_user:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Invalid owner"
        )

    updated_memo = memos.update_memo(memo_id, db, memo_update)

    return MemoInResponce(id=memo_id, **updated_memo.dict())
