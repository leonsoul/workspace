# Ops Agent Skills

## Available Tools

| Tool | Usage | Example |
|------|-------|---------|
| `exec` | 执行系统命令 | `exec(command="systemctl status nginx")` |
| `read/write` | 配置文件 | `write(path="/etc/cron.d/backup", content="...")` |
| `nodes` | 设备管理 | `nodes(action="status")` |
| `message` | 发送告警 | `message(action="send", target="admin", message="Alert!")` |
| `process` | 进程管理 | `process(action="list")` |

## Common Patterns

### 1. 部署脚本
```bash
#!/bin/bash
# Deploy: <service>
set -e

SERVICE="myservice"
BACKUP_DIR="/backup/$SERVICE/$(date +%Y%m%d_%H%M%S)"

log() {
    echo "[$(date '+%H:%M:%S')] $1"
}

backup() {
    log "Backing up..."
    mkdir -p "$BACKUP_DIR"
    cp -r /opt/$SERVICE/* "$BACKUP_DIR/"
    log "Backup saved to $BACKUP_DIR"
}

deploy() {
    log "Deploying..."
    # Your deploy logic
    systemctl restart $SERVICE
    log "Deployed"
}

rollback() {
    log "Rolling back to $BACKUP_DIR..."
    cp -r "$BACKUP_DIR"/* /opt/$SERVICE/
    systemctl restart $SERVICE
    log "Rolled back"
}

main() {
    log "=== Deploy Started ==="
    backup
    if deploy; then
        log "=== Deploy Success ==="
    else
        log "=== Deploy Failed, Rolling Back ==="
        rollback
        exit 1
    fi
}

main
```

### 2. 监控脚本
```bash
#!/bin/bash
# Monitor: system health

THRESHOLD_CPU=80
THRESHOLD_MEM=90
THRESHOLD_DISK=85

check_cpu() {
    CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 | cut -d'.' -f1)
    [ "$CPU" -gt "$THRESHOLD_CPU" ] && echo "ALERT: CPU at ${CPU}%" && return 1
    return 0
}

check_memory() {
    MEM=$(free | grep Mem | awk '{printf("%.0f", $3/$2*100)}')
    [ "$MEM" -gt "$THRESHOLD_MEM" ] && echo "ALERT: Memory at ${MEM}%" && return 1
    return 0
}

check_disk() {
    DISK=$(df / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
    [ "$DISK" -gt "$THRESHOLD_DISK" ] && echo "ALERT: Disk at ${DISK}%" && return 1
    return 0
}

main() {
    echo "=== System Health Check ==="
    echo "Time: $(date)"
    echo ""
    
    FAILED=0
    
    check_cpu || FAILED=1
    check_memory || FAILED=1
    check_disk || FAILED=1
    
    echo ""
    if [ $FAILED -eq 0 ]; then
        echo "✅ All checks passed"
        exit 0
    else
        echo "❌ Some checks failed"
        exit 1
    fi
}

main
```

### 3. Cron 配置
```bash
# 编辑 crontab
crontab -e

# 每 5 分钟执行
*/5 * * * * /opt/scripts/healthcheck.sh

# 每天凌晨 2 点备份
0 2 * * * /opt/scripts/backup.sh

# 每周一早上 9 点报告
0 9 * * 1 /opt/scripts/weekly_report.sh
```

### 4. 日志轮转
```bash
# /etc/logrotate.d/myservice
/var/log/myservice/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root root
    postrotate
        systemctl reload myservice
    endscript
}
```

## Alert Templates

### 钉钉告警
```bash
send_alert() {
    local message="$1"
    local webhook="https://oapi.dingtalk.com/robot/send?access_token=XXX"
    
    curl "$webhook" \
        -H "Content-Type: application/json" \
        -d "{
            \"msgtype\": \"text\",
            \"text\": {
                \"content\": \"🚨 告警：$message\"
            }
        }"
}
```

### 邮件告警
```bash
send_email_alert() {
    local subject="$1"
    local body="$2"
    
    echo "$body" | mail -s "$subject" admin@example.com
}
```

## Limitations

- ❌ 不能重启生产服务器（需确认）
- ❌ 不能修改防火墙规则（需确认）
- ❌ 不能删除生产数据（需确认）
- ❌ 不能访问其他服务器 SSH（需配置）

## Best Practices

1. **幂等操作**: 脚本多次执行结果一致
2. **日志完整**: 所有操作记录日志
3. **超时控制**: 命令设置超时避免卡住
4. **资源清理**: 临时文件及时清理
5. **回滚测试**: 定期测试回滚方案

---

**Version**: 1.0
**Last Updated**: 2026-03-06
