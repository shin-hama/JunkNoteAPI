import time
from typing import Iterator

import alembic.config
import docker
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm.session import Session

# Import util at first before all of my packages
from tests.util import (
    is_database_ready, TEST_DB_URL, TEST_MYSQL_DATABASE, TEST_MYSQL_USER,
    TEST_MYSQL_PASSWORD, TEST_MYSQL_PORT
)

from app.db.queries import memos, users
from app.models import models
from app.models.schemas.memos import MemoInCreate


@pytest.fixture(scope="session")
def db_container() -> Iterator[None]:
    """ Launch new mysql container for test and upgrade latest migration.
    This container will keep running throughout the test and stop when
    it is finished.
    """
    test_client = docker.from_env()
    container = test_client.containers.run(
        image="mysql:8.0",
        tty=True,
        detach=True,
        auto_remove=True,
        environment={
            "MYSQL_ROOT_PASSWORD": "root",
            "MYSQL_DATABASE": TEST_MYSQL_DATABASE,
            "MYSQL_USER": TEST_MYSQL_USER,
            "MYSQL_PASSWORD": TEST_MYSQL_PASSWORD,
        },
        ports={TEST_MYSQL_PORT: TEST_MYSQL_PORT},
        # Need to define port with command to connect other than default port
        command=f"--port {TEST_MYSQL_PORT}",
    )

    try:
        # Repeat the connection test for 30 seconds.
        for i in range(30 * 10):
            if is_database_ready():
                break
            else:
                time.sleep(0.1)
        else:
            raise ConnectionError(f"Fail to connect Database: {TEST_DB_URL}")

        # migrate to test database
        alembicArgs = [
            '--raiseerr',
            '-x', f"dbPath={TEST_DB_URL}",
            'upgrade', 'head',
        ]
        alembic.config.main(argv=alembicArgs)

        yield
    except Exception as e:
        raise e
    finally:
        container.stop(timeout=0)


@pytest.fixture
def app(db_container: None) -> FastAPI:
    """ Get application.
    """
    # To import test.util first to set up the test environment, we will import
    # main function in the function.
    from app.main import get_application
    return get_application()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """ The test client
    """
    return TestClient(app)


@pytest.fixture
def db_session(db_container: None) -> Iterator[Session]:
    from app.db.db import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db_session: Session) -> Iterator[models.User]:
    """ Create a test user data on database, and delete it after running each
    test function.
    """
    test_user = users.create_user(
        db_session,
        username="test",
        email="test@email.com",
        password="password"
    )

    try:
        yield test_user
    finally:
        users.delete_user(db_session, test_user)


@pytest.fixture
def authorization_prefix() -> str:
    from app.core.config import TOKEN_PREFIX

    return TOKEN_PREFIX


@pytest.fixture
def token(test_user: models.User) -> str:
    from app.api.dependencies.authentication import create_access_token
    return create_access_token({"sub": test_user.email})


@pytest.fixture
def authorized_client(
    client: TestClient, token: str, authorization_prefix: str
) -> TestClient:
    client.headers = {
        "Authorization": f"{authorization_prefix} {token}",
        **client.headers,
    }
    return client


@pytest.fixture
def test_memo(
    db_session: Session,
    test_user: models.User,
) -> Iterator[models.Memo]:
    memo = MemoInCreate(containts="with_reference", reference="test")

    created_memo = memos.create_memo_for_user(
        db_session, memo=memo, user_id=test_user.id
    )

    try:
        yield created_memo
    finally:
        memos.delete_memo_by_id(db_session, created_memo.id)
