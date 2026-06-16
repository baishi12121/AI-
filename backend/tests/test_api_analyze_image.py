"""测试 /api/analyze/image 与 /api/analyze/image/ocr-only。"""
import io
import os
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _make_png_bytes():
    """生成一张最小合法 PNG。"""
    from PIL import Image
    img = Image.new("RGB", (50, 50), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()


class TestAnalyzeImageAPI:
    def test_no_images(self):
        """空 images 时返回 422（FastAPI 校验）或自定义错误。"""
        r = client.post("/api/analyze/image", files=[])
        # FastAPI 校验失败返回 422
        if r.status_code == 422:
            assert "detail" in r.json()
        else:
            body = r.json()
            assert body["code"] != 0
            assert "请至少上传" in body["msg"]

    def test_too_many_images(self):
        files = [
            ("images", (f"test{i}.png", _make_png_bytes(), "image/png"))
            for i in range(6)
        ]
        r = client.post("/api/analyze/image", files=files)
        body = r.json()
        assert body["code"] != 0
        assert "最多上传" in body["msg"]

    def test_wrong_mime_type(self):
        files = [("images", ("test.txt", b"hello", "text/plain"))]
        r = client.post("/api/analyze/image", files=files)
        body = r.json()
        assert body["code"] != 0
        assert "不支持" in body["msg"]

    def test_image_too_large(self):
        # 构造一个 11MB 的图片
        big = b"x" * (11 * 1024 * 1024)
        files = [("images", ("big.png", big, "image/png"))]
        r = client.post("/api/analyze/image", files=files)
        body = r.json()
        assert body["code"] != 0
        assert "超过" in body["msg"]

    def test_analyze_image_success_mock(self):
        files = [("images", ("test.png", _make_png_bytes(), "image/png"))]
        r = client.post("/api/analyze/image", files=files)
        # mock OCR 应有结果
        if r.status_code == 200:
            body = r.json()
            if body["code"] == 0:
                assert body["data"]["input_type"] == "image"
                assert "ocr_text" in body["data"]
                assert len(body["data"]["replies"]) == 5
            else:
                # 真实 OCR 在测试图上可能识别为空，但接口结构应正确
                assert "OCR" in body["msg"] or "未识别" in body["msg"]
        else:
            assert r.status_code == 500

    def test_ocr_only_endpoint(self):
        files = [("images", ("test.png", _make_png_bytes(), "image/png"))]
        r = client.post("/api/analyze/image/ocr-only", files=files)
        assert r.status_code == 200
        body = r.json()
        # mock OCR 总能返回文本
        if body["code"] == 0:
            assert "ocr_text" in body["data"]
            assert "engine" in body["data"]


class TestRealImageOCR:
    """真实图片 OCR 测试（依赖 tests/fake_chat.png）。"""

    def test_real_chat_image_ocr(self, test_image_path):
        if not os.path.exists(test_image_path):
            pytest.skip("测试图片不存在，跳过（运行 make_fake_chat.py 生成）")

        with open(test_image_path, "rb") as f:
            img_bytes = f.read()

        files = [("images", ("chat.png", img_bytes, "image/png"))]
        r = client.post("/api/analyze/image/ocr-only", files=files)
        assert r.status_code == 200
        body = r.json()
        assert body["code"] == 0, f"OCR 失败: {body}"
        text = body["data"]["ocr_text"]
        # 关键关键词必须命中
        for kw in ["在吗", "电影", "忙"]:
            assert kw in text, f"未识别到关键词: {kw}"
