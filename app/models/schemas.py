from datetime import datetime
from typing import List

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
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    memos: List[Memo]

    class Config:
        orm_mode = True
