from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import authentication as auth
from app.api.dependencies.database import get_db
from app.db.queries.users import create_user
from app.models.schemas.users import UserInCreate, UserInResponse
from app.services.authentication import check_email_is_taken

router = APIRouter()


@router.post("/token", response_model=UserInResponse, name="auth:login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> UserInResponse:
    user = auth.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})

    return UserInResponse(
        **user.dict(),
        access_token=access_token,
        token_type="bearer"
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserInResponse,
    name="auth:register"
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
    user_db = create_user(db, **user_create.dict())

    access_token = auth.create_access_token(data={"sub": user_create.username})
    return UserInResponse(
        **user_db.__dict__,
        access_token=access_token,
        token_type="bearer"
    )
