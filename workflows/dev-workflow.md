# Development Workflow 🛠️

开发工作流程

---

## 流程概览

```
需求 → 方案 → 开发 → 测试 → 审查 → 提交 → 文档
```

---

## 1. 需求分析

### 输入
- 用户描述/需求文档
- 功能列表
- 技术约束

### 输出
- 需求确认
- 技术方案
- 工作量评估

### Checklist
- [ ] 需求边界清晰
- [ ] 技术方案可行
- [ ] 依赖项明确
- [ ] 风险评估完成

---

## 2. 方案设计

### 内容
- 架构图/流程图
- 数据结构设计
- API 设计（如有）
- 模块划分

### Review
- [ ] 设计符合最佳实践
- [ ] 可扩展性考虑
- [ ] 错误处理设计
- [ ] 日志设计

---

## 3. 开发实现

### 规范
- 代码注释（复杂逻辑）
- 错误处理（try-catch/set -e）
- 日志输出（关键步骤）
- 变量命名清晰

### 工具
- Dev Agent
- Git 版本控制
- 代码模板

---

## 4. 测试验证

### 测试类型
- 功能测试（正常流程）
- 异常测试（错误处理）
- 边界测试（极限值）

### 执行
```bash
# 运行测试
./test.sh

# 手动验证
./script.sh --test
```

---

## 5. 代码审查

### 审查要点
- 代码规范
- 错误处理
- 性能问题
- 安全隐患

### 工具
- QA Agent
- code-review-agent（Phase 2）

---

## 6. 提交代码

### Git 流程
```bash
# 添加
git add -A

# 提交（规范格式）
git commit -m "type: description"

# 推送
git push origin master
```

### Commit 规范
```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

---

## 7. 文档同步

### 更新内容
- README.md（功能说明）
- TOOLS.md（工具配置）
- AGENTS.md（流程更新）
- ARCHITECTURE.md（架构变更）

---

## 自动化

### Git Auto-Sync
```bash
# 每 30 分钟自动同步
*/30 * * * * /home/admin/.openclaw/workspace/projects/git-auto-sync/sync.sh
```

### 每日站会
```bash
# 每天早上 9 点生成报告
0 9 * * * /home/admin/.openclaw/workspace/projects/daily-standup/standup.sh
```

---

**Version**: 1.0  
**Last Updated**: 2026-03-06
