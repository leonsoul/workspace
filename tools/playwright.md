# Playwright 自动化工具

---

## 概述

Playwright 用于网页自动化和 E2E 测试：
- 跨浏览器（Chromium/Firefox/WebKit）
- 自动等待元素
- 截图/录屏
- 网络拦截

---

## 已安装 Skills

| Skill | 来源 | 安全等级 |
|-------|------|----------|
| `playwright-generate-test` | github/awesome-copilot | ✅ Safe |
| `playwright-cli` | microsoft/playwright-cli | ⚠️ Med Risk |

**安装路径**: `~/.agents/skills/`

---

## 基本用法

### 1. 生成测试（playwright-generate-test）
```
用户：为这个页面生成测试
URL: https://example.com/login

Playwright Agent:
1. 分析页面结构
2. 生成测试用例
3. 输出 test.spec.ts
```

### 2. 浏览网站（playwright-explore-website）
```
用户：分析这个网站的结构
URL: https://example.com

输出:
- 页面层级
- 主要功能
- 表单/按钮列表
```

### 3. CLI 工具（playwright-cli）
```bash
# 安装浏览器
npx playwright install

# 运行测试
npx playwright test

# 生成报告
npx playwright show-report
```

---

## 代码示例

### 基础测试
```typescript
import { test, expect } from '@playwright/test';

test('登录测试', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.fill('#username', 'test');
  await page.fill('#password', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

### 截图
```typescript
await page.screenshot({ path: 'screenshot.png' });
```

### 等待元素
```typescript
await page.waitForSelector('.loaded');
await page.waitForTimeout(1000); // 不推荐，优先用 waitForSelector
```

---

## 最佳实践

1. **使用 Page Object 模式**: 封装页面操作
2. **自动等待**: 用 `waitForSelector` 代替 `waitForTimeout`
3. **独立测试**: 每个测试独立，不依赖顺序
4. **数据隔离**: 使用 fixture 数据
5. **CI/CD 集成**: GitHub Actions 自动运行

---

## 工作流程

```
1. 理解需求（测试目标/页面）
2. 分析页面（snapshot/浏览）
3. 生成测试（playwright-generate-test）
4. 运行验证（playwright test）
5. 修复问题（调试/重试）
```

---

## 相关文档

- `workflows/testing-workflow.md` - 测试流程
- `tools/browser.md` - Browser 自动化
- `agents/qa-agent.md` - QA Agent

---

**Version**: 1.0  
**Last Updated**: 2026-03-06  
**Skills Installed**: playwright-generate-test, playwright-cli
