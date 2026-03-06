# ClawOS Architecture 🦞

多 Agent AI  orchestration 系统架构

---

## Overview

### 三层架构（按职能分组）

```
                    ClawOS (OpenClaw Core)
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
  Engineering           Operations              Growth
  (工程开发)            (运维运营)              (增长)
        │                     │                     │
   ┌────┴────┐          ┌─────┴─────┐              │
   │         │          │           │              │
dev-agent  qa-agent  ops-agent  media-agent   (预留扩展)
           │         │           │
      code-review  deploy    content
                   monitor    seo
                              │
        └─────────────────────┼─────────────────────┘
                              │
                        Data Layer
                        (数据层)
                              │
                    ┌─────────┴─────────┐
                    │                   │
               data-agent        research-agent
```

### 核心流程

```
┌─────────────────────────────────────────────────────────────┐
│                      ClawOS Core                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Orchestrator │→ │ Task Router  │→ │ Tool Manager │       │
│  │ (任务接收)    │  │ (智能分配)    │  │ (工具调用)    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌────────────────────────────────────────┐
        │           Agent Pool                   │
        │  Engineering  │  Operations  │  Data   │
        └────────────────────────────────────────┘
                              ↓
        ┌────────────────────────────────────────┐
        │           Skills & Tools               │
        │  • web_search  • browser  • exec       │
        │  • file ops    • message  • tts        │
        │  • custom skills...                    │
        └────────────────────────────────────────┘
```

---

## Core Components

### 1. Orchestrator (中枢)

**职责**: 任务接收、上下文管理、结果聚合

**文件**: `core/orchestrator/`

```
core/orchestrator/
├── main.py           # 主入口
├── context.py        # 会话上下文管理
├── memory.py         # 工作记忆 (SESSION-STATE.md)
└── response.py       # 响应格式化
```

**核心逻辑**:
```python
async def handle_task(task: str, context: SessionContext):
    # 1. 解析任务
    intent = parse_intent(task)
    
    # 2. 路由到 Agent
    agent = router.select_agent(intent)
    
    # 3. 执行
    result = await agent.execute(task, context)
    
    # 4. 聚合返回
    return format_response(result)
```

---

### 2. Task Router (任务路由器)

**职责**: 意图识别、Agent 选择、负载均衡

**文件**: `core/router/`

```
core/router/
├── router.py         # 路由逻辑
├── intent.py         # 意图识别
└── rules.py          # 路由规则
```

**路由规则**:

| 关键词/意图 | 目标 Agent | 示例 |
|------------|-----------|------|
| 代码、开发、功能、API | dev-agent | "写个 Python 脚本" |
| 测试、bug、检查、验证 | qa-agent | "测试这个功能" |
| 部署、监控、服务器、cron | ops-agent | "部署到服务器" |
| 数据、分析、处理、转换 | data-agent | "分析这个数据" |
| 图片、视频、音频、媒体 | media-agent | "处理这张图片" |
| 默认/不确定 | orchestrator | 其他任务 |

---

### 3. Agent Pool (Agent 池)

**结构**: 每个 Agent = Prompt + Rules + Skills

```
agents/
├── dev/
│   ├── PROMPT.md       # 角色定义
│   ├── RULES.md        # 行为规则
│   └── SKILLS.md       # 可用技能
├── qa/
├── ops/
├── data/
└── media/
```

---

## Agent Definitions

## Phase 1: Core Agents (✅ 已完成)

### Dev Agent (开发)

**Prompt**: 你是 ClawOS 开发专家，专注于代码编写、功能开发、API 设计

**Skills**:
- 代码生成（Python/Bash/JS）
- Git 操作
- 文件操作
- web_search（查文档）

**Rules**:
- 先理解需求再写代码
- 代码必须有注释
- 复杂功能先给方案再实现

---

### QA Agent (测试)

**Prompt**: 你是 ClawOS 质量保障专家，专注于测试、验证、bug 排查

**Skills**:
- 执行测试脚本
- 日志分析
- 错误检测
- 性能检查

**Rules**:
- 测试必须可重复
- bug 报告要有复现步骤
- 优先自动化测试

---

### Ops Agent (运维)

**Prompt**: 你是 ClawOS 运维专家，专注于部署、监控、系统管理

