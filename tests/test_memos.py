from fastapi.testclient import TestClient
from starlette.status import HTTP_404_NOT_FOUND


class TestExistsAPI:
    def test_exist_api_root(
        self,
        client: TestClient
    ) -> None:
        res = client.get("/api")
        assert res.status_code == HTTP_404_NOT_FOUND


class TestGetMemo:
    def test_routes_exist(
        self,
        client: TestClient
    ) -> None:
        res = client.get("/api/memos")
        assert res.status_code != HTTP_404_NOT_FOUND
