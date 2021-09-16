from datetime import datetime
from typing import Optional

from app.models.schemas.base import BaseSchema


class MemoInCreate(BaseSchema):
    contents: Optional[str] = ""
    reference: Optional[str] = None


class MemoInUpdate(MemoInCreate):
    removed: bool = False
    pinned: bool = False


class MemoBase(BaseSchema):
    contents: str
    reference: Optional[str] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    pinned: bool = False


class MemoInDB(MemoBase):
    id: int
    owner_id: int
    removed: bool = False


class MemoInResponce(MemoBase):
    id: int
