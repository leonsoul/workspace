# Selenium 自动化工具

---

## 概述

Selenium 用于网页自动化：
- 多浏览器支持（Chrome/Firefox/Edge）
- 多语言绑定（Python/Java/JS）
- 成熟的生态系统
- 适合复杂场景

---

## 已安装 Skills

| Skill | 来源 | 安全等级 |
|-------|------|----------|
| `selenium-automation` | mindrally/skills | ✅ Safe |

**安装路径**: `~/.agents/skills/`

---

## 基本用法

### Python 示例
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

# 启动浏览器
driver = webdriver.Chrome()

# 导航
driver.get("https://example.com")

# 查找元素
element = driver.find_element(By.ID, "username")

# 操作
element.send_keys("test")
driver.find_element(By.CSS_SELECTOR, "button").click()

# 关闭
driver.quit()
```

---

## 代码示例

### 等待元素
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located((By.ID, "myDynamicElement"))
)
```

### 截图
```python
driver.save_screenshot("screenshot.png")
```

### 执行 JavaScript
```python
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
```

---

## Selenium vs Playwright

| 特性 | Selenium | Playwright |
|------|----------|------------|
| 速度 | 较慢 | 快 |
| 自动等待 | 需手动 | 自动 |
| 浏览器 | 全支持 | 主流 |
| 语言 | 多语言 | TS/Python |
| 生态 | 成熟 | 新兴 |

**建议**:
- 新项目 → Playwright
- 遗留项目 → Selenium

---

## 最佳实践

1. **显式等待**: 用 WebDriverWait 代替 sleep
2. **Page Object**: 封装页面逻辑
3. **数据驱动**: 测试数据外置
4. **并行执行**: 用 Grid 提高速度
5. **CI/CD 集成**: 自动化运行

---

## 工作流程

```
1. 理解需求（自动化场景）
2. 分析页面（元素定位策略）
3. 编写脚本（Python + Selenium）
4. 运行验证（本地/CI）
5. 维护更新（页面变更时）
```

---

## 相关文档

- `tools/playwright.md` - Playwright 对比
- `workflows/testing-workflow.md` - 测试流程
- `agents/qa-agent.md` - QA Agent

---

**Version**: 1.0  
**Last Updated**: 2026-03-06  
**Skills Installed**: selenium-automation
