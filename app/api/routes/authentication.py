from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies.authentication import create_access_token, get_user
from app.api.dependencies.database import get_db
from app.models.schemas.users import UserInCreate, UserInDB, UserInResponse
from app.services.security import get_password_hash, verify_password


router = APIRouter()

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


def authenticate_user(
    fake_db: dict[str, dict[str, object]], username: str, password: str
) -> Optional[UserInDB]:
    user = get_user(fake_db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict[str, str]:
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


def exists_email(db: dict[str, dict[str, object]], email: str) -> bool:
    return any([email == user["email"] for user in db.values()])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserInResponse
)
async def register(
    user_create: UserInCreate = Body(..., embed=True, alias="user"),
    db: Session = Depends(get_db)
) -> UserInResponse:
    if exists_email(fake_users_db, user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E mail already exists"
        )

    hashed_password = get_password_hash(user_create.password)

    access_token = create_access_token(data={"sub": user_create.username})

    user_db = UserInDB(**user_create.dict(), hashed_password=hashed_password)

    return UserInResponse(**{
        "user": {
            **user_db.dict(),
            "token": access_token
        }
    })
