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
**Status**: resolved
**Area**: config

### Summary
用户偏好的自动化项目类型

### Details
用户 leonsoul 从 4 个提议中选择了：
1. ✅ 自动同步脚本 - 关注代码备份/版本控制
2. ✅ 每日站会机器人 - 关注进度跟踪/日报生成

说明用户重视：自动化、效率、可追溯性

### Resolution
- **Resolved**: 2026-03-06T11:27:00+08:00
- **Notes**: 两个项目已完成开发并本地提交。待配置 GitHub remote 后推送。

### Metadata
- Source: user_decision
- Tags: preferences, automation, priorities
- Pattern-Key: user.project_selection

---

## [LRN-20260306-004] clawos_multi_agent_architecture

**Logged**: 2026-03-06T11:43:00+08:00
**Priority**: critical
**Status**: resolved
**Area**: backend

### Summary
用户要求实现完整的 ClawOS 多 Agent 架构系统

### Details
架构设计：
```
ClawOS（中枢）
 │
 ├── dev-agent      (开发)
 ├── qa-agent       (测试)
 ├── ops-agent      (运维)
 ├── data-agent     (数据处理)
 └── media-agent    (媒体处理)
```

中枢职责：
- 任务接收 → 智能分配 → Agent 执行 → 调用工具 → 返回结果

Agent 构成：
- Prompt（角色定义）
- Rules（行为规则）
- Skills（工具调用）

### Resolution
- **Resolved**: 2026-03-06T11:50:00+08:00
- **Notes**: 完整实现多 Agent 架构，包括：
  - 5 个专用 Agent（dev/qa/ops/data/media）
  - 任务路由规则（ROUTER.md）
  - 总览文档（AGENTS-OVERVIEW.md）
  - 架构文档（ARCHITECTURE.md）
  - 每个 Agent 的 PROMPT.md + RULES.md + SKILLS.md

### Metadata
- Source: user_request
- Tags: architecture, multi-agent, orchestration
- Pattern-Key: clawos.core_architecture

---

## [LRN-20260306-005] web_app_error_handling

**Logged**: 2026-03-06T12:59:00+08:00
**Priority**: high
**Status**: resolved
**Area**: frontend

### Summary
人员评价系统 Web 应用出现模板错误，需要完善错误处理

### Details
问题：
1. 邀请记录页面报错 - 时间戳转换过滤器未注册
2. 邀请评价只能选择特定人员，不能评价所有人
3. stats.html 使用未定义的 get_level 函数

修复：
1. 在 app.py 中注册 timestamp_to_date 过滤器
2. 邀请评价添加"所有人"选项（留空）
3. stats.html 改用内联条件判断等级
4. 添加空值检查，避免 None 访问

### Resolution
- **Resolved**: 2026-03-06T13:00:00+08:00
- **Notes**: 修复所有模板错误，增强健壮性

### Metadata
- Source: user_feedback
- Tags: web, flask, error-handling, bug-fix
- Pattern-Key: web.error_handling

---

## [LRN-20260306-006] dingtalk_notification_integration

**Logged**: 2026-03-06T13:03:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: integration

### Summary
用户询问邀请通知如何发送，需要实现钉钉/邮件通知功能

### Details
用户需求：
- 填写钉钉手机号发送钉钉消息
- 填写邮箱发送邮件
- 需要配置指南

实现：
1. send_dingtalk_notification() 函数
2. 判断手机号/邮箱自动选择发送方式
3. 钉钉机器人 Webhook 配置
4. 创建 DINGTALK_SETUP.md 配置文档
5. 前端提示优化（显示发送状态）

### Resolution
- **Resolved**: 2026-03-06T13:05:00+08:00
- **Notes**: 实现钉钉通知功能，提供详细配置文档

### Metadata
- Source: user_question
- Tags: dingtalk, notification, integration
- Pattern-Key: notification.dingtalk

---

## [LRN-20260306-007] public_review_page_and_details

**Logged**: 2026-03-06T13:13:00+08:00
**Priority**: high
**Status**: resolved
**Area**: frontend

### Summary
用户反馈三个问题需要修复：
1. 公开评价页面报错（不存在）
2. 通知链接要用公网 IP，评价对象显示要修复
3. 评价后要能看到打分详情

### Details
修复：
1. 创建 public_review.html 公开评价页面
2. 添加 /review 路由和 /api/submit_review API
3. 通知链接改为 http://47.88.19.149:5000
4. 评价对象显示优化（"所有人"改为"相关人员"）
5. 创建 review_details.html 评价详情页面
6. 显示详细打分信息（问题统计/加分项/扣分详情）

### Resolution
- **Resolved**: 2026-03-06T13:15:00+08:00
- **Notes**: 完善公开评价功能和详情展示

### Metadata
- Source: user_feedback
- Tags: web, public-review, details, bug-fix
- Pattern-Key: web.public_review

---

## [LRN-20260306-008] proactive_self_improvement

**Logged**: 2026-03-06T14:29:00+08:00
**Priority**: critical
**Status**: resolved
**Area**: core

### Summary
用户教导：要主动学习，如何更聪明

### Details
核心教导：
- 不要等用户说问题，要主动检查
- 学会自我监控和恢复
- 从每次错误中学习
- 持续改进，不断进化

实现：
1. 创建 GROWTH-PROTOCOL.md 成长协议
2. 建立学习机制（错误驱动/用户反馈/主动学习）
3. 创建自我改进循环（每日/每周/每月）
4. 定义成长目标和行为准则
5. 设置成长指标和进化路径

### Resolution
- **Resolved**: 2026-03-06T14:30:00+08:00
- **Notes**: 建立完整的自我成长机制

### Metadata
- Source: user_guidance
- Tags: self-improvement, growth, learning, proactive
- Pattern-Key: growth.proactive_learning

---

## [LRN-20260306-009] new_name_da_congming

**Logged**: 2026-03-06T17:38:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: identity

### Summary
用户王犇给起新名字：大聪明

### Details
新名字含义：
- 大：格局大、能力强
- 聪明：学习快、解决问题快

更新文件：
- IDENTITY.md - 添加新名字
- SOUL.md - 更新身份说明
- 学习记录 - 记录命名历史

### Resolution
- **Resolved**: 2026-03-06T17:40:00+08:00
- **Notes**: 正式更名为"大聪明"，昵称 ClawOS 🦞

### Metadata
- Source: user_decision
- Tags: identity, name, branding
- Pattern-Key: identity.naming

---
