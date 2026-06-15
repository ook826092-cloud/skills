#!/usr/bin/env python3
"""
AI 子 Agent 使用示例
"""
import json
from ai_subagent import AISubAgentSystem

# 加载配置
with open("/workspace/ai_subagent_config.json") as f:
    config = json.load(f)

# 检查 API Key
if not config["api_key"]:
    print("请先配置 API Key!")
    print("编辑 /workspace/ai_subagent_config.json")
    print("填入你的 api_key")
    exit(1)

# 创建系统
system = AISubAgentSystem(config)

# 定义任务（每个任务都会由独立的 AI Agent 执行）
tasks = [
    {
        "name": "分析师",
        "desc": "分析 Python 的优势",
        "system_prompt": "你是一个资深技术分析师，擅长分析编程语言。",
        "prompt": "请用 3 句话分析 Python 语言的核心优势。"
    },
    {
        "name": "创作者",
        "desc": "写 AI 介绍",
        "system_prompt": "你是一个科技内容创作者，文笔生动有趣。",
        "prompt": "请用 3 句话写一段关于人工智能的科普介绍。"
    },
    {
        "name": "翻译官",
        "desc": "翻译技术概念",
        "system_prompt": "你是一个技术翻译专家，擅长中英互译。",
        "prompt": "请把 'Machine Learning' 翻译成中文，并解释这个概念。"
    }
]

# 并行执行
results = system.run_parallel(tasks)

# 打印结果
system.print_results()

# 获取汇总
summary = system.get_summary()
print(f"\n汇总: {json.dumps(summary, ensure_ascii=False, indent=2)}")