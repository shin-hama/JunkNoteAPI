from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.authentication import (
    create_access_token, get_user, oauth2_scheme
)
from app.core.config import ALGORITHM, SECRET_KEY
from app.db.queries import users as users_db
from app.models.schemas.memos import Memo, MemoCreate
from app.models.schemas.users import UserInCreate, UserInDB, UserWithToken

router = APIRouter()

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


# @router.post("/", response_model=UserWithToken)
# def create_user(
#     user: UserInCreate, db: Session = Depends(get_db)
# ) -> UserWithToken:
#     return users_db.create_user(db=db, user=user)


@router.post("/{user_id}/memos", response_model=Memo)
def create_memo_for_user(
    user_id: int, memo: MemoCreate, db: Session = Depends(get_db)
) -> Memo:
    return users_db.create_memo_for_user(db=db, memo=memo, user_id=user_id)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user)
) -> UserInDB:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/me", response_model=UserWithToken)
async def read_users_me(
    user: UserInDB = Depends(get_current_active_user)
) -> UserInDB:
    # Set response model to hide hashed_password
    access_token = create_access_token(data={"sub": user.username})

    return UserWithToken(**user.dict(), token=access_token)
