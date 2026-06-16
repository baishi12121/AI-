"""测试图片 OCR 接口（真实识别，不依赖 mock）"""
import urllib.request
import urllib.error
import json
import os

def ocr_only_test(image_path: str):
    print("=" * 60)
    print(f"OCR 测试: {image_path}")
    print("=" * 60)

    with open(image_path, "rb") as f:
        img_bytes = f.read()

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="images"; filename="chat.png"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode() + img_bytes + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        "http://localhost:8000/api/analyze/image/ocr-only",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read().decode("utf-8"))

    print(f"  code     = {result['code']}")
    if result["code"] != 0:
        print(f"  msg      = {result['msg']}")
        return
    d = result["data"]
    print(f"  engine   = {d['engine']}")
    print(f"  images   = {d['image_count']}")
    print(f"  ocr_text =")
    for line in d["ocr_text"].split("\n"):
        print(f"    | {line}")


def analyze_image_test(image_path: str):
    print("\n" + "=" * 60)
    print(f"图片分析测试: {image_path}")
    print("=" * 60)

    with open(image_path, "rb") as f:
        img_bytes = f.read()

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="images"; filename="chat.png"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode() + img_bytes + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        "http://localhost:8000/api/analyze/image",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read().decode("utf-8"))

    print(f"  code = {result['code']}")
    if result["code"] != 0:
        print(f"  msg  = {result['msg']}")
        return
    d = result["data"]
    print(f"  relationship = {d['relationship']['label']} ({d['relationship']['confidence']:.0%})")
    print(f"  stage        = {d['stage']}")
    print(f"  emotion      = {d['emotion']['label']} ({d['emotion']['score']:.0%})")
    print(f"  risk count   = {len(d['risk'])}")
    print(f"  replies      = {len(d['replies'])} styles")
    print(f"  summary      = {d['summary']}")
    print(f"  ocr_text     = {d.get('ocr_text', '')[:80]}...")


if __name__ == "__main__":
    img = r"G:\AI聊天助手\tests\fake_chat.png"
    if not os.path.exists(img):
        print(f"测试图片不存在: {img}")
        print("请先运行 python tests/make_fake_chat.py")
    else:
        ocr_only_test(img)
        analyze_image_test(img)
        print("\n图片接口测试通过！")
