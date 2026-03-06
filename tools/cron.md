# Cron 定时任务配置

---

## 已配置任务

| 任务 | 频率 | 时间 | 脚本 |
|------|------|------|------|
| 🔄 自动同步 | 每 30 分钟 | */30 * * * * | `git-auto-sync/sync.sh` |
| 📋 每日站会 | 每天 | 0 9 * * * | `daily-standup/standup.sh` |

---

## 管理命令

### 查看
```bash
crontab -l
```

### 编辑
```bash
crontab -e
```

### 删除
```bash
crontab -r
```

### 查看日志
```bash
# Cron 执行日志
grep CRON /var/log/syslog | tail -20

# 实时查看
tail -f /var/log/syslog | grep CRON
```

---

## 已配置任务详解

### 1. 自动同步（每 30 分钟）

**Cron 表达式**: `*/30 * * * *`

**执行内容**:
```bash
/home/admin/.openclaw/workspace/projects/git-auto-sync/sync.sh
```

**功能**:
- 检测 workspace 变更
- 自动 git add/commit
- 推送到 GitHub
- 记录日志

**日志**: `projects/git-auto-sync/sync.log`

---

### 2. 每日站会（每天早上 9 点）

**Cron 表达式**: `0 9 * * *`

**执行内容**:
```bash
/home/admin/.openclaw/workspace/projects/daily-standup/standup.sh
```

**功能**:
- 读取昨日 Git 提交
- 汇总 learnings 记录
- 生成 Markdown 报告
- 保存到 `reports/standup-YYYY-MM-DD.md`

**报告位置**: `projects/daily-standup/reports/`

---

## 可选任务（已注释）

### 健康检查（每小时）
```cron
0 * * * * /opt/scripts/healthcheck.sh
```
检查 CPU/内存/磁盘，超阈值告警

### 完整备份（每周日凌晨 2 点）
```cron
0 2 * * 0 tar -czf /backup/workspace_$(date +%Y%m%d).tar.gz /home/admin/.openclaw/workspace
```
完整备份 workspace 到 `/backup/`

---

## Cron 表达式语法

```
* * * * *
│ │ │ │ │
│ │ │ │ └─ 星期 (0-7, 0 和 7 都是周日)
│ │ │ └─── 月份 (1-12)
│ │ └───── 日期 (1-31)
│ └─────── 小时 (0-23)
└───────── 分钟 (0-59)
```

### 示例

| 表达式 | 说明 |
|--------|------|
| `*/5 * * * *` | 每 5 分钟 |
| `0 * * * *` | 每小时整点 |
| `0 9 * * *` | 每天早上 9 点 |
| `0 0 * * 0` | 每周日凌晨 0 点 |
| `0 0 1 * *` | 每月 1 号凌晨 0 点 |

---

## 故障排查

### 任务不执行
```bash
# 1. 检查 cron 服务
systemctl status cron

# 2. 查看日志
grep CRON /var/log/syslog | tail -50

# 3. 测试脚本可执行性
bash -n /home/admin/.openclaw/workspace/projects/git-auto-sync/sync.sh

# 4. 手动运行测试
/home/admin/.openclaw/workspace/projects/git-auto-sync/sync.sh
```

### 权限问题
```bash
# 确保脚本可执行
chmod +x /home/admin/.openclaw/workspace/projects/*/standup.sh
chmod +x /home/admin/.openclaw/workspace/projects/*/sync.sh
```

### 环境变量问题
Cron 环境变量最小化，脚本中要用绝对路径。

---

## 最佳实践

1. **输出重定向**: `>> /dev/null 2>&1` 避免邮件轰炸
2. **日志记录**: 脚本内记录详细日志
3. **错误处理**: 脚本要有错误处理
4. **幂等操作**: 多次执行结果一致
5. **定期清理**: 日志文件定期轮转

---

## 相关文档

- `projects/git-auto-sync/README.md` - 自动同步说明
- `projects/daily-standup/README.md` - 每日站会说明
- `workflows/deployment-workflow.md` - 部署流程

---

**Version**: 1.0  
**Last Updated**: 2026-03-06  
**Config File**: `/home/admin/.openclaw/workspace/crontab.txt`
