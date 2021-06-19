from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.schemas.base import BaseSchema
from app.services import security


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
    disabled: bool = False


class UserInResponse(BaseUser):
    access_token: str
    token_type: str


class UserInDB(BaseUser):
    salt: str = ""
    hashed_password: str = ""

    def verify_password(self, password: str) -> bool:
        return security.verify_password(
            self._add_salt(password), self.hashed_password
        )

    def change_password(self, new_password: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(
            self._add_salt(new_password)
        )

    def _add_salt(self, password: str) -> str:
        return f"{password}{self.salt}"
