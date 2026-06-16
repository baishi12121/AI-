"""测试 LLMService：JSON 兜底解析、Mock 模式。"""
import json
import pytest

from app.services.llm_service import LLMService, parse_json_safely


class TestParseJsonSafely:
    def test_direct_json(self):
        text = '{"a": 1, "b": "x"}'
        assert parse_json_safely(text) == {"a": 1, "b": "x"}

    def test_markdown_fenced(self):
        text = '```json\n{"a": 1}\n```'
        assert parse_json_safely(text) == {"a": 1}

    def test_json_in_surrounding_text(self):
        text = '好的，下面是结果：{"x": 2, "y": [1, 2]}，完毕。'
        assert parse_json_safely(text) == {"x": 2, "y": [1, 2]}

    def test_nested_json(self):
        text = '{"a": {"b": {"c": [1, 2, 3]}}}'
        assert parse_json_safely(text)["a"]["b"]["c"] == [1, 2, 3]

    def test_invalid_json_raises(self):
        with pytest.raises(ValueError):
            parse_json_safely("no json at all")

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            parse_json_safely("")


class TestLLMServiceMock:
    """QWEN 未配置时走 mock 路径。"""

    def test_chat_returns_valid_json(self):
        out = LLMService.chat("system", "user")
        parsed = json.loads(out)
        assert "messages" in parsed
        assert "replies" in parsed
        assert len(parsed["replies"]) == 5

    def test_chat_returns_chinese(self):
        out = LLMService.chat("system", "user")
        # mock 输出应包含中文
        assert any("\u4e00" <= ch <= "\u9fff" for ch in out)

    def test_analyze_chat_with_text(self):
        parsed = LLMService.analyze_chat(
            chat_text="[10:00] 我: 在吗\n[10:01] 她: 嗯",
            user_role="我",
            extra_context="",
        )
        # 必须字段全部存在
        assert "relationship" in parsed
        assert parsed["relationship"]["label"] in [
            "同事", "老板", "客户", "女朋友", "男朋友", "家长", "朋友", "陌生人"
        ]
        assert parsed["stage"] in ["破冰", "热聊", "平稳", "冷场", "收尾"]
        assert parsed["emotion"]["label"] in [
            "开心", "生气", "敷衍", "礼貌", "好奇", "无聊", "难过"
        ]
        assert isinstance(parsed["replies"], list)
        assert len(parsed["replies"]) == 5
        for r in parsed["replies"]:
            assert r["style"] in ["high_eq", "humor", "formal", "flirty", "concise"]
            assert "content" in r and len(r["content"]) > 0
            assert "reason" in r
            assert "expected_reply" in r

    def test_health_report_valid_range(self):
        parsed = LLMService.analyze_chat("[10:00] 我: hi", "我", "")
        hr = parsed["health_report"]
        for k in ["naturalness", "engagement", "silence_risk", "reply_quality"]:
            assert 0 <= hr[k] <= 100, f"{k} out of range: {hr[k]}"


class TestNewId:
    def test_new_id_is_unique(self):
        ids = {LLMService.new_id() for _ in range(100)}
        assert len(ids) == 100

    def test_new_id_is_hex(self):
        id_ = LLMService.new_id()
        assert len(id_) == 32
        assert all(c in "0123456789abcdef" for c in id_)
