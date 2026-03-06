#!/usr/bin/env python3
"""
人员评分计算器

评分规则:
- 基础分：5 分
- P0 问题：-5 分/个 (直接到 0)
- P1 问题：-2 分/个
- P2 问题：-0.5 分/个
- P3 问题：-0.25 分/个
- 态度问题：-1 分
- 连续无问题：+0.5 分
- 技术创新：+0.5 分/次
"""

import json
from datetime import datetime
from pathlib import Path

# 配置
DATA_DIR = Path("/home/admin/.openclaw/workspace/projects/performance-review/data")
MEMBERS_DIR = DATA_DIR / "members"
REVIEWS_DIR = DATA_DIR / "reviews"
ISSUES_DIR = DATA_DIR / "issues"

# 确保目录存在
for d in [MEMBERS_DIR, REVIEWS_DIR, ISSUES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 扣分权重
PENALTY = {
    'P0': 5.0,   # 直接到 0
    'P1': 2.0,
    'P2': 0.5,
    'P3': 0.25,
    'attitude': 1.0
}

# 加分项
BONUS = {
    'continuous_clean': 0.5,  # 连续 3 次无问题
    'innovation': 0.5,        # 技术创新
    'fix_proactive': 0.25     # 主动修复
}

# 等级定义
LEVELS = [
    (4.5, "卓越", "无 P1 以上问题，长期稳定高质量"),
    (4.0, "优秀", "无 P1 以上问题，提测质量优秀"),
    (3.75, "良好", "无 P1 以上问题，提测质量较好"),
    (3.5, "正常", "不多于 1 个 P1 及以上问题，提测质量合格"),
    (3.0, "及格", "不多于 1 个 P1 及以上问题，提测质量勉强及格"),
    (2.0, "质量差", "多于 1 个 P1 问题，提测基本不可用"),
    (1.0, "严重质量问题", "有 P0 严重问题"),
    (0.0, "完全不符合", "质量特别差，态度差")
]


def calculate_score(issues, bonuses=None, attitude_issue=False):
    """
    计算评分
    
    Args:
        issues: 问题列表 [{"level": "P1", "description": "..."}, ...]
        bonuses: 加分项列表 ["continuous_clean", "innovation", ...]
        attitude_issue: 是否有态度问题
    
    Returns:
        dict: {"score": 3.5, "level": "正常", "description": "...", "details": {...}}
    """
    base_score = 5.0
    penalty_total = 0.0
    bonus_total = 0.0
    
    # 统计问题
    issue_count = {'P0': 0, 'P1': 0, 'P2': 0, 'P3': 0}
    for issue in issues:
        level = issue.get('level', 'P3')
        if level in issue_count:
            issue_count[level] += 1
        penalty_total += PENALTY.get(level, 0.25)
    
    # P0 直接到 0
    if issue_count['P0'] > 0:
        final_score = 0.0
    else:
        # 计算加分
        if bonuses:
            for bonus in bonuses:
                bonus_total += BONUS.get(bonus, 0)
        
        # 态度问题扣分
        if attitude_issue:
            penalty_total += PENALTY['attitude']
        
        # 最终分数
        final_score = max(0, min(5.0, base_score - penalty_total + bonus_total))
    
    # 确定等级
    level_name = "完全不符合"
    level_desc = "质量特别差，态度差"
    for threshold, name, desc in LEVELS:
        if final_score >= threshold:
            level_name = name
            level_desc = desc
            break
    
    return {
        "score": round(final_score, 2),
        "level": level_name,
        "description": level_desc,
        "details": {
            "base_score": base_score,
            "penalty": round(penalty_total, 2),
            "bonus": round(bonus_total, 2),
            "issue_count": issue_count
        }
    }


def get_level_description(score):
    """根据分数获取等级描述"""
    for threshold, name, desc in LEVELS:
        if score >= threshold:
            return name, desc
    return "完全不符合", "质量特别差，态度差"


def save_review(member_name, score_data, issues, period=None):
    """保存评价记录"""
    if period is None:
        period = datetime.now().strftime("%Y-%m")
    
    review = {
        "member": member_name,
        "period": period,
        "timestamp": datetime.now().isoformat(),
        "score": score_data["score"],
        "level": score_data["level"],
        "description": score_data["description"],
        "details": score_data["details"],
        "issues": issues
    }
    
    # 保存到文件
    review_file = REVIEWS_DIR / period / f"{member_name}.json"
    review_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(review_file, 'w', encoding='utf-8') as f:
        json.dump(review, f, ensure_ascii=False, indent=2)
    
    # 更新人员档案
    update_member_profile(member_name, review)
    
    return review


def update_member_profile(member_name, new_review):
    """更新人员档案"""
    profile_file = MEMBERS_DIR / f"{member_name}.json"
    
    if profile_file.exists():
        with open(profile_file, 'r', encoding='utf-8') as f:
            profile = json.load(f)
    else:
        profile = {
            "name": member_name,
            "created_at": datetime.now().isoformat(),
            "reviews": [],
            "total_reviews": 0,
            "average_score": 0
        }
    
    profile["reviews"].append({
        "period": new_review["period"],
        "score": new_review["score"],
        "level": new_review["level"]
    })
    profile["total_reviews"] = len(profile["reviews"])
    
    # 计算平均分
    scores = [r["score"] for r in profile["reviews"]]
    profile["average_score"] = round(sum(scores) / len(scores), 2) if scores else 0
    
    with open(profile_file, 'w', encoding='utf-8') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def generate_report(member_name, period=None):
    """生成评价报告"""
    if period is None:
        period = datetime.now().strftime("%Y-%m")
    
    review_file = REVIEWS_DIR / period / f"{member_name}.json"
    
    if not review_file.exists():
        return f"未找到 {member_name} 在 {period} 的评价记录"
    
    with open(review_file, 'r', encoding='utf-8') as f:
        review = json.load(f)
    
    report = f"""
# {member_name} - {period} 评价报告

## 评分结果
- **分数**: {review['score']} / 5.0
- **等级**: {review['level']}
- **评价**: {review['description']}

## 问题统计
| 等级 | 数量 | 扣分 |
|------|------|------|
| P0 | {review['details']['issue_count']['P0']} | -{review['details']['issue_count']['P0'] * 5} |
| P1 | {review['details']['issue_count']['P1']} | -{review['details']['issue_count']['P1'] * 2} |
| P2 | {review['details']['issue_count']['P2']} | -{review['details']['issue_count']['P2'] * 0.5} |
| P3 | {review['details']['issue_count']['P3']} | -{review['details']['issue_count']['P3'] * 0.25} |

## 分数计算
- 基础分：{review['details']['base_score']}
- 扣分：-{review['details']['penalty']}
- 加分：+{review['details']['bonus']}
- **最终**: {review['score']}

## 改进建议
根据当前评分，建议：
1. 减少 P1/P2 问题数量
2. 提高提测质量
3. 加强自测

---
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return report


# 示例使用
if __name__ == "__main__":
    # 示例：计算评分
    issues = [
        {"level": "P1", "description": "登录功能异常"},
        {"level": "P2", "description": "UI 显示问题"}
    ]
    
    bonuses = ["continuous_clean"]
    
    result = calculate_score(issues, bonuses, attitude_issue=False)
    
    print(f"评分：{result['score']}")
    print(f"等级：{result['level']}")
    print(f"评价：{result['description']}")
    print(f"详情：{result['details']}")
