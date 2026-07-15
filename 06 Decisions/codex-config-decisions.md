---
type: decision
topics: [codex, configuration]
status: reference
---

# Codex 配置决策记录

> 2026-07-12 从 `~/.codex/config.toml` 分析

**交叉引用：** [[../05 Architecture/codex-system-architecture|系统架构]] · [[rules-default|默认规则]] · [[../07 Lessons/codex-lessons|经验教训]]

## 关键配置项

| 配置 | 值 | 说明 |
|------|-----|------|
| `service_tier` | `priority` | 优先服务等级 |
| `features.js_repl` | `false` | JS REPL 功能已关闭 |
| `desktop.conversationDetailMode` | `STEPS_COMMANDS` | 对话详情显示模式 |
| `desktop.ambient-suggestions-enabled` | `true` | 启用环境建议 |
| `desktop.followUpQueueMode` | `queue` | 跟进问题排队模式 |
| `desktop.dock-icon-preference` | `app-default` | Dock 图标偏好 |

## 打开方式偏好

- 全局默认：在 VS Code 中打开
- 部分 worktree 例外配置为 terminal

## 通知配置

- 通知命令：`SkyComputerUseClient`（turn-ended 事件）
