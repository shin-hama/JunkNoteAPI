from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies.authentication import (
    create_access_token, get_user_by_username
)
from app.api.dependencies.database import get_db
from app.db.queries.users import create_user
from app.models.schemas.users import UserInCreate, UserInDB, UserInResponse
from app.services.authentication import check_email_is_taken
from app.services.security import get_password_hash

router = APIRouter()


def authenticate_user(
    db: Session, username: str, password: str
) -> Optional[UserInDB]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not user.verify_password(password):
        return None
    return user


@router.post("/login", response_model=UserInResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> UserInResponse:
    user = authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})

    return UserInResponse(
        **user.dict(),
        access_token=access_token,
        token_type="bearer"
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserInResponse
)
async def register(
    user_create: UserInCreate = Body(..., embed=True, alias="user"),
    db: Session = Depends(get_db)
) -> UserInResponse:
    if check_email_is_taken(db, user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail already exists"
        )

    hashed_password = get_password_hash(user_create.password)

    access_token = create_access_token(data={"sub": user_create.username})

    user_db = UserInDB(**user_create.dict(), hashed_password=hashed_password)
    create_user(db, user_db)

    return UserInResponse(
        **user_db.dict(),
        access_token=access_token,
        token_type="bearer"
    )
