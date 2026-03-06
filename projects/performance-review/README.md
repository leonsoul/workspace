# 人员评分评价系统 👥

质量评分和评价管理系统

---

## 快速开始

### 启动服务

```bash
cd /home/admin/.openclaw/workspace/projects/performance-review

# 方式 1：直接启动
nohup python3 app.py > /tmp/performance-review.log 2>&1 &

# 方式 2：使用监控脚本（推荐）
bash monitor.sh

# 方式 3：带健康检查
nohup python3 health-check.py > /tmp/health-check.log 2>&1 &
```

### 检查状态

```bash
# 查看进程
ps aux | grep "python3 app.py"

# 查看日志
tail -f /tmp/performance-review.log

# 检查 HTTP
curl http://localhost:5000
```

### 计算评分

```bash
cd /home/admin/.openclaw/workspace/projects/performance-review
python3 calculate-score.py
```

### 添加评价

```python
from calculate_score import calculate_score, save_review

# 问题列表
issues = [
    {"level": "P1", "description": "登录功能异常"},
    {"level": "P2", "description": "UI 显示问题"}
]

# 加分项
bonuses = ["continuous_clean"]  # 连续 3 次无问题

# 计算评分
result = calculate_score(issues, bonuses, attitude_issue=False)

# 保存评价
save_review("张三", result, issues, period="2026-03")
```

### 3. 生成报告

```python
from calculate_score import generate_report

report = generate_report("张三", "2026-03")
print(report)
```

---

## 评分标准

| 分数 | 等级 | 条件 |
|------|------|------|
| 4.5+ | 卓越 | 无 P1 以上问题，长期稳定高质量 |
| 4.0+ | 优秀 | 无 P1 以上问题，提测质量优秀 |
| 3.75+ | 良好 | 无 P1 以上问题，提测质量较好 |
| 3.5 | 正常 | ≤1 个 P1 问题，合格 |
| 3.0 | 及格 | ≤1 个 P1 问题，勉强及格 |
| 2.0 | 质量差 | >1 个 P1 问题 |
| 1.0 | 严重质量问题 | 有 P0 问题 |
| 0 | 完全不符合 | 质量特别差 + 态度差 |

---

## 问题等级

| 等级 | 定义 | 扣分 |
|------|------|------|
| P0 | 致命问题 | -5 分 (直接到 0) |
| P1 | 严重问题 | -2 分 |
| P2 | 一般问题 | -0.5 分 |
| P3 | 轻微问题 | -0.25 分 |

---

## 加分项

| 项目 | 说明 | 加分 |
|------|------|------|
| continuous_clean | 连续 3 次无问题 | +0.5 |
| innovation | 技术创新/优化 | +0.5 |
| fix_proactive | 主动修复问题 | +0.25 |

---

## 文件结构

```
performance-review/
├── README.md                  # 使用说明
├── review-system.md           # 系统文档
├── calculate-score.py         # 评分计算器
└── data/
    ├── members/               # 人员档案
    │   └── 姓名.json
    ├── reviews/               # 评价记录
    │   └── YYYY-MM/
    │       └── 姓名.json
    └── issues/                # 问题记录
```

---

## 人员档案示例

```json
{
  "name": "张三",
  "created_at": "2026-03-06T12:00:00",
  "reviews": [
    {"period": "2026-03", "score": 3.5, "level": "正常"},
    {"period": "2026-04", "score": 4.0, "level": "优秀"}
  ],
  "total_reviews": 2,
  "average_score": 3.75
}
```

---

## 评价记录示例

```json
{
  "member": "张三",
  "period": "2026-03",
  "timestamp": "2026-03-06T12:00:00",
  "score": 3.5,
  "level": "正常",
  "description": "不多于 1 个 P1 及以上问题，提测质量合格",
  "details": {
    "base_score": 5.0,
    "penalty": 1.5,
    "bonus": 0,
    "issue_count": {"P0": 0, "P1": 0, "P2": 3, "P3": 0}
  },
  "issues": [...]
}
```

---

## 自动化集成

### 与 Git 集成

每次提测后自动记录：

```bash
# Git hook: post-commit
python3 /path/to/calculate-score.py --member "张三" --issues "P1:登录问题,P2:UI 问题"
```

### 与钉钉集成

评价完成后自动通知：

```python
from dingtalk import send_message

send_message(
    to="张三",
    content=f"本月评价：{score}分 - {level}"
)
```

---

## 最佳实践

1. **及时记录**: 每次提测后立即记录问题
2. **客观公正**: 问题等级要统一标准
3. **定期回顾**: 每月生成评价报告
4. **正向激励**: 多关注加分项，鼓励改进
5. **数据驱动**: 用数据说话，避免主观评价

---

**Version**: 1.0  
**Created**: 2026-03-06  
**Author**: ClawOS Dev Agent
