#!/usr/bin/env python3
"""
ClawOS 简易代码生成器 (Codex 替代方案)

使用 OpenAI SDK 直接调用，轻量级替代 Codex CLI

用法:
    python codegen.py "写个快速排序算法"
    python codegen.py -m gpt-4 "重构数据库连接"
    python codegen.py --model gpt-3.5-turbo --output code.py "生成 Python 脚本"
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("错误：缺少 openai 库，请运行：pip install openai")
    sys.exit(1)


def get_api_key():
    """获取 API Key"""
    # 1. 环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    # 2. 从 .env.codex 读取
    env_file = Path.home() / ".openclaw" / "workspace" / ".env.codex"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("export OPENAI_API_KEY="):
                return line.split("=", 1)[1].strip('"')
    
    # 3. 从 ~/.codex/config.toml 读取
    config_file = Path.home() / ".codex" / "config.toml"
    if config_file.exists():
        content = config_file.read_text()
        for line in content.splitlines():
            if "api_key" in line and "=" in line:
                return line.split("=", 1)[1].strip('"')
    
    return None


def generate_code(prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=2000):
    """生成代码"""
    api_key = get_api_key()
    if not api_key:
        raise ValueError("未找到 API Key，请设置 OPENAI_API_KEY 环境变量")
    
    client = OpenAI(api_key=api_key)
    
    system_prompt = """你是专业的 Python 工程师。
请根据用户要求生成高质量、可运行的代码。
要求:
1. 代码完整、可运行
2. 添加必要的注释
3. 遵循最佳实践
4. 如有依赖，在开头说明"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False
    )
    
    return {
        "success": True,
        "code": response.choices[0].message.content,
        "model": model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        },
        "timestamp": datetime.now().isoformat()
    }


def save_output(code, output_file):
    """保存输出到文件"""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(code, encoding='utf-8')
    print(f"✅ 代码已保存到：{output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="ClawOS 简易代码生成器 (Codex 替代)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "写个快速排序算法"
  %(prog)s -m gpt-4 "重构数据库连接"
  %(prog)s --model gpt-3.5-turbo --output code.py "生成 Python 脚本"
  %(prog)s --json "写个 API 调用示例"

可用模型:
  gpt-3.5-turbo    便宜，适合简单任务 (推荐)
  gpt-4            高质量，适合复杂任务
  gpt-4-turbo      最新 GPT-4
  gpt-4o           多模态模型
        """
    )
    
    parser.add_argument(
        "prompt",
        nargs="?",
        help="任务描述"
    )
    
    parser.add_argument(
        "-m", "--model",
        default="gpt-3.5-turbo",
        help="模型 (默认：gpt-3.5-turbo)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="输出文件路径"
    )
    
    parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=0.7,
        help="温度 (默认：0.7)"
    )
    
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2000,
        help="最大 token 数 (默认：2000)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="详细输出"
    )
    
    args = parser.parse_args()
    
    # 验证参数
    if not args.prompt:
        parser.print_help()
        sys.exit(1)
    
    # 生成代码
    try:
        if args.verbose:
            print(f"🤖 使用模型：{args.model}")
            print(f"📝 任务：{args.prompt}")
            print()
        
        result = generate_code(
            prompt=args.prompt,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
        
        # 输出
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.output:
            save_output(result["code"], args.output)
            if args.verbose:
                print()
                print("📊 使用统计:")
                print(f"   Prompt tokens: {result['usage']['prompt_tokens']}")
                print(f"   Completion tokens: {result['usage']['completion_tokens']}")
                print(f"   Total tokens: {result['usage']['total_tokens']}")
        else:
            print(result["code"])
            if args.verbose:
                print()
                print("📊 使用统计:")
                print(f"   Total tokens: {result['usage']['total_tokens']}")
        
        return 0
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        
        if args.json:
            print(json.dumps(error_result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 错误：{e}", file=sys.stderr)
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
