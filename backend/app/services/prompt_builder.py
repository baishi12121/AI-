"""Prompt 模板渲染器"""
import yaml
from pathlib import Path
from string import Template
from typing import Any

from app.core.logger import logger

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


class PromptBuilder:
    _cache: dict[str, dict[str, Any]] = {}

    @classmethod
    def _load(cls, name: str) -> dict[str, Any]:
        if name not in cls._cache:
            path = PROMPTS_DIR / f"{name}.yaml"
            with open(path, "r", encoding="utf-8") as f:
                cls._cache[name] = yaml.safe_load(f)
        return cls._cache[name]

    @classmethod
    def render_system(cls, name: str = "analyze") -> str:
        data = cls._load(name)
        return data.get("system", "").strip()

    @classmethod
    def render_user(cls, name: str, **kwargs: Any) -> str:
        """使用 string.Template 渲染 user 模板（$$ 转义为 $）。"""
        data = cls._load(name)
        tpl = data.get("user_template", "").strip()
        # string.Template 不支持 None，需要预处理
        safe_kwargs = {k: ("" if v is None else str(v)) for k, v in kwargs.items()}
        try:
            return Template(tpl).safe_substitute(safe_kwargs)
        except Exception as e:
            logger.error(f"Prompt 渲染失败: {e}")
            return tpl
