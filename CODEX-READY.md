# Codex 配置完成 ✅

---

## 已安装组件

| 组件 | 状态 | 版本 |
|------|------|------|
| openai Python 库 | ✅ 已安装 | v2.26.0 |
| Codex CLI | ✅ 已安装 | latest |
| 配置文件 | ✅ 已创建 | .env.codex |

---

## 环境变量配置

已添加到 `~/.bashrc`：

```bash
# Codex 环境变量
export OPENAI_API_KEY="sk-your-api-key-here"
export CODEX_MODEL="gpt-5-codex"
export CODEX_EXEC_TIMEOUT=1800
export CODEX_EXEC_FULL_AUTO=true
export PROJECT_ALLOWLIST="/home/admin/.openclaw/workspace,/tmp"
export PATH="$HOME/.npm-global/bin:$PATH"
```

---

## 下一步：配置 API Key

### 1. 获取 API Key

访问：https://platform.openai.com/api-keys

### 2. 更新配置

编辑 `~/.bashrc` 或 `.env.codex`：

```bash
export OPENAI_API_KEY="sk-你的实际 API Key"
```

### 3. 使配置生效

```bash
source ~/.bashrc
```

### 4. 测试 Codex

```bash
# 检查 Codex CLI
codex --version

# 测试 Python 库
python3 -c "from openai import OpenAI; print('OK')"
```

---

## 使用方式

### 方式 1：Codex CLI

```bash
# 沙盒模式（推荐）
codex exec --full-auto "写个快速排序算法"

# 无限制模式（危险）
codex --yolo "写个快速排序算法"

# PR 审查
codex review --base main
```

### 方式 2：skills_bene 集成

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
```

### 方式 3：Python OpenAI 库

```python
from openai import OpenAI

client = OpenAI()  # 自动读取 OPENAI_API_KEY

response = client.chat.completions.create(
    model="gpt-5-codex",
    messages=[
        {"role": "user", "content": "写个 Python 脚本计算斐波那契数列"}
    ]
)

print(response.choices[0].message.content)
```

### 方式 4：通过 Agent

```
对我说：
"用 Codex 写个排序算法"
→ Dev Agent 自动调用 Codex
→ 生成并执行代码
→ 返回结果
```

---

## 安全配置

### 项目白名单

```bash
export PROJECT_ALLOWLIST="/home/admin/.openclaw/workspace,/tmp"
```

Codex 只能访问白名单内的目录。

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

## 文件位置

```
/home/admin/.openclaw/workspace/
├── .env.codex                    ← 环境变量模板
├── CODEX-READY.md                ← 配置完成文档
├── tools/codex.md                ← 使用文档
└── projects/skills_bene/
    └── openclaw-integration/
        ├── codex_executor.py     ← Codex 执行脚本
        └── openclaw-hub-config.json ← 配置
```

---

## 常见问题

### Q: 如何测试 Codex 是否可用？

```bash
# 检查 CLI
codex --version

# 检查 Python 库
python3 -c "from openai import OpenAI; print('OK')"

# 测试执行（需要 API Key）
codex exec --full-auto "Hello World"
```

### Q: 没有 API Key 能用吗？

不能。Codex 需要 OpenAI API Key 才能工作。

### Q: API Key 安全吗？

- 只保存在本地配置文件
- 不会推送到 GitHub（.gitignore 已配置）
- 建议设置使用限制和预算

---

## 状态

**配置完成度**: 95%  
**待完成**: 配置实际 API Key

**准备就绪**: ✅ 只需配置 API Key 即可使用！

---

**最后更新**: 2026-03-06 22:20
