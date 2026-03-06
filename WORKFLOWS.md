# Workflows 总览

工作流程索引

---

## 开发流程

| Workflow | 说明 | 文件 |
|----------|------|------|
| 🛠️ Development | 需求→方案→开发→测试→提交 | `workflows/dev-workflow.md` |
| 🧪 Testing | 测试计划→用例→执行→Bug 报告 | `workflows/testing-workflow.md` |
| 🚀 Deployment | 部署计划→备份→部署→监控 | `workflows/deployment-workflow.md` |

---

## 运维流程

| Workflow | 说明 | 文件 |
|----------|------|------|
| 📊 Monitoring | 健康检查→告警→处理 | （Phase 2） |
| 📝 Content | 内容生成→审核→发布 | （Phase 2） |

---

## 数据流程

| Workflow | 说明 | 文件 |
|----------|------|------|
| 📈 Data Processing | 读取→转换→分析→输出 | （Phase 2） |
| 🔍 Research | 信息收集→整理→报告 | （Phase 2） |

---

## 自动化

### Git Auto-Sync
- **路径**: `projects/git-auto-sync/sync.sh`
- **频率**: 每 30 分钟
- **说明**: 自动检测变更并提交推送

### Daily Standup
- **路径**: `projects/daily-standup/standup.sh`
- **频率**: 每天早上 9 点
- **说明**: 生成每日站会报告

---

## 使用方式

### 手动执行
```bash
# 开发流程
cd /home/admin/.openclaw/workspace
./projects/git-auto-sync/sync.sh

# 站会报告
./projects/daily-standup/standup.sh
```

### 定时执行（Cron）
```bash
crontab -e

# 每 30 分钟同步
*/30 * * * * /home/admin/.openclaw/workspace/projects/git-auto-sync/sync.sh

# 每天早上 9 点站会
0 9 * * * /home/admin/.openclaw/workspace/projects/daily-standup/standup.sh
```

---

## 相关文档

- `AGENTS.md` - 工作区规则
- `ARCHITECTURE.md` - 系统架构
- `TOOLS.md` - 工具文档
- `agents/*.md` - Agent 定义

---

**Version**: 1.0  
**Last Updated**: 2026-03-06
