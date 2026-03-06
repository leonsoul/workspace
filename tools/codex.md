# Codex 工具配置

---

## 概述

Codex 是 OpenAI 的代码执行工具，用于：
- 代码执行和测试
- AI 辅助编程
- 自动化脚本运行

---

## 安装

```bash
pip3 install openai --user
```

---

## 配置

### 环境变量

编辑 `~/.bashrc` 或 `.env` 文件：

```bash
export OPENAI_API_KEY="sk-xxxxxxxx"
export CODEX_MODEL="gpt-5-codex"
export CODEX_EXEC_TIMEOUT=1800
export CODEX_EXEC_FULL_AUTO=true
```

### 在 OpenClaw 中使用

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "tools": {
    "codex": {
      "enabled": true,
      "apiKey": "sk-xxxxxxxx",
      "model": "gpt-5-codex",
      "timeout": 1800
    }
  }
}
```

---

## 使用方式

### 1. 直接调用

```python
from openai import OpenAI

client = OpenAI(api_key="sk-xxx")

response = client.chat.completions.create(
    model="gpt-5-codex",
    messages=[
        {"role": "user", "content": "写个 Python 脚本计算斐波那契数列"}
    ]
)

print(response.choices[0].message.content)
```

### 2. 通过 Agent 调用

```
用户：用 Codex 写个排序算法
→ Dev Agent 自动调用 Codex
→ 生成并执行代码
→ 返回结果
```

### 3. 在 skills_bene 中集成

编辑 `skills_bene/integration/openclaw-integration-config.json`：

```json
{
  "codex": {
    "enabled": true,
    "use_for": ["code-generation", "code-review", "testing"]
  }
}
```

---

## 安全配置

### 项目白名单

```bash
export PROJECT_ALLOWLIST="/home/admin/.openclaw/workspace,/tmp"
```

### 执行限制

```bash
# 禁止删除文件
export CODEX_NO_DELETE=true

# 禁止网络访问
export CODEX_NO_NETWORK=false

# 最大执行时间（秒）
export CODEX_TIMEOUT=1800
```

---

## 最佳实践

1. **设置超时** - 避免无限循环
2. **项目白名单** - 限制可访问的目录
3. **日志记录** - 记录所有 Codex 执行
4. **结果验证** - 验证代码执行结果
5. **错误处理** - 捕获并处理异常

---

## 常见问题

### Q: API Key 在哪里获取？
A: https://platform.openai.com/api-keys

### Q: Codex 和普通 GPT 有什么区别？
A: Codex 专门用于代码生成和执行，支持代码解释器

### Q: 如何限制 Codex 的权限？
A: 使用 PROJECT_ALLOWLIST 和 CODEX_NO_* 环境变量

---

**状态**: ✅ 已安装  
**版本**: openai latest  
**最后更新**: 2026-03-06
