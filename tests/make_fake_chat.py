"""生成一张模拟微信聊天截图，用于测试 OCR。"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT_PATH = r"G:\AI聊天助手\tests\fake_chat.png"

# 消息内容（贴近真实微信布局）
# 格式: (side, name, text)   side: "left"=对方, "right"=我
MESSAGES = [
    ("right", "我",   "在吗？"),
    ("left",  "小美", "在的 怎么了"),
    ("right", "我",   "想约你看个电影"),
    ("left",  "小美", "嗯…最近有点忙"),
    ("right", "我",   "好吧 那下次吧"),
    ("left",  "小美", "嗯嗯"),
]

# 颜色
BG = (245, 245, 245)
BUBBLE_LEFT = (255, 255, 255)
BUBBLE_RIGHT = (149, 236, 105)
NAME_COLOR = (130, 130, 130)
TEXT_COLOR = (30, 30, 30)

# 字体（尝试中文字体）
def get_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyh.ttf",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simfang.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()

# 画布
W, H = 480, 720
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# 顶部状态栏模拟
draw.rectangle([0, 0, W, 40], fill=(235, 235, 235))
title_font = get_font(16)
draw.text((W // 2 - 30, 12), "小美", fill=TEXT_COLOR, font=title_font)

font = get_font(18)
name_font = get_font(13)

y = 70
PAD = 12
MAX_W = 280

for side, name, text in MESSAGES:
    # 自动换行
    lines = []
    line = ""
    for ch in text:
        test = line + ch
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > MAX_W - 2 * PAD:
            lines.append(line)
            line = ch
        else:
            line = test
    if line:
        lines.append(line)

    # 气泡高度
    h = (len(lines) * 26) + 2 * PAD + 4
    # 计算气泡宽度
    w = 0
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=font)
        w = max(w, bbox[2] - bbox[0])
    w = min(w + 2 * PAD, MAX_W)

    if side == "right":
        bx = W - w - 20
        color = BUBBLE_RIGHT
    else:
        bx = 20
        color = BUBBLE_LEFT

    # 圆角矩形（用 PIL 的 rounded_rectangle）
    radius = 10
    try:
        draw.rounded_rectangle([bx, y, bx + w, y + h], radius=radius, fill=color)
    except AttributeError:
        draw.rectangle([bx, y, bx + w, y + h], fill=color)

    # 昵称（小字）
    if side == "left":
        draw.text((bx, y - 18), name, fill=NAME_COLOR, font=name_font)
    else:
        nb = draw.textbbox((0, 0), name, font=name_font)
        nw = nb[2] - nb[0]
        draw.text((bx + w - nw, y - 18), name, fill=NAME_COLOR, font=name_font)

    # 文本
    ty = y + PAD // 2
    for ln in lines:
        draw.text((bx + PAD, ty), ln, fill=TEXT_COLOR, font=font)
        ty += 26

    y += h + 32

# 保存
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
img.save(OUT_PATH)
print(f"saved: {OUT_PATH}  size: {os.path.getsize(OUT_PATH)} bytes  {W}x{H}")
