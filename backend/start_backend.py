"""Docker 容器内专用的启动脚本：只跑 uvicorn，不做 pip install"""
import os
import subprocess
import sys

# Railway 会注入 PORT 环境变量，本地默认 8000
host = os.environ.get("HOST", "0.0.0.0")
port = os.environ.get("PORT", "8000")

print(f"==> 启动服务 (http://{host}:{port})...", flush=True)

# 直接跑 uvicorn，不带 --reload（生产环境不需要）
subprocess.check_call([
    sys.executable, "-m", "uvicorn", "app.main:app",
    "--host", host, "--port", str(port),
])
