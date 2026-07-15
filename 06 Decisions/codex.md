---
type: moc
topics: [decisions]
status: active
---

# Decisions MOC

> 记录选择、约束和取舍，帮助未来判断某项做法是否仍然适用。

## 平台配置

- [[06 Decisions/codex-config-decisions|Codex 配置决策]] — 解释核心配置项和启用理由。
- [[06 Decisions/rules-default|默认规则]] — 记录命令许可边界及其与系统配置的关系。

对应架构见 [[05 Architecture/codex-system-architecture|Codex 系统架构]]，验证这些选择的经验见 [[07 Lessons/codex-lessons|Codex 使用经验]]。

## 安全

- [[06 Decisions/security-tools-decision-log|安全工具选择]] — 区分最佳实践、所有权分析和威胁建模。
- [[06 Decisions/linktech-security|LinkTech 安全策略]] — 约束认证、CSRF、Session 和凭证处理。

LinkTech 安全策略直接作用于 [[05 Architecture/linktech-user-system|用户系统]]，排障反馈汇总在 [[07 Lessons/linktech-troubleshooting|故障排查]]。

## 设计

- [[06 Decisions/taste-skill-design-philosophy|Taste Skill 设计理念]] — 解释反模板化设计的原则和边界。

通用原则由 [[03 Skills/taste-skill|Taste Skill]] 执行，项目约束由 [[03 Skills/linktec-frontend-taste|LinkTech Frontend Taste]] 落地。

## 继续探索

- [[../codex|返回 AI-Brain 总入口]]
- [[03 Skills/codex|查看执行决策的能力]]
- [[05 Architecture/codex|查看决策约束的架构]]
- [[07 Lessons/codex|查看决策产生的结果]]
