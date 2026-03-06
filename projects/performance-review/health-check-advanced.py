#!/usr/bin/env python3
"""
人员评价系统 - 高级健康检查

功能:
- HTTP 健康检查
- 响应时间监控
- 自动重启服务
- 钉钉告警
- 指标记录
"""

import requests
import time
import subprocess
import json
from datetime import datetime
from pathlib import Path

# 配置
CONFIG = {
    'service_url': 'http://localhost:5000',
    'health_endpoint': '/health',
    'check_interval': 60,  # 60 秒检查一次
    'max_retries': 2,
    'timeout': 5,
    'log_file': '/tmp/health-check-advanced.log',
    'metrics_file': '/tmp/health-metrics.json',
    'workdir': '/home/admin/.openclaw/workspace/projects/performance-review',
    
    # 钉钉配置
    'dingtalk_enabled': True,
    'dingtalk_webhook': 'https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN',
    'alert_on_failures': 3,  # 连续失败 3 次发送告警
}

class HealthChecker:
    def __init__(self):
        self.consecutive_failures = 0
        self.total_checks = 0
        self.successful_checks = 0
        self.metrics = {
            'start_time': datetime.now().isoformat(),
            'checks': [],
            'avg_response_time': 0,
            'uptime_percentage': 100.0
        }
        self.log_file = Path(CONFIG['log_file'])
        self.metrics_file = Path(CONFIG['metrics_file'])
    
    def log(self, message, level='INFO'):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def send_dingtalk_alert(self, message):
        """发送钉钉告警"""
        if not CONFIG['dingtalk_enabled']:
            return
        
        try:
            headers = {'Content-Type': 'application/json'}
            data = {
                'msgtype': 'text',
                'text': {
                    'content': f"🚨 人员评价系统告警\n{message}"
                }
            }
            response = requests.post(
                CONFIG['dingtalk_webhook'],
                headers=headers,
                json=data,
                timeout=5
            )
            if response.status_code == 200:
                self.log('钉钉告警发送成功')
            else:
                self.log(f'钉钉告警发送失败：{response.status_code}', 'ERROR')
        except Exception as e:
            self.log(f'钉钉告警异常：{e}', 'ERROR')
    
    def check_health(self):
        """执行健康检查"""
        self.total_checks += 1
        start_time = time.time()
        
        try:
            response = requests.get(
                f"{CONFIG['service_url']}{CONFIG['health_endpoint']}",
                timeout=CONFIG['timeout']
            )
            response_time = (time.time() - start_time) * 1000  # ms
            
            if response.status_code == 200:
                self.consecutive_failures = 0
                self.successful_checks += 1
                self.log(f'✅ 健康检查通过 (HTTP {response.status_code}, {response_time:.2f}ms)')
                
                # 记录指标
                self.metrics['checks'].append({
                    'timestamp': datetime.now().isoformat(),
                    'status': 'success',
                    'response_time_ms': round(response_time, 2),
                    'http_code': response.status_code
                })
                
                return True
            else:
                raise Exception(f'HTTP {response.status_code}')
                
        except Exception as e:
            self.consecutive_failures += 1
            self.log(f'❌ 健康检查失败 ({e})', 'ERROR')
            
            # 记录指标
            self.metrics['checks'].append({
                'timestamp': datetime.now().isoformat(),
                'status': 'failed',
                'error': str(e)
            })
            
            # 发送告警
            if self.consecutive_failures >= CONFIG['alert_on_failures']:
                alert_msg = (
                    f"服务连续失败 {self.consecutive_failures} 次\n"
                    f"最后检查：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"错误：{e}"
                )
                self.send_dingtalk_alert(alert_msg)
            
            return False
    
    def restart_service(self):
        """重启服务"""
        self.log('🔄 正在重启服务...', 'WARN')
        
        try:
            # 停止旧进程
            subprocess.run(['pkill', '-f', 'gunicorn.*app:app'], capture_output=True)
            time.sleep(2)
            
            # 启动新进程
            cmd = [
                'gunicorn', '-w', '4', '-b', '0.0.0.0:5000',
                '--timeout', '120', '--keep-alive', '5',
                'app:app'
            ]
            subprocess.Popen(
                cmd,
                cwd=CONFIG['workdir'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            time.sleep(3)
            self.log('✅ 服务重启完成')
            
        except Exception as e:
            self.log(f'❌ 服务重启失败：{e}', 'ERROR')
    
    def update_metrics(self):
        """更新指标"""
        if self.metrics['checks']:
            response_times = [
                c.get('response_time_ms', 0) 
                for c in self.metrics['checks'][-100:]  # 最近 100 次
                if c.get('response_time_ms')
            ]
            if response_times:
                self.metrics['avg_response_time'] = round(
                    sum(response_times) / len(response_times), 2
                )
        
        self.metrics['uptime_percentage'] = round(
            (self.successful_checks / self.total_checks * 100) if self.total_checks > 0 else 100, 2
        )
        
        # 保存指标
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(self.metrics, f, ensure_ascii=False, indent=2)
    
    def run(self):
        """运行健康检查循环"""
        self.log('=' * 50)
        self.log('🚀 高级健康检查启动')
        self.log(f'服务地址：{CONFIG["service_url"]}')
        self.log(f'检查间隔：{CONFIG["check_interval"]}秒')
        self.log('=' * 50)
        
        while True:
            try:
                # 执行检查
                is_healthy = self.check_health()
                
                # 如果不健康且达到重试次数，重启服务
                if not is_healthy and self.consecutive_failures >= CONFIG['max_retries']:
                    self.restart_service()
                
                # 更新指标
                self.update_metrics()
                
                # 等待下次检查
                time.sleep(CONFIG['check_interval'])
                
            except KeyboardInterrupt:
                self.log('👋 健康检查停止')
                break
            except Exception as e:
                self.log(f'⚠️ 检查循环异常：{e}', 'ERROR')
                time.sleep(CONFIG['check_interval'])


if __name__ == '__main__':
    checker = HealthChecker()
    checker.run()
