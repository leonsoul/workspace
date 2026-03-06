# Agent 协作工作流程

---

## 流程说明

当用户提出任务时，自动路由到合适的 Agent：

```
用户任务 → Orchestrator → Router → Agent → 执行 → 返回结果
```

---

## Agent 分工

| Agent | 职责 | 触发词 |
|-------|------|--------|
| Dev Agent | 代码开发、脚本编写 | 写代码、开发、脚本、API |
| QA Agent | 测试、质量保障 | 测试、bug、检查、验证 |
| Ops Agent | 运维、部署、监控 | 部署、服务器、监控、cron |
| Data Agent | 数据分析、处理 | 数据、分析、JSON、CSV |
| Media Agent | 图片、视频处理 | 图片、视频、媒体、OCR |

---

## 实际案例

### 案例 1：搜索伊朗动态

**用户**: "搜索伊朗最新的动态"

**流程**:
1. **Orchestrator** 接收任务
2. **Router** 识别意图 → 信息搜索
3. **Dev Agent** 执行：
   - 打开浏览器
   - 搜索关键词
   - 提取搜索结果
   - 整理汇总信息
4. **返回结果** 给用户

**结果**: ✅ 完成搜索并汇总

### 案例 2：代码审查

**用户**: "审查一下 performance-review 项目"

**流程**:
1. **Orchestrator** 接收任务
2. **Router** 识别意图 → 代码审查
3. **QA Agent** 执行：
   - 调用 skills_bene
   - 运行代码审查脚本
   - 生成审查报告
4. **返回结果** 给用户

**结果**: ✅ 完成审查 (3.8/5.0)

### 案例 3：部署服务

**用户**: "部署人员评价系统"

**流程**:
1. **Orchestrator** 接收任务
2. **Router** 识别意图 → 部署运维
3. **Ops Agent** 执行：
   - 检查服务状态
   - 配置 systemd
   - 启动服务
   - 验证健康检查
4. **返回结果** 给用户

**结果**: ✅ 服务运行中

---

## 配置方式

### 1. Agent 配置文件

每个 Agent 有独立的配置：

```bash
~/.openclaw/agents/
├── dev-agent/config.json
├── qa-agent/config.json
├── ops-agent/config.json
├── data-agent/config.json
└── media-agent/config.json
```

### 2. 路由规则

在 `core/orchestrator/ROUTER.md` 中定义路由规则：

```markdown
| 关键词 | Agent |
|--------|-------|
| 代码、开发 | dev-agent |
| 测试、bug | qa-agent |
| 部署、运维 | ops-agent |
| 数据、分析 | data-agent |
| 图片、视频 | media-agent |
```

### 3. 模型分配

每个 Agent 使用最适合的模型：

| Agent | 模型 |
|-------|------|
| Dev Agent | dashscope-coding/qwen3.5-plus |
| QA Agent | dashscope/qwen3.5-plus |
| Ops Agent | dashscope/qwen3.5-plus |
| Data Agent | dashscope/qwen3-max-2026-01-23 |
| Media Agent | dashscope/qwen3-vl-plus |

---

## 使用示例

### 直接使用
```
"写个 Python 脚本"
→ Dev Agent 自动处理
```

### 指定 Agent
```
"@dev-agent 写个 API"
→ 直接路由到 Dev Agent
```

### 复杂任务
```
"开发一个功能并测试部署"
→ Dev Agent 开发
→ QA Agent 测试
→ Ops Agent 部署
```

---

## 监控和日志

### 查看 Agent 状态
```bash
cat ~/.openclaw/agents/*/config.json
```

### 查看执行日志
```bash
tail -f /tmp/openclaw.log
```

### 查看会话历史
```bash
cat ~/.openclaw/workspace/memory/YYYY-MM-DD.md
```

---

## 最佳实践

1. **明确任务描述** - 让 Router 准确识别
2. **提供足够上下文** - 帮助 Agent 理解需求
3. **指定输出格式** - 如"生成报告"、"写脚本"
4. **检查结果** - 验证 Agent 执行结果
5. **记录学习** - 将经验写入 `.learnings/`

---

## 持续改进

每次任务完成后：
1. 记录到 `.learnings/LEARNINGS.md`
2. 评估 Agent 表现
3. 优化路由规则
4. 更新 Agent 配置

---

**状态**: ✅ 已启用  
**最后更新**: 2026-03-06
