# Model Strategy 模型策略

为不同 Agent 分配合适的模型

---

## 可用模型

### dashscope（阿里云 - 国内）
| 模型 | Context | Max Tokens | 特点 |
|------|---------|-----------|------|
| `qwen3-max-2026-01-23` | 262K | 65K | 推理能力强 |
| `qwen3.5-plus` | **1000K** | 65K | 通用/性价比高 |

### dashscope-us（阿里云 - 美国）
| 模型 | Context | Max Tokens | 特点 |
|------|---------|-----------|------|
| `qwen3-max-2025-09-23` | 32K | 8K | 简单任务 |
| `qwen3-vl-plus` | 32K | 8K | **视觉/图片** |

### dashscope-coding（编码专用）
| 模型 | Context | Max Tokens | 特点 |
|------|---------|-----------|------|
| `qwen3.5-plus` | **1000K** | 65K | **代码优化** |

---

## Agent 模型分配

| Agent | 推荐模型 | 原因 | 优先级 |
|-------|---------|------|--------|
| **Dev Agent** | `dashscope-coding/qwen3.5-plus` | 编码专用，1M context | P0 |
| **QA Agent** | `dashscope/qwen3.5-plus` | 通用，大上下文 | P0 |
| **Ops Agent** | `dashscope/qwen3.5-plus` | 稳定，大上下文 | P0 |
| **Data Agent** | `dashscope/qwen3-max-2026-01-23` | 复杂分析推理 | P1 |
| **Media Agent** | `dashscope/qwen3-vl-plus` | 图片分析专用 | P0 |
| **Code Review** | `dashscope-coding/qwen3.5-plus` | 代码审查专用 | P1 |
| **Deploy Agent** | `dashscope/qwen3.5-plus` | 稳定为主 | P1 |
| **Monitor Agent** | `dashscope/qwen3.5-plus` | 监控告警 | P2 |
| **Research Agent** | `dashscope/qwen3-max-2026-01-23` | 信息整合推理 | P2 |

---

## 配置方式

### 方式 1：独立 Agent Session（推荐）

为每个 Agent 创建独立 session 配置：

```bash
# Dev Agent
mkdir -p ~/.openclaw/agents/dev-agent
cat > ~/.openclaw/agents/dev-agent/config.json << EOF
{
  "model": "dashscope-coding/qwen3.5-plus"
}
EOF

# QA Agent
mkdir -p ~/.openclaw/agents/qa-agent
cat > ~/.openclaw/agents/qa-agent/config.json << EOF
{
  "model": "dashscope/qwen3.5-plus"
}
EOF

# Data Agent
mkdir -p ~/.openclaw/agents/data-agent
cat > ~/.openclaw/agents/data-agent/config.json << EOF
{
  "model": "dashscope/qwen3-max-2026-01-23"
}
EOF

# Media Agent
mkdir -p ~/.openclaw/agents/media-agent
cat > ~/.openclaw/agents/media-agent/config.json << EOF
{
  "imageModel": "dashscope/qwen3-vl-plus"
}
EOF
```

### 方式 2：任务中指定

在任务描述中明确模型：

```
用户：用 qwen3-max 分析这个数据集
→ Data Agent 自动使用 qwen3-max-2026-01-23

用户：用 coding 模型写个脚本
→ Dev Agent 自动使用 dashscope-coding/qwen3.5-plus
```

### 方式 3：修改全局默认

编辑 `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "dashscope-coding/qwen3.5-plus"
      },
      "imageModel": {
        "primary": "dashscope/qwen3-vl-plus"
      }
    }
  }
}
```

---

## 使用场景

### Dev Agent（编码）
```
任务：写个 Python 脚本
模型：dashscope-coding/qwen3.5-plus
原因：代码生成优化，1M context 支持大项目
```

### Data Agent（分析）
```
任务：分析销售数据趋势
模型：dashscope/qwen3-max-2026-01-23
原因：推理能力强，适合复杂分析
```

### Media Agent（图片）
```
任务：分析这张图片内容
模型：dashscope/qwen3-vl-plus
原因：视觉模型专用
```

### QA Agent（测试）
```
任务：生成测试用例
模型：dashscope/qwen3.5-plus
原因：通用能力强，性价比高
```

---

## 成本优化

| 任务类型 | 推荐模型 | 原因 |
|---------|---------|------|
| 简单问答 | `qwen3.5-plus` | 便宜，快速 |
| 代码生成 | `dashscope-coding/qwen3.5-plus` | 优化过 |
| 复杂推理 | `qwen3-max-2026-01-23` | 能力强 |
| 图片分析 | `qwen3-vl-plus` | 专用 |
| 长文档 | `qwen3.5-plus` (1M) | 上下文大 |

---

## 性能对比

| 模型 | 推理速度 | 准确率 | 成本 | 适用场景 |
|------|---------|--------|------|---------|
| `qwen3.5-plus` | ⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 | 通用 |
| `qwen3-max-2026-01-23` | ⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰 | 复杂推理 |
| `qwen3-vl-plus` | ⚡⚡ | ⭐⭐⭐⭐ | 💰💰 | 图片 |
| `qwen3-max-2025-09-23` | ⚡⚡⚡ | ⭐⭐⭐ | 💰 | 简单任务 |

---

## 最佳实践

1. **代码相关** → 优先 `dashscope-coding/qwen3.5-plus`
2. **数据分析** → 优先 `qwen3-max-2026-01-23`
3. **图片处理** → 必须 `qwen3-vl-plus`
4. **日常任务** → 默认 `qwen3.5-plus`
5. **长文档** → 选 1M context 的模型

---

## 监控和调整

定期检查：
- 哪些 Agent 用哪个模型
- 任务完成质量
- 响应时间
- 成本消耗

根据反馈调整模型分配。

---

**Version**: 1.0  
**Last Updated**: 2026-03-06  
**Config**: `~/.openclaw/openclaw.json`
