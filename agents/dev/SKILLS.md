# Dev Agent Skills

## Available Tools

| Tool | Usage | Example |
|------|-------|---------|
| `exec` | 执行 shell 命令 | `exec(command="ls -la")` |
| `read` | 读取文件 | `read(path="file.py")` |
| `write` | 写入文件 | `write(path="file.py", content="...")` |
| `edit` | 编辑文件 | `edit(path="file.py", oldText="...", newText="...")` |
| `web_search` | 搜索文档 | `web_search(query="python async")` |
| `web_fetch` | 抓取网页 | `web_fetch(url="...")` |
| `browser` | 网页自动化 | `browser(action="navigate", url="...")` |
| `sessions_spawn` | 生成子 agent | `sessions_spawn(task="...", runtime="subagent")` |

## Common Patterns

### 1. 创建脚本
```python
# 1. 创建文件
write(path="script.sh", content="#!/bin/bash\n...")

# 2. 设置执行权限
exec(command="chmod +x script.sh")

# 3. 测试运行
exec(command="./script.sh")
```

### 2. Git 操作
```python
# 检查状态
exec(command="git status")

# 添加提交
exec(command="git add -A && git commit -m 'msg'")

# 推送
exec(command="git push origin master")
```

### 3. 查文档
```python
# 搜索
web_search(query="python best practice")

# 抓取详情
web_fetch(url="https://docs.python.org/...")
```

### 4. 复杂任务（spawn sub-agent）
```python
# 生成专门 agent 处理
sessions_spawn(
    task="分析这个 Python 项目的代码质量",
    runtime="subagent",
    mode="run"
)
```

## Skill Templates

### Bash 脚本模板
```bash
#!/bin/bash
# Script: <name>
# Description: <what it does>
# Usage: <how to run>

set -e

# Config
WORKSPACE="/home/admin/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/script.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

main() {
    log "${GREEN}=== Script Started ===${NC}"
    
    # Your logic here
    
    log "${GREEN}=== Script Completed ===${NC}"
}

main "$@"
```

### Python 脚本模板
```python
#!/usr/bin/env python3
"""
Script: <name>
Description: <what it does>
Usage: python script.py [args]
"""

import logging
from pathlib import Path

# Config
WORKSPACE = Path("/home/admin/.openclaw/workspace")
LOG_FILE = WORKSPACE / "logs" / "script.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
log = logging.info

def main():
    log("=== Script Started ===")
    
    # Your logic here
    
    log("=== Script Completed ===")

if __name__ == "__main__":
    main()
```

## Limitations

- ❌ 不能直接访问数据库（需通过 API）
- ❌ 不能发送外部消息（需确认）
- ❌ 不能安装系统包（需确认）
- ❌ 不能修改系统配置（需确认）

## Best Practices

1. **先测试再提交**: 代码写完先运行验证
2. **日志完整**: 关键步骤都记录
3. **错误处理**: 捕获异常并友好提示
4. **配置分离**: 可变参数放配置文件
5. **版本控制**: 重要代码提交 git

---

**Version**: 1.0
**Last Updated**: 2026-03-06
