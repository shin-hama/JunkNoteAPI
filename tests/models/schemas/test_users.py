from app.models.schemas import users
from app.services import security


def test_change_own_password():
    user = users.UserInDB()
    old_salt = user.salt
    old_pw = user.hashed_password

    user.change_password("password")
    assert user.salt != old_salt
    assert user.hashed_password != old_pw


def test_password_is_added_salt():
    """ Password is added salt when changing password
    """
    user = users.UserInDB()
    pw = "password"
    user.change_password(pw)
    pw_with_salt = user._add_salt(pw)
    assert security.verify_password(pw_with_salt, user.hashed_password)


def test_verify_own_password():
    user = users.UserInDB()
    pw = "password"
    user.change_password(pw)
    assert user.verify_password(pw)


def test_verify_incorrect_password():
    user = users.UserInDB()
    user.change_password("password")
    assert user.verify_password("incorrect_password")
