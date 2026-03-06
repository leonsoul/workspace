# 钉钉通知配置指南

---

## 1. 创建钉钉机器人

### 步骤 1：进入群设置
1. 打开钉钉 PC 端
2. 进入要接收通知的群
3. 点击右上角"群设置"（齿轮图标）

### 步骤 2：添加机器人
1. 选择 "智能群助手"
2. 点击 "添加机器人"
3. 选择 "自定义"（通过 Webhook 接入）

### 步骤 3：配置机器人
- **机器人名字**: 人员评价系统
- **头像**: 可选
- **安全设置**: 选择 "自定义关键词"
  - 添加关键词：`【人员评价邀请】`

### 步骤 4：获取 Webhook
复制 Webhook 地址，格式：
```
https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxx
```

---

## 2. 配置到应用

编辑 `app.py`，找到 `send_dingtalk_notification` 函数：

```python
def send_dingtalk_notification(invitation):
    """发送钉钉通知"""
    try:
        import requests
        
        # 替换为你的 Webhook
        webhook = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
        
        # ... 后续代码 ...
```

将 `YOUR_TOKEN` 替换为你复制的 access_token。

---

## 3. 测试发送

### 方式 1：通过 Web 界面
1. 访问 http://localhost:5000/invite
2. 填写邀请信息
3. 被邀请人联系方式填你的钉钉手机号
4. 提交后查看是否收到钉钉消息

### 方式 2：直接测试
```python
# 创建测试邀请
invitation = {
    'id': 'test123',
    'member_name': '测试人员',
    'invitee_email': '13800138000',  # 你的钉钉手机号
    'invitee_name': '测试'
}

# 调用发送函数
from app import send_dingtalk_notification
send_dingtalk_notification(invitation)
```

---

## 4. 通知效果

### 钉钉消息格式
```
【人员评价邀请】

张三，你好！

邀请你对 李四 进行工作质量评价。

评价链接：http://localhost:5000/review?invite_id=20260306130000
有效期：7 天

请客观公正地进行评价，谢谢配合！

—— 人员评价系统
```

### @功能
- 会自动@填写的钉钉手机号
- 被邀请人会收到强提醒

---

## 5. 邮箱通知（可选）

如需启用邮件通知，需要配置 SMTP：

```python
import smtplib
from email.mime.text import MIMEText

def send_email(invitee_email, subject, content):
    # SMTP 配置（根据实际邮箱服务商配置）
    smtp_server = "smtp.company.com"
    smtp_port = 465
    username = "noreply@company.com"
    password = "your_password"
    
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = invitee_email
    
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(username, password)
    server.send_message(msg)
    server.quit()
```

---

## 6. 安全建议

1. **Webhook 保密**: 不要提交到 Git
2. **使用环境变量**:
   ```python
   import os
   webhook = os.environ.get('DINGTALK_WEBHOOK')
   ```
3. **限制发送频率**: 避免被钉钉限流
4. **日志记录**: 记录发送状态便于排查

---

## 7. 常见问题

### Q: 收不到钉钉消息？
A: 检查：
- Webhook 是否正确
- 安全设置关键词是否匹配
- 手机号格式是否正确（11 位数字）

### Q: 提示"机器人被禁用"？
A: 在群设置中重新启用机器人

### Q: 如何@所有人？
A: 修改 payload:
```python
"at": {
    "isAtAll": true
}
```

---

**配置完成后，邀请功能就可以真正发送通知了！** 🎉
