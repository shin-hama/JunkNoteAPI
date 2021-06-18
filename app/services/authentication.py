from sqlalchemy.orm import Session
from app.db.queries import users


def check_email_is_taken(db: Session, email: str) -> bool:
    db_user = users.get_user_by_email(db, email)
    return db_user
