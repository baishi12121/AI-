"""pytest 共享 fixtures"""
import os
import sys
import io
import pytest

# 把 backend 根目录加入 import path
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BACKEND_ROOT)

# 测试时强制 mock 模式
os.environ.setdefault("QWEN_API_KEY", "")
os.environ.setdefault("ENABLE_OCR", "false")


@pytest.fixture
def sample_text() -> str:
    return (
        "[2026-06-15 10:23] 我: 在吗？周末有空吗\n"
        "[2026-06-15 10:25] 她: 在 怎么了\n"
        "[2026-06-15 10:26] 我: 想约你看个电影\n"
        "[2026-06-15 10:30] 她: 嗯…最近有点忙\n"
        "[2026-06-15 10:31] 我: 好吧 那下次吧\n"
        "[2026-06-15 10:35] 她: 嗯嗯"
    )


@pytest.fixture
def sample_png_bytes() -> bytes:
    """生成一张最小的合法 PNG（1x1 白点）。"""
    try:
        from PIL import Image

        img = Image.new("RGB", (10, 10), color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except ImportError:
        # 最小合法 PNG（67 字节，1x1 透明）
        return bytes.fromhex(
            "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4"
            "890000000a49444154789c63000100000005000100" + "0d0a2db4"
            "0000000049454e44ae426082"
        )


@pytest.fixture
def test_image_path() -> str:
    """真实测试图片路径（须先运行 make_fake_chat.py）。"""
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "tests",
        "fake_chat.png",
    )
    return path
