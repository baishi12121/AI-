"""分析接口：/analyze/text 和 /analyze/image"""
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import settings
from app.core.logger import logger
from app.core.response import fail, ok
from app.models.schemas import AnalyzeTextRequest, AnalysisResult
from app.services import analyzer
from app.services.ocr_service import OCRService

router = APIRouter(prefix="/analyze", tags=["analyze"])

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads_tmp"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_MIME = {"image/png", "image/jpeg", "image/jpg", "image/webp"}
MAX_IMAGES = 5
MAX_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/text")
def analyze_text(req: AnalyzeTextRequest):
    if not req.raw_text.strip():
        return fail(1001, "raw_text 不能为空", 400)
    try:
        result: AnalysisResult = analyzer.analyze_text(req)
        return ok(result.model_dump(), request_id=uuid.uuid4().hex)
    except Exception as e:
        logger.exception("文本分析失败")
        return fail(2002, f"分析失败: {e}", 500)


@router.post("/image")
async def analyze_image(images: list[UploadFile] = File(...)):
    if not images:
        return fail(1001, "请至少上传 1 张图片", 400)
    if len(images) > MAX_IMAGES:
        return fail(1002, f"最多上传 {MAX_IMAGES} 张图片", 400)

    saved: list[Path] = []
    try:
        for f in images:
            if f.content_type not in ALLOWED_MIME:
                return fail(1002, f"不支持的图片类型: {f.content_type}", 400)
            content = await f.read()
            if len(content) > MAX_SIZE:
                return fail(1002, f"图片 {f.filename} 超过 10MB", 400)
            ext = ".png"
            if f.content_type == "image/jpeg" or f.content_type == "image/jpg":
                ext = ".jpg"
            elif f.content_type == "image/webp":
                ext = ".webp"
            save_path = UPLOAD_DIR / f"{uuid.uuid4().hex}{ext}"
            save_path.write_bytes(content)
            saved.append(save_path)

        # 1) OCR
        try:
            ocr_text = OCRService.recognize(saved)
        except Exception as e:
            logger.exception("OCR 失败")
            return fail(2001, f"OCR 失败: {e}", 500)

        if not ocr_text.strip():
            return fail(2001, "OCR 未识别到任何文字", 400)

        # 2) LLM 分析
        try:
            result: AnalysisResult = analyzer.analyze_images(saved, ocr_text)
            return ok(result.model_dump(), request_id=uuid.uuid4().hex)
        except Exception as e:
            logger.exception("图片分析失败")
            return fail(2002, f"分析失败: {e}", 500)
    finally:
        # 清理临时文件（即便异常也尝试删除）
        for p in saved:
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass


@router.post("/image/ocr-only")
async def ocr_only(images: list[UploadFile] = File(...)):
    """只做 OCR，不调用 LLM。用于调试 OCR 效果。"""
    if not images:
        return fail(1001, "请至少上传 1 张图片", 400)
    if len(images) > MAX_IMAGES:
        return fail(1002, f"最多上传 {MAX_IMAGES} 张图片", 400)

    saved: list[Path] = []
    try:
        for f in images:
            if f.content_type not in ALLOWED_MIME:
                return fail(1002, f"不支持的图片类型: {f.content_type}", 400)
            content = await f.read()
            if len(content) > MAX_SIZE:
                return fail(1002, f"图片 {f.filename} 超过 10MB", 400)
            ext = ".png"
            if f.content_type == "image/jpeg" or f.content_type == "image/jpg":
                ext = ".jpg"
            elif f.content_type == "image/webp":
                ext = ".webp"
            save_path = UPLOAD_DIR / f"{uuid.uuid4().hex}{ext}"
            save_path.write_bytes(content)
            saved.append(save_path)

        try:
            ocr_text = OCRService.recognize(saved)
        except Exception as e:
            logger.exception("OCR 失败")
            return fail(2001, f"OCR 失败: {e}", 500)

        return ok(
            {
                "engine": OCRService.engine_info(),
                "ocr_text": ocr_text,
                "image_count": len(saved),
            },
            request_id=uuid.uuid4().hex,
        )
    finally:
        for p in saved:
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass
