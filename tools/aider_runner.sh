#!/bin/bash
#
# ClawOS Aider 执行器
# Codex 替代方案 - 使用 Aider 进行 AI 代码生成
#
# 安装：pip install aider-chat
# 使用：./aider_runner.sh "任务描述"
#

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/admin/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs/aider"
MODEL="${AIDER_MODEL:-gpt-3.5-turbo}"  # 默认使用便宜模型

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 显示帮助
show_help() {
    cat << EOF
ClawOS Aider 执行器 (Codex 替代方案)

用法：$0 [选项] <任务描述>

选项:
    -m, --model <MODEL>     模型 (默认：gpt-3.5-turbo)
    -p, --project <PATH>    项目根目录 (默认：$WORKSPACE)
    -n, --no-commit         禁用自动提交
    -d, --dry-run           干运行（不实际执行）
    -v, --verbose           详细输出
    -h, --help              显示帮助

可用模型:
    gpt-3.5-turbo           便宜，适合简单任务 (推荐)
    gpt-4                   高质量，适合复杂任务
    gpt-4-turbo             最新 GPT-4
    claude-3-sonnet         Anthropic Claude
    claude-3-opus           Claude 最强模型
    ollama/codellama        本地 Ollama (免费)

示例:
    $0 "修复人员评价系统的 average_score 错误"
    $0 -m gpt-4 "重构数据库连接管理"
    $0 -m ollama/codellama "写个快速排序算法"
    $0 -n "添加单元测试"  # 不自动提交

EOF
}

# 解析参数
PROJECT="$WORKSPACE"
NO_COMMIT=""
DRY_RUN=false
VERBOSE=false
TASK=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -p|--project)
            PROJECT="$2"
            shift 2
            ;;
        -n|--no-commit)
            NO_COMMIT="--no-auto-commits"
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            TASK="$1"
            shift
            ;;
    esac
done

# 验证参数
if [ -z "$TASK" ]; then
    log_error "任务描述不能为空"
    show_help
    exit 1
fi

if [ ! -d "$PROJECT" ]; then
    log_error "项目目录不存在：$PROJECT"
    exit 1
fi

# 检查 Aider 是否安装
if ! command -v aider &> /dev/null; then
    log_error "Aider 未安装"
    echo ""
    echo "请运行以下命令安装:"
    echo "  pip install aider-chat"
    echo ""
    echo "或使用其他替代方案，参考：tools/CODEX_ALTERNATIVES.md"
    exit 1
fi

# 检查 API Key
if [[ "$MODEL" != ollama/* ]]; then
    if [ -z "$OPENAI_API_KEY" ] && [[ "$MODEL" != claude-* ]]; then
        log_error "未设置 OPENAI_API_KEY 环境变量"
        exit 1
    fi
fi

# 构建 Aider 命令
build_aider_command() {
    local cmd="aider"
    
    # 模型
    cmd="$cmd --model $MODEL"
    
    # 项目目录
    cmd="$cmd --cd $PROJECT"
    
    # 自动提交 (除非禁用)
    if [ -z "$NO_COMMIT" ]; then
        cmd="$cmd --auto-commits --dirty-commits"
    fi
    
    # 详细输出
    if [ "$VERBOSE" = true ]; then
        cmd="$cmd --verbose"
    fi
    
    # 其他配置
    cmd="$cmd --attribute-author --attribute-committer"
    
    # 消息
    cmd="$cmd --message \"$TASK\""
    
    echo "$cmd"
}

# 执行 Aider
execute_aider() {
    local cmd="$1"
    
    log_info "========================================="
    log_info "ClawOS Aider 执行器"
    log_info "========================================="
    log_info "模型：$MODEL"
    log_info "项目：$PROJECT"
    log_info "任务：$TASK"
    log_info "自动提交：$([ -z "$NO_COMMIT" ] && echo "启用" || echo "禁用")"
    log_info "========================================="
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[干运行] 跳过实际执行"
        log_info "命令：$cmd"
        return 0
    fi
    
    # 执行
    local start_time=$(date +%s)
    local log_file="$LOG_DIR/aider_$(date +%Y%m%d_%H%M%S).log"
    
    log_info "执行中..."
    log_info "日志：$log_file"
    echo ""
    
    if [ "$VERBOSE" = true ]; then
        eval "$cmd" 2>&1 | tee "$log_file"
        local exit_code=${PIPESTATUS[0]}
    else
        eval "$cmd" > "$log_file" 2>&1
        local exit_code=$?
    fi
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    echo ""
    log_info "========================================="
    
    # 检查结果
    if [ $exit_code -eq 0 ]; then
        log_info "✅ Aider 任务完成（耗时：${duration}s）"
        log_info "日志：$log_file"
        
        # 显示 Git 状态
        if [ -z "$NO_COMMIT" ]; then
            echo ""
            log_info "Git 变更:"
            cd "$PROJECT" && git log --oneline -3 2>/dev/null || true
        fi
        
        return 0
    else
        log_error "❌ Aider 任务失败（退出码：$exit_code）"
        log_error "日志：$log_file"
        return $exit_code
    fi
}

# 主流程
main() {
    # 构建命令
    local cmd=$(build_aider_command)
    
    if [ "$VERBOSE" = true ]; then
        log_debug "命令：$cmd"
        echo ""
    fi
    
    # 执行
    execute_aider "$cmd"
    exit $?
}

# 运行
main
