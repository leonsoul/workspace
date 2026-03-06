#!/bin/bash
# 人员评价系统监控脚本
# 检查服务状态，自动重启

SERVICE_NAME="python3 app.py"
PORT=5000
LOG_FILE="/tmp/performance-review.log"
WORKDIR="/home/admin/.openclaw/workspace/projects/performance-review"

echo "=== 检查人员评价系统 ==="
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"

# 检查进程
if ! pgrep -f "$SERVICE_NAME" > /dev/null; then
    echo "❌ 服务未运行，正在重启..."
    cd "$WORKDIR"
    nohup python3 app.py > "$LOG_FILE" 2>&1 &
    sleep 3
    echo "✅ 服务已重启"
else
    echo "✅ 服务运行中"
fi

# 检查端口
if ! (netstat -tlnp 2>/dev/null | grep -q ":$PORT " || ss -tlnp 2>/dev/null | grep -q ":$PORT "); then
    echo "❌ 端口 $PORT 未监听"
else
    echo "✅ 端口 $PORT 正常"
fi

# 检查 HTTP 响应
HTTP_CODE=$(curl -s http://localhost:$PORT -o /dev/null -w "%{http_code}" --max-time 5)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ HTTP 响应正常 ($HTTP_CODE)"
else
    echo "❌ HTTP 响应异常 ($HTTP_CODE)"
fi

# 检查日志错误
ERROR_COUNT=$(tail -100 "$LOG_FILE" 2>/dev/null | grep -c -i "error" || echo 0)
if [ "$ERROR_COUNT" -gt 0 ]; then
    echo "⚠️ 发现 $ERROR_COUNT 条错误日志"
    tail -20 "$LOG_FILE" | grep -i "error" | tail -5
else
    echo "✅ 无错误日志"
fi

echo "=== 检查完成 ==="
