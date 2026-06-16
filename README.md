# AI 社恐聊天外挂 · Conversation Coach

> **Not just replies for you — it teaches you how to reply.**
> 不止替你回，更教你如何回。

An AI-powered **conversation coach** that helps socially anxious, dating, and workplace-communication users understand intent, identify risk, and craft multi-style replies with built-in teaching value.

[![Status](https://img.shields.io/badge/status-W1%20ready-brightgreen)]() [![Python](https://img.shields.io/badge/Python-3.12-blue)]() [![Vue](https://img.shields.io/badge/Vue-3.5-42b883)]() [![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)]() [![License](https://img.shields.io/badge/license-MIT-green)]() [![Tests](https://img.shields.io/badge/tests-88%2F88%20passing-success)]()

[English](#-introduction) · [中文简介](#-中文简介) · [Quick Start](#-quick-start) · [PRD](./.trae/documents/PRD.md) · [架构](./.trae/documents/TECH.md)

---

## ✨ Introduction

**AI 社恐聊天外挂** (Conversation Coach) analyzes chat screenshots or pasted transcripts and produces:

- 🧠 **Relationship & stage detection** — coworker / friend / partner / family / stranger, with confidence
- 💬 **Emotion & risk radar** — short replies, dead topics, sensitive words, one-sided initiative
- 💎 **5-style reply suggestions** — High-EQ · Humor · Formal · Flirty · Concise — each with reason and expected counter-reply
- 📊 **Chat health report** — naturalness / engagement / silence risk / reply quality
- 📝 **One-line summary** + actionable advice
- 👍 / 👎 feedback loop for continuous improvement

The product **does not lie for you** — it teaches you *why* a reply works so you grow over time.

---

## 🀄 中文简介

帮社恐、恋爱/职场沟通困难的用户：

1. **读懂对方**：自动识别聊天记录的关系 / 阶段 / 情绪 / 风险
2. **学习怎么回**：5 种风格回复（高情商 / 幽默 / 正式 / 暧昧 / 简洁），每条都附带「为什么这么回」和「对方可能怎么接」
3. **复盘自己**：聊天体检报告 — 自然度 / 互动度 / 冷场风险 / 回复质量
4. **数据本地化**：历史记录存在浏览器 IndexedDB，最多 20 条

支持 **文本粘贴** 和 **图片上传**（OCR 自动识别），OCR 和 LLM 都做了 **mock 降级**，离线也能跑通流程。

---

## 📸 Screenshots

> 截图占位 · Screenshots placeholder

| Home | Result | History |
|---|---|---|
| ![home](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=modern%20minimal%20web%20app%20homepage%20for%20AI%20chat%20coach%2C%20clean%20form%20with%20text%20input%20and%20image%20upload%2C%20soft%20gradient%20background%2C%20light%20mode%2C%20modern%20UI%20design&image_size=portrait_4_3) | ![result](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=modern%20chat%20analysis%20result%20page%2C%20radar%20chart%2C%20tag%20pills%2C%205%20style%20reply%20cards%20with%20reasons%2C%20dark%20mode%20dashboard%20UI&image_size=portrait_4_3) | ![history](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=history%20list%20page%20of%20chat%20analysis%20app%2C%20list%20of%20past%20analyses%20with%20timestamps%2C%20card%20layout%2C%20clean%20minimal%20UI&image_size=portrait_4_3) |

> Replace with real screenshots after running locally:
> `frontend/src/views/{HomeView,ResultView,HistoryView}.vue`

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Browser (Vue 3)                          │
│   ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│   │ HomeView    │  │ ResultView   │  │ HistoryView      │    │
│   │ (upload/txt)│→ │ (analysis)   │  │ (IndexedDB)      │    │
│   └──────┬──────┘  └──────▲───────┘  └──────────────────┘    │
│          │  POST /api/analyze/{text,image}                   │
│          ▼                                                    │
│   Pinia Store + Axios + Tailwind + Lucide                    │
└──────────────────────────┬───────────────────────────────────┘
                           │ HTTP/JSON
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (8000)                     │
│   analyze.py  →  ocr_service.py  →  RapidOCR (ONNX)          │
│        │                  ↓                                  │
│        └──→  llm_service.py  →  QWEN (OpenAI-compat)         │
│                       ↓                                      │
│              prompt_builder.py (YAML + string.Template)      │
│                       ↓                                      │
│              analyzer.py (orchestration)                      │
└──────────────────────────────────────────────────────────────┘
```

**Design principles**

- ✅ **Graceful degradation** — no API key → mock JSON · no OCR engine → mock text · flow always runs
- ✅ **Stateless backend** — no DB / Redis; clients cache history in IndexedDB
- ✅ **Type-safe** — Pydantic v2 on backend, TypeScript strict on frontend
- ✅ **Test-driven** — 88 automated tests (49 backend + 39 frontend) all green

---

## 🛠️ Tech Stack

| Layer | Tech | Why |
|---|---|---|
| **Frontend** | Vue 3.5 + Vite 5 | Composition API, fast HMR |
| | TypeScript 5.6 | Strict typing |
| | Tailwind CSS 3 | Utility-first, tiny bundle |
| | Pinia 2 | Lightweight state |
| | Vue Router 4 | History mode |
| | Axios | Interceptors for response unwrapping |
| | idb-keyval | Promise-friendly IndexedDB |
| | lucide-vue-next | Tree-shakable icons |
| | Vitest 1.6 + happy-dom | Fast unit tests |
| **Backend** | FastAPI 0.115 | Async, OpenAPI auto-gen |
| | Pydantic v2 | Type-safe schemas |
| | Uvicorn | ASGI server |
| | loguru | Pretty logs |
| | PyYAML + string.Template | Prompt templating |
| | RapidOCR (ONNX) | Lightweight Chinese OCR |
| | openai SDK | QWEN OpenAI-compat client |
| | pytest 8.3 | Unit + API tests |

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.10+ (tested on 3.12)
- **Node.js** 18+ (tested on 20)
- **Git**

### 1. Clone

```bash
git clone https://github.com/<your-org>/ai-chat-coach.git
cd ai-chat-coach
```

### 2. Backend (port 8000)

```bash
cd backend

# Create venv
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install deps
pip install -r requirements.txt

# Configure (optional — leave empty to use mock LLM)
cp .env.example .env
# edit .env and set QWEN_API_KEY=sk-xxxxx

# Run
uvicorn app.main:app --reload --port 8000
```

API docs available at **http://127.0.0.1:8000/docs**

### 3. Frontend (port 5173)

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** 🎉

### 4. Quick helpers

```bash
# one-shot backend launcher
python start_backend.py

# one-shot frontend launcher
python start_frontend.py
```

---

## 📂 Project Structure

```
ai-chat-coach/
├── backend/                       # FastAPI
│   ├── app/
│   │   ├── api/v1/                # /analyze /feedback /healthz
│   │   ├── core/                  # config, logger, response helpers
│   │   ├── models/                # Pydantic schemas
│   │   ├── prompts/analyze.yaml   # LLM prompt template
│   │   └── services/              # ocr / llm / analyzer / prompt_builder
│   ├── tests/                     # pytest (49 tests)
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                      # Vue 3
│   ├── src/
│   │   ├── api/client.ts          # axios + types
│   │   ├── components/            # Tag, Uploader, ReplyCard, HealthRadar
│   │   ├── stores/history.ts      # Pinia + IndexedDB
│   │   ├── utils/format.ts        # labels, emojis, time
│   │   ├── views/                 # Home / Result / History
│   │   ├── router/                # / /result/:id /history
│   │   └── main.ts
│   ├── tests/                     # vitest (39 tests)
│   ├── vite.config.ts
│   └── package.json
│
├── tests/                         # E2E scripts + fake data
│   ├── TEST_CASES.md              # full test case catalog
│   ├── make_fake_chat.py          # generate sample screenshot
│   ├── test_image_ocr.py
│   └── test_image_upload_flow.py
│
├── e2e_test.py                    # full HTTP E2E (4 scenarios)
├── start_backend.py
├── start_frontend.py
├── PRD.md                         # product requirements
├── TECH.md                        # architecture doc
└── README.md                      # ← you are here
```

---

## 🧪 Testing

### Backend (49 tests, pytest)

```bash
cd backend
.\.venv\Scripts\python.exe -m pytest -q                # all
.\.venv\Scripts\python.exe -m pytest tests/test_api_*.py # API only
.\.venv\Scripts\python.exe -m pytest --cov=app         # coverage
```

### Frontend (39 tests, vitest)

```bash
cd frontend
npx vitest@1 run                # all
npx vitest@1 run --coverage     # coverage
npx vitest@1                    # watch mode
```

### E2E (4 tests, real HTTP)

```bash
# 1. start backend first
python start_backend.py

# 2. run E2E in another terminal
python e2e_test.py
python tests/test_image_upload_flow.py
```

### Coverage

| Layer | Count | Status |
|---|---|---|
| Backend unit | 31 | ✅ |
| Backend API | 18 | ✅ |
| Frontend unit | 39 | ✅ |
| E2E | 8 | ✅ |
| **Total** | **88** | **✅ 100%** |

Full case catalog → [tests/TEST_CASES.md](tests/TEST_CASES.md)

---

## 🔌 API Reference

### `POST /api/analyze/text`

Analyze a pasted chat transcript.

```jsonc
// Request
{
  "raw_text": "我: 在吗？\n她: 在的怎么了\n我: 想约你看电影\n她: 最近有点忙",
  "user_role": "我",
  "extra_context": "我们认识两个月了"
}

// Response (code: 0)
{
  "code": 0,
  "data": {
    "analysis_id": "uuid",
    "input_type": "text",
    "relationship": { "label": "女朋友", "confidence": 0.82 },
    "stage": "破冰",
    "emotion": { "label": "礼貌", "score": 0.65 },
    "risk": [{ "type": "short_reply", "level": "mid" }],
    "replies": [
      { "style": "high_eq", "content": "...", "reason": "...", "expected_reply": ["..."] }
      // 5 styles total
    ],
    "health_report": {
      "naturalness": 72,
      "engagement": 60,
      "silence_risk": 35,
      "reply_quality": 68
    },
    "summary": "对方礼貌但有距离，建议放慢节奏。",
    "advice": ["...", "..."]
  }
}
```

### `POST /api/analyze/image`

Upload 1–5 chat screenshots (multipart `images[]`).

### `POST /api/analyze/image/ocr-only`

Debug helper: return raw OCR text only.

### `POST /api/feedback`

```json
{ "analysis_id": "uuid", "reply_index": 0, "useful": true, "comment": "optional" }
```

### `GET /api/healthz`

Liveness probe.

Full OpenAPI spec → **http://127.0.0.1:8000/docs**

---

## ⚙️ Configuration

| Variable | Default | Description |
|---|---|---|
| `QWEN_API_KEY` | _(empty)_ | Aliyun DashScope key. Empty → use mock |
| `QWEN_BASE_URL` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | OpenAI-compat endpoint |
| `QWEN_MODEL` | `qwen-plus` | Model name |
| `ENABLE_OCR` | `true` | Toggle OCR engine |
| `HOST` / `PORT` | `0.0.0.0` / `8000` | Server bind |
| `LOG_LEVEL` | `INFO` | loguru level |
| `CORS_ORIGINS` | `http://localhost:5173,...` | Allowed origins |

---

## 🗺️ Roadmap

**W1 ✅ — Done**
- OCR + Prompt end-to-end
- Real RapidOCR integration
- Mock fallback for LLM & OCR
- 88 tests passing

**W2 — In progress**
- [ ] Real PaddleOCR (replace RapidOCR for higher accuracy)
- [ ] Streaming LLM output (SSE)
- [ ] WebSocket for live progress
- [ ] Mobile responsive polish
- [ ] 50-user beta feedback

**W3 — Planned**
- [ ] User accounts + cloud history sync
- [ ] Voice input (ASR)
- [ ] Multi-language support (English / Japanese)
- [ ] Tone customization (humor level, formality)
- [ ] Plugin system for custom analysis modules

See [PRD.md](.trae/documents/PRD.md) for the full plan.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/awesome-thing`
3. Write tests for new behavior
4. Ensure all tests pass: `pytest -q` + `npx vitest@1 run`
5. Submit a PR with a clear description

Please open an issue first for major changes.

---

## 📄 License

[MIT](./LICENSE) © 2026 AI Chat Coach Contributors

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) — excellent Python web framework
- [Vue.js](https://vuejs.org/) — the progressive framework
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) / [RapidOCR](https://github.com/RapidAI/RapidOCR) — Chinese OCR
- [Qwen](https://tongyi.aliyun.com/) — the LLM backbone
- [Tailwind CSS](https://tailwindcss.com/) — utility-first CSS
- [lucide](https://lucide.dev/) — beautiful open-source icons
- All open-source contributors ❤️

---

## ⭐ Star History

If this project helps you, a star is the best encouragement!

> Made with ❤️ for every socially awkward person out there.
