---
type: architecture
topics: [codex]
status: reference
---

# Codex 系统架构概览

> 源自 `~/.codex/` 配置分析，2026-07-12

**交叉引用：** [[../06 Decisions/codex-config-decisions|配置决策]] · [[../03 Skills/skills-moc|Skills 索引]] · [[computer-use-architecture|Computer Use 架构]] · [[../06 Decisions/rules-default|默认规则]]

## 目录结构

```
~/.codex/
├── config.toml              # 主配置（MCP、插件、项目信任等）
├── rules/default.rules      # 默认规则
├── skills/                  # Skills 目录
│   ├── .system/             # 预装系统 Skills
│   │   ├── imagegen/
│   │   ├── openai-docs/
│   │   ├── plugin-creator/
│   │   ├── skill-creator/
│   │   └── skill-installer/
│   ├── pdf/
│   ├── playwright/
│   ├── screenshot/
│   ├── security-best-practices/
│   ├── security-ownership-map/
│   ├── security-threat-model/
│   ├── taste-skill/
│   └── ui-ux-pro-max/
├── computer-use/            # Computer Use 功能
│   ├── config.json
│   └── Codex Computer Use.app/
├── plugins/                 # 插件缓存
├── sessions/                # 会话记录
├── cache/                   # 缓存
├── memories_1.sqlite        # 记忆数据库
├── session_index.jsonl      # 会话索引
├── state_5.sqlite           # 状态数据库
├── goals_1.sqlite           # 目标数据库
├── logs_2.sqlite            # 日志数据库
└── models_cache.json        # 模型缓存
```

## 启用的插件

| 插件 | 来源 Marketplace |
|------|-----------------|
| documents | openai-primary-runtime |
| pdf | openai-primary-runtime |
| spreadsheets | openai-primary-runtime |
| presentations | openai-primary-runtime |
| template-creator | openai-primary-runtime |
| chrome | openai-bundled |
| visualize | openai-bundled |
| browser | openai-bundled |

## MCP 服务器配置

| 服务器 | 类型 | 状态 |
|--------|------|------|
| node_repl | 本地命令 | 启用（浏览器/Chrome/Computer Use） |
| computer-use | 本地应用 | 已禁用 |
| designmd | 远程 URL | 启用 |

## 项目信任配置

已信任的项目路径：
- `/` (根)
- `/Users/LinkTec/`
- `/Users/LinkTec/LinkTech-hydraulic/`
- `/Users/yuanzhe/Documents/Codex/2026-07-02/lia/`
