---
type: moc
topics: [architecture]
status: active
aliases: [Architecture, Architecture MOC]
---

# Architecture MOC

> 系统组成、边界、数据流和运行方式的入口。

## Codex 与本地工具

- [[05 Architecture/codex-system-architecture|Codex 系统架构]] — 解释目录结构、插件、MCP 和项目信任边界。
- [[05 Architecture/computer-use-architecture|Computer Use 架构]] — 解释 macOS 桌面控制组件如何协作。

相关取舍记录在 [[06 Decisions/codex-config-decisions|Codex 配置决策]]，实践结果记录在 [[07 Lessons/codex-lessons|Codex 使用经验]]。

## LinkTech

- [[05 Architecture/linktech-user-system|用户与工单系统]] — 认证、注册、工单 API 和数据库交互。
- [[05 Architecture/linktech-product-system|产品系统]] — 目录驱动的产品导航、模板和品牌界面。
- [[05 Architecture/linktech-deployment|部署与运维]] — 页面生成、Webhook、发布和运维检查。

这些架构服务于 [[02 Projects/LinkTech-hydraulic/linktech-project|LinkTech 项目]]；安全边界由 [[06 Decisions/linktech-security|安全策略]] 约束，已知故障模式汇总在 [[07 Lessons/linktech-troubleshooting|排障手册]]。

## AI RAG

当前架构说明集中在 [[03 Skills/ai-rag-setup-guide#架构总览|AI RAG 架构总览]]。实现侧的演进与调试记录见 [[07 Lessons/rag-playground-dev-log|Playground 开发日志]]。

## 继续探索

- [[../AI-Brain|返回 AI-Brain 总入口]]
- [[03 Skills/skills-moc|从可复用能力进入]]
- [[06 Decisions/decisions-moc|查看架构背后的决策]]
- [[07 Lessons/lessons-moc|查看架构产生的经验]]
