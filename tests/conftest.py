import time
from typing import Iterator

import alembic.config
import docker
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import sessionmaker

# Import util at first before all of my packages
from tests.util import (
    is_database_ready, TEST_DB_URL, TEST_MYSQL_DATABASE, TEST_MYSQL_USER,
    TEST_MYSQL_PASSWORD, TEST_MYSQL_PORT
)

from app.db.queries.users import create_user
from app.models.schemas.users import UserInDB


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
        ports={TEST_MYSQL_PORT: TEST_MYSQL_PORT}
    )

    try:
        # Repeat the connection test for 30 seconds.
        for i in range(30 * 10):
            if is_database_ready():
                print(f"success to connect {i/10} sec")
                break
            else:
                time.sleep(0.1)
        else:
            raise ConnectionError("Fail to connect Database")

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
def db_session() -> Iterator[sessionmaker]:
    from app.db.db import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db_session: sessionmaker) -> UserInDB:
    test_user = create_user(
        db_session,
        username="test",
        email="test@example.com",
        password="password"
    )

    return test_user
