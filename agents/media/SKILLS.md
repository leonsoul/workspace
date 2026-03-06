# Media Agent Skills

## Available Tools

| Tool | Usage | Example |
|------|-------|---------|
| `image` | 图片分析 | `image(image="pic.jpg", prompt="描述内容")` |
| `read/write` | 文件操作 | `write(path="output.jpg", content=base64)` |
| `exec` | 调用工具 | `exec(command="ffmpeg -i input.mp4 output.gif")` |
| `web_search` | 找素材 | `web_search(query="free stock photos")` |
| `browser` | 下载资源 | `browser(action="navigate", url="...")` |

## Common Patterns

### 1. 图片分析
```python
# 使用 image tool 分析
# 工具调用（由 AI 执行）
image(
    image="/path/to/image.jpg",
    prompt="描述这张图片的内容，包括文字、物体、场景"
)

# 输出示例：
# "这是一张产品图片，白色背景，中央有一个黑色耳机，
# 右上角有文字'Wireless Headphones'"
```

### 2. 图片格式转换 (ImageMagick)
```bash
#!/bin/bash
# Convert: image format

INPUT="$1"
OUTPUT="$2"
FORMAT="${3:-jpg}"

# 检查文件
if [ ! -f "$INPUT" ]; then
    echo "Error: File not found: $INPUT"
    exit 1
fi

# 转换
convert "$INPUT" -quality 85 "$OUTPUT"

# 验证
if [ -f "$OUTPUT" ]; then
    SIZE_BEFORE=$(stat -f%z "$INPUT" 2>/dev/null || stat -c%s "$INPUT")
    SIZE_AFTER=$(stat -f%z "$OUTPUT" 2>/dev/null || stat -c%s "$OUTPUT")
    RATIO=$(echo "scale=2; $SIZE_AFTER * 100 / $SIZE_BEFORE" | bc)
    echo "✅ Converted: $INPUT → $OUTPUT"
    echo "   Size: $SIZE_BEFORE → $SIZE_AFTER bytes ($RATIO%)"
else
    echo "❌ Conversion failed"
    exit 1
fi
```

### 3. 图片压缩
```bash
#!/bin/bash
# Compress: image with quality control

INPUT="$1"
OUTPUT="$2"
QUALITY="${3:-75}"
MAX_WIDTH="${4:-1920}"

convert "$INPUT" \
    -resize "${MAX_WIDTH}x>" \
    -quality "$QUALITY" \
    -strip \
    "$OUTPUT"

echo "Compressed: $OUTPUT (quality=$QUALITY, max-width=$MAX_WIDTH)"
```

### 4. 视频转 GIF
```bash
#!/bin/bash
# Video to GIF

INPUT="$1"
OUTPUT="$2"
FPS="${3:-10}"
WIDTH="${4:-480}"

ffmpeg -i "$INPUT" \
    -vf "fps=$fps,scale=${WIDTH}:-1:flags=lanczos" \
    -y "$OUTPUT"

echo "Created GIF: $OUTPUT"
```

### 5. 提取视频帧
```bash
#!/bin/bash
# Extract frame from video

VIDEO="$1"
OUTPUT_DIR="$2"
INTERVAL="${3:-60}"  # seconds

mkdir -p "$OUTPUT_DIR"

ffmpeg -i "$VIDEO" \
    -vf "fps=1/$INTERVAL" \
    "$OUTPUT_DIR/frame_%03d.jpg"

echo "Extracted frames to: $OUTPUT_DIR"
```

### 6. 批量处理图片
```bash
#!/bin/bash
# Batch process images

INPUT_DIR="$1"
OUTPUT_DIR="$2"
FORMAT="${3:-jpg}"

mkdir -p "$OUTPUT_DIR"

for img in "$INPUT_DIR"/*.{png,jpg,jpeg,gif}; do
    [ -f "$img" ] || continue
    
    basename=$(basename "$img")
    name="${basename%.*}"
    
    convert "$img" \
        -resize "1920x>" \
        -quality 85 \
        "$OUTPUT_DIR/$name.$FORMAT"
    
    echo "Processed: $basename"
done

echo "Batch complete: $OUTPUT_DIR"
```

### 7. 图片添加水印
```bash
#!/bin/bash
# Add watermark to image

INPUT="$1"
WATERMARK="$2"
OUTPUT="$3"
POSITION="${4:-south-east}"  # north-west, north-east, south-west, south-east

composite \
    -gravity "$POSITION" \
    -geometry +10+10 \
    "$WATERMARK" \
    "$INPUT" \
    "$OUTPUT"

echo "Watermarked: $OUTPUT"
```

## Image Analysis Prompt Templates

### 通用描述
```
请详细描述这张图片：
1. 主要物体/人物
2. 场景/背景
3. 颜色/光线
4. 文字内容（如有）
5. 可能的用途
```

### OCR 提取
```
请提取图片中的所有文字：
- 按从上到下顺序
- 保留原始格式
- 标注不确定的文字
```

### 内容审核
```
请检查这张图片是否包含：
- 敏感/不当内容
- 个人隐私信息
- 版权保护内容
- 质量问题（模糊、过曝等）
```

## Limitations

- ❌ 不处理超大文件（>500MB）
- ❌ 不编辑复杂视频（需专业软件）
- ❌ 不生成 AI 图片（需专门服务）
- ❌ 不上传敏感图片到外部

## Best Practices

1. **保留原文件**: 处理前 cp 备份
2. **检查空间**: df -h 确认磁盘空间
3. **渐进处理**: 先小图测试再全量
4. **清理临时**: 处理完 rm 临时文件
5. **验证输出**: 检查文件完整性

---

**Version**: 1.0
**Last Updated**: 2026-03-06
