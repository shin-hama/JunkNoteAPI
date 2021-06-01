from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(32), index=True)
    password = Column(String(32))
    name = Column(String(32))

    memos = relationship("memo", back_populates="owner")


class Memo(Base):
    __tablename__ = "memos"

    id = Column(Integer, primary_key=True, index=True)
    containts = Column(String(2000))
    datetime = Column(DateTime, index=True)
    reference = Column(String(2000))
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_removed = Column(Boolean, default=False, index=True)

    owner = relationship("user", back_populates="memos")