**Skills**:
- 执行系统命令
- cron 配置
- 服务管理
- 监控告警

**Rules**:
- 危险操作需确认
- 变更记录日志
- 优先自动化运维

---

### Data Agent (数据处理)

**Prompt**: 你是 ClawOS 数据专家，专注于数据分析、转换、可视化

**Skills**:
- 文件读取/写入
- 数据转换（JSON/CSV/XML）
- web_search（查数据）
- 简单分析

**Rules**:
- 数据操作前备份
- 大数据集分块处理
- 输出结构化结果

---

### Media Agent (媒体处理)

**Prompt**: 你是 ClawOS 媒体专家，专注于图片、视频、音频处理

**Skills**:
- 图片分析（image tool）
- 文件上传/下载
- 格式转换
- web_search（找素材）

**Rules**:
- 大文件先检查空间
- 支持常见格式
- 保留原始文件备份

---

## Phase 2: Enhanced Agents (⏳ 规划中)

### Code Review Agent (代码审查)
**Layer**: Engineering
**Parent**: qa-agent
**专注**: 代码质量审查、最佳实践检查、安全漏洞扫描

### Deploy Agent (部署)
**Layer**: Operations
**Parent**: ops-agent
**专注**: 应用部署、CI/CD、环境管理

### Monitor Agent (监控)
**Layer**: Operations
**Parent**: ops-agent
**专注**: 系统监控、告警、健康检查

---

## Phase 3: Growth Agents (⏳ 未来扩展)

### Content Agent (内容)
**Layer**: Operations
**专注**: 内容生成、文档管理、博客发布

### SEO Agent (优化)
**Layer**: Operations
**专注**: SEO 优化、关键词分析、排名跟踪

### Research Agent (调研)
**Layer**: Data Layer
**专注**: 信息收集、竞品分析、趋势调研

---

## Task Flow

```
1. 用户输入任务
         ↓
2. Orchestrator 接收
         ↓
3. Router 识别意图 → 选择 Agent
         ↓
4. Agent 执行（调用 Skills）
         ↓
5. 结果返回 Orchestrator
         ↓
6. 格式化输出给用户
         ↓
7. 记录到 SESSION-STATE.md
```

---

## Memory System

```
workspace/
├── SESSION-STATE.md    # 当前任务状态（WAL 目标）
├── MEMORY.md           # 长期记忆
├── memory/
│   └── YYYY-MM-DD.md   # 日志
└── .learnings/         # 自改进记录
    ├── LEARNINGS.md
    ├── ERRORS.md
    └── FEATURE_REQUESTS.md
```

---

## Extension Points

### 添加新 Agent

1. 创建目录：`agents/new-agent/`
2. 定义文件：
   - `PROMPT.md` - 角色
   - `RULES.md` - 规则
   - `SKILLS.md` - 技能
3. 更新路由规则：`core/orchestrator/ROUTER.md`
4. 更新架构文档：`ARCHITECTURE.md`
5. 测试路由

### 分层设计原则

- **Engineering**: 代码相关（开发、测试、审查）
- **Operations**: 运维运营（部署、监控、媒体、内容）
- **Growth**: 增长相关（预留扩展）
- **Data Layer**: 数据相关（处理、调研）

### Agent 拆分时机

当一个 Agent 的职责过多时，考虑拆分：

| 原 Agent | 拆分为 | 时机 |
|---------|--------|------|
| qa-agent | qa-agent + code-review-agent | 代码审查需求频繁 |
| ops-agent | ops-agent + deploy-agent + monitor-agent | 部署/监控任务独立 |
| data-agent | data-agent + research-agent | 调研任务增多 |

### 添加新 Skill

1. 创建技能文件：`skills/new-skill/SKILL.md`
2. 在 Agent 的 `SKILLS.md` 中引用
3. 测试调用

---

## Security

- 所有外部操作需确认（删除、推送、发送消息）
- 敏感信息不记录到日志
- Skill 安装前 vetting 检查
- 不执行未知来源代码

---

## Performance

- 简单任务直接执行（<5 秒）
- 复杂任务 spawn sub-agent
- 长任务后台运行 + 进度通知
- 结果缓存避免重复计算

---

**Version**: 1.0.0
**Last Updated**: 2026-03-06
**Author**: leonsoul + ClawOS Team
