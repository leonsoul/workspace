# Data Agent Skills

## Available Tools

| Tool | Usage | Example |
|------|-------|---------|
| `read` | 读取数据文件 | `read(path="data.json")` |
| `write` | 写入数据文件 | `write(path="output.csv", content="...")` |
| `exec` | 执行处理脚本 | `exec(command="jq '.name' data.json")` |
| `web_fetch` | 抓取网页数据 | `web_fetch(url="...")` |
| `web_search` | 搜索数据源 | `web_search(query="dataset XXX")` |

## Common Patterns

### 1. JSON 处理 (Python)
```python
#!/usr/bin/env python3
import json

# 读取
with open('data.json', 'r') as f:
    data = json.load(f)

# 处理
result = [item for item in data if item['status'] == 'active']

# 写入
with open('output.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f"Processed {len(result)} records")
```

### 2. CSV 处理 (Python)
```python
#!/usr/bin/env python3
import csv

# 读取
with open('input.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# 处理
filtered = [row for row in data if int(row['age']) > 18]

# 写入
with open('output.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=filtered[0].keys())
    writer.writeheader()
    writer.writerows(filtered)

print(f"Exported {len(filtered)} records")
```

### 3. JSON ↔ CSV 转换
```python
#!/usr/bin/env python3
import json
import csv

# JSON to CSV
with open('data.json') as f:
    data = json.load(f)

with open('data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

# CSV to JSON
with open('data.csv') as f:
    reader = csv.DictReader(f)
    data = list(reader)

with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### 4. 数据统计
```python
#!/usr/bin/env python3
import json
from collections import Counter

with open('data.json') as f:
    data = json.load(f)

# 统计
status_count = Counter(item['status'] for item in data)
print("Status distribution:")
for status, count in status_count.items():
    print(f"  {status}: {count}")

# 平均值
values = [item['value'] for item in data if 'value' in item]
if values:
    print(f"Average: {sum(values)/len(values):.2f}")
```

### 5. 数据清洗
```python
#!/usr/bin/env python3
import json

with open('raw.json') as f:
    data = json.load(f)

# 清洗规则
cleaned = []
for item in data:
    # 跳过无效记录
    if not item.get('id'):
        continue
    
    # 标准化字段
    item['name'] = item.get('name', '').strip()
    item['email'] = item.get('email', '').lower().strip()
    
    # 移除多余字段
    item.pop('_id', None)
    
    cleaned.append(item)

with open('clean.json', 'w') as f:
    json.dump(cleaned, f, indent=2)

print(f"Cleaned: {len(data)} → {len(cleaned)} records")
```

### 6. Bash + jq 处理 JSON
```bash
#!/bin/bash

# 提取字段
jq '.name' data.json

# 过滤
jq '[.[] | select(.status == "active")]' data.json

# 统计
jq 'length' data.json

# 转换
jq -r '.[] | "\(.name),\(.email)"' data.json > output.csv
```

## Data Validation

### JSON Schema 验证
```python
import json
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
    },
    "required": ["name", "age"]
}

with open('data.json') as f:
    data = json.load(f)

try:
    validate(instance=data, schema=schema)
    print("✅ Valid")
except Exception as e:
    print(f"❌ Invalid: {e}")
```

## Limitations

- ❌ 不处理超大文件（>1GB，需分块）
- ❌ 不连接数据库（需通过 API）
- ❌ 不执行复杂分析（需专业工具）
- ❌ 不修改原始数据（先备份）

## Best Practices

1. **备份优先**: 修改前 cp 原文件
2. **流式处理**: 大文件逐行读取
3. **验证输入**: 检查格式和编码
4. **原子写入**: 先写临时文件再 mv
5. **记录日志**: 处理数量、错误数

---

**Version**: 1.0
**Last Updated**: 2026-03-06
