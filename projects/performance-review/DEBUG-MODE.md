# 服务不稳定问题深入分析

---

## 现象

服务频繁停止，需要不断重启

---

## 可能原因

### 1. 内存泄漏
**检查**: 
```bash
ps aux | grep python3
# 观察内存使用是否持续增长
```

**解决**: 使用 gunicorn 替代 Flask 开发服务器

### 2. 异常未捕获
**检查**:
```bash
tail -100 /tmp/performance-review.log | grep -i error
```

**解决**: 添加全局异常处理

### 3. 资源耗尽
**检查**:
```bash
ulimit -n  # 文件描述符限制
free -h    # 内存
df -h      # 磁盘
```

**解决**: 优化资源使用

### 4. Flask 开发服务器限制
**问题**: Flask 内置服务器不适合生产
**解决**: 使用 gunicorn/uwsgi

---

## 立即修复：使用 Gunicorn

### 安装
```bash
pip3 install gunicorn --user
```

### 启动
```bash
cd /home/admin/.openclaw/workspace/projects/performance-review
nohup gunicorn -w 2 -b 0.0.0.0:5000 app:app > /tmp/performance-review.log 2>&1 &
```

### 配置 systemd
```ini
[Service]
ExecStart=/home/admin/.local/bin/gunicorn -w 2 -b 0.0.0.0:5000 app:app
Restart=always
```

---

## 监控改进

### 添加内存监控
```bash
# 在 monitor.sh 中添加
MEM_USAGE=$(ps -o rss= -p $(pgrep -f "python3 app.py") 2>/dev/null || echo 0)
echo "内存使用：$((MEM_USAGE/1024)) MB"
```

### 添加进程监控
```bash
# 检查进程是否存在
if ! pgrep -f "python3 app.py" > /dev/null; then
    echo "进程不存在，重启"
fi
```

---

## 日志分析

添加详细日志：
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/performance-review.log'),
        logging.StreamHandler()
    ]
)
```

---

**下一步**: 安装 gunicorn，替换 Flask 开发服务器！
