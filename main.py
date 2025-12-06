#!/usr/bin/env python3
"""
受害者靶场 - 包含多个故意设计的错误
"""

# 场景 A: 依赖缺失 - 导入 numpy 但 requirements.txt 中没有
import numpy as np

# 场景 B: 环境变量缺失 - 读取未配置的 API_KEY
import os

def main():
    print("开始执行受害者脚本...")
    
    # 场景 A: 使用 numpy（但 requirements.txt 中没有）
    arr = np.array([1, 2, 3, 4, 5])
    print(f"NumPy 数组: {arr}")
    
    # 场景 B: 读取环境变量（但 GitHub Secrets 中没有配置）
    api_key = os.environ["API_KEY"]
    print(f"API Key: {api_key[:10]}...")  # 只显示前10个字符
    
    print("执行完成！")

if __name__ == "__main__":
    main()

