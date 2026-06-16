# 多模型协作分析 Skill

## 📖 这是什么？

这是一个**通用的**多模型协作分析技能。通过分配多个子Agent（不同难度任务给不同模型）并行分析，最后由主Agent整合所有结果给出综合判断。

**特点：不依赖特定模型，支持任意provider和模型组合！**

---

## 🎯 核心价值

**不是简单列出多个模型的结果，而是：**
1. ✅ 分配任务：不同难度给不同模型
2. ✅ 一次性调用：避免超时问题
3. ✅ 整合分析：主Agent给出真正深入的判断

---

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| SKILL.md | 完整的技能说明和使用方法 |
| QUICKREF.md | 快速参考卡片 |
| examples.md | 实战案例（足球预测、产品分析、技术评估） |

---

## 🚀 快速开始

### Step 1: 查看你的可用模型

```javascript
// 查看已配置的AI提供者
mcp__Localfilemanagement__ai_providers()
```

### Step 2: 一次性调用（根据实际配置填写）

```javascript
mcp__Localfilemanagement__ai_multi_chat({
  message: "请分析...",
  targets: [
    // 根据你的实际配置修改以下内容
    {"provider": "你的provider1", "model": "模型1", "max_tokens": 300},
    {"provider": "你的provider2", "model": "模型2", "max_tokens": 400},
    {"provider": "你的provider3", "model": "模型3", "max_tokens": 400},
    {"provider": "你的provider4", "model": "模型4", "max_tokens": 400}
  ]
})
```

### Step 3: 整合结果

收到四个模型的结果后，主Agent进行整合分析，给出综合判断。

---

## 💡 适用场景

- ⚽ 体育赛事预测
- 📱 产品决策分析
- 💻 技术方案评估
- 📊 市场趋势分析
- ⚠️ 风险评估
- 🎯 任何需要多角度分析的问题

---

## 📌 关键经验

### ❌ 错误做法
1. 逐个调用模型（会超时）
2. 只是罗列结果，不做整合
3. 把模型名称硬编码

### ✅ 正确做法
1. **一次性调用**所有模型
2. **分工明确**：基础模型做基础事，高级模型做高级事
3. **主Agent是核心**：整合所有结果，给出真正有价值的判断
4. **模型可替换**：根据实际配置调整

---

## 🎯 成功案例

### 案例：2026世界杯法国 vs 塞内加尔预测
- Agent1(基础)：两队基本信息对比
- Agent2(中等)：战术对位分析
- Agent3(高级)：胜负概率推演
- Agent4(专家)：最终预测建议
- **主Agent整合**：法国70%概率赢，预测比分2-1

---

## 🔄 如何切换模型？

只需要修改 `targets` 数组中的 provider 和 model 名称即可：

```javascript
// 从 DeepSeek 切换到 Qwen
// 之前
{"provider": "DeepSeek", "model": "deepseek-chat", ...}

// 之后
{"provider": "Qwen", "model": "qwen-plus", ...}
```

**方法论不变，模型可以随便换！**

---

> 💡 **记住：模型提供信息，你提供智慧。模型可以换，方法论不变。**
