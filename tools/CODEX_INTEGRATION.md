# Codex 集成指南

## 当前状态

| 组件 | 状态 | 说明 |
|------|------|------|
| Codex CLI | ✅ 已安装 | v0.111.0 |
| API Key | ⚠️ 配额超限 | 需要充值或更换 Key |
| 登录状态 | ✅ 已登录 | 通过 API Key |
| 配置文件 | ✅ 已创建 | `~/.codex/config.toml` |
| 环境变量 | ✅ 已配置 | `~/.bashrc` |

---

## 配置说明

### 1. 环境变量（已配置）

```bash
# ~/.bashrc 中已添加
export OPENAI_API_KEY="sk-proj-xxxxxxxx"
export CODEX_MODEL="gpt-5-codex"
export CODEX_EXEC_TIMEOUT=1800
export CODEX_EXEC_FULL_AUTO=true
export PROJECT_ALLOWLIST="/home/admin/.openclaw/workspace,/tmp"
export CODEX_EXTRA_CONSTRAINTS="仅修改 src/ 与 tests/，禁止触碰部署脚本"
```

### 2. Codex 配置

```bash
# ~/.codex/config.toml
model = "gpt-5-codex"

[provider]
type = "openai"
api_key = "sk-proj-xxxxxxxx"

sandbox = "workspace-write"

[features]
full_auto = true
```

### 3. 登录方式

```bash
# 使用 API Key 登录（推荐）
echo "sk-proj-xxx" | codex login --with-api-key

# 或使用 ChatGPT 账号（需要 Plus/Pro 订阅）
codex login
```

---

## 使用方式

### 方式 1: Codex CLI 直接调用

```bash
cd /home/admin/.openclaw/workspace

# 简单任务
codex exec --full-auto "写个 Python 脚本计算斐波那契数列"

# 指定模型
codex exec -m "gpt-5-codex" --full-auto "重构 utils 目录"

# 代码审查
codex review --base main

# 应用变更
codex apply
```

### 方式 2: Python OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-proj-xxx"
)

response = client.chat.completions.create(
    model="gpt-5-codex",
    messages=[
        {"role": "system", "content": "你是一个专业的 Python 工程师"},
        {"role": "user", "content": "写个快速排序算法"}
    ]
)

print(response.choices[0].message.content)
```

### 方式 3: Codex Executor 脚本

```bash
cd /home/admin/.openclaw/workspace

# 修复 Bug
python3 projects/skills_bene/skills/openclaw-integration/codex_executor.py \
  --mode fix \
  --project-root /home/admin/.openclaw/workspace \
  --task "修复人员评价系统的 average_score 错误"

# 生成测试
python3 projects/skills_bene/skills/openclaw-integration/codex_executor.py \
  --mode testgen \
  --project-root /home/admin/.openclaw/workspace \
  --task "为 UItest 项目生成单元测试"

# 代码重构
python3 projects/skills_bene/skills/openclaw-integration/codex_executor.py \
  --mode refactor \
  --project-root /home/admin/.openclaw/workspace \
  --task "优化数据库连接管理"
```

输出示例：
```json
{
  "success": true,
  "mode": "fix",
  "project_root": "/home/admin/.openclaw/workspace",
  "task": "修复人员评价系统的 average_score 错误",
  "duration_seconds": 45.2,
  "exit_code": 0,
  "last_message": "已完成修复...",
  "stdout_tail": "...",
  "stderr_tail": "..."
}
```

---

## ClawOS 集成方案

### 1. Agent 路由配置

在 OpenClaw 中配置 Codex 作为**Dev Agent**的后端：

```json
{
  "agents": {
    "dev": {
      "backend": "codex",
      "model": "gpt-5-codex",
      "auto_execute": true,
      "sandbox": "workspace-write"
    }
  }
}
```

### 2. 任务类型映射

| 用户请求 | Codex Mode | 示例 |
|---------|-----------|------|
| "修复 XXX bug" | `fix` | 自动定位并修复 |
| "写个测试" | `testgen` | 生成单元测试 |
| "优化 XXX" | `refactor` | 重构代码 |
| "实现 XXX 功能" | `exec` | 完整功能开发 |

### 3. 自动化工作流

```bash
#!/bin/bash
# codex_workflow.sh

# 1. 接收任务
TASK="$1"
MODE="$2"  # fix|testgen|refactor

# 2. 执行 Codex
python3 codex_executor.py \
  --mode "$MODE" \
  --project-root /home/admin/.openclaw/workspace \
  --task "$TASK" \
  --output /tmp/codex_result.json

# 3. 解析结果
RESULT=$(cat /tmp/codex_result.json)
SUCCESS=$(echo "$RESULT" | jq -r '.success')

