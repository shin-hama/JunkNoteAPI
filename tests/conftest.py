import time
from typing import Iterator

import docker
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from tests.util import is_database_ready
from app.core.config import (
    MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER
)


@pytest.fixture(scope="session")
def db_container() -> Iterator[None]:
    print("start to run container")

    test_client = docker.from_env()
    container = test_client.containers.run(
        image="mysql:8.0",
        tty=True,
        detach=True,
        auto_remove=True,
        environment={
            "MYSQL_ROOT_PASSWORD": "mysql",
            "MYSQL_DATABASE": MYSQL_DATABASE,
            "MYSQL_USER": MYSQL_USER,
            "MYSQL_PASSWORD": MYSQL_PASSWORD,
        },
        ports={MYSQL_PORT: MYSQL_PORT}
    )
    for i in range(30 * 10):
        if is_database_ready("localhost"):
            print("success to connect", i)
            break
        else:
            time.sleep(0.1)
    yield
    container.stop(timeout=0)


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application
    return get_application()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
