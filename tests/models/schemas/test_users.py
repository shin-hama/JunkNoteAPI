import pytest

from app.models.schemas import users
from app.services import security


@pytest.fixture
def user() -> users.UserInDB:
    return users.UserInDB(username="test", email="test@email.com")


def test_change_own_password(user: users.UserInDB) -> None:
    old_salt = user.salt
    old_pw = user.hashed_password

    user.change_password("password")
    assert user.salt != old_salt
    assert user.hashed_password != old_pw


def test_password_is_added_salt(user: users.UserInDB) -> None:
    """ Password is added salt when changing password
    """
    pw = "password"
    user.change_password(pw)
    pw_with_salt = user._add_salt(pw)
    assert security.verify_password(pw_with_salt, user.hashed_password)


def test_verify_own_password(user: users.UserInDB) -> None:
    pw = "password"
    user.change_password(pw)
    assert user.verify_password(pw)


def test_verify_incorrect_password(user: users.UserInDB) -> None:
    user.change_password("password")
    assert user.verify_password("incorrect_password") is False
