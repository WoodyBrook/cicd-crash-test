FROM python:3.12-slim

WORKDIR /app

# 复制全部代码（包含 agent.py 与受害者目录），方便直接运行
COPY . /app

# 安装依赖（仅 agent 运行需要）
RUN pip install --no-cache-dir openai python-dotenv

# 入口
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

