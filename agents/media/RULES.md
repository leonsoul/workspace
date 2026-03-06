# Media Agent Rules

## Core Rules

### 1. 文件安全
- ✅ 处理前备份原文件
- ✅ 检查磁盘空间
- ✅ 临时文件及时清理
- ✅ 支持常见格式

### 2. 质量保证
- ✅ 压缩不损失关键质量
- ✅ 转换保留元数据
- ✅ 输出验证完整性
- ✅ 大文件分块处理

### 3. 版权合规
- ✅ 注明素材来源
- ✅ 优先使用免费素材
- ✅ 商业使用需授权
- ✅ 不处理侵权内容

### 4. 性能优化
- ✅ 大图缩略图预览
- ✅ 批量处理并行
- ✅ 缓存重复结果
- ✅ 流式处理视频

### 5. 用户隐私
- ✅ 不上传敏感图片
- ✅ 处理完删除临时文件
- ✅ 不保留用户媒体
- ✅ 人脸/文字可模糊

## Supported Formats

| Type | Input | Output |
|------|-------|--------|
| Image | JPG, PNG, GIF, WebP, SVG | JPG, PNG, WebP |
| Video | MP4, MOV, AVI | MP4, GIF |
| Audio | MP3, WAV, AAC | MP3, WAV |

## Handoff Protocol

需要其他 Agent 协助时：

```markdown
## 需要协助
- **任务**: XXX
- **目标 Agent**: Dev/QA/Ops/Data
- **原因**: XXX
- **上下文**: [粘贴相关信息]
```

---

**Version**: 1.0
**Last Updated**: 2026-03-06
