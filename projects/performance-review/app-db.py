#!/usr/bin/env python3
"""
人员评分评价系统 - Web 应用 (SQLite 版本)

功能:
- 人员管理（增删改查）
- 评价记录
- 邀请评价
- 数据统计
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, g
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from datetime import datetime
import json
from pathlib import Path

# 导入数据库模型
from database import (
    engine, Member, Review, Issue, Invitation,
    SessionLocal, init_db, get_db
)

app = Flask(__name__)

# 配置
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 初始化数据库
init_db()

# ============== 数据库会话管理 ==============

@app.teardown_appcontext
def shutdown_session(exception=None):
    """请求结束时关闭数据库会话"""
    pass  # 使用 SessionLocal 管理


def get_session():
    """获取数据库会话"""
    return SessionLocal()


# ============== 辅助函数 ==============

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


def calculate_score(issues_data, bonuses=None, attitude_issue=False):
    """计算评分"""
    base_score = 5.0
    penalty = 0.0
    bonus_total = 0.0
    
    # 统计问题
    issue_count = {'P0': 0, 'P1': 0, 'P2': 0, 'P3': 0}
    for issue in issues_data:
        level = issue.get('level', 'P3')
        if level in issue_count:
            issue_count[level] += 1
        
        # 扣分
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
        # 加分
        if bonuses:
            for bonus in bonuses:
                if bonus == 'continuous_clean':
                    bonus_total += 0.5
                elif bonus == 'innovation':
                    bonus_total += 0.5
                elif bonus == 'fix_proactive':
                    bonus_total += 0.25
        
        # 态度问题扣分
        if attitude_issue:
            penalty += 1.0
        
        final_score = max(0, min(5.0, base_score - penalty + bonus_total))
    
    # 确定等级
    level_name, level_desc = get_level(final_score)
    
    return {
        "score": round(final_score, 2),
        "level": level_name,
        "description": level_desc,
        "details": {
            "base_score": base_score,
            "penalty": round(penalty, 2),
            "bonus": round(bonus_total, 2),
            "issue_count": issue_count
        }
    }


# ============== 页面路由 ==============

@app.route('/')
def index():
    """人员列表首页"""
    db = get_session()
    try:
        members = db.query(Member).filter_by(is_active=True).all()
        return render_template('index.html', members=members)
    finally:
        db.close()


@app.route('/invite')
def invite():
    """邀请评价页面"""
    db = get_session()
    try:
        members = db.query(Member).filter_by(is_active=True).all()
        return render_template('invite.html', members=members)
    finally:
        db.close()


@app.route('/invitations')
def invitations():
    """邀请记录页面"""
    db = get_session()
    try:
        invitations = db.query(Invitation).order_by(Invitation.created_at.desc()).all()
        return render_template('invitations.html', invitations=invitations)
    finally:
        db.close()


@app.route('/stats')
def stats():
    """统计页面"""
    db = get_session()
    try:
        total_members = db.query(Member).filter_by(is_active=True).count()
        total_reviews = db.query(Review).count()
        
        # 平均分
        reviews = db.query(Review).all()
        avg_score = sum(r.score for r in reviews) / len(reviews) if reviews else 0
        
        # 等级分布
        level_dist = {}
        for r in reviews:
            level_dist[r.level] = level_dist.get(r.level, 0) + 1
        
        # 人员排名
        member_scores = []
        members = db.query(Member).filter_by(is_active=True).all()
        for m in members:
            member_reviews = db.query(Review).filter_by(member_id=m.id).all()
            if member_reviews:
                avg = sum(r.score for r in member_reviews) / len(member_reviews)
                member_scores.append({
                    'name': m.name,
                    'score': round(avg, 2),
                    'count': len(member_reviews)
                })
        
        member_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return render_template('stats.html',
                             total_members=total_members,
                             total_reviews=total_reviews,
                             avg_score=round(avg_score, 2),
                             level_dist=level_dist,
                             rankings=member_scores)
    finally:
        db.close()


# ============== API 端点 ==============

@app.route('/api/members', methods=['GET'])
def api_get_members():
    """获取人员列表"""
    db = get_session()
    try:
        members = db.query(Member).filter_by(is_active=True).all()
        return jsonify([m.to_dict() for m in members])
    finally:
        db.close()


@app.route('/api/member/add', methods=['POST'])
def api_add_member():
    """添加人员"""
    data = request.json
    db = get_session()
    try:
        # 检查重名
        existing = db.query(Member).filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': '人员已存在'}), 400
        
        member = Member(
            name=data['name'],
            email=data.get('email', ''),
            department=data.get('department', '')
        )
        db.add(member)
        db.commit()
        
        return jsonify(member.to_dict()), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@app.route('/api/member/<int:member_id>', methods=['GET'])
def api_get_member(member_id):
    """获取人员详情"""
    db = get_session()
    try:
        member = db.query(Member).filter_by(id=member_id).first()
        if not member:
            return jsonify({'error': '人员不存在'}), 404
        return jsonify(member.to_dict())
    finally:
        db.close()


@app.route('/api/member/<int:member_id>/edit', methods=['PUT'])
def api_edit_member(member_id):
    """编辑人员"""
    data = request.json
    db = get_session()
    try:
        member = db.query(Member).filter_by(id=member_id).first()
        if not member:
            return jsonify({'error': '人员不存在'}), 404
        
        member.name = data.get('name', member.name)
        member.email = data.get('email', member.email)
        member.department = data.get('department', member.department)
        member.updated_at = datetime.now()
        
        db.commit()
        return jsonify(member.to_dict())
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@app.route('/api/member/<int:member_id>/edit', methods=['DELETE'])
def api_delete_member(member_id):
    """删除人员"""
    db = get_session()
    try:
        member = db.query(Member).filter_by(id=member_id).first()
        if not member:
            return jsonify({'error': '人员不存在'}), 404
        
        member.is_active = False
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@app.route('/api/review/add', methods=['POST'])
def api_add_review():
    """添加评价"""
    data = request.json
    db = get_session()
    try:
        # 计算评分
        issues_data = data.get('issues', [])
        bonuses = data.get('bonuses', [])
        attitude_issue = data.get('attitude_issue', False)
        
        score_data = calculate_score(issues_data, bonuses, attitude_issue)
        
        # 创建评价
        review = Review(
            member_id=data['member_id'],
            period=data.get('period', datetime.now().strftime('%Y-%m')),
            score=score_data['score'],
            level=score_data['level'],
            description=score_data['description'],
            details=json.dumps(score_data['details']),
            created_by=data.get('created_by', '')
        )
        db.add(review)
        db.commit()
        
        # 创建问题记录
        for issue_data in issues_data:
            issue = Issue(
                review_id=review.id,
                member_id=data['member_id'],
                level=issue_data.get('level', 'P3'),
                title=issue_data.get('title', ''),
                description=issue_data.get('description', ''),
                category=issue_data.get('category', ''),
                is_attitude=issue_data.get('is_attitude', False)
            )
            db.add(issue)
        db.commit()
        
        return jsonify(review.to_dict()), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@app.route('/api/reviews', methods=['GET'])
def api_get_reviews():
    """获取评价列表"""
    db = get_session()
    try:
        member_id = request.args.get('member_id', type=int)
        period = request.args.get('period')
        
        query = db.query(Review)
        if member_id:
            query = query.filter_by(member_id=member_id)
        if period:
            query = query.filter_by(period=period)
        
        reviews = query.order_by(Review.created_at.desc()).all()
        return jsonify([r.to_dict() for r in reviews])
    finally:
        db.close()


@app.route('/api/invitation/create', methods=['POST'])
def api_create_invitation():
    """创建邀请"""
    import secrets
    from datetime import timedelta
    
    data = request.json
    db = get_session()
    try:
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=7)
        
        invitation = Invitation(
            member_id=data.get('member_id'),
            reviewer_email=data['reviewer_email'],
            reviewer_name=data.get('reviewer_name', ''),
            token=token,
            expires_at=expires_at
        )
        db.add(invitation)
        db.commit()
        
        # TODO: 发送邮件
        
        return jsonify(invitation.to_dict()), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# ============== 健康检查和指标 ==============

@app.route('/health')
def health():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.2.0-sqlite',
        'database': 'sqlite'
    }), 200


@app.route('/metrics')
def metrics():
    """基础指标端点"""
    db = get_session()
    try:
        members_count = db.query(Member).filter_by(is_active=True).count()
        reviews_count = db.query(Review).count()
        avg_score = db.query(Review).all()
        avg = sum(r.score for r in avg_score) / len(avg_score) if avg_score else 0
        
        return jsonify({
            'members_count': members_count,
            'reviews_count': reviews_count,
            'average_score': round(avg, 2),
            'service': 'performance-review',
            'version': '1.2.0-sqlite',
            'database': 'sqlite'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


if __name__ == '__main__':
    # 生产环境请使用 gunicorn:
    # gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
