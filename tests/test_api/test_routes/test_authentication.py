from fastapi import status
from fastapi.testclient import TestClient

from app.models.models import User


def test_unable_to_register_same_email_user(
    client: TestClient, test_user: User
) -> None:
    res = client.post(
        "/api/users",
        json={"user": {
            "email": test_user.email,
            "password": "password2",
            "username": "test2",
        }},
    )

    assert res.status_code == status.HTTP_400_BAD_REQUEST
