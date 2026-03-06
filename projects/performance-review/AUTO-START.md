# 自动启动和监控指南

---

## 服务启动方式

### 方式 1：手动启动
```bash
cd /home/admin/.openclaw/workspace/projects/performance-review
nohup python3 app.py > /tmp/performance-review.log 2>&1 &
```

### 方式 2：监控脚本（推荐）
```bash
bash monitor.sh
```
自动检查并重启服务

### 方式 3：健康检查守护进程
```bash
nohup python3 health-check.py > /tmp/health-check.log 2>&1 &
```
每 5 分钟检查一次，失败自动重启

---

## 开机自启动

### 方式 1：Cron (@reboot)

编辑 crontab：
```bash
crontab -e
```

添加：
```cron
@reboot cd /home/admin/.openclaw/workspace/projects/performance-review && nohup python3 app.py > /tmp/performance-review.log 2>&1 &
@reboot sleep 10 && nohup python3 /home/admin/.openclaw/workspace/projects/performance-review/health-check.py > /tmp/health-check.log 2>&1 &
```

### 方式 2：Systemd 服务

创建服务文件：
```bash
sudo nano /etc/systemd/system/performance-review.service
```

内容：
```ini
[Unit]
Description=Performance Review System
After=network.target

[Service]
Type=simple
User=admin
WorkingDirectory=/home/admin/.openclaw/workspace/projects/performance-review
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10
StandardOutput=append:/tmp/performance-review.log
StandardError=append:/tmp/performance-review.log

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable performance-review
sudo systemctl start performance-review
sudo systemctl status performance-review
```

### 方式 3：Supervisor

安装 supervisor：
```bash
sudo apt-get install supervisor
```

创建配置：
```bash
sudo nano /etc/supervisor/conf.d/performance-review.conf
```

内容：
```ini
[program:performance-review]
command=/usr/bin/python3 app.py
directory=/home/admin/.openclaw/workspace/projects/performance-review
user=admin
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/tmp/performance-review.log
```

启用：
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start performance-review
```

---

## 监控和告警

### 监控脚本

```bash
# 手动检查
bash monitor.sh

# 定时检查（每 5 分钟）
*/5 * * * * bash /home/admin/.openclaw/workspace/projects/performance-review/monitor.sh >> /tmp/monitor.log 2>&1
```

### 健康检查

健康检查脚本 (`health-check.py`) 会：
- 每 5 分钟检查服务
- 失败自动重启
- 连续失败 3 次发送钉钉告警
- 记录所有操作日志

### 查看日志

```bash
# 服务日志
tail -f /tmp/performance-review.log

# 健康检查日志
tail -f /tmp/health-check.log

# 监控日志
tail -f /tmp/monitor.log
```

---

## 故障排查

### 服务无法启动

```bash
# 检查端口占用
netstat -tlnp | grep 5000

# 检查 Python 版本
python3 --version

# 检查依赖
pip3 list | grep -i flask

# 手动启动看错误
cd /home/admin/.openclaw/workspace/projects/performance-review
python3 app.py
```

### 无法访问

```bash
# 检查防火墙
sudo ufw status

# 检查监听地址
netstat -tlnp | grep python

# 测试本地访问
curl http://localhost:5000

# 测试远程访问
curl http://47.88.19.149:5000
```

### 钉钉通知失败

检查：
1. Webhook 是否正确
2. 网络是否可达
3. 签名是否匹配

测试：
```bash
python3 test_dingtalk.py
```

---

## 最佳实践

1. **使用监控脚本**: 确保服务始终运行
2. **配置开机自启**: 服务器重启后自动恢复
3. **定期检查日志**: 及时发现和解决问题
4. **备份数据**: 定期备份 data/ 目录
5. **设置告警**: 故障时及时通知

---

**配置完成后，服务会自动运行和恢复！** 🎉
