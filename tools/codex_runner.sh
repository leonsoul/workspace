#!/bin/bash
#
# ClawOS Codex 执行器
# 用于在 ClawOS 工作流中调用 Codex
#

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/admin/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs/codex"
OUTPUT_FILE="/tmp/codex_result_$(date +%s).json"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 显示帮助
show_help() {
    cat << EOF
ClawOS Codex 执行器

用法：$0 [选项] <任务描述>

选项:
    -m, --mode <MODE>       执行模式 (fix|testgen|refactor|exec)
    -p, --project <PATH>    项目根目录 (默认：$WORKSPACE)
    -o, --output <FILE>     输出文件 (默认：自动生成)
    -t, --timeout <SECONDS> 超时时间 (默认：1800)
    -d, --dry-run           干运行（不实际执行）
    -v, --verbose           详细输出
    -h, --help              显示帮助

模式说明:
    fix       修复 Bug
    testgen   生成测试
    refactor  代码重构
    exec      通用执行

示例:
    $0 -m fix "修复人员评价系统的 average_score 错误"
    $0 -m testgen -p /path/to/project "为 utils 目录生成单元测试"
    $0 -m refactor "优化数据库连接管理"

EOF
}

# 解析参数
MODE="exec"
PROJECT="$WORKSPACE"
TIMEOUT=1800
DRY_RUN=false
VERBOSE=false
TASK=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--mode)
            MODE="$2"
            shift 2
            ;;
        -p|--project)
            PROJECT="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -t|--timeout)
            TIMEOUT="$2"
            shift 2
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

# 检查 Codex 是否安装
if ! command -v codex &> /dev/null; then
    log_error "Codex CLI 未安装，请先运行：npm install -g @openai/codex"
    exit 1
fi

# 检查登录状态
if ! codex login status &> /dev/null; then
    log_warn "Codex 未登录，尝试使用环境变量..."
    if [ -z "$OPENAI_API_KEY" ]; then
        log_error "未设置 OPENAI_API_KEY 环境变量"
        exit 1
    fi
fi

# 构建提示
build_prompt() {
    local mode="$1"
    local task="$2"
    local project="$3"
    
    local description=""
    case $mode in
        fix)
            description="修复问题并确保行为不回归"
            ;;
        testgen)
            description="补充或改进自动化测试"
            ;;
        refactor)
            description="在不改变行为前提下重构代码结构"
            ;;
        exec)
            description="执行代码任务"
            ;;
    esac
    
    cat << EOF
你是资深工程师，请在项目中${description}。

项目路径：${project}
任务：${task}

要求:
1) 优先做最小必要改动，避免影响无关模块。
2) 变更后运行最小可行验证（测试或静态检查）。
3) 输出结果包含：修改文件、关键改动、验证结果。
EOF
}

# 执行 Codex
execute_codex() {
    local prompt="$1"
    local project="$2"
    local output="$3"
    local timeout="$4"
    
    log_info "执行 Codex 任务..."
    log_info "模式：$MODE"
    log_info "项目：$project"
    log_info "任务：$TASK"
    log_info "超时：${timeout}s"
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[干运行] 跳过实际执行"
        return 0
    fi
    
    # 构建命令
    local cmd="timeout ${timeout} codex exec --full-auto -C ${project} --output-last-message ${output} --sandbox workspace-write"
    
    if [ "$VERBOSE" = true ]; then
        log_info "命令：$cmd"
    fi
    
    # 执行
    local start_time=$(date +%s)
    
    if [ "$VERBOSE" = true ]; then
        eval "$cmd" "$prompt" 2>&1 | tee "$LOG_DIR/codex_$(date +%Y%m%d_%H%M%S).log"
        local exit_code=${PIPESTATUS[0]}
    else
        eval "$cmd" "$prompt" > "$LOG_DIR/codex_$(date +%Y%m%d_%H%M%S).log" 2>&1
        local exit_code=$?
    fi
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    # 检查结果
    if [ $exit_code -eq 0 ]; then
        log_info "✅ Codex 任务完成（耗时：${duration}s）"
        
        # 输出结果
        if [ -f "$output" ]; then
            echo ""
            log_info "执行结果:"
            cat "$output"
        fi
        
        return 0
    elif [ $exit_code -eq 124 ]; then
        log_error "❌ Codex 任务超时（${timeout}s）"
        return 124
    else
        log_error "❌ Codex 任务失败（退出码：$exit_code）"
        log_error "日志：$LOG_DIR/codex_$(date +%Y%m%d_%H%M%S).log"
        return $exit_code
    fi
}

# 主流程
main() {
    log_info "========================================="
    log_info "ClawOS Codex 执行器"
    log_info "========================================="
    
    # 构建提示
    local prompt=$(build_prompt "$MODE" "$TASK" "$PROJECT")
    
    if [ "$VERBOSE" = true ]; then
        log_info "提示词:"
        echo "$prompt"
        echo ""
    fi
    
    # 执行
    execute_codex "$prompt" "$PROJECT" "$OUTPUT_FILE" "$TIMEOUT"
    local result=$?
    
    # 输出 JSON 结果（便于程序解析）
    if [ -f "$OUTPUT_FILE" ]; then
        echo ""
        echo "JSON 输出:"
        cat "$OUTPUT_FILE"
    fi
    
    exit $result
}

# 运行
main
