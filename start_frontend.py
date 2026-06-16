import subprocess
import os
import shutil
import sys

frontend_dir = r"G:\AI聊天助手\frontend"

# 找到 npm
npm = shutil.which("npm")
if not npm:
    # 尝试常见路径
    candidates = [
        os.path.expandvars(r"%ProgramFiles%\nodejs\npm.cmd"),
        os.path.expandvars(r"%ProgramFiles(x86)%\nodejs\npm.cmd"),
        r"C:\Program Files\nodejs\npm.cmd",
        r"C:\Program Files (x86)\nodejs\npm.cmd",
    ]
    for c in candidates:
        if os.path.exists(c):
            npm = c
            break
if not npm:
    print("ERROR: 找不到 npm，请先安装 Node.js")
    sys.exit(1)

# 安装依赖
node_modules = os.path.join(frontend_dir, "node_modules")
if not os.path.exists(node_modules):
    print("==> 安装前端依赖...")
    subprocess.check_call([npm, "install"], cwd=frontend_dir)

# 启动 vite
print(f"==> 启动前端 (npm={npm})...")
subprocess.check_call([npm, "run", "dev"], cwd=frontend_dir)
