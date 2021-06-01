from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.db import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    password = Column(String)
    name = Column(String)

    memos = relationship("Memo", back_populates="owner")


class Memo(Base):
    __tablename__ = "Memos"

    id = Column(Integer, primary_key=True, index=True)
    containts = Column(String)
    datetime = Column(DateTime, index=True)
    reference = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_removed = Column(Boolean, default=False, index=True)

    owner = relationship("User", back_populates="memos")
