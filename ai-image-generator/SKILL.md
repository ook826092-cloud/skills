---
name: ai-image-generator
description: AI 图片生成 Skill：通过调用大模型 API 生成图片，支持 OpenAI DALL-E、硅基流动、通义万相、可灵等多种 API。
---

## 功能介绍

AI 图片生成 Skill：通过调用大模型 API 生成图片。
支持多种生图 API（OpenAI DALL-E、Agnes AI、硅基流动、通义万相、可灵等）。
支持三种 API 格式：images/generations、chat/completions、异步任务。

## 使用方法

### 1. 基本用法

```bash
# 使用 OpenAI DALL-E
curl -X POST "https://api.openai.com/v1/images/generations" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"prompt": "一只可爱的猫咪", "n": 1, "size": "1024x1024"}'
```

### 2. 支持的 API

| API | 格式 | 说明 |
|-----|------|------|
| OpenAI DALL-E | images/generations | 标准格式 |
| 硅基流动 | chat/completions | 兼容格式 |
| 通义万相 | 异步任务 | 需要轮询 |
| 可灵 | 异步任务 | 需要轮询 |

### 3. 参数说明

- `prompt`: 图片描述（必填）
- `size`: 图片尺寸（1024x1024, 512x512 等）
- `n`: 生成数量
- `model`: 使用的模型

## 文件位置（均在本 skill 目录内）

- 使用说明：本文件

## 注意事项

- 需要配置相应的 API Key
- 不同 API 的计费方式不同
- 异步 API 需要轮询获取结果
