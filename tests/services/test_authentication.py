from sqlalchemy.orm import Session

from app.models import models
from app.services.authentication import check_email_is_taken


def test_email_is_taken(
    test_user: models.User,
    db_session: Session,
) -> None:
    is_taken = check_email_is_taken(db_session, test_user.email)
    assert is_taken


def test_email_is_not_taken(
    test_user: models.User,
    db_session: Session,
) -> None:
    no_taken_email = "no_taken_email@example.com"
    is_taken = check_email_is_taken(db_session, no_taken_email)
    assert is_taken is False
