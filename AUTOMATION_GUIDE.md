# ClawOS 自动化系统集成手册

> 🦞 将 ClawOS 打造成真正的自动化操作系统

---

## 目录

1. [系统概览](#系统概览)
2. [UItest 自动化测试](#uitest-自动化测试)
3. [Codex AI 代码助手](#codex-ai-代码助手)
4. [Git 自动同步](#git-自动同步)
5. [钉钉通知集成](#钉钉通知集成)
6. [Cron 定时任务](#cron-定时任务)
7. [最佳实践](#最佳实践)

---

## 系统概览

### 架构图

```
┌─────────────────────────────────────────────────────────┐
│                    ClawOS Workspace                      │
│  /home/admin/.openclaw/workspace                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   UItest     │  │    Codex     │  │     Git      │  │
│  │  自动化测试   │  │  AI 代码助手   │  │   版本控制    │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │           │
│         └────────────────┼────────────────┘           │
│                          │                             │
│                 ┌────────▼────────┐                    │
│                 │  Cron Scheduler │                    │
│                 │   定时任务调度   │                    │
│                 └────────┬────────┘                    │
│                          │                             │
│                 ┌────────▼────────┐                    │
│                 │  Dingtalk Bot   │                    │
│                 │    钉钉通知     │                    │
│                 └─────────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

### 核心组件

| 组件 | 位置 | 状态 | 用途 |
|------|------|------|------|
| UItest | `projects/UItest/` | ✅ 运行中 | Web UI 自动化测试 |
| Codex | `tools/codex*` | ⚠️ 需充值 | AI 代码生成与执行 |
| Git Sync | `.git/` | ✅ 运行中 | 代码版本控制 |
| Cron | `/etc/cron.d/` | ✅ 配置中 | 定时任务调度 |
| Dingtalk | `utils/PreProcessing/` | ✅ 已集成 | 消息通知 |

---

## UItest 自动化测试

### 快速开始

```bash
cd /home/admin/.openclaw/workspace/projects/UItest

# 运行测试
python run.py 0  # alltuu 环境
python run.py 1  # guituu 环境

# 查看报告
allure open Reports/alltuu/allure-report/
```

### 配置说明

**conf.ini** - 全局配置
```ini
[BrowserType]
type = chrome
show_type = head  # headless 用于 CI/CD

[Environ]
run_env = Dev
is_debug = False
```

**conf/alltuu_conf.ini** - 环境配置
```ini
[Dev]
index = https://www.alltuu.com
user_name = 11155555555
password = alltuu123@
```

### 集成到 ClawOS

```bash
# 1. 添加到 Cron（每日凌晨 2 点）
0 2 * * * cd /home/admin/.openclaw/workspace/projects/UItest && python run.py 0 >> /var/log/uitest.log 2>&1

# 2. 失败时发送钉钉通知
# 在 run.py 中已集成 DingtalkChatbot
```

### 报告查看

```bash
# 本地查看
allure open Reports/alltuu/allure-report/

# 或部署到 Web
allure generate Reports/alltuu/allure-result/ -o /var/www/html/uitest/ --clean
# 访问 http://your-server/uitest/
```

**详细文档**: `projects/UItest/CLAWOS_INTEGRATION.md`

---

## Codex AI 代码助手

### 快速开始

```bash
cd /home/admin/.openclaw/workspace

# 使用包装脚本
./tools/codex_runner.sh -m fix "修复人员评价系统的 average_score 错误"

# 或直接调用 Codex CLI
codex exec --full-auto "写个 Python 脚本计算斐波那契数列"
```

### 执行模式

| 模式 | 说明 | 示例 |
|------|------|------|
| `fix` | 修复 Bug | `-m fix "修复登录失败问题"` |
| `testgen` | 生成测试 | `-m testgen "为 utils 生成单元测试"` |
| `refactor` | 代码重构 | `-m refactor "优化数据库连接"` |
| `exec` | 通用执行 | `-m exec "实现用户注册功能"` |

### 使用示例

```bash
# 修复 Bug
./tools/codex_runner.sh -m fix \
  -p /home/admin/.openclaw/workspace \
  "修复人员评价系统的 average_score 计算错误"

# 生成测试
./tools/codex_runner.sh -m testgen \
  -p /home/admin/.openclaw/workspace/projects/UItest \
  "为 Test_HomeElement.py 添加边界测试用例"

# 代码重构
./tools/codex_runner.sh -m refactor \
  -p /home/admin/.openclaw/workspace \
  "优化数据库连接池管理，添加连接重试机制"
```

### 配置说明

**环境变量** (`~/.bashrc`)
```bash
export OPENAI_API_KEY="sk-proj-xxx"
export CODEX_MODEL="gpt-5-codex"
export CODEX_EXEC_TIMEOUT=1800
export CODEX_EXEC_FULL_AUTO=true
export PROJECT_ALLOWLIST="/home/admin/.openclaw/workspace,/tmp"
```

**Codex 配置** (`~/.codex/config.toml`)
```toml
model = "gpt-5-codex"

[provider]
type = "openai"
api_key = "sk-proj-xxx"

sandbox = "workspace-write"

[features]
full_auto = true
```

### 登录 Codex

```bash
# 使用 API Key 登录
echo "sk-proj-xxx" | codex login --with-api-key

# 验证登录状态
codex login status
```

### 当前状态

⚠️ **API Key 配额超限**，需要：
1. 充值 OpenAI API
2. 或使用 ChatGPT Plus/Pro 账号登录

**详细文档**: `tools/CODEX_INTEGRATION.md`

---

## Git 自动同步

### 配置说明

**自动同步脚本** (`scripts/git-sync.sh`)
```bash
#!/bin/bash
cd /home/admin/.openclaw/workspace
git pull origin master
git add -A
git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M')"
git push
```

**Cron 配置** (`/etc/cron.d/openclaw-git`)
```bash
# 每 30 分钟自动同步
*/30 * * * * admin /home/admin/.openclaw/workspace/scripts/git-sync.sh >> /var/log/git-sync.log 2>&1
```

### 手动同步

```bash
cd /home/admin/.openclaw/workspace

# 拉取最新代码
git pull origin master

# 提交本地变更
git add -A
git commit -m "manual: 描述你的变更"
git push
```

### 查看同步历史

```bash
cd /home/admin/.openclaw/workspace
git log --oneline -20
```

---

## 钉钉通知集成

### 配置 Webhook

**环境变量**
```bash
export DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=xxx"
export DINGTALK_SECRET="SECxxx"
```

### 发送通知

**Python**
```python
from DingtalkChatbot import DingtalkChatbot

bot = DingtalkChatbot(webhook)
bot.send_text("""
🦞 ClawOS 通知

任务：UI 自动化测试
状态：✅ 通过
用例：114/114
报告：http://your-server/uitest/
""")
```

**Bash**
```bash
curl 'https://oapi.dingtalk.com/robot/send?access_token=xxx' \
  -H 'Content-Type: application/json' \
  -d '{
    "msgtype": "text",
    "text": {
        "content": "🦞 ClawOS 通知\n\n任务完成！"
    }
  }'
```

### 集成场景

1. **测试完成通知**
   - UItest 执行完毕
   - 通过率统计
   - 报告链接

2. **Codex 任务通知**
   - 任务开始/完成
   - 执行结果
   - 变更摘要

3. **Git 同步通知**
   - 同步成功/失败
   - 变更文件列表
   - Commit 信息

4. **系统告警**
   - 服务异常
   - 资源不足
   - 任务失败

---

## Cron 定时任务

### 配置位置

```bash
# 系统 Cron 目录
/etc/cron.d/openclaw

# 或用户 Cron
crontab -e
```

### 完整配置示例

```bash
# /etc/cron.d/openclaw

# UI 自动化测试 - 每日凌晨 2 点
0 2 * * * admin cd /home/admin/.openclaw/workspace/projects/UItest && python run.py 0 >> /var/log/uitest.log 2>&1

# Git 自动同步 - 每 30 分钟
*/30 * * * * admin cd /home/admin/.openclaw/workspace && git pull origin master >> /var/log/git-sync.log 2>&1

# Codex 代码审查 - 每日上午 9 点
0 9 * * * admin cd /home/admin/.openclaw/workspace && codex review --base main >> /var/log/codex-review.log 2>&1

# 健康检查 - 每 5 分钟
*/5 * * * * admin /home/admin/.openclaw/workspace/scripts/health-check.sh >> /var/log/health.log 2>&1

# 清理日志 - 每周日凌晨 3 点
0 3 * * 0 admin find /var/log -name "*.log" -mtime +7 -delete
```

### 管理命令

```bash
# 查看 Cron 状态
systemctl status cron

# 重启 Cron 服务
sudo systemctl restart cron

# 查看 Cron 日志
tail -f /var/log/cron.log

# 验证 Cron 配置
sudo crontab -l  # 用户 Cron
sudo cat /etc/cron.d/openclaw  # 系统 Cron
```

---

## 最佳实践

### 1. 任务自动化原则

- **最小必要改动** - 避免影响无关模块
- **验证先行** - 变更前先有测试
- **日志完整** - 记录所有执行过程
- **失败通知** - 及时告警异常

### 2. 安全工作流

```bash
# 1. Codex 生成代码
./tools/codex_runner.sh -m fix "修复 XXX"

# 2. 人工审查变更
git diff

# 3. 运行测试验证
cd projects/UItest && python run.py 0

# 4. 查看测试报告
allure open Reports/alltuu/allure-report/

# 5. 提交代码
git add -A
git commit -m "fix: AI 辅助修复 XXX"
git push

# 6. 发送通知
dingtalk-notify "✅ 任务完成：修复 XXX"
```

### 3. 错误处理

```bash
#!/bin/bash
set -e  # 遇到错误立即退出

# 执行任务
if ! ./tools/codex_runner.sh -m fix "XXX"; then
    log_error "任务失败"
    dingtalk-notify "❌ Codex 任务失败"
    exit 1
fi

# 验证结果
if ! pytest tests/ -q; then
    log_error "测试失败"
    dingtalk-notify "❌ 测试未通过"
    exit 1
fi

log_info "✅ 任务成功"
dingtalk-notify "✅ 任务完成"
```

### 4. 性能优化

- **并行执行** - 多个测试并行运行
- **增量处理** - 只处理变更文件
- **缓存配置** - 减少重复计算
- **超时限制** - 避免无限等待

### 5. 监控指标

```python
metrics = {
    "uitest": {
        "total": 114,
        "passed": 110,
        "failed": 4,
        "duration": 1800
    },
    "codex": {
        "tasks_today": 5,
        "success_rate": 0.95,
        "avg_duration": 45
    },
    "git": {
        "commits_today": 12,
        "sync_status": "ok"
    }
}
```

---

## 故障排查

### UItest 失败

```bash
# 1. 检查 Chrome
google-chrome --version

# 2. 检查依赖
cd projects/UItest
pip install -r requirements.txt

# 3. 查看日志
tail -f Reports/Log/*/system.log

# 4. 运行单个测试
pytest TestCases/BeforeLoginCase/Test_HomeElement.py -v
```

### Codex 配额超限

```bash
# 1. 检查用量
curl https://api.openai.com/v1/usage -H "Authorization: Bearer $OPENAI_API_KEY"

# 2. 充值或更换 Key
# https://platform.openai.com/account/billing

# 3. 使用 ChatGPT 账号登录
codex login
```

### Git 同步失败

```bash
# 1. 检查网络连接
ping github.com

# 2. 检查 SSH Key
ssh -T git@github.com

# 3. 手动拉取
cd /home/admin/.openclaw/workspace
git pull origin master

# 4. 查看日志
tail -f /var/log/git-sync.log
```

---

## 下一步

1. **充值 Codex API** - 解决配额问题
2. **部署报告服务** - Nginx 托管 Allure 报告
3. **配置完整 Cron** - 部署所有定时任务
4. **完善通知模板** - 美化钉钉消息
5. **添加监控面板** - Grafana 展示指标

---

**最后更新**: 2026-03-07  
**维护者**: ClawOS Team 🦞
