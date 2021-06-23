from datetime import datetime
from typing import Optional

from app.models.schemas.base import BaseSchema


class MemoInCreate(BaseSchema):
    containts: Optional[str] = None
    reference: Optional[str] = None


class MemoInUpdate(MemoInCreate):
    is_removed: bool = False
    datetime: Optional[datetime] = None


class MemoBase(BaseSchema):
    containts: str
    reference: Optional[str] = None
    datetime: datetime


class MemoInDB(MemoBase):
    id: int
    owner_id: int
    is_removed: bool = False


class MemoInResponce(MemoBase):
    id: int
