# 启动后端服务的辅助脚本
import subprocess
import sys
import os

backend_dir = r"G:\AI聊天助手\backend"
python_exe = os.path.join(backend_dir, ".venv", "Scripts", "python.exe")
requirements = os.path.join(backend_dir, "requirements.txt")

os.chdir(backend_dir)

# 安装依赖
print("==> 安装依赖...")
subprocess.check_call([python_exe, "-m", "pip", "install", "-q", "-r", requirements])

# 启动 uvicorn
print("==> 启动服务...")
subprocess.check_call([python_exe, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
