# [LRN-20260307-001] uitest_integration

**Logged**: 2026-03-07T08:45:00+08:00
**Priority**: high
**Status**: resolved
**Area**: automation

### Summary
UItest 自动化测试项目集成到 ClawOS 的完整流程与经验

### Details

**项目克隆**:
```bash
git clone git@github.com:leonsoul/UItest.git projects/UItest
```

**依赖安装问题与解决**:
1. numpy 2.x 与 opencv-python 不兼容 → `pip install 'numpy<2'`
2. PyYAML 构建失败 → `pip install PyYAML --upgrade`
3. wrapt 兼容性问题 → `pip install wrapt --upgrade`
4. Pillow 构建失败 → `pip install Pillow --upgrade`

**路径解析 Bug 修复**:
```python
# 问题：大小写敏感 'UiTest' vs 'UItest'
def get_file_path(file_path, DirectoryName='UItest'):  # 统一大写
    Dir_path = os.path.abspath(os.path.dirname(__file__))
    project_root = Dir_path
    for _ in range(5):
        if os.path.basename(project_root) == DirectoryName:
            break
        project_root = os.path.dirname(project_root)
    return os.path.join(project_root, file_path)
```

**运行验证**:
```bash
cd projects/UItest
python run.py 0  # 成功收集 114 个测试用例
```

### Resolution
- **Resolved**: 2026-03-07T08:40:00+08:00
- **Notes**: 测试框架可正常运行，文档已创建

### Metadata
- Source: hands_on
- Tags: uitest, pytest, selenium, automation, testing
- Pattern-Key: automation.uitest_integration

---

# [LRN-20260307-002] codex_cli_setup

**Logged**: 2026-03-07T08:45:00+08:00
**Priority**: high
**Status**: resolved
**Area**: automation

### Summary
Codex CLI 安装、配置与集成到 ClawOS 工作流

### Details

**安装方式**:
```bash
npm install -g @openai/codex
# 或
brew install --cask codex
```

**登录方式对比**:
1. **API Key 登录** (推荐用于自动化)
   ```bash
   echo "sk-xxx" | codex login --with-api-key
   ```
   优点：适合脚本自动化
   缺点：有配额限制

2. **ChatGPT 账号登录** (推荐个人使用)
   ```bash
   codex login
   ```
   优点：Plus/Pro 账号无限使用
   缺点：需要手动扫码

**配置模板** (`~/.codex/config.toml`):
```toml
model = "gpt-5-codex"

[provider]
type = "openai"
api_key = "sk-xxx"

sandbox = "workspace-write"

[features]
full_auto = true
```

**执行模式**:
- `fix` - 修复 Bug
- `testgen` - 生成测试
- `refactor` - 代码重构
- `exec` - 通用执行

**包装脚本** (`tools/codex_runner.sh`):
```bash
./tools/codex_runner.sh -m fix "修复 XXX 问题"
```

### Resolution
- **Resolved**: 2026-03-07T08:45:00+08:00
- **Notes**: Codex 已集成，API Key 配额超限需充值

### Metadata
- Source: hands_on
- Tags: codex, ai, code-generation, automation
- Pattern-Key: automation.codex_integration

---

# [LRN-20260307-003] python3_13_compatibility

**Logged**: 2026-03-07T08:45:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: devops

### Summary
Python 3.13 环境下的依赖兼容性问题分析与解决

### Details

**问题现象**:
```
AttributeError: _ARRAY_API not found  # opencv-python
ImportError: cannot import name 'formatargspec' from 'inspect'  # wrapt
KeyError: '__version__'  # Pillow
```

**根本原因**:
- Python 3.13 太新，很多包还没完全兼容
- numpy 2.x API 变更导致 opencv-python 失败
- 一些包使用已废弃的 API

**解决方案**:
```bash
# 1. numpy 降级 (opencv-python 需要 1.x)
pip install 'numpy<2'

# 2. 升级问题包到最新版
pip install --upgrade PyYAML wrapt Pillow

# 3. 过滤 requirements.txt 中的问题包
grep -v "^numpy\|^Pillow\|^wrapt" requirements.txt > filtered.txt
pip install -r filtered.txt
```

**经验教训**:
1. 新项目优先使用 Python 3.10/3.11 (LTS)
2. 安装依赖前先检查 Python 版本兼容性
3. 遇到兼容性问题优先降级而非升级
4. 使用 `pip install 'package<version'` 指定版本范围

### Resolution
- **Resolved**: 2026-03-07T08:35:00+08:00
- **Notes**: 所有依赖安装成功，测试可运行

### Metadata
- Source: bug_fix
- Tags: python, compatibility, dependencies, debugging
- Pattern-Key: devops.python_compatibility

---

# [LRN-20260307-004] documentation_driven_development

**Logged**: 2026-03-07T08:45:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: methodology

### Summary
文档驱动开发 (DDD) 在 ClawOS 自动化集成中的实践

### Details

**文档驱动流程**:
```
1. 先写使用文档 (AUTOMATION_GUIDE.md)
   ↓ 明确用户怎么用
2. 再写配置文档 (CODEX_INTEGRATION.md)
   ↓ 明确环境怎么配
3. 最后写实现文档 (codex_runner.sh)
   ↓ 明确代码怎么写
```

**文档结构标准**:
```markdown
# 标题

## 快速开始 (5 分钟上手)
## 配置说明 (环境要求)
## 使用示例 (常见场景)
## API 参考 (接口定义)
## 最佳实践 (经验总结)
## 故障排查 (常见问题)
```

**文档产出**:
- `AUTOMATION_GUIDE.md` - 自动化系统手册 (8.8KB)
- `tools/CODEX_INTEGRATION.md` - Codex 使用指南 (6.3KB)
- `projects/UItest/CLAWOS_INTEGRATION.md` - UItest 集成 (5.1KB)
- `GROWTH-REPORT-2026-03-07.md` - 自我成长报告 (3.9KB)

**价值**:
1. 文档即设计 - 写文档过程理清思路
2. 文档即测试 - 按文档操作应该成功
3. 文档即传承 - 下次可以直接用

### Resolution
- **Resolved**: 2026-03-07T08:45:00+08:00
- **Notes**: 文档驱动方法有效，继续坚持

### Metadata
- Source: methodology
- Tags: documentation, methodology, best-practices
- Pattern-Key: methodology.documentation_driven

---
