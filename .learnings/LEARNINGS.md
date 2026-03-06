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

## [LRN-20260306-002] proactive_skill_test

**Logged**: 2026-03-06T11:24:00+08:00
**Priority**: high
**Status**: resolved
**Area**: config

### Summary
用户要求测试新激活的 self-improvement 和 proactive-agent 技能

### Details
用户 (leonsoul) 要求验证两个技能是否正确激活并工作。需要展示：
1. WAL 协议 - 回复前先写 SESSION-STATE.md
2. 主动行为 - 提议用户没想到的功能
3. 自改进 - 记录交互到 learnings

### Resolution
- **Resolved**: 2026-03-06T11:25:00+08:00
- **Notes**: 测试通过。用户选定了提议 1（自动同步脚本）和提议 3（每日站会机器人）进行开发

### Metadata
- Source: user_request
- Tags: self-improvement, proactive, skill-test
- Pattern-Key: skill.activation_test

---

## [LRN-20260306-003] user_project_preferences

**Logged**: 2026-03-06T11:25:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
用户偏好的自动化项目类型

### Details
用户 leonsoul 从 4 个提议中选择了：
1. ✅ 自动同步脚本 - 关注代码备份/版本控制
2. ✅ 每日站会机器人 - 关注进度跟踪/日报生成

说明用户重视：自动化、效率、可追溯性

### Suggested Action
优先完成这两个项目，设计时考虑通用性便于复用

### Metadata
- Source: user_decision
- Tags: preferences, automation, priorities
- Pattern-Key: user.project_selection

---
