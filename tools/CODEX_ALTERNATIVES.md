# Codex 替代方案指南

> 💡 Codex API Key 配额超限？试试这些替代方案！

---

## 快速推荐

| 方案 | 成本 | 难度 | 推荐度 | 适用场景 |
|------|------|------|--------|----------|
| **Aider** | 💰 API Key | ⭐⭐ | ⭐⭐⭐⭐⭐ | CLI 代码助手 |
| **Ollama 本地** | 🆓 免费 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 隐私敏感 |
| **OpenAI SDK** | 💰 API Key | ⭐⭐ | ⭐⭐⭐⭐ | Python 集成 |
| **Claude Code** | 💰 API Key | ⭐⭐ | ⭐⭐⭐⭐ | 高质量代码 |
| **GitHub Copilot** | 💳 订阅 | ⭐ | ⭐⭐⭐ | IDE 集成 |

---

## 方案 1: Aider ⭐⭐⭐⭐⭐ (强烈推荐)

**最接近 Codex 的开源替代品**

### 特点
- 🚀 支持多种模型 (GPT-4, Claude, Llama 等)
- 🛠️ Git 自动提交
- 📝 代码编辑能力强
- 🆓 开源免费 (只需 API Key)

### 安装
```bash
pip install aider-chat
```

### 使用
```bash
# 基础使用
aider

# 指定模型
aider --model gpt-4

# 使用 Claude
aider --model claude-3-sonnet

# 使用本地模型
aider --model ollama/llama2
```

### 示例
```bash
cd /home/admin/.openclaw/workspace

# 修复 Bug
aider --message "修复人员评价系统的 average_score 计算错误"

# 添加功能
aider --message "为人员评价系统添加 Excel 导出功能"

# 代码重构
aider --message "优化数据库连接管理，添加连接池"
```

### 配置
```bash
# ~/.aider.conf.yml
model: gpt-4
auto-commits: true
dirty-commits: true
attribute-author: true
attribute-committer: true
```

### 优势
- ✅ Git 集成好 (自动 commit)
- ✅ 支持多种模型
- ✅ 代码编辑能力强
- ✅ 活跃维护

### 劣势
- ❌ 需要 API Key (但可选择便宜模型)
- ❌ 本地模型需要 GPU

---

## 方案 2: Ollama 本地运行 🆓

**完全免费，隐私保护**

### 特点
- 🆓 完全免费
- 🔒 本地运行，隐私保护
- 🖥️ 支持多种开源模型
- ⚡ 快速响应

### 安装
```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull codellama:7b
ollama pull llama2
ollama pull deepseek-coder:6.7b
```

### 使用
```bash
# 运行模型
ollama run codellama:7b "写个快速排序算法"

# API 调用
curl http://localhost:11434/api/generate -d '{
  "model": "codellama",
  "prompt": "写个 Python 脚本计算斐波那契数列"
}'
```

### Python 集成
```python
import requests

def generate_code(prompt):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'codellama',
            'prompt': prompt,
            'stream': False
        }
    )
    return response.json()['response']

code = generate_code("写个快速排序算法")
print(code)
```

### 推荐模型
| 模型 | 大小 | 代码能力 | 推荐度 |
|------|------|----------|--------|
| CodeLlama:7b | 7B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| DeepSeek-Coder:6.7b | 6.7B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Llama2:7b | 7B | ⭐⭐⭐ | ⭐⭐⭐ |
| StarCoder:7b | 7B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

### 优势
- ✅ 完全免费
- ✅ 隐私保护
- ✅ 无需网络
- ✅ 可定制

### 劣势
- ❌ 需要 GPU (至少 8GB 显存)
- ❌ 代码能力不如 GPT-4
- ❌ 模型下载大

---

## 方案 3: OpenAI SDK 直接调用

**已有 SDK，直接使用**

### 特点
- ✅ 已有 Python SDK
- ✅ 支持多种模型
- ✅ 灵活控制

