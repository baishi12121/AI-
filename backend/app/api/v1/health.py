"""健康检查"""
from fastapi import APIRouter

from app.core.config import settings
from app.core.response import ok

router = APIRouter(tags=["health"])


@router.get("/healthz")
def healthz():
    return ok(
        {
            "status": "ok",
            "model": settings.qwen_model,
            "ocr_enabled": settings.enable_ocr,
        }
    )
