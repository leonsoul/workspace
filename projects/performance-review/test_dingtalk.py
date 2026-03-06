#!/usr/bin/env python3
"""
测试钉钉通知发送（带签名）
"""

import requests
import hmac
import hashlib
import base64
import urllib.parse
import time

# 钉钉机器人配置
access_token = "7acf606300e4ba07aa0795f6d6c33a5c1d11b7787f58e0aa3240ae20ceac2590"
secret = "SEC59df22914da93ef59cf1c9c9231d89eca9a86b8010fc9cbba33e542cf6fa6cf7"

# 计算签名
timestamp = str(round(time.time() * 1000))
secret_enc = secret.encode('utf-8')
string_to_sign = f'{timestamp}\n{secret}'
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

# 构建带签名的 Webhook
webhook = f"https://oapi.dingtalk.com/robot/send?access_token={access_token}&timestamp={timestamp}&sign={sign}"

print(f"Webhook: {webhook[:100]}...")

# 测试消息
content = """【人员评价邀请】

测试消息

如果你收到这条消息，说明钉钉通知配置成功！

—— 人员评价系统"""

payload = {
    "msgtype": "text",
    "text": {
        "content": content
    },
    "at": {
        "isAtAll": True
    }
}

print("发送测试消息...")
response = requests.post(webhook, json=payload, timeout=5)

if response.status_code == 200:
    result = response.json()
    if result.get('errcode') == 0:
        print("✅ 发送成功！")
    else:
        print(f"❌ 发送失败：{result}")
else:
    print(f"❌ HTTP 错误：{response.status_code}")
    print(response.text)
