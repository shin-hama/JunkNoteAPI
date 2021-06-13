import os
import subprocess
from typing import Any, AsyncIterator, Iterator
import uuid
import warnings

import alembic
from alembic.config import Config
from asgi_lifespan import LifespanManager
import docker as pydocker
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest


config = Config("alembic.ini")


@pytest.fixture(scope="session")
def docker() -> pydocker.APIClient:
    # base url is the unix socket we use to communicate with docker
    return pydocker.APIClient(
        base_url="unix://var/run/docker.sock", version="auto"
    )


@pytest.fixture(scope="session", autouse=True)
def mysql_container(docker: pydocker.APIClient) -> Iterator[Any]:
    """
    Use docker to spin up a mysql container for the duration of the testing
    session. Kill it as soon as all tests are run.
    DB actions persist across the entirety of the testing session.
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    image = "mysql:8.0"
    docker.pull(image)

    # create the new container using
    # the same image used by our database
    command = """head -1 /proc/self/cgroup|cut -d/ -f3"""
    bin_own_container_id = subprocess.check_output(['sh', '-c', command])
    own_container_id = bin_own_container_id.decode().replace('\n', '')
    inspection = docker.inspect_container(own_container_id)

    network = list(inspection["NetworkSettings"]["Networks"].keys())[0]
    networking_config = docker.create_networking_config({
        network: docker.create_endpoint_config()
    })

    container_name = f"test-mysql-{uuid.uuid4()}"
    container = docker.create_container(
        image=image,
        name=container_name,
        detach=True,
        networking_config=networking_config
    )
    docker.start(container=container["Id"])

    inspection = docker.inspect_container(container["Id"])
    ip = inspection['NetworkSettings']['Networks'][network]['IPAddress']
    dsn = f"mysql+pymysql://mysql:mysql@{ip}/mysql"

    try:
        os.environ['DATABASE_URL'] = dsn
        alembic.command.upgrade(config, "head")
        yield container
    finally:
        docker.kill(container["Id"])
        docker.remove_container(container["Id"])


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application
    return get_application()


@pytest.fixture
async def client(app: FastAPI) -> TestClient:
    return TestClient(app)