### 使用
```python
from openai import OpenAI

client = OpenAI(api_key="sk-proj-xxx")

# 代码生成
response = client.chat.completions.create(
    model="gpt-4",  # 或 gpt-3.5-turbo (便宜)
    messages=[
        {"role": "system", "content": "你是专业的 Python 工程师"},
        {"role": "user", "content": "写个快速排序算法"}
    ]
)

print(response.choices[0].message.content)
```

### 包装脚本
```python
#!/usr/bin/env python3
"""
简易代码生成器 (Codex 替代)
"""

from openai import OpenAI
import sys

def generate_code(prompt, model="gpt-3.5-turbo"):
    client = OpenAI(api_key="sk-proj-xxx")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是专业的 Python 工程师"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python codegen.py '任务描述'")
        sys.exit(1)
    
    prompt = " ".join(sys.argv[1:])
    code = generate_code(prompt)
    print(code)
```

### 优势
- ✅ 已有 SDK
- ✅ 简单灵活
- ✅ 可选择便宜模型 (gpt-3.5-turbo)

### 劣势
- ❌ 需要 API Key
- ❌ 没有 Git 集成
- ❌ 需要自己包装

---

## 方案 4: Claude Code (Anthropic)

**高质量代码生成**

### 特点
- 🎯 代码质量高
- 📝 理解能力强
- 🔒 安全性好

### 安装
```bash
pip install anthropic
```

### 使用
```python
from anthropic import Anthropic

client = Anthropic(api_key="sk-ant-xxx")

response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=2000,
    messages=[
        {"role": "user", "content": "写个快速排序算法"}
    ]
)

print(response.content[0].text)
```

### 优势
- ✅ 代码质量高
- ✅ 理解能力强
- ✅ 安全性好

### 劣势
- ❌ 需要 API Key
- ❌ 价格较贵
- ❌ 国内访问受限

---

## 方案 5: GitHub Copilot

**IDE 集成最佳**

### 特点
- 💻 VSCode/JetBrains 集成
- ⚡ 实时补全
- 🎯 代码理解好

### 安装
1. 订阅 GitHub Copilot ($10/月)
2. 安装 VSCode 插件
3. 登录 GitHub 账号

### 优势
- ✅ IDE 集成好
- ✅ 实时补全
- ✅ 代码质量高

### 劣势
- ❌ 需要订阅
- ❌ 仅限 IDE
- ❌ 无 CLI

---

## 综合对比

| 特性 | Aider | Ollama | OpenAI SDK | Claude | Copilot |
|------|-------|--------|-----------|--------|---------|
| 成本 | 💰 | 🆓 | 💰 | 💰💰 | 💳 |
| 代码质量 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 易用性 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Git 集成 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 隐私保护 | ❌ | ✅ | ❌ | ❌ | ❌ |
| 离线使用 | ❌ | ✅ | ❌ | ❌ | ❌ |

---

## 推荐方案

### 🏆 最佳选择：Aider

**理由**:
1. 最接近 Codex 的体验
2. Git 自动集成
3. 支持多种模型 (可切换便宜模型)
4. 开源活跃维护

**快速开始**:
```bash
# 安装
pip install aider-chat

# 配置 API Key
export OPENAI_API_KEY="sk-proj-xxx"

# 使用
aider --model gpt-3.5-turbo "修复这个 Bug"
```

---

### 🆓 免费选择：Ollama + DeepSeek-Coder

**理由**:
1. 完全免费
2. 本地运行
3. 隐私保护
4. 代码能力不错

**快速开始**:
```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull deepseek-coder:6.7b

# 使用
ollama run deepseek-coder:6.7b "写个快速排序"
```

---

### 💰 经济选择：OpenAI SDK + GPT-3.5

**理由**:
1. 已有 SDK
2. GPT-3.5 便宜
3. 灵活控制

**快速开始**:
```bash
# 创建脚本
cat > codegen.py << 'EOF'
from openai import OpenAI
import sys

client = OpenAI(api_key="sk-proj-xxx")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": " ".join(sys.argv[1:])}]
)
print(response.choices[0].message.content)
EOF

# 使用
python codegen.py "写个快速排序"
```

---

## ClawOS 集成方案

### 方案 A: Aider 集成

