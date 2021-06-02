from datetime import datetime

from pydantic import BaseModel


class MemoBase(BaseModel):
    containts: str
    datetime: datetime
    reference = str

    class Config:
        orm_mode = True


class MemoCreate(MemoBase):
    pass


class Memo(MemoBase):
    owner_id: int
    is_removed: bool


class UserBase(BaseModel):
    user_id: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    name: str
    memos: list[Memo]

    class Config:
        orm_mode = True
