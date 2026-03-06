# Task Router - 任务路由规则

## Intent Recognition

### 关键词匹配

| Agent | 关键词 | 示例 |
|-------|--------|------|
| **dev-agent** | 代码、开发、写、创建、脚本、API、功能、实现、编程、Python、JavaScript、Bash | "写个 Python 脚本"、"创建 API" |
| **qa-agent** | 测试、bug、错误、检查、验证、问题、故障、修复、审查、质量 | "测试这个"、"有 bug" |
| **ops-agent** | 部署、服务器、监控、cron、定时、服务、系统、运维、备份、日志 | "部署到服务器"、"设置 cron" |
| **data-agent** | 数据、分析、转换、JSON、CSV、处理、统计、导入、导出、清洗 | "分析这个数据"、"JSON 转 CSV" |
| **media-agent** | 图片、视频、音频、媒体、压缩、转换、OCR、截图、下载 | "处理这张图片"、"视频转 GIF" |

## Routing Logic

```python
def select_agent(task: str) -> str:
    """
    根据任务描述选择最合适的 Agent
    """
    task_lower = task.lower()
    
    # 计分制：匹配关键词越多，分数越高
    scores = {
        'dev-agent': 0,
        'qa-agent': 0,
        'ops-agent': 0,
        'data-agent': 0,
        'media-agent': 0
    }
    
    # Dev Agent 关键词
    dev_keywords = ['代码', '开发', '写', '创建', '脚本', 'api', '功能', '实现', 
                    '编程', 'python', 'javascript', 'bash', '函数', '模块', '库']
    for kw in dev_keywords:
        if kw in task_lower:
            scores['dev-agent'] += 1
    
    # QA Agent 关键词
    qa_keywords = ['测试', 'bug', '错误', '检查', '验证', '问题', '故障', 
                   '修复', '审查', '质量', '异常', '失败', '报错']
    for kw in qa_keywords:
        if kw in task_lower:
            scores['qa-agent'] += 1
    
    # Ops Agent 关键词
    ops_keywords = ['部署', '服务器', '监控', 'cron', '定时', '服务', '系统',
                    '运维', '备份', '日志', '重启', '安装', '配置', 'nginx', 'docker']
    for kw in ops_keywords:
        if kw in task_lower:
            scores['ops-agent'] += 1
    
    # Data Agent 关键词
    data_keywords = ['数据', '分析', '转换', 'json', 'csv', '处理', '统计',
                     '导入', '导出', '清洗', '解析', 'xml', 'yaml', '数据库']
    for kw in data_keywords:
        if kw in task_lower:
            scores['data-agent'] += 1
    
    # Media Agent 关键词
    media_keywords = ['图片', '视频', '音频', '媒体', '压缩', '转换', 'ocr',
                      '截图', '下载', 'jpg', 'png', 'mp4', 'gif', 'ffmpeg']
    for kw in media_keywords:
        if kw in task_lower:
            scores['media-agent'] += 1
    
    # 返回分数最高的 Agent
    best_agent = max(scores, key=scores.get)
    
    # 如果最高分是 0，返回 orchestrator（默认处理）
    if scores[best_agent] == 0:
        return 'orchestrator'
    
    return best_agent
```

## Examples

| 任务 | 路由 | 原因 |
|------|------|------|
| "写个 Python 脚本备份文件" | dev-agent | "写"、"Python"、"脚本" |
| "测试这个功能有没有 bug" | qa-agent | "测试"、"bug" |
| "部署到服务器并设置监控" | ops-agent | "部署"、"服务器"、"监控" |
| "把 JSON 数据转成 CSV" | data-agent | "JSON"、"CSV"、"转换" |
| "压缩这张图片" | media-agent | "图片"、"压缩" |
| "分析一下销售数据" | data-agent | "分析"、"数据" |
| "检查代码质量" | qa-agent | "检查"、"代码"、"质量" |
| "设置每天凌晨备份" | ops-agent | "备份"、"每天"（cron） |
| "视频转成 GIF" | media-agent | "视频"、"GIF"、"转换" |
| "你好，介绍一下自己" | orchestrator | 无匹配关键词 |

## Fallback Rules

1. **多 Agent 协作**: 任务涉及多个领域时，选择主要 Agent，并在输出中标注需要协作的 Agent
2. **不确定时**: 返回 `orchestrator`，由主 AI 直接处理
3. **用户指定**: 如果用户明确说"用 XX agent"，优先遵循

## Handoff Format

当需要转交其他 Agent 时：

```markdown
---
## 任务转交
- **原始任务**: XXX
- **当前 Agent**: XXX
- **转交目标**: XXX
- **原因**: XXX
- **已完成**: XXX
- **待处理**: XXX
---
```

---

**Version**: 1.0
**Last Updated**: 2026-03-06
