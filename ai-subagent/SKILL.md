---
name: ai-subagent
description: AI 子 Agent 系统：支持多个独立 AI Agent 并行执行任务，每个子 Agent 都有独立的 AI 推理能力，适用于并行分析、批量生成、多角度研究等场景。
---

## 功能介绍

AI 子 Agent 系统：支持多个独立 AI Agent 并行执行任务。
每个子 Agent 都有独立的 AI 推理能力，可以同时思考、同时返回结果。
适用于：并行分析、批量生成、多角度研究、任务分发等场景。

## 使用方法

### 1. 基本用法

```python
from ai_subagent import SubAgentSystem

# 创建子 Agent 系统
system = SubAgentSystem(api_key="your_api_key")

# 定义任务
tasks = [
    {"prompt": "分析这个方案的优缺点", "model": "deepseek"},
    {"prompt": "从用户角度评估这个设计", "model": "deepseek"},
    {"prompt": "找出潜在的技术风险", "model": "deepseek"},
]

# 并行执行
results = system.run_parallel(tasks)
```

### 2. 配置文件

配置文件 `ai_subagent_config.json` 包含：
- API 密钥
- 默认模型
- 并行数量限制
- 超时设置

### 3. 返回结果

```python
results = system.run_parallel(tasks)
for result in results:
    print(f"任务 {result['task_id']}: {result['response']}")
```

## 文件位置（均在本 skill 目录内）

- 核心系统：`ai_subagent.py`
- 配置文件：`ai_subagent_config.json`
- 使用示例：`example_subagent.py`

## 注意事项

- 需要配置 API Key 才能使用
- 每个 Agent 会消耗 API 调用额度
- 并行数量建议不超过 5 个（避免 API 限流）
- 结果会自动汇总，可以打印或进一步处理
