from datetime import datetime
from typing import Optional

from app.models.schemas.base import BaseSchema


class MemoBase(BaseSchema):
    containts: str
    reference: Optional[str] = None


class MemoCreate(MemoBase):
    pass


class MemoInDB(MemoBase):
    id: int
    owner_id: int
    is_removed: bool = False
    datetime: datetime


class MemoInResponce(MemoBase):
    id: int