# 4. 钉钉通知
if [ "$SUCCESS" = "true" ]; then
    dingtalk-notify "✅ Codex 任务完成：$TASK"
else
    dingtalk-notify "❌ Codex 任务失败：$TASK"
fi

# 5. Git 提交
if [ "$SUCCESS" = "true" ]; then
    git add -A
    git commit -m "codex: $TASK"
    git push
fi
```

### 4. Cron 定时任务

```bash
# 每日代码审查
0 9 * * * cd /home/admin/.openclaw/workspace && codex review --base main | dingtalk-notify

# 每周重构优化
0 3 * * 0 python3 codex_executor.py --mode refactor --task "代码质量优化"

# 测试覆盖率检查
0 6 * * * pytest --cov=src/ --cov-report=term-missing | codex exec "分析测试覆盖率并生成改进建议"
```

---

## 安全配置

### 1. 项目白名单

```bash
export PROJECT_ALLOWLIST="/home/admin/.openclaw/workspace,/tmp"
```

只允许 Codex 修改白名单内的目录。

### 2. 执行约束

```bash
export CODEX_EXTRA_CONSTRAINTS="仅修改 src/ 与 tests/，禁止触碰部署脚本"
```

### 3. 沙盒模式

```bash
# 安全工作目录
codex exec --sandbox workspace-write "..."

# 完全隔离（推荐用于未知代码）
codex exec --sandbox strict "..."
```

### 4. 超时限制

```bash
export CODEX_EXEC_TIMEOUT=1800  # 30 分钟
```

---

## 最佳实践

### 1. 任务描述模板

```
[目标] 清晰描述要完成的任务
[约束] 说明限制条件
[验证] 指定如何验证结果

示例：
[目标] 为人员评价系统添加单元测试
[约束] 使用 pytest，覆盖率达到 80%
[验证] 运行 pytest tests/ 全部通过
```

### 2. 代码审查流程

```bash
# 1. Codex 审查
codex review --base main

# 2. 人工确认
git diff

# 3. 应用变更
codex apply

# 4. 运行测试
pytest

# 5. 提交
git commit -m "review: AI 辅助代码审查"
```

### 3. 错误处理

```python
try:
    result = run_codex(task)
    if result['success']:
        apply_changes(result)
    else:
        log_error(result['error'])
        notify_failure(result)
except TimeoutExpired:
    log_error("任务超时")
except Exception as e:
    log_error(f"未知错误：{e}")
```

---

## 常见问题

### Q: "Quota exceeded" 怎么办？
A: 
1. 检查 OpenAI 账单：https://platform.openai.com/usage
2. 充值或等待下月配额
3. 使用 ChatGPT Plus/Pro 账号登录（包含无限使用）

### Q: 如何切换 API Key？
```bash
# 1. 登出
codex logout

# 2. 登录新 Key
echo "sk-new-key" | codex login --with-api-key

# 3. 验证
codex login status
```

### Q: Codex 和普通 GPT 有什么区别？
A: 
- Codex 专门用于代码生成和执行
- 支持沙盒隔离
- 可直接修改文件
- 理解项目结构

### Q: 如何限制 Codex 权限？
A: 
```bash
# 只读模式
codex exec --sandbox read-only "..."

# 指定目录
codex exec -c 'sandbox_permissions=["disk-full-read-access"]' "..."

# 禁止网络
codex exec -c 'shell_environment_policy.inherit=none' "..."
```

---

## 性能优化

### 1. 缓存配置

```toml
# ~/.codex/config.toml
[cache]
enabled = true
max_size_mb = 500
```

### 2. 并行执行

```bash
# 多个任务并行
codex exec "任务 1" &
codex exec "任务 2" &
wait
```

### 3. 增量处理

```bash
# 只处理变更文件
git diff --name-only | xargs codex exec "审查变更"
```

---

## 监控与日志

### 1. 执行日志

```bash
# Codex 日志目录
ls ~/.codex/log/

# 查看最近执行
tail -f ~/.codex/log/latest.log
```

### 2. 审计追踪

```bash
# 记录所有 Codex 执行
script -c "codex exec ..." /tmp/codex_audit.log
```

### 3. 指标收集

```python
# 收集执行指标
metrics = {
    "duration": result["duration_seconds"],
    "success": result["success"],
    "exit_code": result["exit_code"],
    "tokens_used": estimate_tokens(result)
}
```

---

## 下一步

1. **充值 API Key** - 解决配额问题
2. **配置 Agent 路由** - 集成到 ClawOS
3. **设置 Cron 任务** - 自动化执行
4. **钉钉通知** - 结果推送
5. **Git 集成** - 自动提交

---

**最后更新**: 2026-03-07  
**状态**: ⚠️ API Key 配额超限，需要充值
