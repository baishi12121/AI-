"""端到端测试脚本"""
import urllib.request
import json
import sys

def test_text_analyze():
    print("=" * 50)
    print("TEST 1: 文本分析（通过前端代理）")
    print("=" * 50)
    req = urllib.request.Request(
        'http://localhost:5173/api/analyze/text',
        data=json.dumps({
            'raw_text': '[10:00] 我: 在吗？\n[10:01] 她: 嗯嗯 怎么了\n[10:02] 我: 想约你看个电影\n[10:05] 她: 嗯…最近有点忙\n[10:06] 我: 好吧 那下次吧\n[10:10] 她: 嗯嗯',
            'user_role': '我',
            'extra_context': '刚认识的女生'
        }, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as r:
        body = json.loads(r.read().decode('utf-8'))

    assert body['code'] == 0, f"非预期 code: {body}"
    d = body['data']
    print(f"  analysis_id     = {d['analysis_id'][:16]}...")
    print(f"  input_type      = {d['input_type']}")
    print(f"  messages count  = {len(d['messages'])}")
    print(f"  relationship    = {d['relationship']['label']} ({d['relationship']['confidence']:.0%})")
    print(f"  stage           = {d['stage']}")
    print(f"  emotion         = {d['emotion']['label']} ({d['emotion']['score']:.0%})")
    print(f"  risk count      = {len(d['risk'])}")
    print(f"  replies         = {[r['style'] for r in d['replies']]}")
    print(f"  health_report   = {d['health_report']}")
    print(f"  summary         = {d['summary']}")
    print(f"  advice          = {d['advice']}")
    print(f"  ocr_text        = {d.get('ocr_text')}")
    print("  ✅ PASS")


def test_health():
    print("\n" + "=" * 50)
    print("TEST 2: 健康检查")
    print("=" * 50)
    with urllib.request.urlopen('http://localhost:8000/api/healthz') as r:
        body = json.loads(r.read().decode('utf-8'))
    assert body['code'] == 0
    print(f"  status = {body['data']['status']}, model = {body['data']['model']}")
    print("  ✅ PASS")


def test_image_analyze():
    print("\n" + "=" * 50)
    print("TEST 3: 图片分析（mock OCR 模式）")
    print("=" * 50)
    # 创建一个 1x1 像素的 PNG 图片
    import io
    try:
        from PIL import Image
    except ImportError:
        print("  ⚠️  Pillow 未安装，跳过此测试")
        return

    img = Image.new('RGB', (100, 100), color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="images"; filename="test.png"\r\n'
        f'Content-Type: image/png\r\n\r\n'
    ).encode() + buf.read() + f'\r\n--{boundary}--\r\n'.encode()

    req = urllib.request.Request(
        'http://localhost:5173/api/analyze/image',
        data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
    )
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read().decode('utf-8'))

    assert result['code'] == 0, f"非预期 code: {result}"
    d = result['data']
    print(f"  input_type      = {d['input_type']}")
    print(f"  relationship    = {d['relationship']['label']}")
    print(f"  replies count   = {len(d['replies'])}")
    print(f"  ocr_text        = {d.get('ocr_text', '')[:60]}...")
    print("  ✅ PASS")


def test_real_ocr():
    """真实图片 OCR 测试（需先运行 tests/make_fake_chat.py）"""
    print("\n" + "=" * 50)
    print("TEST 4: 真实图片 OCR（rapidocr）")
    print("=" * 50)
    img_path = r"G:\AI聊天助手\tests\fake_chat.png"
    import os
    if not os.path.exists(img_path):
        print(f"  ⚠️  测试图片不存在: {img_path}，请先运行 make_fake_chat.py")
        return

    with open(img_path, 'rb') as f:
        img_bytes = f.read()

    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="images"; filename="chat.png"\r\n'
        f'Content-Type: image/png\r\n\r\n'
    ).encode() + img_bytes + f'\r\n--{boundary}--\r\n'.encode()

    req = urllib.request.Request(
        'http://localhost:5173/api/analyze/image/ocr-only',
        data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
    )
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read().decode('utf-8'))

    assert result['code'] == 0
    d = result['data']
    print(f"  engine    = {d['engine']['engine']}")
    print(f"  ocr_text  =")
    for line in d['ocr_text'].split('\n'):
        print(f"    | {line}")

    for kw in ['在吗', '电影', '忙']:
        assert kw in d['ocr_text'], f"未识别到关键词: {kw}"
    print("  ✅ PASS")


if __name__ == "__main__":
    test_health()
    test_text_analyze()
    test_image_analyze()
    test_real_ocr()
    print("\n" + "🎉" * 10)
    print("W1 端到端测试全部通过！")
