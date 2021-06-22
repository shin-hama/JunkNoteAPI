from fastapi import status
from fastapi.testclient import TestClient


class TestGetMemo:
    def test_routes_exist(
        self,
        client: TestClient
    ) -> None:
        res = client.get("/api/memos")
        assert res.status_code == status.HTTP_200_OK
