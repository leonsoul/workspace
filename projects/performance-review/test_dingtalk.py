#!/usr/bin/env python3
"""
测试钉钉通知发送
"""

import requests

webhook = "https://oapi.dingtalk.com/robot/send?access_token=7acf606300e4ba07aa0795f6d6c33a5c1d11b7787f58e0aa3240ae20ceac2590"

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
