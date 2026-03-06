# Browser 自动化工具

---

## 概述

Browser 工具用于网页自动化：
- 导航到 URL
- 点击元素
- 填写表单
- 截图
- 提取内容

---

## 基本用法

### 导航
```
browser(action="navigate", url="https://example.com")
```

### 截图
```
browser(action="screenshot", fullPage=true)
```

### 点击
```
browser(action="act", kind="click", ref="e12")
```

### 输入
```
browser(action="act", kind="type", ref="e15", text="hello")
```

### 提取内容
```
browser(action="snapshot", refs="aria")
```

---

## 工作流程

```
1. 导航到页面
2. 等待加载
3. 截图/快照
4. 识别元素（ref）
5. 执行操作（click/type）
6. 验证结果
```

---

## 示例

### 1. 登录网页
```
1. navigate: https://example.com/login
2. snapshot: 获取元素 refs
3. type: 用户名 → e1
4. type: 密码 → e2
5. click: 登录按钮 → e3
6. snapshot: 验证登录成功
```

### 2. 抓取数据
```
1. navigate: https://example.com/data
2. snapshot: refs="aria"
3. evaluate: 提取数据的 JS
4. 保存结果
```

---

## 最佳实践

1. **等待加载**: 操作前确保页面加载完成
2. **使用 ARIA refs**: 更稳定的元素定位
3. **错误处理**: 操作失败要有备选方案
4. **截图验证**: 关键步骤截图记录

---

## 限制

- 不支持复杂验证码
- 需要页面可访问
- 大文件下载需特殊处理

---

**Version**: 1.0  
**Last Updated**: 2026-03-06
