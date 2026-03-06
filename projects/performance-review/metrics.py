#!/usr/bin/env python3
"""
人员评价系统 - 性能监控

功能:
- 收集性能指标
- 生成 Prometheus 格式 metrics
- 提供 /metrics 端点
"""

import time
import json
from pathlib import Path
from datetime import datetime
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

# 指标定义
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_latency_seconds',
    'HTTP request latency',
    ['endpoint'],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections'
)

SYSTEM_UPTIME = Gauge(
    'system_uptime_seconds',
    'System uptime in seconds'
)

REVIEW_COUNT = Gauge(
    'reviews_total',
    'Total number of reviews'
)

MEMBER_COUNT = Gauge(
    'members_total',
    'Total number of members'
)

AVG_SCORE = Gauge(
    'average_score',
    'Average performance score'
)

# 启动时间
START_TIME = time.time()
SYSTEM_UPTIME.set(0)


def init_metrics(app, data_dir):
    """初始化指标收集"""
    
    @app.before_request
    def before_request():
        request.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        # 记录请求指标
        latency = time.time() - request.start_time
        endpoint = request.endpoint or 'unknown'
        
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()
        
        # 更新系统运行时间
        SYSTEM_UPTIME.set(time.time() - START_TIME)
        
        return response
    
    @app.route('/metrics')
    def metrics():
        """Prometheus metrics 端点"""
        # 更新业务指标
        update_business_metrics(data_dir)
        
        return Response(
            generate_latest(),
            mimetype=CONTENT_TYPE_LATEST
        )
    
    return app


def update_business_metrics(data_dir):
    """更新业务指标"""
    try:
        data_dir = Path(data_dir)
        
        # 统计人员数量
        members_file = data_dir / 'members.json'
        if members_file.exists():
            with open(members_file, 'r', encoding='utf-8') as f:
                members = json.load(f)
                MEMBER_COUNT.set(len(members))
        
        # 统计评价数量和平均分
        reviews_file = data_dir / 'reviews.json'
        if reviews_file.exists():
            with open(reviews_file, 'r', encoding='utf-8') as f:
                reviews = json.load(f)
                REVIEW_COUNT.set(len(reviews))
                
                if reviews:
                    avg_score = sum(r.get('score', 0) for r in reviews) / len(reviews)
                    AVG_SCORE.set(round(avg_score, 2))
    
    except Exception as e:
        print(f"更新业务指标失败：{e}")


# 独立的 metrics 服务器（可选）
def run_metrics_server(port=9090):
    """运行独立的 metrics 服务器"""
    from prometheus_client import start_http_server
    
    start_http_server(port)
    print(f"Metrics server running on port {port}")
    
    while True:
        time.sleep(60)
        update_business_metrics('/home/admin/.openclaw/workspace/projects/performance-review/data')


if __name__ == '__main__':
    run_metrics_server()
