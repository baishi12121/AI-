"""业务编排：串联 OCR / LLM / 数据组装。"""
import uuid
from typing import Literal

from app.core.logger import logger
from app.models.schemas import (
    AnalysisResult,
    AnalyzeTextRequest,
    Emotion,
    HealthReport,
    Relationship,
    Reply,
    Risk,
)
from app.services.llm_service import LLMService
from app.services.ocr_service import OCRService


def _clamp(v: int, lo: int = 0, hi: int = 100) -> int:
    return max(lo, min(hi, v))


def _normalize_parsed(parsed: dict, input_type: Literal["text", "image"], ocr_text: str | None) -> dict:
    """把 LLM 返回的不规则 dict 归一化到 AnalysisResult 可解析的形状。"""
    # messages：优先使用 LLM 的归一化输出
    msgs = parsed.get("messages") or []
    normalized_msgs = [
        {
            "time": str(m.get("time", "")),
            "sender": str(m.get("sender", "未知")),
            "content": str(m.get("content", "")),
        }
        for m in msgs
        if m.get("content")
    ]

    rel = parsed.get("relationship") or {}
    emo = parsed.get("emotion") or {}
    risk_list = parsed.get("risk") or []
    replies = parsed.get("replies") or []
    hr = parsed.get("health_report") or {}

    return {
        "messages": normalized_msgs,
        "relationship": {
            "label": rel.get("label", "陌生人"),
            "confidence": float(rel.get("confidence", 0.5)),
            "evidence": rel.get("evidence"),
        },
        "stage": parsed.get("stage", "破冰"),
        "emotion": {
            "label": emo.get("label", "礼貌"),
            "score": float(emo.get("score", 0.5)),
        },
        "risk": [
            {
                "type": r.get("type", "single_side_initiative"),
                "level": r.get("level", "low"),
                "evidence": r.get("evidence"),
            }
            for r in risk_list
        ],
        "replies": [
            {
                "style": rep.get("style", "concise"),
                "content": rep.get("content", ""),
                "reason": rep.get("reason", ""),
                "expected_reply": rep.get("expected_reply") or [],
            }
            for rep in replies
        ],
        "health_report": {
            "naturalness": _clamp(int(hr.get("naturalness", 70))),
            "engagement": _clamp(int(hr.get("engagement", 60))),
            "silence_risk": _clamp(int(hr.get("silence_risk", 40))),
            "reply_quality": _clamp(int(hr.get("reply_quality", 65))),
        },
        "summary": parsed.get("summary", ""),
        "advice": parsed.get("advice") or [],
        "analysis_id": LLMService.new_id(),
        "input_type": input_type,
        "ocr_text": ocr_text,
    }


def analyze_text(req: AnalyzeTextRequest) -> AnalysisResult:
    parsed = LLMService.analyze_chat(
        chat_text=req.raw_text,
        user_role=req.user_role or "我",
        extra_context=req.extra_context or "",
    )
    data = _normalize_parsed(parsed, input_type="text", ocr_text=None)
    return AnalysisResult(**data)


def analyze_images(image_paths: list, ocr_text: str) -> AnalysisResult:
    parsed = LLMService.analyze_chat(
        chat_text=ocr_text,
        user_role="我",
        extra_context="（以上内容由 OCR 识别）",
    )
    data = _normalize_parsed(parsed, input_type="image", ocr_text=ocr_text)
    return AnalysisResult(**data)
