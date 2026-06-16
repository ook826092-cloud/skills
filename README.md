# RikkaHub Skills

> 🤖 41 个 AI Agent 技能包，专为 RikkaHub 优化

**🌐 语言切换 | [English](README.en.md) | [繁體中文](README.zh-Hant.md)**

## 📦 技能列表

| # | 名称 | 说明 |
|---|------|------|
| 1 | ai-image-generator | AI 图片生成，支持 DALL-E、硅基流动、通义万相、可灵等 |
| 2 | ai-subagent | AI 子 Agent 系统，支持多个 Agent 并行执行任务 |
| 3 | ai-video-generator | AI 视频生成，支持 Sora、Veo、可灵、混元等 |
| 4 | caveman | 简化复杂概念，用通俗易懂的方式解释 |
| 5 | de-ai-ify | 去除 AI 味道，让文本更自然 |
| 6 | design-an-interface | 设计用户界面 |
| 7 | diagnose | 诊断问题并提供解决方案 |
| 8 | edit-article | 编辑和优化文章 |
| 9 | elon-musk-perspective | 用马斯克的思维方式分析问题 |
| 10 | git-guardrails-claude-code | Git 安全防护，防止危险操作 |
| 11 | grill-me | 深度拷问你的计划或设计 |
| 12 | grill-with-docs | 带文档的深度拷问 |
| 13 | gsap-helper | GSAP 动画库助手 |
| 14 | handoff | 将对话压缩成交接文档 |
| 15 | hu-chenfeng-skill | 户晨风视角分析，消费现实主义思维框架 |
| 15 | hu-chen-feng-skill | 胡晨枫视角分析 |
| 16 | improve-codebase-architecture | 改进代码架构 |
| 17 | migrate-to-shoehorn | 迁移到 Shoehorn 框架 |
| 18 | obsidian-vault | Obsidian 知识库管理 |
| 19 | prototype | 快速原型制作 |
| 20 | qa | 质量保证和测试 |
| 21 | request-refactor-plan | 请求重构计划 |
| 22 | review | 代码/文档审查 |
| 23 | scaffold-exercises | 创建练习题 |
| 24 | serenity-skill | 投资分析，供应链瓶颈识别 |
| 25 | setup-matt-pocock-skills | 设置 Matt Pocock 技能 |
| 26 | setup-pre-commit | 设置 Git pre-commit 钩子 |
| 27 | tdd | 测试驱动开发 |
| 28 | teach | 教学和知识传授 |
| 29 | to-issues | 将内容转换为 GitHub Issues |
| 30 | to-prd | 将内容转换为产品需求文档 |
| 31 | tong-jincheng-perspective | 童锦程视角分析 |
| 32 | triage | 问题分类和优先级排序 |
| 33 | ubiquitous-language | 统一语言定义（领域驱动设计） |
| 34 | write-a-skill | 创建新的 Agent 技能 |
| 35 | writing-beats | 写作节拍和节奏 |
| 36 | writing-fragments | 写作片段 |
| 37 | writing-shape | 写作结构和形状 |
| 38 | zhangxuefeng-perspective | 张雪峰视角分析 |
| 39 | zoom-out | 跳出细节，宏观思考 |
| 40 | multi-agent-analysis | 多模型协作分析系统：通过分配多个子Agent并行分析，最后整合结果给出综合判断 |

## 🚀 使用方法

### 在 RikkaHub 中使用

1. 打开 RikkaHub
2. 进入「代理技能」页面
3. 技能会自动加载

### 手动安装

```bash
# 克隆仓库
git clone https://github.com/ook826092-cloud/skills.git

# 将技能目录复制到 RikkaHub 的 skills 目录
cp -r skills/* /path/to/rikkahub/skills/
```

## 📁 目录结构

```
skills/
├── ai-image-generator/
│   └── SKILL.md
├── ai-subagent/
│   ├── SKILL.md
│   ├── ai_subagent.py
│   ├── ai_subagent_config.json
│   └── example_subagent.py
├── ai-video-generator/
│   └── SKILL.md
├── ... 其他技能
├── LICENSE              # MIT 许可证（英文）
├── LICENSE-zh-Hans      # MIT 许可证（简体中文）
├── LICENSE-zh-Hant      # MIT 许可证（繁体中文）
├── README.md            # 本文档（简体中文）
├── README.en.md         # English
└── README.zh-Hant.md    # 繁體中文
```

## ⚠️ 注意事项

- 部分技能需要配置 API Key 才能使用
- AI 生成类技能会消耗 API 额度
- 建议定期更新技能包

## 📝 更新日志

| 日期 | 版本 | 内容 |
|------|------|------|
| 2026-06-15 | 1.0 | 初始版本，41 个技能 |

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

中文版：[LICENSE-zh-Hans](LICENSE-zh-Hans) | 繁體中文：[LICENSE-zh-Hant](LICENSE-zh-Hant)

---

> 🤖 由 RikkaHub 社区维护
