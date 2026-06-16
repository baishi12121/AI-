"""测试 analyzer 业务编排：归一化、字段裁剪。"""
import pytest

from app.services.analyzer import analyze_text, _clamp, _normalize_parsed
from app.models.schemas import AnalyzeTextRequest


class TestClamp:
    @pytest.mark.parametrize(
        "v,lo,hi,expected",
        [
            (50, 0, 100, 50),
            (-5, 0, 100, 0),
            (150, 0, 100, 100),
            (101, 0, 100, 100),
        ],
    )
    def test_clamp(self, v, lo, hi, expected):
        assert _clamp(v, lo, hi) == expected


class TestNormalizeParsed:
    def test_normalize_minimal(self):
        raw = {
            "relationship": {"label": "朋友", "confidence": 0.8},
            "stage": "破冰",
            "emotion": {"label": "礼貌", "score": 0.5},
        }
        out = _normalize_parsed(raw, input_type="text", ocr_text=None)
        assert out["input_type"] == "text"
        assert out["relationship"]["label"] == "朋友"
        assert out["stage"] == "破冰"
        assert out["ocr_text"] is None
        # health_report 4 项必须存在
        assert set(out["health_report"].keys()) == {
            "naturalness", "engagement", "silence_risk", "reply_quality"
        }
        # health_report 必须在 0~100
        for v in out["health_report"].values():
            assert 0 <= v <= 100

    def test_normalize_clamps_out_of_range(self):
        raw = {
            "health_report": {
                "naturalness": 200,  # 越界
                "engagement": -10,
                "silence_risk": 50,
                "reply_quality": 99.9,
            }
        }
        out = _normalize_parsed(raw, input_type="text", ocr_text=None)
        assert out["health_report"]["naturalness"] == 100
        assert out["health_report"]["engagement"] == 0
        assert out["health_report"]["silence_risk"] == 50
        assert out["health_report"]["reply_quality"] == 99

    def test_normalize_filters_empty_messages(self):
        raw = {"messages": [{"time": "10:00", "sender": "我", "content": "hi"},
                            {"time": "10:01", "sender": "?", "content": ""}]}
        out = _normalize_parsed(raw, input_type="text", ocr_text=None)
        assert len(out["messages"]) == 1
        assert out["messages"][0]["content"] == "hi"

    def test_normalize_generates_analysis_id(self):
        raw = {}
        out = _normalize_parsed(raw, input_type="text", ocr_text=None)
        assert "analysis_id" in out
        assert len(out["analysis_id"]) == 32  # uuid4 hex


class TestAnalyzeText:
    def test_analyze_text_returns_valid_model(self, sample_text):
        req = AnalyzeTextRequest(
            raw_text=sample_text,
            user_role="我",
            extra_context="刚认识的女生",
        )
        result = analyze_text(req)
        # 必须字段
        assert result.analysis_id
        assert result.input_type == "text"
        assert len(result.messages) >= 1
        assert result.relationship.label in [
            "同事", "老板", "客户", "女朋友", "男朋友", "家长", "朋友", "陌生人"
        ]
        assert len(result.replies) == 5
        assert result.summary
