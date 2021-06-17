from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.core.config import TOKEN_EXPIRE, ALGORITHM, SECRET_KEY
from app.models.schemas.users import UserInDB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")


def get_user(
    db: dict[str, dict[str, object]], username: str
) -> Optional[UserInDB]:
    if username in db:
        return UserInDB(**db[username])
    return None


def create_access_token(data: dict[str, object]) -> str:
    expires_delta = timedelta(minutes=TOKEN_EXPIRE)

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt
