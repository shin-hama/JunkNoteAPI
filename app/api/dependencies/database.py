from typing import Iterator

from sqlalchemy.orm.session import Session

from app.db.db import SessionLocal


# Dependency
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
