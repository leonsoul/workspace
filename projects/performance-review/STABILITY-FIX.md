# 服务稳定性修复

---

## 问题现象

用户反馈："为什么你总离线啊"

---

## 根因分析

### 1. Flask Debug 模式自动重启
**问题**: `app.run(debug=True)`
**现象**: 代码/配置变化时自动重启，重启瞬间服务不可用
**解决**: 关闭 debug 模式

### 2. 健康检查间隔过长
**问题**: 5 分钟检查一次
**现象**: 服务挂了最多要等 5 分钟才发现
**解决**: 缩短到 1 分钟

### 3. 无守护进程管理
**问题**: 只用 nohup 后台运行
**现象**: 进程意外退出不会立即恢复
**解决**: 使用 systemd 管理（推荐）

---

## 已实施的修复

### 修复 1：关闭 Debug 模式
```python
# app.py
app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
```

**效果**: 
- ✅ 不再自动重启
- ✅ 性能提升
- ✅ 更稳定

### 修复 2：缩短健康检查间隔
```python
# health-check.py
'check_interval': 60,  # 1 分钟检查一次
'max_retries': 2
```

**效果**:
- ✅ 更快发现问题
- ✅ 更快自动恢复

### 修复 3：Systemd 服务配置
创建 `performance-review.service`:
```ini
[Service]
Restart=always
RestartSec=5
```

**效果**:
- ✅ 系统启动自动运行
- ✅ 进程崩溃自动重启
- ✅ 日志统一管理

---

## 使用方法

### 方式 1：Systemd（推荐）
```bash
# 复制服务文件
sudo cp performance-review.service /etc/systemd/system/

# 启用并启动
sudo systemctl daemon-reload
sudo systemctl enable performance-review
sudo systemctl start performance-review

# 查看状态
sudo systemctl status performance-review

# 查看日志
sudo journalctl -u performance-review -f
```

### 方式 2：手动启动
```bash
# 停止旧进程
pkill -f "python3 app.py"
pkill -f "health-check.py"

# 启动服务
cd /home/admin/.openclaw/workspace/projects/performance-review
nohup python3 app.py > /tmp/performance-review.log 2>&1 &

# 启动健康检查
nohup python3 health-check.py > /tmp/health-check.log 2>&1 &

# 查看状态
ps aux | grep python3
curl http://localhost:5000
```

---

## 监控命令

```bash
# 检查进程
ps aux | grep -E "python3.*app.py|health-check" | grep -v grep

# 检查端口
netstat -tlnp | grep 5000

# 检查 HTTP
curl -s http://localhost:5000 -o /dev/null -w "%{http_code}"

# 查看日志
tail -f /tmp/performance-review.log

# 查看健康检查
tail -f /tmp/health-check.log
```

---

## 预期效果

修复后：
- ✅ 服务持续运行，不再频繁重启
- ✅ 即使挂了，1 分钟内自动恢复
- ✅ 系统重启后自动启动（systemd）
- ✅ 有完整的日志记录

**可用性目标**: > 99%

---

## 后续优化

1. **使用 Gunicorn** (生产级 WSGI 服务器)
```bash
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **使用 Nginx 反向代理**
```nginx
location / {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

3. **添加性能监控**
- CPU 使用率
- 内存使用率
- 响应时间
- 请求数统计

---

**修复完成！服务会更稳定！** 🦞
