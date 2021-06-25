from typing import Iterator
from fastapi import status
from fastapi.applications import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm.session import Session

from app.db.queries import memos, users
from app.models import models
from app.models.schemas.memos import MemoInCreate


@pytest.fixture
def another_user(db_session: Session) -> Iterator[models.User]:
    another_user = users.create_user(
        db_session,
        "another",
        "another@email.com",
        "password"
    )
    try:
        yield another_user
    finally:
        users.delete_user(db_session, another_user)


@pytest.fixture
def another_memo(
    db_session: Session,
    another_user: models.User,
) -> Iterator[models.Memo]:
    another_memo = MemoInCreate()
    another_memo = memos.create_memo_for_user(
        db_session, memo=another_memo, user_id=another_user.id
    )

    try:
        yield another_memo
    finally:
        memos.delete_memo_by_id(db_session, another_memo.id)


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


def test_unable_update_memo_by_unauthorized_user(
    app: FastAPI,
    client: TestClient,
    test_memo: models.Memo
) -> None:
    res = client.put(
        app.url_path_for("memos:update", memo_id=test_memo.id),
        json={"memo": {"containts": "test"}},
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unable_update_memo_of_another_user(
    app: FastAPI,
    authorized_client: TestClient,
    another_memo: models.Memo,
) -> None:
    res = authorized_client.put(
        app.url_path_for("memos:update", memo_id=another_memo.id),
        json={"memo": {"containts": "test"}},
    )
    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_unable_update_memo_is_not_existed(
    app: FastAPI,
    authorized_client: TestClient,
    test_memo: models.Memo,
) -> None:
    res = authorized_client.put(
        app.url_path_for("memos:update", memo_id=test_memo.id + 1),
        json={"memo": {"containts": "test"}},
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "update_body",
    (
        {"containts": "with_reference"},
        {"reference": "test"},
        {"is_removed": "true"}
    )
)
def test_update_memo(
    app: FastAPI,
    authorized_client: TestClient,
    test_memo: models.Memo,
    update_body: dict[str, str],
) -> None:
    res = authorized_client.put(
        app.url_path_for("memos:update", memo_id=test_memo.id),
        json={"memo": update_body},
    )
    assert res.status_code == status.HTTP_200_OK


def test_unable_to_delete_memo_by_unauthorized_user(
    app: FastAPI,
    client: TestClient,
    test_memo: models.Memo
) -> None:
    res = client.delete(app.url_path_for("memos:delete", memo_id=test_memo.id))

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unable_delete_memo_of_another_user(
    app: FastAPI,
    authorized_client: TestClient,
    another_memo: models.Memo,
) -> None:
    res = authorized_client.delete(
        app.url_path_for("memos:delete", memo_id=another_memo.id)
    )

    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_unable_delete_memo_is_not_existed(
    app: FastAPI,
    authorized_client: TestClient,
    test_memo: models.Memo,
) -> None:
    res = authorized_client.delete(
        app.url_path_for("memos:delete", memo_id=test_memo.id + 1)
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND
