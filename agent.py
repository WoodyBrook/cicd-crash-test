#!/usr/bin/env python3
"""
Phase 1 本地 MVP：读取错误日志 -> 调用 LLM -> 通过工具函数仅修改配置文件

使用方法：
  export OPENAI_API_KEY=sk-***
  python agent.py
可选环境变量：
  LOG_FILE=<路径>          默认 sample_failure.log
  TARGET_DIR=<目录>        默认 "cicd crash test"（受害者仓库）
  MODEL_NAME=<模型名>      默认 gpt-4o
"""

import json
import os
from pathlib import Path

from openai import OpenAI

# ================= 配置区 =================
LOG_FILE = os.getenv("LOG_FILE", "sample_failure.log")
TARGET_DIR = os.getenv("TARGET_DIR", "cicd crash test")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")

# 只允许 Agent 修改的文件类型（建立信任基线）
ALLOWED_SUFFIXES = (
    ".txt",
    ".json",
    ".yml",
    ".yaml",
    ".ini",
    ".cfg",
    ".toml",
    ".env",
    ".lock",
)
# =========================================


def read_log(max_lines: int = 200) -> str:
    """
    读取报错日志末尾 N 行，避免 token 过长且不截断 UTF-8。
    """
    log_path = Path(LOG_FILE)
    if not log_path.exists():
        raise FileNotFoundError(f"日志文件不存在: {log_path}")

    lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    tail = lines[-max_lines:]
    return "\n".join(tail)


def update_file(filename: str, content: str) -> str:
    """
    给 LLM 的工具：写入配置文件。
    - 仅允许白名单后缀
    - 防御越界写入
    """
    target_root = Path(TARGET_DIR).resolve()
    target_root.mkdir(parents=True, exist_ok=True)

    target_path = (target_root / filename).resolve()

    # 阻止目录穿越
    if target_root not in target_path.parents and target_root != target_path:
        raise ValueError("非法路径，拒绝写入。")

    if not target_path.suffix.lower() in ALLOWED_SUFFIXES:
        raise ValueError(f"不允许修改的文件类型: {target_path.suffix}")

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")

    preview = content.replace("\n", " ")
    print(f"[Agent] 已写入 {target_path}: {preview[:80]}...")
    return "File updated successfully."


# 定义 LLM 可调用的工具列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "update_file",
            "description": "Writes full content to a file in the repository. Use this to fix dependencies or config.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to edit (e.g., requirements.txt)",
                    },
                    "content": {
                        "type": "string",
                        "description": "The full content to write into the file",
                    },
                },
                "required": ["filename", "content"],
            },
        },
    }
]


def run_agent():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 OPENAI_API_KEY 环境变量。")

    client = OpenAI(api_key=api_key)

    log_content = read_log()
    print(f"系统: 已读取日志末尾 {len(log_content)} 字符，调用模型分析中...")

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个 DevOps 自动化助手。分析 CI/CD 报错日志，"
                "若发现缺少依赖或配置，请只修改配置文件（如 requirements.txt、*.yml、*.json 等），"
                "禁止修改业务代码。需要写文件时调用工具 update_file。"
            ),
        },
        {
            "role": "user",
            "content": f"构建失败日志片段如下，请修复:\n\n{log_content}\n",
        },
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    message = response.choices[0].message
    tool_calls = message.tool_calls

    if tool_calls:
        for tool_call in tool_calls:
            if tool_call.function.name != "update_file":
                continue
            args = json.loads(tool_call.function.arguments)
            update_file(args["filename"], args["content"])
    else:
        print("系统: 模型未调用工具，原样输出：")
        print(message.content)


if __name__ == "__main__":
    run_agent()

