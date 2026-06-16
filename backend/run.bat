@echo off
REM 一键启动后端
cd /d %~dp0
if not exist .venv (
    echo [1/3] 创建虚拟环境...
    python -m venv .venv
)
call .venv\Scripts\activate
echo [2/3] 安装依赖...
pip install -q -r requirements.txt
if not exist .env (
    copy .env.example .env
    echo [!] 已生成 .env，请填入 QWEN_API_KEY 后重新启动
)
echo [3/3] 启动服务...
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
