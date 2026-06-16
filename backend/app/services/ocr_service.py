"""OCR 服务：支持多种后端，按优先级自动降级。

后端优先级（启动时探测，可用即采用）：
1. RapidOCR（ONNX 推理，中文友好，轻量）
2. PaddleOCR（CPU 推理，效果好但依赖重）
3. Mock（无 OCR 环境下的占位文本，仅用于联调）

输出格式：与微信聊天记录一致，便于 LLM 直接分析
   [HH:MM] 发送方: 内容
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from app.core.config import settings
from app.core.logger import logger


class OCRService:
    _engine_name: str = "none"
    _engine = None  # RapidOCR 或 PaddleOCR 实例
    _init_done: bool = False

    @classmethod
    def _try_init(cls):
        if cls._init_done:
            return
        cls._init_done = True

        if not settings.enable_ocr:
            cls._engine_name = "disabled"
            logger.info("OCR 已禁用（ENABLE_OCR=false）")
            return

        # 1) 优先 RapidOCR（轻量、中文 OK）
        try:
            from rapidocr_onnxruntime import RapidOCR  # type: ignore

            cls._engine = RapidOCR()
            cls._engine_name = "rapidocr"
            logger.info("OCR 引擎: RapidOCR")
            return
        except Exception as e:
            logger.warning(f"RapidOCR 初始化失败: {e}")

        # 2) 退回 PaddleOCR
        try:
            from paddleocr import PaddleOCR  # type: ignore

            cls._engine = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
            cls._engine_name = "paddleocr"
            logger.info("OCR 引擎: PaddleOCR")
            return
        except Exception as e:
            logger.warning(f"PaddleOCR 初始化失败: {e}")

        cls._engine_name = "mock"
        logger.warning("OCR 引擎: Mock（所有后端都不可用）")

    @classmethod
    def recognize(cls, image_paths: list[Path]) -> str:
        """识别多张图片，返回合并后的文本。"""
        cls._try_init()
        if cls._engine_name == "disabled":
            return cls._mock_output()
        if cls._engine_name == "mock" or cls._engine is None:
            return cls._mock_output()

        all_lines: list[str] = []
        for p in image_paths:
            try:
                lines = cls._recognize_one(p)
                if lines:
                    all_lines.extend(lines)
            except Exception as e:
                logger.error(f"识别 {p.name} 失败: {e}")

        if not all_lines:
            logger.warning("OCR 未识别到任何文字，返回 mock")
            return cls._mock_output()

        # 后处理：尝试把识别结果整理成 [时间] 发送方: 内容 的形式
        return cls._post_process(all_lines)

    @classmethod
    def _recognize_one(cls, image_path: Path) -> list[tuple[float, float, str]]:
        """识别单张图片，返回 [(y, x, text), ...]。"""
        if cls._engine_name == "rapidocr":
            return cls._rapidocr_one(image_path)
        if cls._engine_name == "paddleocr":
            return cls._paddleocr_one(image_path)
        return []

    @staticmethod
    def _rapidocr_one(image_path: Path) -> list[tuple[float, float, str]]:
        """RapidOCR 返回 (box, text, score) 列表。"""
        engine = OCRService._engine
        result, _elapsed = engine(str(image_path))
        if not result:
            return []
        lines: list[tuple[float, float, str]] = []
        for box, text, _score in result:
            if not text or not text.strip():
                continue
            # box 形如 [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]，取左上角 y 与中心 x
            y = min(pt[1] for pt in box)
            x = sum(pt[0] for pt in box) / 4
            lines.append((y, x, text.strip()))
        # 按 y 排序（从上到下）
        lines.sort(key=lambda t: (t[0], t[1]))
        return lines

    @staticmethod
    def _paddleocr_one(image_path: Path) -> list[tuple[float, float, str]]:
        """PaddleOCR 返回 [box, (text, score)] 列表。"""
        engine = OCRService._engine
        out = engine.ocr(str(image_path), cls=True)
        if not out or not out[0]:
            return []
        lines: list[tuple[float, float, str]] = []
        for item in out[0]:
            if isinstance(item, list) and len(item) == 2 and isinstance(item[1], tuple):
                box, (text, _score) = item
                if not text or not text.strip():
                    continue
                y = min(pt[1] for pt in box)
                x = sum(pt[0] for pt in box) / 4
                lines.append((y, x, text.strip()))
        lines.sort(key=lambda t: (t[0], t[1]))
        return lines

    @staticmethod
    def _post_process(lines: list[tuple[float, float, str]]) -> str:
        """把识别出的行整理成 [时间] 发送方: 内容 格式。

        微信截图的典型布局：
        - 左侧（x 较小）= 对方
        - 右侧（x 较大）= 我
        - 行内常见 "10:23 昵称  内容"
        - 同一发送方的连续行合并为一条
        """
        if not lines:
            return ""

        # 计算 x 中位数，作为左右分界
        xs = [x for _y, x, _t in lines]
        xs_sorted = sorted(xs)
        median_x = xs_sorted[len(xs_sorted) // 2]

        merged: list[tuple[str, str]] = []  # (sender, text)
        TIME_RE = re.compile(r"^(\d{1,2}:\d{2})(?:\s|$)")
        COLON_RE = re.compile(r"^(.{1,12}?)\s*[:：]\s*(.*)$")

        current_sender: Optional[str] = None
        current_text: list[str] = []
        first_time: Optional[str] = None

        def flush():
            nonlocal current_sender, current_text, first_time, merged
            if current_sender is not None and current_text:
                text = " ".join(current_text).strip()
                # 尝试从首段提取时间
                m = TIME_RE.match(text)
                ts = ""
                if m:
                    ts = f"[{m.group(1)}] "
                    text = text[m.end():].strip()
                # 尝试提取昵称 + 内容
                m2 = COLON_RE.match(text)
                if m2:
                    name = m2.group(1).strip()
                    body = m2.group(2).strip()
                    merged.append((ts, f"{name}: {body}"))
                else:
                    merged.append((ts, text))
            current_sender = None
            current_text = []
            first_time = None

        last_y = None
        for y, x, text in lines:
            sender = "对方" if x < median_x else "我"
            # 同 y 区间（±30）且同 sender 则合并
            if sender != current_sender or last_y is None or abs(y - last_y) > 40:
                flush()
                current_sender = sender
            else:
                # 同一发送方的相邻行
                pass
            current_text.append(text)
            last_y = y
        flush()

        if not merged:
            return "\n".join(t for _y, _x, t in lines)

        return "\n".join(f"{ts}{text}".rstrip() for ts, text in merged if text.strip())

    @staticmethod
    def _mock_output() -> str:
        """未启用 OCR 或识别失败时的占位文本，仅用于联调。"""
        return (
            "[10:23] 我: 在吗？\n"
            "[10:24] 她: 嗯嗯 怎么了\n"
            "[10:25] 我: 想约你看个电影\n"
            "[10:30] 她: 嗯…最近有点忙\n"
            "[10:31] 我: 好吧 那下次吧\n"
            "[10:35] 她: 嗯嗯"
        )

    @classmethod
    def engine_info(cls) -> dict:
        cls._try_init()
        return {"engine": cls._engine_name, "ocr_enabled": settings.enable_ocr}
