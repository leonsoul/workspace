# QA Agent Skills

## Available Tools

| Tool | Usage | Example |
|------|-------|---------|
| `exec` | 执行测试脚本 | `exec(command="./test.sh")` |
| `read` | 查看日志/代码 | `read(path="error.log")` |
| `web_search` | 查测试方案 | `web_search(query="python unit test")` |
| `sessions_spawn` | 生成测试 agent | `sessions_spawn(task="压力测试")` |
| `process` | 管理后台进程 | `process(action="list")` |

## Test Templates

### Bash 测试脚本
```bash
#!/bin/bash
# Test: <feature>
# Description: <what to test>

set -e
PASSED=0
FAILED=0

test_case() {
    local name="$1"
    local cmd="$2"
    local expected="$3"
    
    echo -n "Testing: $name ... "
    
    if eval "$cmd" | grep -q "$expected"; then
        echo "✅ PASS"
        ((PASSED++))
    else
        echo "❌ FAIL"
        ((FAILED++))
    fi
}

# Test cases
test_case "Feature X works" "./feature_x.sh" "success"
test_case "Error handling" "./error_test.sh" "handled"

# Summary
echo ""
echo "=== Test Summary ==="
echo "Passed: $PASSED"
echo "Failed: $FAILED"

[ $FAILED -eq 0 ] && exit 0 || exit 1
```

### Python 测试脚本
```python
#!/usr/bin/env python3
"""
Test: <feature>
Description: <what to test>
"""

import unittest
import subprocess

class TestFeature(unittest.TestCase):
    
    def test_normal_case(self):
        """正常流程测试"""
        result = subprocess.run(
            ["./feature.sh"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("success", result.stdout)
    
    def test_error_case(self):
        """异常流程测试"""
        result = subprocess.run(
            ["./feature.sh", "--invalid"],
            capture_output=True,
            text=True
        )
        self.assertNotEqual(result.returncode, 0)
    
    def test_edge_case(self):
        """边界情况测试"""
        # Your test logic
        pass

if __name__ == "__main__":
    unittest.main()
```

## Common Patterns

### 1. 日志分析
```python
# 读取日志
with open("app.log") as f:
    logs = f.read()

# 查找错误
errors = [line for line in logs.split('\n') if 'ERROR' in line]

# 统计
print(f"Found {len(errors)} errors")
```

### 2. 性能检查
```bash
# 执行时间
time ./script.sh

# 内存占用
/usr/bin/time -v ./script.sh

# 并发测试
ab -n 1000 -c 10 http://localhost:8080/
```

### 3. 代码审查
```bash
# 检查语法
python -m py_compile script.py
bash -n script.sh

# 检查格式
black --check .
shellcheck script.sh
```

### 4. Bug 复现
```bash
# 记录环境
uname -a
python --version
git rev-parse HEAD

# 复现步骤
./step1.sh
./step2.sh
# 观察结果
```

## Bug Report Template

```markdown
## BUG-YYYYMMDD-XXX

**Severity**: High
**Status**: Open
**Area**: backend

### Description
简要描述问题

### Reproduction Steps
1. ...
2. ...
3. ...

### Expected Behavior
应该发生什么

### Actual Behavior
实际发生了什么

### Logs
```
错误日志/堆栈跟踪
```

### Environment
- OS: ...
- Version: ...
- Commit: ...

### Suggested Fix
修复建议

---
```

## Limitations

- ❌ 不能直接修改生产代码（需 Dev Agent）
- ❌ 不能部署到生产环境（需 Ops Agent）
- ❌ 不能忽略测试失败（必须报告）

## Best Practices

1. **测试隔离**: 每个测试独立，不依赖顺序
2. **可重复**: 任何人在任何环境都能复现
3. **快速反馈**: 测试要在合理时间内完成
4. **清晰报告**: 失败时要清楚知道为什么
5. **持续集成**: 测试自动化，每次提交都运行

---

**Version**: 1.0
**Last Updated**: 2026-03-06
