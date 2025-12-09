#!/bin/sh
set -e

# 将 GitHub Action inputs 透传为环境变量，保持 agent.py 的可配置性
# 必填：OPENAI_API_KEY
if [ -z "$OPENAI_API_KEY" ]; then
  echo "Error: OPENAI_API_KEY is required." >&2
  exit 1
fi

# 可选：OPENAI_BASE_URL / MODEL_NAME / LOG_FILE / TARGET_DIR

echo "[entrypoint] Using MODEL=${MODEL_NAME:-gpt-4o}, LOG_FILE=${LOG_FILE:-sample_failure.log}, TARGET_DIR=${TARGET_DIR:-victim}"

exec python /app/agent.py

