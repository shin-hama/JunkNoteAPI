from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.api.routes import memos, users


router = APIRouter()
router.include_router(memos.router, tags=["memos"], prefix="/memos")
router.include_router(users.router, tags=["users"], prefix="/users")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


class FakeUser(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[str] = None


class UserInDB(FakeUser):
    hashed_password: str


def fake_hash_password(password: str) -> str:
    return "fakehashed" + password


def fake_decode_token(token: str) -> Optional[UserInDB]:
    if token in fake_users_db:
        return UserInDB(**fake_users_db[token])
    return None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user


@router.get("/users/me")
async def read_users_me(
    current: UserInDB = Depends(get_current_user)
) -> UserInDB:
    return current


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict[str, str]:
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )

    return {"access_token": user.username, "token_type": "bearer"}
