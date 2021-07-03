from app.services.authentication import check_email_is_taken
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Body
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies import authentication as auth
from app.core.config import TOKEN_PREFIX
from app.db.queries import users as users_db
from app.models import models
from app.models.schemas.users import UserInDB, UserInResponse, UserInUpdate


router = APIRouter()


@router.get(
    "/me",
    response_model=UserInResponse,
    name="users:get-current-user"
)
async def read_users_me(
    user: models.User = Depends(auth.get_current_user)
) -> UserInResponse:
    # Set response model to hide hashed_password
    token = auth.create_access_token(data={"sub": user.email})

    return UserInResponse(
        **user.__dict__,
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
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
) -> UserInResponse:
    if user_update.email and user_update.email != current_user.email:
        if check_email_is_taken(db, user_update.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail already exists"
            )

    updated_user = users_db.update_user(
        db, UserInDB(**current_user.__dict__), **user_update.dict()
    )

    token = auth.create_access_token(data={"sub": updated_user.email})
    return UserInResponse(
        **updated_user.dict(),
        access_token=token,
        token_type=TOKEN_PREFIX
    )


@router.delete("", name="memos:delete")
async def delete_current_user(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
) -> None:
    users_db.delete_user(db, current_user)
