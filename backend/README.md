# AI 社恐聊天外挂 — Backend (FastAPI)

## W1 范围
- 文本分析 `/api/analyze/text`
- 图片分析 `/api/analyze/image`（OCR + LLM）
- 反馈 `/api/feedback`
- 健康检查 `/api/healthz`

## 快速启动

```bash
# 1. 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 .env
copy .env.example .env
# 编辑 .env，填入 QWEN_API_KEY

# 4. 启动
uvicorn app.main:app --reload --port 8000
```

或直接运行 `run.bat`。

## 端到端测试

```bash
curl -X POST http://localhost:8000/api/analyze/text \
  -H "Content-Type: application/json" \
  -d "{\"raw_text\":\"[10:00] 我: 在吗\n[10:01] 她: 嗯\"}"
```

Swagger 文档：http://localhost:8000/docs

## Mock 模式
未配置 `QWEN_API_KEY` 时，自动返回 mock 数据，便于本地联调。
未安装 PaddleOCR 时，OCR 自动降级为 mock 文本。
