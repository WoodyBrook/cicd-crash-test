# 受害者靶场 (Victim Repo)

这是一个故意设计为构建失败的 GitHub 仓库，用于测试 DevOps 工具和自动化 Agent。

## 🎯 项目目的

这个项目包含了三个故意设计的错误场景，用于测试 CI/CD 错误检测和修复能力。

## 💣 埋雷场景

### 场景 A: 依赖缺失
- **问题**: `main.py` 中导入了 `numpy`，但 `requirements.txt` 中没有包含
- **预期失败**: `ModuleNotFoundError: No module named 'numpy'`

### 场景 B: 环境变量缺失
- **问题**: `main.py` 中读取 `os.environ["API_KEY"]`，但 GitHub Actions 中没有配置
- **预期失败**: `KeyError: 'API_KEY'`

### 场景 C: 语法错误
- **问题**: `.github/workflows/test.yml` 中可能存在缩进或语法问题
- **预期失败**: GitHub Actions 解析错误或执行失败

## 🚀 使用方法

1. 将此仓库推送到 GitHub
2. 观察 GitHub Actions 自动运行并失败 ❌
3. 使用你的 Agent 工具来检测和修复这些错误

## 📝 修复指南

要修复这些错误，需要：

1. **场景 A**: 在 `requirements.txt` 中添加 `numpy`
2. **场景 B**: 在 GitHub Secrets 中配置 `API_KEY`，或在 workflow 文件中添加环境变量
3. **场景 C**: 检查并修复 YAML 文件的语法和缩进

## ⚠️ 警告

这个项目是故意设计为失败的，不要在生产环境中使用！

