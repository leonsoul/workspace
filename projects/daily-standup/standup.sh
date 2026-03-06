#!/bin/bash
# Daily Standup Bot
# 自动生成每日站会报告（昨日完成/今日计划）
# 用法：./standup.sh [output_format: text|markdown|json]

set -e

# 配置
WORKSPACE="/home/admin/.openclaw/workspace"
GIT_LOG="$WORKSPACE/projects/daily-standup/git-history.log"
OUTPUT_DIR="$WORKSPACE/projects/daily-standup/reports"
DATE=$(date '+%Y-%m-%d')
YESTERDAY=$(date -d "yesterday" '+%Y-%m-%d')

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

cd "$WORKSPACE"

# 颜色输出
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}=== 每日站会报告 ===${NC}"
echo -e "日期：$DATE"
echo ""

# 1. 获取昨日 git 提交
echo -e "${GREEN}📦 昨日完成 (Git 提交):${NC}"
echo "---"

COMMITS=$(git log --since="$YESTERDAY 00:00" --until="$DATE 00:00" --pretty=format:"  • %s" 2>/dev/null || echo "  无提交记录")

if [ "$COMMITS" = "  无提交记录" ] || [ -z "$COMMITS" ]; then
    # 尝试获取最近的提交（如果没有昨日的）
    COMMITS=$(git log -n 5 --pretty=format:"  • %s" 2>/dev/null || echo "  无提交记录")
    if [ "$COMMITS" = "  无提交记录" ] || [ -z "$COMMITS" ]; then
        echo "  暂无 Git 提交记录"
    else
        echo -e "${YELLOW}  (最近提交):${NC}"
        echo "$COMMITS"
    fi
else
    echo "$COMMITS"
fi

echo ""

# 2. 获取 learnings 更新
echo -e "${GREEN}🧠 学习记录 (.learnings):${NC}"
echo "---"

if [ -f "$WORKSPACE/.learnings/LEARNINGS.md" ]; then
    # 获取今天的学习记录
    TODAY_LEARNINGS=$(grep -A5 "$DATE" "$WORKSPACE/.learnings/LEARNINGS.md" 2>/dev/null | head -20 || echo "  无新增学习")
    if [ -z "$TODAY_LEARNINGS" ] || ! echo "$TODAY_LEARNINGS" | grep -q "## \[LRN"; then
        # 尝试获取最近的学习
        RECENT_LEARNINGS=$(grep "## \[LRN" "$WORKSPACE/.learnings/LEARNINGS.md" | head -5 || echo "  无学习记录")
        if [ -z "$RECENT_LEARNINGS" ]; then
            echo "  暂无学习记录"
        else
            echo -e "${YELLOW}  (最近学习):${NC}"
            echo "$RECENT_LEARNINGS" | sed 's/## /  /g'
        fi
    else
        echo "$TODAY_LEARNINGS" | grep -E "(^## |^### |^  )" | head -10
    fi
else
    echo "  无学习记录文件"
fi

echo ""

# 3. 获取错误记录
echo -e "${GREEN}⚠️ 错误记录 (Errors):${NC}"
echo "---"

if [ -f "$WORKSPACE/.learnings/ERRORS.md" ] && grep -q "## \[ERR" "$WORKSPACE/.learnings/ERRORS.md" 2>/dev/null; then
    RECENT_ERRORS=$(grep "## \[ERR" "$WORKSPACE/.learnings/ERRORS.md" | head -3 || echo "  无错误记录")
    echo "$RECENT_ERRORS" | sed 's/## /  /g'
else
    echo "  无错误记录"
fi

echo ""

# 4. 待办事项
echo -e "${GREEN}📋 待办事项 (SESSION-STATE.md):${NC}"
echo "---"

if [ -f "$WORKSPACE/SESSION-STATE.md" ] && grep -q "Pending" "$WORKSPACE/SESSION-STATE.md"; then
    # 提取 Pending 部分
    awk '/## Pending/,/^##/' "$WORKSPACE/SESSION-STATE.md" | grep -v "^##" | grep -v "^$" | head -10 || echo "  无待办事项"
else
    echo "  无待办事项"
fi

echo ""

# 5. 生成报告文件
REPORT_FILE="$OUTPUT_DIR/standup-$DATE.md"

cat > "$REPORT_FILE" << EOF
# 每日站会报告

**日期**: $DATE
**生成时间**: $(date '+%H:%M:%S')

---

## 昨日完成

$COMMITS

---

## 学习记录

$(cat "$WORKSPACE/.learnings/LEARNINGS.md" 2>/dev/null | grep "## \[LRN" | head -5 || echo "无")

---

## 待办事项

$(awk '/## Pending/,/^##/' "$WORKSPACE/SESSION-STATE.md" 2>/dev/null | grep -v "^##" | grep -v "^$" || echo "无")

---

*报告由 Daily Standup Bot 自动生成*
EOF

echo -e "${BLUE}📄 报告已保存：$REPORT_FILE${NC}"
echo ""
echo -e "${GREEN}=== 报告完成 ===${NC}"
