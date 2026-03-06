#!/usr/bin/env python3
"""
人员评价系统健康检查
- 检查服务状态
- 自动重启
- 发送告警通知
"""

import requests
import subprocess
import time
from datetime import datetime

CONFIG = {
    'url': 'http://localhost:5000',
    'port': 5000,
    'workdir': '/home/admin/.openclaw/workspace/projects/performance-review',
    'log_file': '/tmp/performance-review.log',
    'check_interval': 60,   # 1 分钟检查一次
    'max_retries': 2
}

def check_service():
    """检查服务是否可访问"""
    try:
        response = requests.get(CONFIG['url'], timeout=5)
        if response.status_code == 200:
            return True
        else:
            print(f"HTTP 状态码异常：{response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("连接失败 - 服务未运行")
        return False
    except requests.exceptions.Timeout:
        print("连接超时")
        return False
    except Exception as e:
        print(f"检查异常：{e}")
        return False

def restart_service():
    """重启服务"""
    try:
        # 停止旧进程
        subprocess.run(['pkill', '-f', 'python3 app.py'], timeout=5)
        time.sleep(2)
        
        # 启动新进程
        import os
        os.chdir(CONFIG['workdir'])
        subprocess.Popen(
            ['nohup', 'python3', 'app.py'],
            stdout=open(CONFIG['log_file'], 'a'),
            stderr=subprocess.STDOUT,
            start_new_session=True
        )
        
        # 等待启动
        time.sleep(3)
        return check_service()
    except Exception as e:
        print(f"重启失败：{e}")
        return False

def send_alert(message):
    """发送告警通知（钉钉）"""
    try:
        webhook = "https://oapi.dingtalk.com/robot/send?access_token=7acf606300e4ba07aa0795f6d6c33a5c1d11b7787f58e0aa3240ae20ceac2590"
        
        content = f"""【系统告警】

人员评价系统异常

{message}

时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

—— 自动监控"""
        
        payload = {
            "msgtype": "text",
            "text": {"content": content}
        }
        
        requests.post(webhook, json=payload, timeout=5)
    except:
        pass

def main_loop():
    """主监控循环"""
    print(f"开始监控 - {datetime.now()}")
    print(f"检查间隔：{CONFIG['check_interval']}秒")
    
    consecutive_failures = 0
    
    while True:
        if not check_service():
            consecutive_failures += 1
            print(f"❌ 服务不可用 (连续{consecutive_failures}次)")
            
            if consecutive_failures >= CONFIG['max_retries']:
                print("尝试重启服务...")
                send_alert(f"服务不可用，尝试重启 (连续失败{consecutive_failures}次)")
                
                if restart_service():
                    print("✅ 重启成功")
                    send_alert("服务已自动重启成功")
                    consecutive_failures = 0
                else:
                    print("❌ 重启失败")
                    send_alert("服务重启失败，需要人工干预！")
        else:
            if consecutive_failures > 0:
                print(f"✅ 服务已恢复 (之前失败{consecutive_failures}次)")
            consecutive_failures = 0
        
        time.sleep(CONFIG['check_interval'])

if __name__ == '__main__':
    # 首次检查
    if not check_service():
        print("服务未运行，尝试启动...")
        if restart_service():
            print("✅ 服务已启动")
        else:
            print("❌ 启动失败")
    
    # 开始监控
    main_loop()
