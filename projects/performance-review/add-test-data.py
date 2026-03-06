#!/usr/bin/env python3
"""
添加测试数据
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/projects/performance-review')

from database import Member, Review, Issue, SessionLocal, init_db
from datetime import datetime
import random

def add_test_data():
    """添加测试数据"""
    init_db()
    db = SessionLocal()
    
    try:
        # 添加人员
        members_data = [
            {'name': '张三', 'email': 'zhangsan@example.com', 'department': '研发部'},
            {'name': '李四', 'email': 'lisi@example.com', 'department': '测试部'},
            {'name': '王五', 'email': 'wangwu@example.com', 'department': '产品部'},
            {'name': '赵六', 'email': 'zhaoliu@example.com', 'department': '研发部'},
            {'name': '孙七', 'email': 'sunqi@example.com', 'department': '设计部'},
        ]
        
        print("📝 添加人员...")
        for m in members_data:
            # 检查是否已存在
            existing = db.query(Member).filter_by(name=m['name']).first()
            if not existing:
                member = Member(**m)
                db.add(member)
                print(f"   + {m['name']}")
            else:
                print(f"   ✓ {m['name']} (已存在)")
        db.commit()
        
        members = db.query(Member).filter_by(is_active=True).all()
        print(f"✅ 共有 {len(members)} 个人员")
        
        # 添加评价
        levels = ['卓越', '优秀', '良好', '正常', '及格']
        scores = [4.8, 4.3, 3.9, 3.6, 3.2]
        
        print("📝 添加评价记录...")
        for member in members:
            for i in range(3):  # 每人 3 条评价
                idx = random.randint(0, len(levels)-1)
                review = Review(
                    member_id=member.id,
                    period=f"2026-{random.randint(1,3):02d}",
                    score=scores[idx],
                    level=levels[idx],
                    description=f"{member.name} 在 {i+1} 月份表现{levels[idx]}",
                    details='{"base_score": 5.0, "penalty": 0.5, "bonus": 0.25}',
                    created_by='系统'
                )
                db.add(review)
                db.commit()  # 先 commit review 获取 ID
                
                # 添加一些问题
                if idx > 2:  # 评分较低时添加问题
                    issue = Issue(
                        review_id=review.id,
                        member_id=member.id,
                        level='P2',
                        title='功能缺陷',
                        description='测试发现的问题',
                        category='功能'
                    )
                    db.add(issue)
                    db.commit()
        
        # 统计
        reviews = db.query(Review).all()
        issues = db.query(Issue).all()
        
        print(f"✅ 已添加 {len(reviews)} 条评价")
        print(f"✅ 已添加 {len(issues)} 个问题")
        
        # 显示统计
        print("\n📊 数据统计:")
        for member in members:
            member_reviews = db.query(Review).filter_by(member_id=member.id).all()
            if member_reviews:
                avg = sum(r.score for r in member_reviews) / len(member_reviews)
                print(f"   {member.name}: {len(member_reviews)} 条评价，平均分 {avg:.2f}")
        
        print("\n🎉 测试数据添加完成！")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 添加失败：{e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == '__main__':
    add_test_data()
