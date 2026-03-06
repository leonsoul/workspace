# 可用技能清单

**更新时间**: 2026-03-06 21:50  
**适用**: ClawOS / OpenClaw 主 Agent

---

## 🎯 核心技能（已激活）

### 1. **qqbot-cron** - QQ 智能提醒
- **位置**: `~/.openclaw/extensions/qqbot/skills/qqbot-cron/`
- **用途**: 设置定时提醒、周期任务
- **触发**: 提醒、定时、周期任务
- **关键规则**: 
  - `payload.kind` 必须是 `"agentTurn"`（❌ 不能用 `"systemEvent"`）
  - `deliver: true`, `channel: "qqbot"`, `to: "{openid}"`
  - `atMs` 必须是绝对毫秒时间戳

### 2. **qqbot-media** - QQ 媒体发送
- **位置**: `~/.openclaw/extensions/qqbot/skills/qqbot-media/`
- **用途**: 发送本地/网络图片
- **触发**: 发图、图片、文件
- **关键规则**:
  - 使用 `<qqimg>图片路径</qqimg>` 标签
  - ❌ 不要说"无法发送图片"

### 3. **searxng** - 隐私搜索
- **位置**: `~/.openclaw/workspace/skills/searxng/`
- **用途**: 本地 SearXNG 实例搜索
- **触发**: 搜索、查找信息
- **配置**: `SEARXNG_URL` 环境变量

### 4. **self-improvement** - 自改进
- **位置**: `~/.openclaw/workspace/skills/self-improving-agent/`
- **用途**: 记录学习、错误、改进
- **触发**: 错误、纠正、新功能请求
- **文件**: `.learnings/LEARNINGS.md`, `ERRORS.md`, `FEATURE_REQUESTS.md`

### 5. **proactive-agent** - 主动代理
- **位置**: `~/.openclaw/workspace/skills/proactive-agent/`
- **用途**: 主动行为、WAL 协议、工作缓冲
- **触发**: 所有会话
- **核心**: WAL 协议、工作缓冲、主动检查

---

## 📁 工作区技能（链接到 skills_bene）

### 6. **ai-code-review** - AI 代码审查
- **位置**: `~/workspace/projects/skills_bene/skills/ai-code-review`
- **用途**: 自动代码审查
- **触发**: 代码提交、PR

### 7. **bugbot** - Bug 追踪
- **位置**: `~/workspace/projects/skills_bene/skills/bugbot`
- **用途**: Bug 检测和报告
- **触发**: 错误、异常

### 8. **github-code-review** - GitHub 审查
- **位置**: `~/workspace/projects/skills_bene/skills/github-cr`
- **用途**: GitHub PR 审查
- **触发**: GitHub PR 事件

### 9. **gitlab-code-review** - GitLab 审查
- **位置**: `~/workspace/projects/skills_bene/skills/gitlab-aicr`
- **用途**: GitLab MR 审查
- **触发**: GitLab MR 事件

---

## 🔧 工具类技能

### 10. **find-skills** - 技能发现
- **位置**: `~/.openclaw/workspace/skills/find-skills/`
- **用途**: 搜索和安装新技能
- **触发**: "找技能"、"有没有技能可以..."

### 11. **skill-vetter** - 技能审查
- **位置**: `~/.openclaw/workspace/skills/skill-vetter/`
- **用途**: 安全检查技能
- **触发**: 安装技能前

### 12. **agent-browser** - 浏览器自动化
- **位置**: `~/.openclaw/workspace/skills/agent-browser/`
- **用途**: Rust 无头浏览器控制
- **触发**: 网页操作、截图

---

## 📋 使用指南

### 提醒设置示例
```json
{
  "action": "add",
  "job": {
    "name": "喝水提醒",
    "schedule": { "kind": "at", "atMs": 1772804898183 + 300000 },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "deleteAfterRun": true,
    "payload": {
      "kind": "agentTurn",
      "message": "你是一个暖心的提醒助手。请用温暖、有趣的方式提醒用户：该喝水了。要求：(1) 不要回复 HEARTBEAT_OK (2) 不要解释你是谁 (3) 直接输出一条暖心的提醒消息 (4) 可以加一句简短的鸡汤或关怀的话 (5) 控制在 2-3 句话以内 (6) 用 emoji 点缀",
      "deliver": true,
      "channel": "qqbot",
      "to": "49AAA075AF1986BC5A69B9DBF3E53A1E"
    }
  }
}
```

### 发送图片示例
```
这是你要的图片：
<qqimg>/home/admin/workspace/image.png</qqimg>
```

### 搜索示例
```bash
uv run scripts/searxng.py search "query" -n 10
```

---

## 🔄 技能加载机制

### 自动加载
- **QQBot 技能**: 启动时自动加载 `~/.openclaw/extensions/qqbot/skills/`
- **工作区技能**: 启动时自动加载 `~/.openclaw/workspace/skills/`

### 手动安装
```bash
# 通过 ClawHub
clawhub install skill-name

# 通过 ClawdHub
clawdhub install skill-name

# 手动克隆
git clone <repo> ~/.openclaw/workspace/skills/skill-name
```

---

## ⚠️ 重要规则

### QQBot 提醒
1. `payload.kind` 只能是 `"agentTurn"`
2. `deliver/channel/to` 缺一不可
3. `atMs` 直接用计算好的毫秒数
4. 周期任务用 `schedule.kind="cron"` + `expr` + `tz="Asia/Shanghai"`

### 图片发送
1. 使用 `<qqimg>路径</qqimg>` 标签
2. 绝对路径或网络 URL
3. ❌ 不要说"无法发送"

### 自改进
1. 错误 → `.learnings/ERRORS.md`
2. 纠正 → `.learnings/LEARNINGS.md` (category: correction)
3. 新功能 → `.learnings/FEATURE_REQUESTS.md`
4. 广泛适用 → 提升到 `AGENTS.md`, `SOUL.md`, `TOOLS.md`

---

## 📊 技能优先级

| 优先级 | 技能 | 说明 |
|--------|------|------|
| P0 | qqbot-cron | QQ 提醒核心功能 |
| P0 | qqbot-media | QQ 图片发送 |
| P1 | self-improvement | 持续改进机制 |
| P1 | proactive-agent | 主动行为模式 |
| P2 | searxng | 联网搜索（优先使用） |
| P2 | skill-vetter | 安全检查 |
| P3 | agent-browser | 浏览器自动化 |
| P3 | github/gitlab-review | 代码审查 |

---

## 🎯 快速参考

### 提醒
- 一次性：`schedule.kind="at"` + `atMs`
- 周期性：`schedule.kind="cron"` + `expr` + `tz`

### 图片
- `<qqimg>/path/to/image.png</qqimg>`

### 搜索
- `uv run scripts/searxng.py search "query"`

### 学习
- 错误 → `ERRORS.md`
- 纠正 → `LEARNINGS.md`
- 功能 → `FEATURE_REQUESTS.md`

---

**维护**: ClawOS  
**最后更新**: 2026-03-06 21:50
