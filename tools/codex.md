# Codex 工具配置

---

## 概述

Codex 是 OpenAI 的代码执行工具，用于：
- 代码执行和测试
- AI 辅助编程
- 自动化脚本运行

---

## 安装完成

### ✅ 已安装
```bash
# Python OpenAI 库
pip3 install openai --user

# Codex CLI（需要 Node.js）
npm install -g @openai/codex
```

### ✅ 配置文件
- `.env.codex` - 环境变量模板
- `tools/codex.md` - 使用文档

---

## 配置

### 环境变量

编辑 `~/.bashrc` 或复制 `.env.codex`：

```bash
export OPENAI_API_KEY="sk-xxxxxxxx"
export CODEX_MODEL="gpt-5-codex"
export CODEX_EXEC_TIMEOUT=1800
export CODEX_EXEC_FULL_AUTO=true
export PROJECT_ALLOWLIST="/home/admin/.openclaw/workspace,/tmp"
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

### 1. 直接调用（Python OpenAI）

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

### 2. 通过 Codex CLI

```bash
# 沙盒模式（推荐）
codex exec --full-auto "写个快速排序算法"

# 无限制模式（危险）
codex --yolo "写个快速排序算法"

# PR 审查
codex review --base main
```

### 3. 通过 Agent 调用

```
对我说：
"用 Codex 写个排序算法"
→ Dev Agent 自动调用 Codex
→ 生成并执行代码
→ 返回结果
```

### 4. 在 skills_bene 中使用

```bash
cd /home/admin/.openclaw/workspace/projects/skills_bene

# 修复 bug
python3 skills/openclaw-integration/codex_executor.py \
  --mode fix \
  --project-root /home/admin/.openclaw/workspace \
  --task "修复人员评价系统的 average_score 错误"

# 生成测试
python3 skills/openclaw-integration/codex_executor.py \
  --mode testgen \
  --project-root /home/admin/.openclaw/workspace \
  --task "为人员评价系统生成单元测试"

# 代码重构
python3 skills/openclaw-integration/codex_executor.py \
  --mode refactor \
  --project-root /home/admin/.openclaw/workspace \
  --task "优化数据库连接管理"
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

## 状态

| 组件 | 状态 |
|------|------|
| openai Python 库 | ✅ 已安装 (v2.26.0) |
| Codex CLI | ⏳ 安装中 |
| 配置文件 | ✅ 已创建 (.env.codex) |
| skills_bene 集成 | ✅ 已配置 |

**最后更新**: 2026-03-06
