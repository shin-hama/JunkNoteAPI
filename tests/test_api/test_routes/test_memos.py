from fastapi import status
from fastapi.applications import FastAPI
from fastapi.testclient import TestClient


def test_user_can_get_own_memos(
    app: FastAPI,
    authorized_client: TestClient
) -> None:
    res = authorized_client.get(app.url_path_for("memos:get-own-memos"))
    assert res.status_code == status.HTTP_200_OK


def test_unable_to_get_memos_by_unauthorized_user(
    app: FastAPI,
    client: TestClient,
) -> None:
    res = client.get(app.url_path_for("memos:get-own-memos"))
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
