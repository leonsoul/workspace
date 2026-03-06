#!/usr/bin/env python3
"""
人员评价系统 - 数据库模型

使用 SQLAlchemy ORM 替代 JSON 文件存储
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import json

Base = declarative_base()

# 数据库配置
DATABASE_URL = "sqlite:////home/admin/.openclaw/workspace/projects/performance-review/data/performance.db"

engine = create_engine(DATABASE_URL, echo=False, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Member(Base):
    """人员表"""
    __tablename__ = 'members'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    department = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    
    # 关联评价
    reviews = relationship("Review", back_populates="member", cascade="all, delete-orphan")
    issues = relationship("Issue", back_populates="member", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'review_count': len(self.reviews),
            'average_score': self.get_average_score()
        }
    
    def get_average_score(self):
        if not self.reviews:
            return 0.0
        scores = [r.score for r in self.reviews]
        return round(sum(scores) / len(scores), 2)


class Review(Base):
    """评价记录表"""
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False, index=True)
    period = Column(String(20), nullable=False, index=True)  # 例如：2026-03
    score = Column(Float, nullable=False, default=5.0)
    level = Column(String(50), nullable=False, default='正常')
    description = Column(Text, nullable=True)
    details = Column(Text, nullable=True)  # JSON 字符串
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(String(100), nullable=True)
    
    # 关联
    member = relationship("Member", back_populates="reviews")
    issues = relationship("Issue", back_populates="review", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'member_name': self.member.name if self.member else None,
            'period': self.period,
            'score': self.score,
            'level': self.level,
            'description': self.description,
            'details': json.loads(self.details) if self.details else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.created_by,
            'issue_count': len(self.issues)
        }


class Issue(Base):
    """问题记录表"""
    __tablename__ = 'issues'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(Integer, ForeignKey('reviews.id'), nullable=False, index=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=True, index=True)
    level = Column(String(10), nullable=False, index=True)  # P0, P1, P2, P3
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)  # 功能、性能、UI 等
    is_attitude = Column(Boolean, default=False)  # 是否态度问题
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联
    review = relationship("Review", back_populates="issues")
    member = relationship("Member", back_populates="issues")
    
    def to_dict(self):
        return {
            'id': self.id,
            'review_id': self.review_id,
            'member_id': self.member_id,
            'level': self.level,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'is_attitude': self.is_attitude,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Invitation(Base):
    """邀请评价记录表"""
    __tablename__ = 'invitations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=True)
    reviewer_email = Column(String(255), nullable=False)
    reviewer_name = Column(String(100), nullable=True)
    status = Column(String(20), default='pending')  # pending, sent, completed, expired
    token = Column(String(100), unique=True, nullable=False)
    sent_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联
    member = relationship("Member")
    
    def to_dict(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'reviewer_email': self.reviewer_email,
            'reviewer_name': self.reviewer_name,
            'status': self.status,
            'token': self.token,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


def init_db():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 数据迁移函数
def migrate_from_json():
    """从 JSON 文件迁移数据到 SQLite"""
    from pathlib import Path
    
    data_dir = Path("/home/admin/.openclaw/workspace/projects/performance-review/data")
    
    # 初始化数据库
    init_db()
    db = SessionLocal()
    
    try:
        # 迁移人员
        members_file = data_dir / "members.json"
        if members_file.exists():
            with open(members_file, 'r', encoding='utf-8') as f:
                members_data = json.load(f)
                for m in members_data:
                    member = Member(
                        name=m.get('name', ''),
                        email=m.get('email', ''),
                        department=m.get('department', ''),
                        is_active=m.get('is_active', True)
                    )
                    db.add(member)
            db.commit()
            print(f"✅ 迁移 {len(members_data)} 个人员")
        
        # 迁移评价
        reviews_file = data_dir / "reviews.json"
        if reviews_file.exists():
            with open(reviews_file, 'r', encoding='utf-8') as f:
                reviews_data = json.load(f)
                for r in reviews_data:
                    # 查找对应的人员
                    member = db.query(Member).filter_by(name=r.get('member_name', '')).first()
                    if member:
                        review = Review(
                            member_id=member.id,
                            period=r.get('period', ''),
                            score=r.get('score', 5.0),
                            level=r.get('level', '正常'),
                            description=r.get('description', ''),
                            details=json.dumps(r.get('details', {})),
                            created_by=r.get('created_by', '')
                        )
                        db.add(review)
            db.commit()
            print(f"✅ 迁移评价记录")
        
        print("🎉 数据迁移完成！")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 迁移失败：{e}")
        raise
    finally:
        db.close()


if __name__ == '__main__':
    init_db()
    print("✅ 数据库初始化完成")
