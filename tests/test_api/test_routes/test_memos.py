from fastapi import status
from fastapi.applications import FastAPI
from fastapi.testclient import TestClient
import pytest


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


def test_unable_to_create_memo_by_unauthorized_user(
    app: FastAPI,
    client: TestClient,
) -> None:
    res = client.post(
        app.url_path_for("memos:create-own-memo"),
        json={"memo": {"containts": "test", "reference": "test"}},
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "json_body",
    (
        {"containts": "no_reference"},
        {"containts": "with_reference", "reference": "test"},
    ),
)
def test_create_memo(
    app: FastAPI,
    authorized_client: TestClient,
    json_body: dict[str, str]
) -> None:
    res = authorized_client.post(
        app.url_path_for("memos:create-own-memo"),
        json={"memo": json_body},
    )
    assert res.status_code == status.HTTP_200_OK

    authorized_client.delete(
        app.url_path_for("memos:delete", memo_id=res.json()["id"])
    )
