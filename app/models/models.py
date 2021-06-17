from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128), index=True)
    hashed_password = Column(String(32))
    username = Column(String(32))
    created_at = Column(DateTime, index=True)

    memos = relationship("Memo", back_populates="owner")


class Memo(Base):
    __tablename__ = "memos"

    id = Column(Integer, primary_key=True, index=True)
    containts = Column(String(2000))
    datetime = Column(DateTime, index=True)
    reference = Column(String(2000))
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_removed = Column(Boolean, default=False, index=True)

    owner = relationship("User", back_populates="memos")
