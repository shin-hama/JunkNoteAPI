from fastapi.testclient import TestClient
from starlette.status import HTTP_404_NOT_FOUND


class TestHedgehogsRoutes:
    def test_routes_exist(
        self,
        db_container: None,
        client: TestClient
    ) -> None:
        res = client.get("/api")
        assert res.status_code != HTTP_404_NOT_FOUND
