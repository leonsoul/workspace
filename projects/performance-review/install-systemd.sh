#!/bin/bash
# 人员评价系统 - Systemd 服务安装脚本

set -e

SERVICE_NAME="performance-review"
SERVICE_FILE="${SERVICE_NAME}.service"
WORKDIR="/home/admin/.openclaw/workspace/projects/performance-review"
USER="admin"
LOG_DIR="/var/log/performance-review"

echo "=== 安装人员评价系统 Systemd 服务 ==="
echo ""

# 检查是否以 root 运行
if [ "$EUID" -ne 0 ]; then 
    echo "❌ 请使用 sudo 运行此脚本"
    echo "   sudo ./install-systemd.sh"
    exit 1
fi

# 创建日志目录
echo "📁 创建日志目录..."
mkdir -p "$LOG_DIR"
chown $USER:$USER "$LOG_DIR"

# 复制服务文件
echo "📋 复制服务文件..."
cp "$SERVICE_FILE" "/etc/systemd/system/$SERVICE_NAME.service"

# 重新加载 systemd
echo "🔄 重新加载 systemd 配置..."
systemctl daemon-reload

# 启用服务
echo "⚙️ 启用服务..."
systemctl enable $SERVICE_NAME

# 启动服务
echo "🚀 启动服务..."
systemctl start $SERVICE_NAME

# 等待服务启动
sleep 3

# 检查状态
echo ""
echo "=== 服务状态 ==="
systemctl status $SERVICE_NAME --no-pager

echo ""
echo "=== 安装完成 ==="
echo ""
echo "常用命令:"
echo "  查看状态：sudo systemctl status $SERVICE_NAME"
echo "  查看日志：sudo journalctl -u $SERVICE_NAME -f"
echo "  重启服务：sudo systemctl restart $SERVICE_NAME"
echo "  停止服务：sudo systemctl stop $SERVICE_NAME"
echo ""

# 测试服务
echo "🧪 测试服务..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 --max-time 5)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ 服务运行正常 (HTTP $HTTP_CODE)"
else
    echo "⚠️  服务响应异常 (HTTP $HTTP_CODE)"
    echo "   请查看日志：sudo journalctl -u $SERVICE_NAME -n 50"
fi
