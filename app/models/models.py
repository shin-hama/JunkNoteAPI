import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.db import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.Text, nullable=False)
    email = sa.Column(sa.Text, index=True, nullable=False, unique=True)
    salt = sa.Column(sa.Text, nullable=False)
    hashed_password = sa.Column(sa.String(60), nullable=False)
    created_at = sa.Column(sa.DateTime, index=True)

    memos = relationship("Memo", back_populates="owner")


class Memo(Base):
    __tablename__ = "memos"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    containts = sa.Column(sa.Text)
    datetime = sa.Column(sa.DateTime, index=True)
    reference = sa.Column(sa.Text)
    owner_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    is_removed = sa.Column(sa.Boolean, default=False, index=True)

    owner = relationship("User", back_populates="memos")
