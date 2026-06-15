---
name: ai-video-generator
description: AI 视频生成 Skill：通过调用大模型 API 生成视频，支持 OpenAI Sora、Google Veo、可灵、混元等多种 API。
---

## 功能介绍

AI 视频生成 Skill：通过调用大模型 API 生成视频。
支持多种视频生成 API（Agnes AI、OpenAI Sora、Google Veo、可灵、混元等）。
支持三种 API 格式：/v1/video/generations、/v1/videos、异步任务轮询。

## 使用方法

### 1. 基本用法

```bash
# 使用可灵 API
curl -X POST "https://api.klingai.com/v1/videos" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"prompt": "一只猫在草地上奔跑", "duration": 5}'
```

### 2. 支持的 API

| API | 格式 | 说明 |
|-----|------|------|
| OpenAI Sora | /v1/videos | 官方格式 |
| Google Veo | 异步任务 | 需要轮询 |
| 可灵 | 异步任务 | 需要轮询 |
| 混元 | 异步任务 | 需要轮询 |

### 3. 参数说明

- `prompt`: 视频描述（必填）
- `duration`: 视频时长（秒）
- `resolution`: 分辨率
- `model`: 使用的模型

## 文件位置（均在本 skill 目录内）

- 使用说明：本文件

## 注意事项

- 需要配置相应的 API Key
- 视频生成通常需要较长时间
- 大部分 API 使用异步模式，需要轮询结果
- 生成的视频会保存到指定位置
