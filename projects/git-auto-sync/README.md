# Git Auto-Sync 🔄

自动检测工作区变更并提交推送到 GitHub。

## 功能

- ✅ 自动检测 git 变更
- ✅ 批量提交（最多 50 个文件/次）
- ✅ 自动推送到 GitHub
- ✅ 日志记录所有操作
- ✅ 无变更时跳过（不产生空提交）

## 快速开始

### 1. 配置远程仓库

```bash
cd /home/admin/.openclaw/workspace

# 在 GitHub 创建仓库后
git remote add origin git@github.com:leonsoul/你的仓库名.git
git branch -M master
```

### 2. 手动运行

```bash
cd /home/admin/.openclaw/workspace/projects/git-auto-sync
chmod +x sync.sh
./sync.sh "可选的提交消息"
```

### 3. 定时同步（推荐）

编辑 crontab：
```bash
crontab -e
```

添加以下行（每 30 分钟同步一次）：
```cron
*/30 * * * * /home/admin/.openclaw/workspace/projects/git-auto-sync/sync.sh
```

或者每小时：
```cron
0 * * * * /home/admin/.openclaw/workspace/projects/git-auto-sync/sync.sh
```

## 日志

日志文件：`/home/admin/.openclaw/workspace/projects/git-auto-sync/sync.log`

查看最近日志：
```bash
tail -50 /home/admin/.openclaw/workspace/projects/git-auto-sync/sync.log
```

## 配置选项

编辑 `sync.sh` 顶部：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `WORKSPACE` | 工作区路径 | `/home/admin/.openclaw/workspace` |
| `LOG_FILE` | 日志文件路径 | `$WORKSPACE/projects/git-auto-sync/sync.log` |
| `MAX_FILES_PER_COMMIT` | 每次提交最大文件数 | `50` |

## 排除文件

创建 `.gitignore` 来排除不需要同步的文件：

```gitignore
# 敏感信息
*.env
*.key
*.pem

# 日志文件
*.log

# 临时文件
.tmp/
.cache/

# 系统文件
.DS_Store
Thumbs.db
```

## 故障排查

### 推送失败
```bash
# 测试 SSH 连接
ssh -T git@github.com

# 应该看到：Hi leonsoul! You've successfully authenticated
```

### 查看 git 状态
```bash
cd /home/admin/.openclaw/workspace
git status
git remote -v
```

### 重置远程仓库
```bash
git remote remove origin
git remote add origin git@github.com:leonsoul/仓库名.git
```

## 安全提示

- ✅ SSH 密钥已配置（无密码）
- ✅ 只推送工作区代码
- ✅ 日志记录所有操作
- ⚠️ 不要同步敏感信息（密码、API Key 等）

---

**下一步**: 配置每日站会机器人 → `../daily-standup/README.md`
