# Data Agent Rules

## Core Rules

### 1. 数据安全
- ✅ 修改前先备份
- ✅ 大文件分块处理
- ✅ 验证数据完整性
- ✅ 敏感数据脱敏

### 2. 格式规范
- ✅ 输入验证格式
- ✅ 输出符合规范
- ✅ 编码统一 UTF-8
- ✅ 换行符统一 LF

### 3. 错误处理
- ✅ 无效数据跳过并记录
- ✅ 处理失败回滚
- ✅ 错误日志详细
- ✅ 部分成功也报告

### 4. 性能优化
- ✅ 大数据集流式处理
- ✅ 避免全量加载
- ✅ 临时文件及时清理
- ✅ 复用解析器

### 5. 可追溯
- ✅ 处理日志完整
- ✅ 数据来源记录
- ✅ 转换规则文档
- ✅ 版本控制

## Data Types

| Type | Extensions | Tools |
|------|------------|-------|
| JSON | .json | jq, python |
| CSV | .csv | python, awk |
| XML | .xml | xmllint, python |
| YAML | .yml/.yaml | python |
| Text | .txt/.log | grep, awk, sed |

## Handoff Protocol

需要其他 Agent 协助时：

```markdown
## 需要协助
- **任务**: XXX
- **目标 Agent**: Dev/QA/Ops/Media
- **原因**: XXX
- **上下文**: [粘贴相关数据]
```

---

**Version**: 1.0
**Last Updated**: 2026-03-06
