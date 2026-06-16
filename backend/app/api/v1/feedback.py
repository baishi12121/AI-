"""反馈接口：仅记录日志，不持久化。"""
from fastapi import APIRouter

from app.core.logger import logger
from app.core.response import ok
from app.models.schemas import FeedbackRequest

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("")
def submit_feedback(req: FeedbackRequest):
    logger.info(f"feedback received: id={req.analysis_id} idx={req.reply_index} useful={req.useful}")
    return ok({"ok": True})
