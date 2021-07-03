from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.db.queries import users
from app.models import models
from app.models.schemas.users import UserInDB
from app.services.security import oauth2_scheme


def authenticate_user(
    db: Session, email: str, password: str
) -> Optional[UserInDB]:
    """ Get user data that is matched username and password
    """
    db_user = users.get_user_by_email(db, email)
    if not db_user:
        return None
    user = UserInDB(**db_user.__dict__)
    if not user.verify_password(password):
        return None
    return user


def create_access_token(data: dict[str, object]) -> str:
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encode_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = users.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception

    return user
