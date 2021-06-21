from fastapi import FastAPI, status
from fastapi.testclient import TestClient
import pytest

from app.models.schemas.users import UserInDB


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
