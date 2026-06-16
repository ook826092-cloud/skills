---
name: multi-agent-analysis
description: 多模型协作分析系统：通过分配多个子Agent（不同难度任务给不同模型）并行分析，最后由主Agent整合所有结果给出综合判断。适用于复杂问题的多角度分析、预测、决策等场景。
---

# 多模型协作分析系统

## 📌 核心理念

**不是简单列出多个模型的结果，而是：**
1. **分配任务**：不同难度的任务给不同能力的模型
2. **并行执行**：一次性调用所有模型，避免超时
3. **整合分析**：主Agent融合所有见解，给出真正深入的综合判断

---

## 🎯 第一步：查看可用模型

在使用前，先查看你配置了哪些模型：

```javascript
// 查看已配置的AI提供者
mcp__Localfilemanagement__ai_providers()
```

然后根据实际配置的模型来分配任务。

---

## 🎯 模型分配策略（通用）

**原则：能力强的模型做复杂任务，能力弱的模型做简单任务**

| 任务难度 | 推荐模型类型 | 职责 |
|:---:|:---:|------|
| ⭐ 基础 | 轻量级/快速模型 | 数据整理、基本信息对比 |
| ⭐⭐ 中等 | 中等能力模型 | 战术分析、对手分析 |
| ⭐⭐⭐ 高级 | 强能力模型 | 概率推演、场景分析 |
| ⭐⭐⭐⭐ 专家 | 最强模型 | 综合判断、最终预测 |

### 模型分配示例（根据实际配置调整）

```javascript
// 示例1：如果你配置的是 DeepSeek
targets: [
  {"provider": "DeepSeek", "model": "deepseek-chat", "max_tokens": 300},
  {"provider": "DeepSeek", "model": "deepseek-coder", "max_tokens": 400},
  {"provider": "DeepSeek", "model": "deepseek-reasoner", "max_tokens": 400},
  {"provider": "DeepSeek", "model": "deepseek-chat", "max_tokens": 400}
]

// 示例2：如果你配置的是 Qwen
targets: [
  {"provider": "Qwen", "model": "qwen-turbo", "max_tokens": 300},
  {"provider": "Qwen", "model": "qwen-plus", "max_tokens": 400},
  {"provider": "Qwen", "model": "qwen-max", "max_tokens": 400},
  {"provider": "Qwen", "model": "qwen-max", "max_tokens": 400}
]

// 示例3：混合多个provider
targets: [
  {"provider": "Provider1", "model": "model-a", "max_tokens": 300},
  {"provider": "Provider2", "model": "model-b", "max_tokens": 400},
  {"provider": "Provider3", "model": "model-c", "max_tokens": 400},
  {"provider": "Provider4", "model": "model-d", "max_tokens": 400}
]
```

---

## 🚀 使用方法

### 第一步：一次性调用所有模型

**必须使用 `mcp__Localfilemanagement__ai_multi_chat` 一次性调用，不要逐个调用！**

```
错误做法 ❌：逐个调用 model-a → model-b → model-c → model-d
正确做法 ✅：一次性调用四个模型
```

### 第二步：调用模板

```javascript
// 使用 mcp__Localfilemanagement__ai_multi_chat
{
  "message": "你的分析主题和要求...",
  "targets": [
    {"provider": "你的provider", "model": "模型1", "max_tokens": 300},
    {"provider": "你的provider", "model": "模型2", "max_tokens": 400},
    {"provider": "你的provider", "model": "模型3", "max_tokens": 400},
    {"provider": "你的provider", "model": "模型4", "max_tokens": 400}
  ]
}
```

### 第三步：主Agent整合分析

**收到四个模型的结果后，主Agent必须：**

1. **提取关键洞察**：从每个Agent的分析中提取核心观点
2. **识别共识与分歧**：哪些观点一致？哪些有冲突？
3. **补充自身判断**：结合你的知识和逻辑推理
4. **给出最终结论**：一个清晰、有深度的综合判断

---

## 📋 分析流程模板

### 1. 足球比赛分析

```
Step 1: 搜索比赛信息（使用 mcp__exa__web_search_exa）
Step 2: 一次性调用四个模型分析
Step 3: 主Agent整合，给出最终预测
```

**调用示例：**
```
message: "请分析[赛事] [队伍A] vs [队伍B] 的比赛。

【队伍A信息】...
【队伍B信息】...

请各自分析：
1. Agent1(基础)：两队基本信息对比
2. Agent2(中等)：战术对位分析  
3. Agent3(高级)：胜负概率推演
4. Agent4(专家)：最终预测建议"
```

### 2. 产品决策分析

```
message: "请分析 [产品/方案] 的可行性。

【背景信息】...

请各自分析：
1. Agent1(基础)：市场数据和基本信息
2. Agent2(中等)：竞争分析和用户需求
3. Agent3(高级)：风险评估和场景推演
4. Agent4(专家)：综合建议和决策"
```

### 3. 技术方案评估

```
message: "请评估 [技术方案] 的优劣。

【方案详情】...

请各自分析：
1. Agent1(基础)：技术栈对比
2. Agent2(中等)：性能和可维护性
3. Agent3(高级)：扩展性和风险
4. Agent4(专家)：最终推荐"
```

---

## ✅ 整合分析模板

收到四个Agent的结果后，按以下结构整合：

```markdown
# [分析主题] 综合分析报告

## 📌 核心结论
[一句话总结]

## 🧠 综合四个Agent的洞察

### 一、[关键点1]
[整合Agent们的观点 + 你的判断]

### 二、[关键点2]  
[整合Agent们的观点 + 你的判断]

### 三、[关键点3]
[整合Agent们的观点 + 你的判断]

## ⚠️ 风险与注意事项
[从所有Agent中提取的警告]

## 🎯 最终判断
| 项目 | 预测 |
|------|------|
| [关键指标1] | [你的预测] |
| [关键指标2] | [你的预测] |

## 💬 一句话总结
> [精炼的最终结论]
```

---

## ⚠️ 注意事项

1. **必须一次性调用**：逐个调用会导致超时
2. **控制token数量**：每个Agent的max_tokens建议300-500
3. **主Agent是核心**：模型提供视角，主Agent负责整合判断
4. **不要只是罗列**：真正的价值在于整合分析
5. **模型可替换**：根据实际配置调整模型名称

---

## 📁 文件位置

- 本文件：`/skills/multi-agent-analysis/SKILL.md`
- 快速参考：`/skills/multi-agent-analysis/QUICKREF.md`
- 实战案例：`/skills/multi-agent-analysis/examples.md`

---

## 🎯 适用场景

- ✅ 体育赛事预测
- ✅ 产品决策分析  
- ✅ 技术方案评估
- ✅ 市场趋势分析
- ✅ 风险评估
- ✅ 任何需要多角度分析的问题

---

> 💡 **记住：模型提供信息，你提供智慧。模型可以换，方法论不变。**
