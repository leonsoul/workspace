# Python 开发工具

---

## 已安装 Skills

| Skill | 来源 | 安全等级 | 说明 |
|-------|------|----------|------|
| `async-python-patterns` | wshobson/agents | ✅ Safe | Python 异步编程模式 |

**安装路径**: `~/.agents/skills/`

---

## 异步编程（async-python-patterns）

### 基础模式
```python
import asyncio

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    tasks = [
        fetch_data('https://api1.com'),
        fetch_data('https://api2.com')
    ]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

### 最佳实践
1. 用 `async/await` 代替阻塞 IO
2. 用 `asyncio.gather` 并发执行
3. 用 `asyncio.Semaphore` 限流
4. 用 `aiohttp` 代替 `requests`

---

## 其他推荐 Skills（可选）

| Skill | 说明 |
|-------|------|
| `python-performance-optimization` | 性能优化 |
| `python-testing-patterns` | 测试模式 |
| `python-production-code` | 生产代码规范 |

---

## 常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest tests/

# 代码检查
flake8 .
black --check .

# 性能分析
python -m cProfile script.py
```

---

## 项目结构

```
project/
├── src/
│   └── app.py
├── tests/
│   └── test_app.py
├── requirements.txt
└── README.md
```

---

## 相关文档

- `agents/dev-agent.md` - Dev Agent
- `workflows/dev-workflow.md` - 开发流程
- `tools/git.md` - Git 工具

---

**Version**: 1.0  
**Last Updated**: 2026-03-06  
**Skills Installed**: async-python-patterns
