# Testing Workflow 🧪

测试工作流程

---

## 流程概览

```
测试计划 → 用例设计 → 执行测试 → Bug 报告 → 回归测试
```

---

## 1. 测试计划

### 输入
- 需求文档
- 技术方案
- 功能列表

### 输出
- 测试范围
- 测试策略
- 资源评估

### Checklist
- [ ] 测试目标明确
- [ ] 测试范围清晰
- [ ] 测试环境准备
- [ ] 测试数据准备

---

## 2. 用例设计

### 测试类型

| 类型 | 说明 | 示例 |
|------|------|------|
| 功能测试 | 验证功能 | 正常流程 |
| 异常测试 | 错误处理 | 无效输入 |
| 边界测试 | 极限值 | 最大/最小值 |
| 性能测试 | 响应时间 | 并发测试 |
| 安全测试 | 漏洞检查 | 注入测试 |

### 用例模板
```markdown
## TC-YYYYMMDD-XXX

**Type**: 功能测试
**Priority**: High

### Preconditions
- ...

### Steps
1. ...
2. ...
3. ...

### Expected
- ...

### Actual
- ...

### Status
- [ ] Pass
- [ ] Fail
```

---

## 3. 执行测试

### 自动化测试
```bash
# 运行测试套件
./test_all.sh

# 单项测试
./test_feature.sh
```

### 手动测试
- 按用例执行
- 记录结果
- 截图/日志

---

## 4. Bug 报告

### 模板
```markdown
## BUG-YYYYMMDD-XXX

**Severity**: High
**Status**: Open

### Description
...

### Reproduction Steps
1. ...
2. ...
3. ...

### Expected vs Actual
- Expected: ...
- Actual: ...

### Logs
```
错误信息
```

### Suggested Fix
...
```

### Severity 定义

| Level | 定义 | 响应 |
|-------|------|------|
| Critical | 系统崩溃 | 立即 |
| High | 核心功能失效 | 24h |
| Medium | 部分功能异常 | 1 周 |
| Low | 体验问题 | 排期 |

---

## 5. 回归测试

### 触发时机
- Bug 修复后
- 代码变更后
- 发布前

### 执行
```bash
# 回归测试套件
./test_regression.sh
```

---

## 工具

- QA Agent
- 测试脚本模板
- Bug 跟踪（.learnings/ERRORS.md）

---

**Version**: 1.0  
**Last Updated**: 2026-03-06
