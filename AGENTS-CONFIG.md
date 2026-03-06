# Agents Configuration 配置

每个 Agent 的独立模型配置

---

## 已配置 Agents

| Agent | 模型 | Image 模型 | 配置路径 |
|-------|------|-----------|---------|
| 🛠️ Dev Agent | `dashscope-coding/qwen3.5-plus` | - | `~/.openclaw/agents/dev-agent/config.json` |
| 🧪 QA Agent | `dashscope/qwen3.5-plus` | - | `~/.openclaw/agents/qa-agent/config.json` |
| 🚀 Ops Agent | `dashscope/qwen3.5-plus` | - | `~/.openclaw/agents/ops-agent/config.json` |
| 📊 Data Agent | `dashscope/qwen3-max-2026-01-23` | - | `~/.openclaw/agents/data-agent/config.json` |
| 🎨 Media Agent | `dashscope/qwen3.5-plus` | `dashscope/qwen3-vl-plus` | `~/.openclaw/agents/media-agent/config.json` |

---

## 配置文件

### Dev Agent
```json
{
  "model": "dashscope-coding/qwen3.5-plus",
  "description": "Dev Agent - 代码开发专用模型",
  "reason": "编码优化，1M context 支持大项目"
}
```

### QA Agent
```json
{
  "model": "dashscope/qwen3.5-plus",
  "description": "QA Agent - 测试质量保障",
  "reason": "通用能力强，性价比高，大上下文"
}
```

### Ops Agent
```json
{
  "model": "dashscope/qwen3.5-plus",
  "description": "Ops Agent - 运维部署监控",
  "reason": "稳定，大上下文，适合运维场景"
}
```

### Data Agent
```json
{
  "model": "dashscope/qwen3-max-2026-01-23",
  "description": "Data Agent - 数据分析推理",
  "reason": "推理能力强，适合复杂数据分析"
}
```

### Media Agent
```json
{
  "model": "dashscope/qwen3.5-plus",
  "imageModel": "dashscope/qwen3-vl-plus",
  "description": "Media Agent - 媒体处理",
  "reason": "图片分析必须用 qwen3-vl-plus"
}
```

---

## 验证配置

```bash
# 查看所有配置
cat ~/.openclaw/agents/*/config.json

# 查看特定 Agent
cat ~/.openclaw/agents/dev-agent/config.json
```

---

## 修改配置

编辑对应配置文件：

```bash
# 例如修改 Dev Agent
nano ~/.openclaw/agents/dev-agent/config.json

# 重启 Agent（如需要）
openclaw restart
```

---

## 相关文档

- `MODEL-STRATEGY.md` - 模型策略总览
- `ARCHITECTURE.md` - 系统架构
- `AGENTS-OVERVIEW.md` - Agents 总览

---

**Version**: 1.0  
**Last Updated**: 2026-03-06  
**Config Path**: `~/.openclaw/agents/*/config.json`