```bash
#!/bin/bash
# aider_runner.sh

cd /home/admin/.openclaw/workspace

# 执行任务
aider \
  --model gpt-3.5-turbo \
  --auto-commits \
  --message "$1" \
  2>&1 | tee /var/log/aider.log

# 钉钉通知
dingtalk-notify "✅ Aider 任务完成：$1"
```

### 方案 B: Ollama 集成

```python
#!/usr/bin/env python3
# ollama_runner.py

import requests
import sys
import subprocess

def generate_code(prompt):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'deepseek-coder:6.7b',
            'prompt': prompt,
            'stream': False
        }
    )
    return response.json()['response']

if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:])
    code = generate_code(prompt)
    print(code)
    
    # 可选：自动执行代码
    # subprocess.run(['python', '-c', code])
```

### 方案 C: OpenAI SDK 集成

```python
#!/usr/bin/env python3
# openai_runner.py

from openai import OpenAI
import sys
import json

def generate_code(prompt, model="gpt-3.5-turbo"):
    client = OpenAI(api_key="sk-proj-xxx")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是专业的 Python 工程师"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    return {
        "success": True,
        "code": response.choices[0].message.content,
        "model": model,
        "usage": response.usage.model_dump()
    }

if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:])
    result = generate_code(prompt)
    print(json.dumps(result, indent=2))
```

---

## 成本对比

### Codex (当前)
- API Key: $0.02/1K tokens
- 月度配额：有限
- **状态**: ❌ 配额超限

### Aider + GPT-3.5
- API Key: $0.002/1K tokens (便宜 10 倍!)
- 月度配额：无限制
- **估算**: $5/月 足够日常使用

### Aider + GPT-4
- API Key: $0.03/1K tokens
- 月度配额：无限制
- **估算**: $20-50/月

### Ollama 本地
- 成本：🆓 免费
- 硬件：需要 GPU (8GB+ 显存)
- **估算**: $0/月 (电费除外)

---

## 迁移步骤

### 从 Codex 迁移到 Aider

```bash
# 1. 安装 Aider
pip install aider-chat

# 2. 配置 API Key (同 Codex)
export OPENAI_API_KEY="sk-proj-xxx"

# 3. 测试
aider --model gpt-3.5-turbo "Hello"

# 4. 替换脚本
# 将 codex_runner.sh 改为 aider_runner.sh
```

### 从 Codex 迁移到 Ollama

```bash
# 1. 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. 拉取模型
ollama pull deepseek-coder:6.7b

# 3. 创建包装脚本
cat > ollama_runner.sh << 'EOF'
#!/bin/bash
ollama run deepseek-coder:6.7b "$1"
EOF
chmod +x ollama_runner.sh

# 4. 测试
./ollama_runner.sh "写个快速排序"
```

---

## 最佳实践

### 1. 多模型策略

```bash
# 简单任务 → GPT-3.5 (便宜)
aider --model gpt-3.5-turbo "修复小 Bug"

# 复杂任务 → GPT-4 (高质量)
aider --model gpt-4 "重构核心模块"

# 日常练习 → Ollama (免费)
ollama run deepseek-coder "写个排序算法"
```

### 2. 成本控制

```bash
# 设置预算告警
export OPENAI_BUDGET_LIMIT="10.00"  # $10/月

# 使用便宜模型优先
DEFAULT_MODEL="gpt-3.5-turbo"

# 监控用量
curl https://api.openai.com/v1/usage \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### 3. 质量保证

```bash
# AI 生成代码后自动运行测试
aider --message "添加单元测试"
pytest tests/ -v

# 代码审查
aider --message "审查代码质量问题"

# 性能测试
time python script.py
```

---

## 总结

| 需求 | 推荐方案 |
|------|----------|
| 最佳体验 | Aider + GPT-4 |
| 性价比 | Aider + GPT-3.5 |
| 完全免费 | Ollama + DeepSeek-Coder |
| 隐私保护 | Ollama 本地 |
| 快速迁移 | OpenAI SDK |

**立即行动**:
```bash
# 推荐：安装 Aider
pip install aider-chat

# 测试
aider --model gpt-3.5-turbo "Hello, World!"
```

---

**最后更新**: 2026-03-07  
**状态**: ✅ 5 种替代方案 ready
