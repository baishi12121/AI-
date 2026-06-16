# 1. 使用官方稳定的 Python 3.10 镜像，绕过 Railway 底层的编译验证 Bug
FROM python:3.10-slim

# 2. 设置容器内的工作目录
WORKDIR /app

# 3. 将本地的所有代码复制到容器中
COPY . /app

# 4. 升级 pip 并安装依赖（使用清华源加速，避免超时）
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. 暴露出运行时端口（Railway 会动态注入 PORT 环境变量）
EXPOSE 8080

# 6. 启动命令（根据你的项目启动脚本调整）
CMD ["python", "start_backend.py"]
