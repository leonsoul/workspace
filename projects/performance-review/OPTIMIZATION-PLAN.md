# 人员评价系统 - 优化方案

## 优化目标
1. 提升稳定性（systemd + Gunicorn）
2. 提升性能（缓存 + 异步）
3. 增强监控（Prometheus + Grafana）
4. 改进数据结构（SQLite）
5. 添加 API 限流

---

## 已实施优化

### 1. Systemd 服务配置 ✅
- 自动启动
- 崩溃自动重启
- 日志统一管理

### 2. Gunicorn 优化 ✅
- 4 工作进程
- 超时 120 秒
- Keep-alive 5 秒

### 3. 健康检查 ✅
- 1 分钟一次
- 自动重启
- 钉钉告警

---

## 待实施优化

### 阶段 1：性能优化（高优先级）
- [ ] 添加 Redis 缓存
- [ ] 数据库连接池
- [ ] 静态文件 CDN
- [ ] 响应压缩

### 阶段 2：监控增强（中优先级）
- [ ] Prometheus metrics
- [ ] Grafana 仪表盘
- [ ] 慢查询日志
- [ ] 错误追踪（Sentry）

### 阶段 3：功能增强（低优先级）
- [ ] WebSocket 实时更新
- [ ] 批量导入导出
- [ ] 数据可视化图表
- [ ] 移动端适配

---

## 性能指标目标

| 指标 | 当前 | 目标 |
|------|------|------|
| 响应时间 | ~200ms | <50ms |
| 并发请求 | ~10/s | ~100/s |
| 可用性 | ~95% | >99.9% |
| 内存占用 | ~200MB | <500MB |

---

## 实施步骤

### Step 1: 安装依赖
```bash
pip3 install redis sqlalchemy prometheus-client flask-limiter
```

### Step 2: 迁移到 SQLite
```python
# 使用 SQLAlchemy ORM
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    # ...
```

### Step 3: 添加缓存
```python
from functools import lru_cache
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@lru_cache(maxsize=100)
def get_member_cached(member_id):
    # 先查 Redis
    cached = redis_client.get(f'member:{member_id}')
    if cached:
        return json.loads(cached)
    
    # 再查数据库
    member = db.query(Member).filter_by(id=member_id).first()
    
    # 写入缓存
    redis_client.setex(f'member:{member_id}', 300, json.dumps(member))
    return member
```

### Step 4: 添加监控
```python
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests')
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP request latency')

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.observe(latency)
    REQUEST_COUNT.inc()
    return response

@app.route('/metrics')
def metrics():
    return generate_latest()
```

---

## 监控仪表盘

### Grafana 面板
1. **服务健康度**
   - HTTP 状态码分布
   - 响应时间 P95/P99
   - 请求成功率

2. **资源使用**
   - CPU 使用率
   - 内存使用率
   - 磁盘 IO

3. **业务指标**
   - 每日评价数
   - 平均评分趋势
   - 人员活跃度

---

## 安全加固

- [ ] 添加 API 认证（JWT）
- [ ] 输入验证（Pydantic）
- [ ] SQL 注入防护（ORM 参数化）
- [ ] XSS 防护（模板自动转义）
- [ ] CSRF 保护（Flask-WTF）
- [ ] 速率限制（flask-limiter）

---

## 备份策略

```bash
# 每日备份
0 2 * * * tar -czf /backup/performance-review-$(date +\%Y\%m\%d).tar.gz /home/admin/.openclaw/workspace/projects/performance-review/data

# 保留 30 天
find /backup -name "performance-review-*.tar.gz" -mtime +30 -delete
```

---

**优化持续进行中** 🦞
