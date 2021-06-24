from datetime import datetime
from typing import Optional

from app.models.schemas.base import BaseSchema


class MemoInCreate(BaseSchema):
    containts: Optional[str] = None
    reference: Optional[str] = None


class MemoInUpdate(MemoInCreate):
    is_removed: bool = False


class MemoBase(BaseSchema):
    containts: str
    reference: Optional[str] = None
    created: Optional[datetime] = None


class MemoInDB(MemoBase):
    id: int
    owner_id: int
    is_removed: bool = False


class MemoInResponce(MemoBase):
    id: int
