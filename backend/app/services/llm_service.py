"""LLM 服务：封装 QWEN（OpenAI 兼容协议），含 JSON 兜底解析与 Mock 模式。"""
import json
import re
import uuid
from typing import Any, Optional

from app.core.config import settings
from app.core.logger import logger
from app.services.prompt_builder import PromptBuilder


def parse_json_safely(text: str) -> dict:
    """尝试从模型输出中提取 JSON 对象。"""
    text = text.strip()

    # 1) 直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2) 去除 markdown 围栏
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fenced:
        try:
            return json.loads(fenced.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 3) 提取首个 { ... } 块
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as e:
            logger.warning(f"JSON 提取失败: {e}")

    raise ValueError(f"无法解析模型输出为 JSON: {text[:200]}...")


class LLMService:
    _client = None

    @classmethod
    def _get_client(cls):
        if cls._client is not None:
            return cls._client
        if not settings.qwen_api_key:
            return None
        try:
            from openai import OpenAI

            cls._client = OpenAI(
                api_key=settings.qwen_api_key,
                base_url=settings.qwen_base_url,
                timeout=60.0,
            )
            return cls._client
        except Exception as e:
            logger.error(f"OpenAI 客户端初始化失败: {e}")
            return None

    @classmethod
    def chat(cls, system: str, user: str, temperature: float = 0.7, max_retries: int = 1) -> str:
        client = cls._get_client()
        if client is None:
            logger.warning("LLM 未配置（QWEN_API_KEY 为空），使用 mock 输出")
            return cls._mock_output()

        last_err: Optional[Exception] = None
        for attempt in range(max_retries + 1):
            try:
                resp = client.chat.completions.create(
                    model=settings.qwen_model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    temperature=temperature,
                    response_format={"type": "json_object"},
                )
                return resp.choices[0].message.content or ""
            except Exception as e:
                last_err = e
                logger.warning(f"LLM 调用失败 (第 {attempt + 1} 次): {e}")
        raise RuntimeError(f"LLM 调用失败: {last_err}")

    @staticmethod
    def _mock_output() -> str:
        """当未配置 API Key 时返回 mock 数据，便于本地联调。"""
        return json.dumps(
            {
                "messages": [
                    {"time": "10:23", "sender": "我", "content": "在吗？"},
                    {"time": "10:24", "sender": "她", "content": "嗯嗯 怎么了"},
                ],
                "relationship": {"label": "朋友", "confidence": 0.7, "evidence": "对话语气轻松"},
                "stage": "破冰",
                "emotion": {"label": "礼貌", "score": 0.65},
                "risk": [{"type": "single_side_initiative", "level": "low", "evidence": "我方先发起"}],
                "replies": [
                    {
                        "style": "high_eq",
                        "content": "刚看到一家挺有意思的店，想问问你的意见~",
                        "reason": "用'挺有意思'降低压力",
                        "expected_reply": ["愿意听", "追问细节"],
                    },
                    {
                        "style": "humor",
                        "content": "你今天回复速度破纪录了，给你颁个奖 🏆",
                        "reason": "轻松调侃活跃气氛",
                        "expected_reply": ["哈哈", "嫌弃式回复"],
                    },
                    {
                        "style": "formal",
                        "content": "你好，方便的话想和你聊几句。",
                        "reason": "正式但不生硬",
                        "expected_reply": ["好的", "什么事"],
                    },
                    {
                        "style": "flirty",
                        "content": "感觉你今天心情不错？是因为我吗 😏",
                        "reason": "轻微调侃",
                        "expected_reply": ["自恋", "害羞"],
                    },
                    {
                        "style": "concise",
                        "content": "在忙吗？",
                        "reason": "简洁明了",
                        "expected_reply": ["还好", "在"],
                    },
                ],
                "health_report": {
                    "naturalness": 75,
                    "engagement": 60,
                    "silence_risk": 40,
                    "reply_quality": 70,
                },
                "summary": "目前处于破冰阶段，对方态度礼貌中性。",
                "advice": ["可以多问开放式问题", "适当分享自己的状态"],
            },
            ensure_ascii=False,
        )

    @classmethod
    def analyze_chat(
        cls,
        chat_text: str,
        user_role: str = "我",
        extra_context: str = "",
    ) -> dict[str, Any]:
        system = PromptBuilder.render_system("analyze")
        extra_line = f"【额外背景】{extra_context}" if extra_context else ""
        user = PromptBuilder.render_user(
            "analyze",
            chat_text=chat_text,
            user_role=user_role,
            extra_context_line=extra_line,
        )
        raw = cls.chat(system, user)
        parsed = parse_json_safely(raw)
        return parsed

    @staticmethod
    def new_id() -> str:
        return uuid.uuid4().hex
