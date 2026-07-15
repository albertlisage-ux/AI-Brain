---
type: moc
topics: [skills]
status: active
---

# Skills MOC

> 可复用能力与工作流入口。按任务选择 Skill，再沿链接进入其架构、决策或使用经验。

## Codex 平台能力

| Skill | 解决的问题 |
|---|---|
| [[03 Skills/system-openai-docs-skill|OpenAI Docs]] | 查找官方 OpenAI 与 Codex 资料 |
| [[03 Skills/system-skill-creator-skill|Skill Creator]] | 创建结构清晰、可验证的 Skill |
| [[03 Skills/system-skill-installer-skill|Skill Installer]] | 安装和管理 Skill |
| [[03 Skills/system-plugin-creator-skill|Plugin Creator]] | 创建 Codex 插件及 marketplace 元数据 |

理解这些能力如何装配，继续阅读 [[05 Architecture/codex-system-architecture|Codex 系统架构]]；理解配置取舍，进入 [[06 Decisions/codex-config-decisions|Codex 配置决策]]。

## 内容与自动化

| Skill | 解决的问题 |
|---|---|
| [[03 Skills/pdf-skill|PDF]] | 读取、生成并渲染检查 PDF |
| [[03 Skills/system-imagegen-skill|ImageGen]] | 生成或编辑位图 |
| [[03 Skills/playwright-skill|Playwright]] | 自动化浏览器交互和页面验证 |
| [[03 Skills/screenshot-skill|Screenshot]] | 捕获桌面或应用画面 |
| [[03 Skills/ai-rag-setup-guide|AI RAG]] | 在本地知识库上进行语义检索与问答 |

AI RAG 的实现经验记录在 [[07 Lessons/rag-playground-dev-log|Playground 开发日志]]。

## 安全

| Skill | 使用时机 |
|---|---|
| [[03 Skills/security-best-practices-skill|Security Best Practices]] | 检查支持语言的安全默认值 |
| [[03 Skills/security-ownership-map-skill|Security Ownership Map]] | 从 Git 历史分析敏感代码所有权 |
| [[03 Skills/security-threat-model-skill|Security Threat Model]] | 建模资产、边界和滥用路径 |

三者的选择逻辑见 [[06 Decisions/security-tools-decision-log|安全工具决策]]。

## 设计

| Skill | 使用时机 |
|---|---|
| [[03 Skills/taste-skill|Taste Skill]] | 避免模板化、缺乏辨识度的前端设计 |
| [[03 Skills/ui-ux-pro-max-skill|UI/UX Pro Max]] | 查询布局、配色、字体和体验规则 |
| [[03 Skills/linktec-frontend-taste|LinkTech Frontend Taste]] | 将通用设计原则约束到工业门户 |

设计取舍的理由见 [[06 Decisions/taste-skill-design-philosophy|Taste Skill 设计理念]]。

## 项目专用

[[03 Skills/linktec-skill|LinkTech Skill]] 将项目规则映射到 [[02 Projects/LinkTech-hydraulic/linktec|项目主页]]、实现架构、安全决策和排障经验。

## 继续探索

- [[../codex|返回 AI-Brain 总入口]]
- [[05 Architecture/codex|按系统查看架构]]
- [[06 Decisions/codex|按作用范围查看决策]]
- [[07 Lessons/codex|按来源查看经验]]
