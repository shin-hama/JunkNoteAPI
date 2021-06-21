from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.core.config import TOKEN_EXPIRE, ALGORITHM, SECRET_KEY
from app.db.queries import users
from app.models.schemas.users import UserInDB
from app.services.security import oauth2_scheme


def authenticate_user(
    db: Session, username: str, password: str
) -> Optional[UserInDB]:
    """ Get user data that is matched username and password
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not user.verify_password(password):
        return None
    return user


def create_access_token(data: dict[str, object]) -> str:
    expires_delta = timedelta(minutes=TOKEN_EXPIRE)

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserInDB:
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

    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception

    return user


def get_user_by_username(
    db: Session, username: str
) -> Optional[UserInDB]:
    db_user = users.get_user_by_username(db, username)
    if db_user:
        return UserInDB(
            username=db_user.username,
            email=db_user.email,
            created_at=db_user.created_at,
            hashed_password=db_user.hashed_password,
            salt=db_user.salt,
        )

    return None
