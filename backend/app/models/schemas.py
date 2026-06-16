"""数据模型 / Pydantic 契约"""
from typing import Literal, Optional
from pydantic import BaseModel, Field


# ===== Request =====
class AnalyzeTextRequest(BaseModel):
    raw_text: str = Field(..., min_length=1, max_length=20000, description="聊天记录原文")
    user_role: str = Field(default="我", description="用户身份标识")
    extra_context: str = Field(default="", description="额外背景信息")


# ===== Core Models =====
class Message(BaseModel):
    time: str
    sender: str
    content: str


class Relationship(BaseModel):
    label: Literal["同事", "老板", "客户", "女朋友", "男朋友", "家长", "朋友", "陌生人"]
    confidence: float = Field(..., ge=0, le=1)
    evidence: Optional[str] = None


class Emotion(BaseModel):
    label: Literal["开心", "生气", "敷衍", "礼貌", "好奇", "无聊", "难过"]
    score: float = Field(..., ge=0, le=1)


class Risk(BaseModel):
    type: Literal[
        "single_side_initiative",
        "short_reply",
        "dead_topic",
        "sensitive_word",
        "do_not_continue",
    ]
    level: Literal["low", "mid", "high"]
    evidence: Optional[str] = None


class Reply(BaseModel):
    style: Literal["high_eq", "humor", "formal", "flirty", "concise"]
    content: str
    reason: str
    expected_reply: list[str] = Field(default_factory=list)


class HealthReport(BaseModel):
    naturalness: int = Field(..., ge=0, le=100)
    engagement: int = Field(..., ge=0, le=100)
    silence_risk: int = Field(..., ge=0, le=100)
    reply_quality: int = Field(..., ge=0, le=100)


class AnalysisResult(BaseModel):
    analysis_id: str
    input_type: Literal["text", "image"]
    messages: list[Message] = Field(default_factory=list)
    relationship: Relationship
    stage: Literal["破冰", "热聊", "平稳", "冷场", "收尾"]
    emotion: Emotion
    risk: list[Risk] = Field(default_factory=list)
    replies: list[Reply] = Field(default_factory=list)
    health_report: HealthReport
    summary: str
    advice: list[str] = Field(default_factory=list)
    ocr_text: Optional[str] = None


# ===== Feedback =====
class FeedbackRequest(BaseModel):
    analysis_id: str
    reply_index: int
    useful: bool
    comment: Optional[str] = None
