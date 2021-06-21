from typing import Any
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
import pytest

from app.api.dependencies.authentication import get_user_by_username
from app.db.queries.users import delete_user
from app.models.schemas.users import UserInDB, UserInResponse


@pytest.fixture(params=(
    "", "value", "Token value", "JWT value", "Bearer value"
))
def wrong_authorization_header(request: Any) -> str:
    return request.param


@pytest.mark.parametrize(
    "api_method, route_name",
    (("GET", "users:get-current-user"), ("PUT", "users:update-current-user")),
)
def test_user_can_not_access_own_profile_if_not_logged_in(
    app: FastAPI,
    client: TestClient,
    test_user: UserInDB,
    api_method: str,
    route_name: str,
) -> None:
    res = client.request(api_method, app.url_path_for(route_name))
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "api_method, route_name",
    (("GET", "users:get-current-user"), ("PUT", "users:update-current-user")),
)
def test_user_can_not_retrieve_own_profile_if_wrong_token(
    app: FastAPI,
    client: TestClient,
    test_user: UserInDB,
    api_method: str,
    route_name: str,
    wrong_authorization_header: str,
) -> None:
    res = client.request(
        api_method,
        app.url_path_for(route_name),
        headers={"Authorization": wrong_authorization_header},
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_can_retrieve_own_profile(
    app: FastAPI,
    authorized_client: TestClient,
    test_user: UserInDB,
    token: str,
    db_session: None,
) -> None:
    res = authorized_client.get(app.url_path_for("users:get-current-user"))
    assert res.status_code == status.HTTP_200_OK

    user_profile = UserInResponse(**res.json())
    assert user_profile.access_token == token


@pytest.mark.parametrize(
    "update_field, update_value",
    (
        ("username", "new_username"),
        ("email", "new_email@email.com"),
    ),
)
def test_user_can_update_own_profile(
    app: FastAPI,
    authorized_client: TestClient,
    db_session: None,
    update_value: str,
    update_field: str,
) -> None:
    res = authorized_client.put(
        app.url_path_for("users:update-current-user"),
        json={"user": {update_field: update_value}},
    )
    assert res.status_code == status.HTTP_200_OK

    user_profile = UserInResponse(**res.json()).dict()
    assert user_profile[update_field] == update_value
    user = get_user_by_username(
        db_session, username=user_profile["username"]
    )
    print(user)

    from datetime import datetime
    delete_user(db_session, UserInDB(
        username="",
        created_at=datetime.now(),
        email=user_profile["email"])
    )


def test_user_can_change_password(
    app: FastAPI,
    authorized_client: TestClient,
    db_session: None
) -> None:
    res = authorized_client.put(
        app.url_path_for("users:update-current-user"),
        json={"user": {"password": "new_password"}},
    )
    assert res.status_code == status.HTTP_200_OK
    user_profile = UserInResponse(**res.json())

    # TODO: Need to create new session to get updated value
    # create db_session on every query running
    # user = get_user_by_username(
    #     db_session, username=user_profile.username
    # )
    # assert user is not None
    # assert user.verify_password("new_password")
