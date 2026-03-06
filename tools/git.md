# Git 工具文档

---

## 配置

### 用户信息
```bash
git config --global user.name "leonsoul"
git config --global user.email "1301017238@qq.com"
```

### SSH 密钥
```bash
# 生成
ssh-keygen -t ed25519 -C "openclaw@github" -f ~/.ssh/id_ed25519 -N ""

# 添加到 GitHub
# https://github.com/settings/keys

# 测试
ssh -T git@github.com
```

---

## 常用命令

### 基础操作
```bash
# 状态
git status

# 添加
git add -A

# 提交
git commit -m "type: description"

# 推送
git push origin master

# 拉取
git pull origin master
```

### 分支管理
```bash
# 查看分支
git branch

# 创建分支
git checkout -b feature-xxx

# 切换分支
git checkout master

# 合并分支
git merge feature-xxx

# 删除分支
git branch -d feature-xxx
```

### 远程仓库
```bash
# 添加远程
git remote add origin git@github.com:leonsoul/workspace.git

# 查看远程
git remote -v

# 删除远程
git remote remove origin
```

### 当前配置
```
Remote: origin
URL: git@github.com:leonsoul/workspace.git
Branch: master → origin/master
```

---

## Commit 规范

### 格式
```
type: description

[optional body]

[optional footer]
```

### Types
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

### 示例
```
feat: 添加自动同步脚本

- 实现 git-auto-sync
- 支持定时任务
- 添加日志记录

Closes #123
```

---

## 最佳实践

1. **小步提交**: 每次提交一个功能点
2. **规范消息**: 遵循 commit 规范
3. **及时推送**: 本地提交后尽快推送
4. **分支开发**: 新功能用 feature 分支
5. **Code Review**: 合并前审查

---

## 自动化

### Git Auto-Sync
```bash
# 路径
/home/admin/.openclaw/workspace/projects/git-auto-sync/sync.sh

# Cron（每 30 分钟）
*/30 * * * * /home/admin/.openclaw/workspace/projects/git-auto-sync/sync.sh
```

---

**Version**: 1.0  
**Last Updated**: 2026-03-06
