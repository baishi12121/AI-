# 启动后端服务的辅助脚本
import subprocess
import sys
import os

# 尝试加载 backend/.env（PORT/HOST 等配置项）
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", ".env"))
except ImportError:
    pass

backend_dir = r"G:\AI聊天助手\backend"
python_exe = os.path.join(backend_dir, ".venv", "Scripts", "python.exe")
requirements = os.path.join(backend_dir, "requirements.txt")

os.chdir(backend_dir)

# 安装依赖
print("==> 安装依赖...")
subprocess.check_call([python_exe, "-m", "pip", "install", "-q", "-r", requirements])

# 端口从环境变量 PORT 读取，默认 8000
host = os.environ.get("HOST", "0.0.0.0")
port = os.environ.get("PORT", "8000")

# 启动 uvicorn
print(f"==> 启动服务 (http://{host}:{port})...")
subprocess.check_call([
    python_exe, "-m", "uvicorn", "app.main:app",
    "--host", host, "--port", str(port), "--reload",
])
