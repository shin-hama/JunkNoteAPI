import time
from typing import Iterator

import alembic.config
import docker
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from tests.util import (
    is_database_ready, TEST_DB_URL, TEST_MYSQL_DATABASE, TEST_MYSQL_USER,
    TEST_MYSQL_PASSWORD, TEST_MYSQL_PORT
)


@pytest.fixture(scope="session")
def db_container() -> Iterator[None]:
    print("start to run container")
    try:
        test_client = docker.from_env()
        container = test_client.containers.run(
            image="mysql:8.0",
            tty=True,
            detach=True,
            auto_remove=True,
            environment={
                "MYSQL_ROOT_PASSWORD": "mysql",
                "MYSQL_DATABASE": TEST_MYSQL_DATABASE,
                "MYSQL_USER": TEST_MYSQL_USER,
                "MYSQL_PASSWORD": TEST_MYSQL_PASSWORD,
            },
            ports={TEST_MYSQL_PORT: TEST_MYSQL_PORT}
        )

        for i in range(30 * 10):
            if is_database_ready():
                print(f"success to connect {i/10} sec")
                break
            else:
                time.sleep(0.1)
        else:
            raise Exception("Fail to connect Database")

        # migrate to test database
        alembicArgs = [
            '--raiseerr',
            '-x', f"dbPath={TEST_DB_URL}",
            'upgrade', 'head',
        ]
        alembic.config.main(argv=alembicArgs)

        yield
    finally:
        container.stop(timeout=0)


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application
    return get_application()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
