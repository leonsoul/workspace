# Learnings Log

持续改进的学习记录 —— 修正、知识缺口、最佳实践

---

## [LRN-20260306-001] git_ssh_authentication

**Logged**: 2026-03-06T11:21:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: config

### Summary
配置 SSH 密钥连接 GitHub 的完整流程

### Details
- 生成 ed25519 密钥：`ssh-keygen -t ed25519 -C "openclaw@github" -f ~/.ssh/id_ed25519 -N ""`
- 公钥添加到 GitHub Settings → SSH Keys
- 验证：`ssh -T git@github.com` 看到 "Hi <username>! You've successfully authenticated"
- 配置 Git 用户：`git config --global user.name` 和 `git config --global user.email`

### Suggested Action
已完成，作为标准流程记录

### Metadata
- Source: conversation
- Tags: git, ssh, github, authentication
- Pattern-Key: git.ssh_setup

---

## [LRN-20260306-010] git_push_best_practices

**Logged**: 2026-03-06T21:23:00+08:00
**Priority**: high
**Status**: resolved
**Area**: devops

### Summary
用户教导：环境配置和本地文件不要推送到 GitHub

### Details
问题：
- Miniconda 安装包（154MB）超过 GitHub 100MB 限制
- 环境配置文件不应该推送到公共仓库
- 需要学会判断什么应该推送，什么不应该

解决：
1. 使用 git filter-branch 清理历史记录
2. 更新 .gitignore 添加环境配置规则
3. 强制推送到 GitHub

教训：
- 安装包、二进制文件不推送
- 本地环境配置不推送
- 敏感信息不推送
- 大文件使用 Git LFS 或外部存储

### Resolution
- **Resolved**: 2026-03-06T21:25:00+08:00
- **Notes**: 已清理历史并更新 .gitignore

### Metadata
- Source: user_guidance
- Tags: git, github, best-practices, devops
- Pattern-Key: git.push_best_practices

---

## [LRN-20260306-011] self_optimization

**Logged**: 2026-03-06T21:34:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: backend

### Summary
用户要求：自己优化（修复服务错误）

### Details
问题：
- 服务返回 HTTP 500 错误
- Jinja2 模板错误：'database.Member object' has no attribute 'average_score'
- 模板使用 `member.average_score` 但数据库模型只有 `get_average_score()` 方法

解决：
1. 在 Member 类添加 `@property average_score`
2. 保留 `get_average_score()` 方法作为兼容
3. 重启服务验证修复
4. 安装缺失的 flask-socketio 依赖

修复内容：
```python
@property
def average_score(self):
    """计算平均分"""
    if not self.reviews:
        return 0.0
    scores = [r.score for r in self.reviews]
    return round(sum(scores) / len(scores), 2)
```

### Resolution
- **Resolved**: 2026-03-06T21:40:00+08:00
- **Notes**: 服务已修复，HTTP 200 正常

### Metadata
- Source: user_request
- Tags: self-healing, optimization, bug-fix, flask
- Pattern-Key: self.optimization

---
