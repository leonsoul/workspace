#!/usr/bin/env python3
"""
数据迁移脚本 - 从 JSON 到 SQLite

使用方法:
    python3 migrate-to-sqlite.py
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/projects/performance-review')

from database import init_db, migrate_from_json, Member, Review, Issue, Invitation, SessionLocal
from pathlib import Path
import json

def main():
    print("=" * 60)
    print("人员评价系统 - 数据迁移工具")
    print("=" * 60)
    print()
    
    data_dir = Path("/home/admin/.openclaw/workspace/projects/performance-review/data")
    
    # 检查源数据
    print("📊 检查源数据...")
    members_file = data_dir / "members.json"
    reviews_file = data_dir / "reviews.json"
    invitations_file = data_dir / "invitations.json"
    
    members_count = 0
    reviews_count = 0
    invitations_count = 0
    
    if members_file.exists():
        with open(members_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            members_count = len(data)
        print(f"   ✅ 人员：{members_count} 个")
    else:
        print(f"   ⚠️  人员文件不存在")
    
    if reviews_file.exists():
        with open(reviews_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            reviews_count = len(data)
        print(f"   ✅ 评价：{reviews_count} 条")
    else:
        print(f"   ⚠️  评价文件不存在")
    
    if invitations_file.exists():
        with open(invitations_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            invitations_count = len(data)
        print(f"   ✅ 邀请：{invitations_count} 条")
    else:
        print(f"   ⚠️  邀请文件不存在")
    
    print()
    
    if members_count == 0 and reviews_count == 0:
        print("⚠️  没有数据需要迁移，仅初始化数据库结构")
        init_db()
        print("✅ 数据库初始化完成")
        return
    
    # 确认迁移
    print(f"准备迁移 {members_count} 个人员、{reviews_count} 条评价、{invitations_count} 条邀请")
    response = input("继续迁移？(y/n): ")
    if response.lower() != 'y':
        print("❌ 迁移取消")
        return
    
    print()
    print("🚀 开始迁移...")
    print()
    
    try:
        # 初始化数据库
        init_db()
        print("✅ 数据库表已创建")
        
        # 迁移数据
        migrate_from_json()
        
        # 验证迁移结果
        db = SessionLocal()
        print()
        print("📊 迁移结果验证:")
        print(f"   人员：{db.query(Member).count()} 个")
        print(f"   评价：{db.query(Review).count()} 条")
        print(f"   问题：{db.query(Issue).count()} 个")
        print(f"   邀请：{db.query(Invitation).count()} 条")
        db.close()
        
        print()
        print("=" * 60)
        print("🎉 迁移完成！")
        print("=" * 60)
        print()
        print("下一步:")
        print("1. 验证数据：python3 database.py")
        print("2. 更新 app.py 使用数据库")
        print("3. 备份 JSON 文件（可选）")
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ 迁移失败：{e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
