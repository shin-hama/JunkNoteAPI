from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class MemoBase(BaseModel):
    containts: str
    datetime: datetime
    reference: Optional[str] = None


class MemoCreate(MemoBase):
    pass


class Memo(MemoBase):
    id: int
    owner_id: int
    is_removed: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    user_id: str
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    memos: List[Memo] = []
    created_at: datetime

    class Config:
        orm_mode = True
