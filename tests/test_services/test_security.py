import pytest

from app.services import security


@pytest.fixture
def pw() -> str:
    return "password"


def test_generate_salt_difference_every_time():
    salt1 = security.generate_salt()
    salt2 = security.generate_salt()
    assert salt1 != salt2


def test_verify_correct_password(pw: str):
    hashed_pw = security.get_password_hash(pw)
    assert security.verify_password(pw, hashed_pw)


def test_verify_incorrect_password():
    hashed_pw = security.get_password_hash("password")
    assert security.verify_password("incorrect_password", hashed_pw) is False


def test_generate_hash(pw: str):
    hashed = security.get_password_hash(pw)
    assert hashed != pw
    assert len(hashed) is 256


def test_get_same_hash(pw: str):
    first = security.get_password_hash(pw)
    second = security.get_password_hash(pw)
    assert first == second


def test_get_different_hash():
    pw1 = "password1"
    pw2 = "password2"
    first = security.get_password_hash(pw1)
    second = security.get_password_hash(pw2)
    assert first != second
