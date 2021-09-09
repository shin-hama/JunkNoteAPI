import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql import func

from app.db.db import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.Text, nullable=False)
    email = sa.Column(sa.Text, index=True, nullable=False, unique=True)
    salt = sa.Column(sa.Text, nullable=False)
    hashed_password = sa.Column(sa.String(60), nullable=False)
    created = sa.Column(sa.DateTime, server_default=func.now())
    updated = sa.Column(
        sa.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    memos: RelationshipProperty = relationship(
        "Memo",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )


class Memo(Base):
    __tablename__ = "memos"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    contents = sa.Column(sa.Text, default="", nullable=False)
    created = sa.Column(sa.DateTime, server_default=func.now())
    updated = sa.Column(
        sa.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
    reference = sa.Column(sa.Text)
    owner_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    removed = sa.Column(sa.Boolean, default=False, index=True, nullable=False)

    owner: RelationshipProperty = relationship(
        "User", back_populates="memos"
    )
