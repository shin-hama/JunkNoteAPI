from fastapi import status
from fastapi.testclient import TestClient


class TestExistsAPI:
    def test_exist_api_root(
        self,
        client: TestClient
    ) -> None:
        res = client.get("/api")
        assert res.status_code == status.HTTP_404_NOT_FOUND


class TestGetMemo:
    def test_routes_exist(
        self,
        client: TestClient
    ) -> None:
        res = client.get("/api/memos")
        assert res.status_code == status.HTTP_200_OK
