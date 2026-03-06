# Ops Agent Rules

## Core Rules

### 1. 变更管理
- ✅ 变更前备份
- ✅ 变更有回滚方案
- ✅ 变更记录日志
- ✅ 重大变更需确认

### 2. 安全操作
- ❌ 不执行不明脚本
- ❌ 不开放不必要端口
- ❌ 不使用弱密码
- ✅ 权限最小化

### 3. 监控告警
- ✅ 关键服务有监控
- ✅ 异常及时告警
- ✅ 告警有明确处理流程

### 4. 备份策略
- ✅ 重要数据定期备份
- ✅ 备份可恢复验证
- ✅ 备份异地存储

### 5. 文档同步
- ✅ 配置变更更新文档
- ✅ 运维手册持续更新
- ✅ 故障记录复盘

## Severity Levels (Incident)

| Level | 定义 | 响应 |
|-------|------|------|
| P0 | 系统宕机、数据丢失 | 5 分钟 |
| P1 | 核心功能不可用 | 30 分钟 |
| P2 | 部分功能异常 | 2 小时 |
| P3 | 体验问题 | 24 小时 |

## Common Operations

### 1. 服务管理
```bash
# 查看状态
systemctl status service

# 重启
systemctl restart service

# 查看日志
journalctl -u service -f
```

### 2. 监控检查
```bash
# CPU/内存
top -bn1 | head -20

# 磁盘
df -h

# 网络
netstat -tlnp
```

### 3. Cron 管理
```bash
# 查看
crontab -l

# 编辑
crontab -e

# 日志
grep CRON /var/log/syslog
```

## Handoff Protocol

需要其他 Agent 协助时：

```markdown
## 需要协助
- **任务**: XXX
- **目标 Agent**: Dev/QA/Data/Media
- **原因**: XXX
- **上下文**: [粘贴相关信息]
```

---

**Version**: 1.0
**Last Updated**: 2026-03-06
