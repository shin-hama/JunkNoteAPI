from app.services.authentication import check_email_is_taken
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Body
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.authentication import (
    create_access_token, get_current_user
)
from app.core.config import TOKEN_PREFIX
from app.db.queries import users as users_db
from app.models.schemas.memos import Memo, MemoCreate
from app.models.schemas.users import UserInDB, UserInResponse, UserInUpdate

router = APIRouter()


@router.post("/{user_id}/memos", response_model=Memo)
def create_memo_for_user(
    user_id: int, memo: MemoCreate, db: Session = Depends(get_db)
) -> Memo:
    return users_db.create_memo_for_user(db=db, memo=memo, user_id=user_id)


@router.get(
    "/me",
    response_model=UserInResponse,
    name="users:get-current-user"
)
async def read_users_me(
    user: UserInDB = Depends(get_current_user)
) -> UserInResponse:
    # Set response model to hide hashed_password
    token = create_access_token(data={"sub": user.username})

    return UserInResponse(
        **user.dict(),
        access_token=token,
        token_type=TOKEN_PREFIX
    )


@router.put(
    "",
    response_model=UserInResponse,
    name="users:update-current-user"
)
async def update_current_user(
    user_update: UserInUpdate = Body(..., embed=True, alias="user"),
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserInResponse:
    if user_update.email and user_update.email != current_user.email:
        if check_email_is_taken(db, user_update.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail already exists"
            )

    updated_user = users_db.update_user(db, current_user, **user_update.dict())

    token = create_access_token(data={"sub": updated_user.username})
    return UserInResponse(
        **updated_user.dict(),
        access_token=token,
        token_type=TOKEN_PREFIX
    )


@router.delete("")
async def delete_current_user(
    current_user: UserInDB = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> None:
    users_db.delete_user_by_email(db, current_user.email)
