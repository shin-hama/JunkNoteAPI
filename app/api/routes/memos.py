from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Body
from sqlalchemy.orm import Session

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.database import get_db
from app.api.dependencies.memos import check_owner_is_collect, get_memo_by_id
from app.db.queries import memos
from app.models import models
from app.models.schemas.memos import MemoInResponce, MemoInCreate, MemoInUpdate


router = APIRouter()


@router.get(
    "",
    response_model=List[MemoInResponce],
    name="memos:get-own-memos",
)
def get_memos_for_current_user(
    skip: int = 0, limit: int = 100, removed: bool = False, q: str = "",
    current_user: models.User = Depends(get_current_user),
) -> list[models.Memo]:
    return memos.get_memos_for_user(current_user, skip, limit, removed, q)


@router.get("/{memo_id}", response_model=MemoInResponce)
def get_memo(
    memo_id: int, db: Session = Depends(get_db)
) -> models.Memo:
    return get_memo_by_id(db=db, id=memo_id)


@router.post("", response_model=MemoInResponce, name="memos:create-own-memo")
def create_memo_for_user(
    memo: MemoInCreate = Body(..., embed=True, alias="memo"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> models.Memo:
    return memos.create_memo_for_user(
        db=db,
        memo=memo,
        user_id=current_user.id
    )


@router.put("/{memo_id}", response_model=MemoInResponce, name="memos:update")
def update_memo(
    memo_id: int,
    memo_update: MemoInUpdate = Body(..., embed=True, alias="memo"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> models.Memo:
    """ Update memo that the current user has. logical delete is done too.
    """
    if check_owner_is_collect(memo_id, db, current_user) is False:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Invalid owner",
        )

    return memos.update_memo(db, memo_id, memo_update)


@router.delete("/{memo_id}", name="memos:delete")
def delete_memo(
    memo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> dict[str, str]:
    if check_owner_is_collect(memo_id, db, current_user) is False:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Invalid owner",
        )

    if memos.delete_memo_by_id(db, memo_id) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect memo",
        )

    return {"status": "Success to delete"}
