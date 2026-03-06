# Daily Standup Bot 📋

自动生成每日站会报告，跟踪进度和 learnings。

## 功能

- ✅ 自动读取 Git 提交历史
- ✅ 汇总 learnings 学习记录
- ✅ 追踪待办事项 (SESSION-STATE.md)
- ✅ 生成 Markdown 报告
- ✅ 支持定时运行（cron）

## 输出示例

```markdown
# 每日站会报告
日期：2026-03-06

📦 昨日完成 (Git 提交):
  • feat: 添加自动同步脚本
  • fix: 修复 SSH 配置

🧠 学习记录:
  • LRN-20260306-001: Git SSH 配置流程

📋 待办事项:
  • [ ] 测试自改进能力
  • [ ] 自动同步脚本
```

## 快速开始

### 1. 手动运行

```bash
cd /home/admin/.openclaw/workspace/projects/daily-standup
chmod +x standup.sh
./standup.sh
```

### 2. 定时运行（推荐）

编辑 crontab：
```bash
crontab -e
```

**每天早上 9 点生成报告**：
```cron
0 9 * * * /home/admin/.openclaw/workspace/projects/daily-standup/standup.sh
```

**每周一早上 9 点生成周报**：
```cron
0 9 * * 1 /home/admin/.openclaw/workspace/projects/daily-standup/standup.sh
```

### 3. 查看报告

报告保存在：
```
/home/admin/.openclaw/workspace/projects/daily-standup/reports/standup-YYYY-MM-DD.md
```

查看最新报告：
```bash
cat /home/admin/.openclaw/workspace/projects/daily-standup/reports/standup-$(date '+%Y-%m-%d').md
```

## 输出格式

默认输出到终端 + Markdown 文件。

支持格式（修改脚本参数）：
- `text` - 纯文本
- `markdown` - Markdown 格式（默认）
- `json` - JSON 格式（便于集成）

## 集成到钉钉/微信

### 钉钉机器人

1. 创建钉钉群机器人，获取 Webhook URL
2. 修改脚本添加推送：

```bash
# 添加到 standup.sh 末尾
WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"

curl "$WEBHOOK" \
  -H "Content-Type: application/json" \
  -d "{
    \"msgtype\": \"markdown\",
    \"markdown\": {
      \"title\": \"每日站会\",
      \"text\": \"$(cat $REPORT_FILE | sed 's/\"/\\\"/g' | tr '\n' '\\n')\"
    }
  }"
```

### 微信企业版

类似，使用企业微信 Webhook。

## 配置选项

编辑 `standup.sh` 顶部：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `WORKSPACE` | 工作区路径 | `/home/admin/.openclaw/workspace` |
| `OUTPUT_DIR` | 报告输出目录 | `$WORKSPACE/projects/daily-standup/reports` |
| `DATE` | 报告日期 | 当天 |
| `YESTERDAY` | 统计起始日期 | 昨天 |

## 自定义报告内容

编辑 `standup.sh` 中的输出部分：

```bash
# 添加新的数据源
echo -e "${GREEN}🔥 新增模块:${NC}"
# 你的逻辑...
```

## 报告历史

所有历史报告保存在 `reports/` 目录：

```bash
# 查看所有报告
ls -la /home/admin/.openclaw/workspace/projects/daily-standup/reports/

# 查看上周报告
cat /home/admin/.openclaw/workspace/projects/daily-standup/reports/standup-2026-03-01.md
```

## 故障排查

### 没有 Git 提交记录
```bash
# 检查 git 配置
cd /home/admin/.openclaw/workspace
git log --oneline -5
```

### 报告文件为空
```bash
# 检查输出目录权限
ls -la /home/admin/.openclaw/workspace/projects/daily-standup/
```

### cron 不执行
```bash
# 检查 cron 日志
grep CRON /var/log/syslog | tail -20

# 测试脚本可执行性
bash -n /home/admin/.openclaw/workspace/projects/daily-standup/standup.sh
```

---

**上一步**: Git 自动同步 → `../git-auto-sync/README.md`
