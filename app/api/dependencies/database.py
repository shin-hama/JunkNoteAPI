from typing import Iterator

from app.db.db import SessionLocal


# Dependency
def get_db() -> Iterator[SessionLocal]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
