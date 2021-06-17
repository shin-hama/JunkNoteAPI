from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.models.schemas.base import BaseSchema


class UserInLogin(BaseSchema):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str


class UserInUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class BaseUser(BaseSchema):
    username: str
    email: str
    disabled: bool


class UserWithToken(BaseUser):
    token: str


class UserInResponse(BaseSchema):
    user: UserWithToken


class UserInDB(BaseUser):
    hashed_password: str = ""
