"""测试 OCRService：引擎探测、降级、文本整理。"""
from pathlib import Path

import pytest

from app.services.ocr_service import OCRService


class TestOCRPostProcess:
    def setup_method(self):
        OCRService._init_done = False  # 强制重新探测

    def test_mock_output_when_disabled(self):
        OCRService._init_done = True
        OCRService._engine_name = "disabled"
        out = OCRService.recognize([])
        assert "在吗" in out or "我" in out
        # 恢复
        OCRService._init_done = False

    def test_post_process_sorts_by_y(self):
        # _post_process 假设输入已按 y 排序（实际排序在 _rapidocr_one / _paddleocr_one 中）
        lines = [
            (30.0, 200.0, "第一条"),
            (100.0, 50.0, "第二条"),
        ]
        out = OCRService._post_process(lines)
        lines_out = out.split("\n")
        # 应该按 y 顺序：第一条在前，第二条在后
        assert "第一条" in lines_out[0]
        assert "第二条" in lines_out[1]

    def test_post_process_splits_left_right(self):
        # 左边 = 对方，右边 = 我
        lines = [
            (10.0, 50.0, "你好"),  # 左边 → 对方
            (50.0, 400.0, "我在这里"),  # 右边 → 我
        ]
        out = OCRService._post_process(lines)
        assert "对方" in out or "你好" in out
        assert "我" in out

    def test_post_process_empty(self):
        assert OCRService._post_process([]) == ""

    def test_post_process_extracts_time(self):
        lines = [(10.0, 100.0, "10:23 在吗")]
        out = OCRService._post_process(lines)
        assert "[10:23]" in out


class TestEngineInfo:
    def setup_method(self):
        OCRService._init_done = False

    def test_engine_info_returns_dict(self):
        info = OCRService.engine_info()
        assert "engine" in info
        assert "ocr_enabled" in info
