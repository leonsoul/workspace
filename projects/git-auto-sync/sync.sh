#!/bin/bash
# Git Auto-Sync Script
# 自动检测变更并提交推送到 GitHub
# 用法：./sync.sh [commit_message]

set -e

# 配置
WORKSPACE="/home/admin/.openclaw/workspace"
LOG_FILE="$WORKSPACE/projects/git-auto-sync/sync.log"
MAX_FILES_PER_COMMIT=50

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cd "$WORKSPACE"

log "${GREEN}=== Git Auto-Sync 开始 ===${NC}"

# 检查 git 状态
STATUS=$(git status --porcelain 2>&1)

if [ -z "$STATUS" ]; then
    log "${YELLOW}✓ 没有变更，跳过同步${NC}"
    exit 0
fi

# 显示变更文件
CHANGED_COUNT=$(echo "$STATUS" | wc -l)
log "${YELLOW}发现 $CHANGED_COUNT 个变更文件:${NC}"
echo "$STATUS" | head -20

if [ "$CHANGED_COUNT" -gt 20 ]; then
    log "... 等 $((CHANGED_COUNT - 20)) 个文件"
fi

# 添加所有变更
git add -A
log "✓ 已添加所有变更"

# 提交
COMMIT_MSG="${1:-auto-sync: $(date '+%Y-%m-%d %H:%M') - $CHANGED_COUNT files changed}"
git commit -m "$COMMIT_MSG"
log "✓ 已提交：$COMMIT_MSG"

# 推送
log "正在推送到 GitHub..."
PUSH_OUTPUT=$(git push origin master 2>&1) || {
    log "${RED}✗ 推送失败，请检查 SSH 密钥和远程仓库配置${NC}"
    log "$PUSH_OUTPUT"
    exit 1
}
echo "$PUSH_OUTPUT" | tee -a "$LOG_FILE"
log "${GREEN}✓ 推送成功！${NC}"

log "${GREEN}=== Git Auto-Sync 完成 ===${NC}"
