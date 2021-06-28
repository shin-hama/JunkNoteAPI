from fastapi import FastAPI, status
from fastapi.testclient import TestClient
import pytest

from app.models import models


def test_unable_to_register_same_email_user(
    app: FastAPI, client: TestClient, test_user: models.User
) -> None:
    res = client.post(
        app.url_path_for("auth:register"),
        json={"user": {
            "email": test_user.email,
            "password": "password2",
            "username": "test2",
        }},
    )

    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_unable_to_login_no_registered_user(
    app: FastAPI, client: TestClient
) -> None:
    res = client.post(
        app.url_path_for("auth:login"),
        data={"username": "wrong_user", "password": "Null"},
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "username, password",
    (("test", "wrong_password"), ("wrong_user", "password")),
)
def test_unable_to_login_with_wrong_input_oneside(
    app: FastAPI,
    client: TestClient,
    test_user: models.User,
    username: str,
    password: str
) -> None:
    res = client.post(
        app.url_path_for("auth:login"),
        data={"username": username, "password": password},
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
