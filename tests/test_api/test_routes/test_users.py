from typing import Any

from fastapi import FastAPI, status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm.session import Session

from app.api.dependencies.authentication import get_current_user
from app.db.queries.users import create_user, delete_user_by_email
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
    db_session: Session,
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
    db_session: Session,
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

    # Delete updated data not to effect another test because unable to delete
    # when change email
    delete_user_by_email(db_session, email=user_profile["email"])


def test_user_can_change_password(
    app: FastAPI,
    authorized_client: TestClient,
) -> None:
    res = authorized_client.put(
        app.url_path_for("users:update-current-user"),
        json={"user": {"password": "new_password"}},
    )
    assert res.status_code == status.HTTP_200_OK
    user_profile = UserInResponse(**res.json())

    # Create new session to check update by another session of api
    from app.db.db import SessionLocal

    db = SessionLocal()
    user = get_current_user(db, user_profile.username)
    UserInDB(**user.__dict__)
    assert user.verify_password("new_password")
    db.close()


def test_user_can_not_take_already_used_credentials(
    app: FastAPI,
    authorized_client: TestClient,
    db_session: Session,
) -> None:
    """ Cannot Email is unique
    """
    unique_key = "email"
    user_dict = {
        "username": "new_user",
        "password": "password",
        unique_key: "new_user@email.com",
    }
    create_user(db_session, **user_dict)

    res = authorized_client.put(
        app.url_path_for("users:update-current-user"),
        json={"user": {unique_key: user_dict[unique_key]}},
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    # Delete updated data not to effect another test because unable to delete
    # when change email
    delete_user_by_email(db_session, email=user_dict["email"])
