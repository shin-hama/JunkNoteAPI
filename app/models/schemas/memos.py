from datetime import datetime
from typing import Optional

from app.models.schemas.base import BaseSchema


class MemoCreate(BaseSchema):
    containts: str
    reference: Optional[str] = None


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
