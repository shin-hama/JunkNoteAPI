from fastapi.testclient import TestClient
from starlette.status import HTTP_404_NOT_FOUND


class TestHedgehogsRoutes:
    def test_routes_exist(
        self,
        db_container,
        client: TestClient
    ) -> None:
        res = client.get("/")
        assert res.status_code != HTTP_404_NOT_FOUND
