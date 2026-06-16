"""FastAPI 入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import analyze, feedback, health
from app.core.config import settings
from app.core.logger import logger

app = FastAPI(
    title="AI 社恐聊天外挂 API",
    version="0.1.0",
    description="W1 端到端打通：文本/图片分析",
)

origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")
app.include_router(feedback.router, prefix="/api")


@app.on_event("startup")
def on_startup():
    logger.info("服务启动完成")
    logger.info(f"QWEN model = {settings.qwen_model}")
    logger.info(f"QWEN key configured = {bool(settings.qwen_api_key)}")
    logger.info(f"OCR enabled = {settings.enable_ocr}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=False)
