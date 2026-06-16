"""测试 /api/analyze/text 接口。"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestAnalyzeTextAPI:
    def test_health(self):
        r = client.get("/api/healthz")
        assert r.status_code == 200
        body = r.json()
        assert body["code"] == 0
        assert body["data"]["status"] == "ok"

    def test_analyze_text_success(self, sample_text):
        r = client.post(
            "/api/analyze/text",
            json={"raw_text": sample_text, "user_role": "我", "extra_context": "测试"},
        )
        assert r.status_code == 200
        body = r.json()
        assert body["code"] == 0
        d = body["data"]
        assert d["input_type"] == "text"
        assert d["relationship"]["label"]
        assert len(d["replies"]) == 5
        styles = {rep["style"] for rep in d["replies"]}
        assert styles == {"high_eq", "humor", "formal", "flirty", "concise"}

    def test_analyze_text_empty_input(self):
        r = client.post("/api/analyze/text", json={"raw_text": "   ", "user_role": "我"})
        body = r.json()
        assert body["code"] != 0
        assert "不能为空" in body["msg"] or "raw_text" in body["msg"].lower()

    def test_analyze_text_missing_field(self):
        r = client.post("/api/analyze/text", json={})
        assert r.status_code == 422  # FastAPI 参数校验失败

    def test_analyze_text_over_long(self):
        r = client.post(
            "/api/analyze/text",
            json={"raw_text": "x" * 20001, "user_role": "我"},
        )
        assert r.status_code == 422

    def test_analyze_text_with_chinese(self):
        r = client.post(
            "/api/analyze/text",
            json={"raw_text": "我: 你好\n她: 你好", "user_role": "我"},
        )
        assert r.status_code == 200
        body = r.json()
        assert body["code"] == 0
