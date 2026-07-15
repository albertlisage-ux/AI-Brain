---
type: lesson
topics: [codex]
status: reference
---

# Codex 使用经验记录

> 2026-07-12 初始导入

**交叉引用：** [[../05 Architecture/codex-system-architecture|系统架构]] · [[../06 Decisions/codex-config-decisions|配置决策]] · [[../00 Inbox/codex-import-2026-07-12|导入记录]]

## 已知注意事项

- `config.toml` 中 Computer Use 当前为禁用状态
- JS REPL 功能已关闭
- 通知通过 `SkyComputerUseClient` 发送 turn-ended 事件
- 个人 marketplace 路径：`~/.agents/plugins/marketplace.json`
- Skill 安装后需要**下一次对话**才生效
- `.system` 下的 Skills 是预装的，不需要手动安装

## 安全相关

- 开发环境下不应报告缺少 TLS 的问题
- 不推荐 HSTS（可能导致严重后果）
- `secure` cookie 仅在 TLS 部署下启用
- 安全修复时优先考虑不破坏现有功能
