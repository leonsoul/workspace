# ClawOS Agents 总览 🦞

多 Agent AI 协作系统

---

## 快速导航

| Agent | 职责 | 文件路径 |
|-------|------|----------|
| 🤖 **Orchestrator** | 中枢调度、任务分配 | `core/orchestrator/` |
| 🛠️ **Dev Agent** | 代码开发、脚本编写 | `agents/dev/` |
| 🧪 **QA Agent** | 测试、质量保障 | `agents/qa/` |
| 🚀 **Ops Agent** | 运维、部署、监控 | `agents/ops/` |
| 📊 **Data Agent** | 数据处理、分析 | `agents/data/` |
| 🎨 **Media Agent** | 图片、视频、音频 | `agents/media/` |

---

## 架构示意

```
用户输入
    ↓
┌─────────────────┐
│  Orchestrator   │ ← 任务接收、上下文管理
└────────┬────────┘
         ↓
┌─────────────────┐
│   Task Router   │ ← 意图识别、Agent 选择
└────────┬────────┘
         ↓
    ┌────┴────┬─────────┬────────┬────────┐
    ↓         ↓         ↓        ↓        ↓
┌──────┐ ┌──────┐ ┌───────┐ ┌───────┐ ┌────────┐
│ Dev  │ │ QA   │ │ Ops   │ │ Data  │ │ Media  │
│Agent │ │Agent │ │Agent  │ │Agent  │ │ Agent  │
└──┬───┘ └──┬───┘ └───┬───┘ └───┬───┘ └───┬────┘
   ↓         ↓         ↓         ↓         ↓
         ┌───┴─────────┴─────────┴─────────┴───┐
         │          Skills & Tools             │
         │  exec, read, write, web_search...   │
         └─────────────────────────────────────┘
                                 ↓
                          返回结果给用户
```

---

## 使用方式

### 方式 1：自然语言（推荐）

直接描述任务，系统自动路由：

```
用户：写个 Python 脚本分析 JSON 数据
→ 自动路由到：Dev Agent（编写代码）
→ 可能协作：Data Agent（数据格式）

用户：测试一下这个脚本
→ 自动路由到：QA Agent

用户：部署到服务器
→ 自动路由到：Ops Agent
```

### 方式 2：指定 Agent

明确指定使用哪个 Agent：

```
用户：@dev-agent 写个备份脚本
用户：@qa-agent 检查代码质量
用户：@ops-agent 设置 cron 任务
```

### 方式 3：多 Agent 协作

复杂任务自动触发多 Agent：

```
用户：开发一个数据分析工具并部署

流程：
1. Dev Agent → 编写代码
2. QA Agent → 测试验证
3. Ops Agent → 部署上线
```

---

## Agent 详细文档

### 🤖 Orchestrator（中枢）

**职责**:
- 接收用户任务
- 调用 Router 选择 Agent
- 管理会话上下文
- 聚合返回结果

**核心文件**:
- `core/orchestrator/ROUTER.md` - 路由规则

---

### 🛠️ Dev Agent

**专长**:
- Python/Bash/JavaScript 编程
- Git 版本控制
- 脚本自动化
- API 开发

**配置文件**:
- `agents/dev/PROMPT.md` - 角色定义
- `agents/dev/RULES.md` - 行为规则
- `agents/dev/SKILLS.md` - 可用技能

**示例任务**:
- "写个 Python 脚本处理 API 数据"
- "创建 Git 自动同步脚本"
- "实现一个数据转换工具"

---

### 🧪 QA Agent

**专长**:
- 测试用例设计
- Bug 排查
- 代码审查
- 性能测试

**配置文件**:
- `agents/qa/PROMPT.md`
- `agents/qa/RULES.md`
- `agents/qa/SKILLS.md`

**示例任务**:
- "测试这个脚本有没有 bug"
- "检查代码质量"
- "验证功能是否正常"

---

### 🚀 Ops Agent

**专长**:
- 系统部署
- 服务监控
- Cron 定时任务
- 日志管理

**配置文件**:
- `agents/ops/PROMPT.md`
- `agents/ops/RULES.md`
- `agents/ops/SKILLS.md`

**示例任务**:
- "部署到服务器"
- "设置每天备份"
- "检查系统健康状态"

---

### 📊 Data Agent

**专长**:
- JSON/CSV/XML 处理
- 数据转换
- 统计分析
- 数据清洗

**配置文件**:
- `agents/data/PROMPT.md`
- `agents/data/RULES.md`
- `agents/data/SKILLS.md`

**示例任务**:
- "把 JSON 转成 CSV"
- "分析这个数据集"
- "清洗无效数据"

---

### 🎨 Media Agent

**专长**:
- 图片分析（OCR、内容识别）
- 格式转换
- 压缩优化
- 视频处理

**配置文件**:
- `agents/media/PROMPT.md`
- `agents/media/RULES.md`
- `agents/media/SKILLS.md`

**示例任务**:
- "压缩这张图片"
- "视频转 GIF"
- "提取图片中的文字"

---

## 任务路由示例

| 用户输入 | 路由 Agent | 关键词匹配 |
|---------|-----------|-----------|
| "写个脚本" | Dev | 写、脚本 |
| "测试一下" | QA | 测试 |
| "部署上线" | Ops | 部署 |
| "分析数据" | Data | 分析、数据 |
| "处理图片" | Media | 处理、图片 |
| "检查 bug" | QA | 检查、bug |
| "设置定时任务" | Ops | 定时任务 |
| "JSON 转 CSV" | Data | JSON、CSV、转 |
| "视频转 GIF" | Media | 视频、GIF、转 |
| "备份系统" | Ops | 备份 |
| "代码优化" | Dev | 代码 |
| "性能测试" | QA | 测试、性能 |

---

## 扩展指南

### 添加新 Agent

1. 创建目录：`agents/new-agent/`
2. 添加配置文件：
   - `PROMPT.md` - 角色定义
   - `RULES.md` - 行为规则
   - `SKILLS.md` - 可用技能
3. 更新路由规则：`core/orchestrator/ROUTER.md`
4. 更新总览：`AGENTS-OVERVIEW.md`

### 添加新 Skill

1. 在 Agent 的 `SKILLS.md` 中添加
2. 提供使用示例
3. 标注限制和注意事项

---

## 最佳实践

1. **明确描述**: 任务描述越清晰，路由越准确
2. **上下文完整**: 复杂任务提供足够背景
3. **结果验证**: 关键操作后验证结果
4. **日志记录**: 重要操作记录到 SESSION-STATE.md
5. **安全确认**: 危险操作（删除、推送）需确认

---

## 相关文件

- `ARCHITECTURE.md` - 系统架构
- `AGENTS.md` - 工作区规则
- `SESSION-STATE.md` - 当前任务状态
- `.learnings/LEARNINGS.md` - 学习记录

---

**Version**: 1.0.0
**Created**: 2026-03-06
**Author**: leonsoul + ClawOS Team
