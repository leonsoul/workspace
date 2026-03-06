#!/usr/bin/env python3
"""
人员评分评价系统 - Web 应用

功能:
- 人员管理（增删改查）
- 评价记录
- 邀请评价
- 数据统计
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from datetime import datetime
from pathlib import Path
import os

app = Flask(__name__)

# 配置
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MEMBERS_FILE = DATA_DIR / "members.json"
REVIEWS_FILE = DATA_DIR / "reviews.json"
INVITATIONS_FILE = DATA_DIR / "invitations.json"

# 确保目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 初始化数据文件
def init_data():
    if not MEMBERS_FILE.exists():
        with open(MEMBERS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    
    if not REVIEWS_FILE.exists():
        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    
    if not INVITATIONS_FILE.exists():
        with open(INVITATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

# 评分等级
LEVELS = [
    (4.5, "卓越", "#9333EA"),
    (4.0, "优秀", "#10B981"),
    (3.75, "良好", "#3B82F6"),
    (3.5, "正常", "#6B7280"),
    (3.0, "及格", "#F59E0B"),
    (2.0, "质量差", "#EF4444"),
    (1.0, "严重质量问题", "#DC2626"),
    (0.0, "完全不符合", "#991B1B")
]

def get_level(score):
    """根据分数获取等级"""
    for threshold, name, color in LEVELS:
        if score >= threshold:
            return name, color
    return "完全不符合", "#991B1B"

def load_members():
    """加载人员列表"""
    with open(MEMBERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_members(members):
    """保存人员列表"""
    with open(MEMBERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(members, f, ensure_ascii=False, indent=2)

def load_reviews():
    """加载评价记录"""
    with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_review(review):
    """保存评价"""
    reviews = load_reviews()
    reviews.append(review)
    with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

def load_invitations():
    """加载邀请记录"""
    with open(INVITATIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_invitation(invitation):
    """保存邀请"""
    invitations = load_invitations()
    invitations.append(invitation)
    with open(INVITATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(invitations, f, ensure_ascii=False, indent=2)

def calculate_score(issues, bonuses=None, attitude_issue=False):
    """计算评分"""
    base_score = 5.0
    penalty = 0.0
    bonus_score = 0.0
    
    issue_count = {'P0': 0, 'P1': 0, 'P2': 0, 'P3': 0}
    for issue in issues:
        level = issue.get('level', 'P3')
        if level in issue_count:
            issue_count[level] += 1
        
        if level == 'P0':
            penalty += 5.0
        elif level == 'P1':
            penalty += 2.0
        elif level == 'P2':
            penalty += 0.5
        elif level == 'P3':
            penalty += 0.25
    
    # P0 直接到 0
    if issue_count['P0'] > 0:
        final_score = 0.0
    else:
        if bonuses:
            for bonus in bonuses:
                if bonus == 'continuous_clean':
                    bonus_score += 0.5
                elif bonus == 'innovation':
                    bonus_score += 0.5
                elif bonus == 'fix_proactive':
                    bonus_score += 0.25
        
        if attitude_issue:
            penalty += 1.0
        
        final_score = max(0, min(5.0, base_score - penalty + bonus_score))
    
    level_name, level_color = get_level(final_score)
    
    return {
        "score": round(final_score, 2),
        "level": level_name,
        "color": level_color,
        "details": {
            "base": base_score,
            "penalty": round(penalty, 2),
            "bonus": round(bonus_score, 2),
            "issue_count": issue_count
        }
    }

# ============ Routes ============

@app.route('/')
def index():
    """首页 - 人员列表"""
    members = load_members()
    reviews = load_reviews()
    
    # 计算每个人的平均分
    for member in members:
        member_reviews = [r for r in reviews if r.get('member_id') == member['id']]
        if member_reviews:
            member['average_score'] = round(sum(r['score'] for r in member_reviews) / len(member_reviews), 2)
            member['review_count'] = len(member_reviews)
            level_name, level_color = get_level(member['average_score'])
            member['level'] = level_name
            member['color'] = level_color
        else:
            member['average_score'] = 0
            member['review_count'] = 0
            member['level'] = '未评价'
            member['color'] = '#6B7280'
    
    return render_template('index.html', members=members)

@app.route('/member/add', methods=['GET', 'POST'])
def add_member():
    """添加人员"""
    if request.method == 'POST':
        data = request.json
        members = load_members()
        
        new_member = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'name': data['name'],
            'email': data.get('email', ''),
            'department': data.get('department', ''),
            'created_at': datetime.now().isoformat()
        }
        
        members.append(new_member)
        save_members(members)
        
        return jsonify({'success': True, 'member': new_member})
    
    return render_template('add_member.html')

@app.route('/member/<member_id>/edit', methods=['GET', 'PUT', 'DELETE'])
def edit_member(member_id):
    """编辑/删除人员"""
    members = load_members()
    member = next((m for m in members if m['id'] == member_id), None)
    
    if not member:
        return jsonify({'success': False, 'error': '人员不存在'}), 404
    
    if request.method == 'DELETE':
        members = [m for m in members if m['id'] != member_id]
        save_members(members)
        return jsonify({'success': True})
    
    if request.method == 'PUT':
        data = request.json
        member['name'] = data.get('name', member['name'])
        member['email'] = data.get('email', member['email'])
        member['department'] = data.get('department', member['department'])
        member['updated_at'] = datetime.now().isoformat()
        save_members(members)
        return jsonify({'success': True, 'member': member})
    
    return jsonify({'success': True, 'member': member})

@app.route('/member/<member_id>/review', methods=['GET', 'POST'])
def review_member(member_id):
    """评价人员"""
    members = load_members()
    member = next((m for m in members if m['id'] == member_id), None)
    
    if not member:
        return jsonify({'success': False, 'error': '人员不存在'}), 404
    
    if request.method == 'POST':
        data = request.json
        
        issues = data.get('issues', [])
        bonuses = data.get('bonuses', [])
        attitude_issue = data.get('attitude_issue', False)
        comment = data.get('comment', '')
        
        score_result = calculate_score(issues, bonuses, attitude_issue)
        
        review = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'member_id': member_id,
            'member_name': member['name'],
            'score': score_result['score'],
            'level': score_result['level'],
            'color': score_result['color'],
            'details': score_result['details'],
            'issues': issues,
            'bonuses': bonuses,
            'attitude_issue': attitude_issue,
            'comment': comment,
            'reviewer': data.get('reviewer', '系统'),
            'created_at': datetime.now().isoformat()
        }
        
        save_review(review)
        
        return jsonify({'success': True, 'review': review})
    
    return render_template('review.html', member=member)

@app.route('/member/<member_id>/history')
def member_history(member_id):
    """查看人员评价历史"""
    members = load_members()
    member = next((m for m in members if m['id'] == member_id), None)
    
    if not member:
        return jsonify({'success': False, 'error': '人员不存在'}), 404
    
    reviews = load_reviews()
    member_reviews = [r for r in reviews if r.get('member_id') == member_id]
    
    # 按时间倒序
    member_reviews.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return render_template('history.html', member=member, reviews=member_reviews)

@app.route('/invite', methods=['GET', 'POST'])
def invite():
    """邀请评价"""
    if request.method == 'POST':
        data = request.json
        
        invitation = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'member_id': data['member_id'],
            'member_name': data['member_name'],
            'invitee_email': data['invitee_email'],
            'invitee_name': data.get('invitee_name', ''),
            'message': data.get('message', ''),
            'status': 'pending',  # pending, accepted, completed
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now().timestamp() + 7*24*3600) * 1000  # 7 天过期
        }
        
        save_invitation(invitation)
        
        # TODO: 发送邮件/钉钉通知
        # send_invitation_email(invitation)
        
        return jsonify({'success': True, 'invitation': invitation})
    
    members = load_members()
    return render_template('invite.html', members=members)

@app.route('/invitations')
def invitations():
    """邀请记录"""
    invitations = load_invitations()
    invitations.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    # 添加时间转换辅助函数
    def timestamp_to_date(ts):
        try:
            if isinstance(ts, (int, float)):
                return datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d')
            return datetime.fromisoformat(ts[:19]).strftime('%Y-%m-%d')
        except:
            return '未知'
    
    app.jinja_env.filters['timestamp_to_date'] = timestamp_to_date
    
    return render_template('invitations.html', invitations=invitations)

@app.route('/stats')
def stats():
    """统计页面"""
    members = load_members()
    reviews = load_reviews()
    
    # 统计
    total_members = len(members)
    total_reviews = len(reviews)
    
    if reviews:
        avg_score = round(sum(r['score'] for r in reviews) / len(reviews), 2)
    else:
        avg_score = 0
    
    # 等级分布
    level_dist = {}
    for review in reviews:
        level = review.get('level', '未知')
        level_dist[level] = level_dist.get(level, 0) + 1
    
    # 排名
    member_scores = []
    for member in members:
        member_reviews = [r for r in reviews if r.get('member_id') == member['id']]
        if member_reviews:
            avg = round(sum(r['score'] for r in member_reviews) / len(member_reviews), 2)
            member_scores.append({
                'name': member['name'],
                'score': avg,
                'count': len(member_reviews)
            })
    
    member_scores.sort(key=lambda x: x['score'], reverse=True)
    
    return render_template('stats.html', 
                         total_members=total_members,
                         total_reviews=total_reviews,
                         avg_score=avg_score,
                         level_dist=level_dist,
                         rankings=member_scores)

if __name__ == '__main__':
    init_data()
    app.run(host='0.0.0.0', port=5000, debug=True)
