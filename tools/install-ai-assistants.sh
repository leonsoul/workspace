#!/bin/bash
#
# ClawOS AI 代码助手安装脚本
# 一键安装 Codex 替代方案
#

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

show_banner() {
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║         ClawOS AI 代码助手安装脚本                         ║
║              Codex 替代方案一键安装                        ║
╚═══════════════════════════════════════════════════════════╝

EOF
}

show_menu() {
    cat << 'EOF'
请选择要安装的方案:

  1) Aider (推荐) ⭐⭐⭐⭐⭐
     - 最接近 Codex 的体验
     - Git 自动集成
     - 支持多种模型
     - 成本：API Key (GPT-3.5 很便宜)

  2) Ollama 本地模型 🆓
     - 完全免费
     - 本地运行，隐私保护
     - 需要 GPU (8GB+ 显存)
     - 成本：免费

  3) OpenAI SDK (轻量) ⭐⭐⭐⭐
     - 已有 Python SDK
     - 简单灵活
     - 成本：API Key

  4) 全部安装
     - 安装所有方案
     - 根据需要选择使用

  0) 退出

EOF
}

install_aider() {
    log_step "安装 Aider..."
    
    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装"
        return 1
    fi
    
    # 安装
    pip3 install aider-chat --quiet
    
    # 验证
    if command -v aider &> /dev/null; then
        log_info "✅ Aider 安装成功"
        echo ""
        echo "使用示例:"
        echo "  aider --model gpt-3.5-turbo \"Hello\""
        echo "  aider --model gpt-4 \"复杂任务\""
        echo ""
        return 0
    else
        log_error "❌ Aider 安装失败"
        return 1
    fi
}

install_ollama() {
    log_step "安装 Ollama..."
    
    # 检查是否已安装
    if command -v ollama &> /dev/null; then
        log_info "Ollama 已安装"
    else
        # 下载安装
        curl -fsSL https://ollama.com/install.sh | sh
        
        if command -v ollama &> /dev/null; then
            log_info "✅ Ollama 安装成功"
        else
            log_error "❌ Ollama 安装失败"
            return 1
        fi
    fi
    
    # 拉取推荐模型
    echo ""
    log_info "拉取推荐模型..."
    
    models=("deepseek-coder:6.7b" "codellama:7b" "llama2:7b")
    
    for model in "${models[@]}"; do
        echo ""
        log_info "拉取 $model ..."
        ollama pull "$model" || log_warn "模型 $model 拉取失败，跳过"
    done
    
    echo ""
    echo "使用示例:"
    echo "  ollama run deepseek-coder:6.7b \"写个快速排序\""
    echo "  ollama run codellama:7b \"解释这段代码\""
    echo ""
    
    return 0
}

install_openai_sdk() {
    log_step "安装 OpenAI SDK..."
    
    # 检查是否已安装
    if python3 -c "import openai" 2>/dev/null; then
        log_info "OpenAI SDK 已安装"
    else
        pip3 install openai --quiet
        
        if python3 -c "import openai" 2>/dev/null; then
            log_info "✅ OpenAI SDK 安装成功"
        else
            log_error "❌ OpenAI SDK 安装失败"
            return 1
        fi
    fi
    
    # 复制工具脚本
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    WORKSPACE="/home/admin/.openclaw/workspace"
    
    if [ -f "$WORKSPACE/tools/codegen.py" ]; then
        log_info "✅ 代码生成器已就绪：$WORKSPACE/tools/codegen.py"
        echo ""
        echo "使用示例:"
        echo "  python $WORKSPACE/tools/codegen.py \"写个快速排序\""
        echo "  python $WORKSPACE/tools/codegen.py -m gpt-4 \"复杂任务\""
        echo "  python $WORKSPACE/tools/codegen.py -o output.py \"生成脚本\""
        echo ""
    fi
    
    return 0
}

install_all() {
    log_info "安装所有方案..."
    echo ""
    
    install_aider
    echo ""
    
    install_ollama
    echo ""
    
    install_openai_sdk
    echo ""
    
    log_info "✅ 所有方案安装完成!"
    
    show_summary
}

show_summary() {
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║                    安装完成总结                            ║
╚═══════════════════════════════════════════════════════════╝

已安装工具:
  ✅ Aider          - CLI 代码助手 (推荐)
  ✅ Ollama         - 本地模型 (免费)
  ✅ OpenAI SDK     - Python 集成 (轻量)

快速开始:

  1. Aider (推荐用于日常开发)
     aider --model gpt-3.5-turbo "任务描述"

  2. Ollama (免费，隐私保护)
     ollama run deepseek-coder:6.7b "任务描述"

  3. OpenAI SDK (Python 集成)
     python tools/codegen.py "任务描述"

配置 API Key:

  编辑 ~/.bashrc 添加:
  export OPENAI_API_KEY="sk-proj-xxx"

  然后运行:
  source ~/.bashrc

详细文档:
  tools/CODEX_ALTERNATIVES.md

EOF
}

# 主流程
main() {
    show_banner
    
    # 检查是否非交互式调用
    if [ -n "$1" ]; then
        case "$1" in
            1|aider)
                install_aider
                ;;
            2|ollama)
                install_ollama
                ;;
            3|openai)
                install_openai_sdk
                ;;
            4|all)
                install_all
                ;;
            *)
                log_error "未知选项：$1"
                show_menu
                exit 1
                ;;
        esac
        exit 0
    fi
    
    # 交互式菜单
    while true; do
        show_menu
        read -p "请选择 [0-4]: " choice
        
        case $choice in
            1)
                install_aider
                ;;
            2)
                install_ollama
                ;;
            3)
                install_openai_sdk
                ;;
            4)
                install_all
                ;;
            0)
                log_info "退出安装"
                exit 0
                ;;
            *)
                log_error "无效选择，请重试"
                ;;
        esac
        
        echo ""
        read -p "继续安装其他方案？[y/N]: " cont
        if [[ ! "$cont" =~ ^[Yy]$ ]]; then
            break
        fi
        echo ""
    done
    
    show_summary
}

main "$@"
