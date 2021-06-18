from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from app.core.config import TOKEN_EXPIRE, ALGORITHM, SECRET_KEY
from app.db.queries import users
from app.models.schemas.users import UserInDB


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")


def get_user_by_username(
    db: Session, username: str
) -> Optional[UserInDB]:
    db_user = users.get_user_by_username(db, username)
    if db_user:
        return UserInDB(
            username=db_user.username,
            email=db_user.email,
            disabled=db_user.disabled,
            hashed_password=db_user.hashed_password
        )

    return None


def create_access_token(data: dict[str, object]) -> str:
    expires_delta = timedelta(minutes=TOKEN_EXPIRE)

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt
