"""测试 PromptBuilder：YAML 加载、模板渲染。"""
import pytest

from app.services.prompt_builder import PromptBuilder


class TestPromptBuilder:
    def setup_method(self):
        PromptBuilder._cache = {}  # 清缓存确保每次都重读

    def test_render_system_returns_non_empty(self):
        s = PromptBuilder.render_system("analyze")
        assert isinstance(s, str)
        assert len(s) > 50
        assert "社交心理学" in s or "教练" in s

    def test_render_user_with_chat_text(self):
        out = PromptBuilder.render_user(
            "analyze",
            chat_text="[10:00] 我: 在吗",
            user_role="我",
            extra_context_line="",
        )
        assert "[10:00] 我: 在吗" in out
        assert "我" in out

    def test_render_user_with_extra_context(self):
        out = PromptBuilder.render_user(
            "analyze",
            chat_text="...",
            user_role="A",
            extra_context_line="【额外背景】刚认识",
        )
        assert "刚认识" in out

    def test_render_user_empty_extra_context(self):
        out = PromptBuilder.render_user(
            "analyze",
            chat_text="x",
            user_role="我",
            extra_context_line="",
        )
        # 不应该残留 "【额外背景】" 字样
        assert "【额外背景】" not in out

    def test_render_user_handles_none(self):
        # 即便传入 None（被 safe_substitute 转成 "None"），也不应崩溃
        out = PromptBuilder.render_user(
            "analyze",
            chat_text="x",
            user_role=None,
            extra_context_line=None,
        )
        assert isinstance(out, str)
        assert len(out) > 0

    def test_cache_works(self):
        s1 = PromptBuilder.render_system("analyze")
        s2 = PromptBuilder.render_system("analyze")
        assert s1 == s2
        assert "analyze" in PromptBuilder._cache
