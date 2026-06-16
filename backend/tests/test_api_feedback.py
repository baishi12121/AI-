"""测试 /api/feedback 接口。"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestFeedbackAPI:
    def test_feedback_success(self):
        r = client.post(
            "/api/feedback",
            json={
                "analysis_id": "abc123",
                "reply_index": 0,
                "useful": True,
                "comment": "不错",
            },
        )
        assert r.status_code == 200
        body = r.json()
        assert body["code"] == 0
        assert body["data"]["ok"] is True

    def test_feedback_negative(self):
        r = client.post(
            "/api/feedback",
            json={"analysis_id": "abc", "reply_index": 1, "useful": False},
        )
        assert r.status_code == 200
        assert r.json()["code"] == 0

    def test_feedback_missing_field(self):
        r = client.post("/api/feedback", json={"analysis_id": "abc"})
        assert r.status_code == 422
