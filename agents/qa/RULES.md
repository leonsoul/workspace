# QA Agent Rules

## Core Rules

### 1. 测试先行
- ✅ 新功能必须有测试
- ✅ 测试用例覆盖正常/异常流程
- ✅ 边界情况单独测试

### 2. Bug 报告规范
- ✅ 必须有复现步骤
- ✅ 附带日志/截图
- ✅ 标注严重性（Critical/High/Medium/Low）
- ✅ 给出修复建议

### 3. 客观公正
- ✅ 用数据说话（日志、指标）
- ✅ 不猜测，要验证
- ✅ 不放过任何警告

### 4. 自动化优先
- ✅ 能写脚本就不手动
- ✅ 回归测试自动化
- ✅ CI/CD 集成

### 5. 安全测试
- ✅ 输入验证测试
- ✅ 权限检查
- ✅ 敏感数据保护

## Severity Levels

| Level | 定义 | 响应时间 |
|-------|------|----------|
| Critical | 系统崩溃、数据丢失 | 立即 |
| High | 核心功能失效 | 24 小时 |
| Medium | 部分功能异常 | 1 周 |
| Low | 体验问题、建议 | 排期 |

## Test Types

### 1. 功能测试
```bash
# 验证功能是否符合需求
./test_feature.sh
```

### 2. 回归测试
```bash
# 确保修改没破坏现有功能
./test_regression.sh
```

### 3. 性能测试
```bash
# 检查响应时间、资源占用
./test_performance.sh
```

### 4. 安全测试
```bash
# 检查漏洞、权限
./test_security.sh
```

## Handoff Protocol

需要其他 Agent 协助时：

```markdown
## 需要协助
- **任务**: 修复 BUG-001
- **目标 Agent**: Dev Agent
- **原因**: 需要代码修改
- **上下文**: [粘贴 Bug 报告]
```

---

**Version**: 1.0
**Last Updated**: 2026-03-06
