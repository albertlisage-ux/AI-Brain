---
type: architecture
topics: [codex, automation]
status: reference
---

# Computer Use 架构

**来源**: `~/.codex/computer-use/`  
**用途**: 控制 macOS 桌面应用的 Computer Use 功能  
**参考**: [[codex-system-architecture|Codex 系统架构]]

## 组件

```
Codex Computer Use.app
└── SkyComputerUseClient.app
    └── SkyComputerUseClient (主二进制)
```

## 配置

```json
{
  "accentColor": "#339cff",
  "direction": "ltr",
  "locale": "zh-CN",
  "strings": {
    "usingComputer": "ChatGPT is using your computer",
    "escToCancel": "Esc to cancel"
  }
}
```

- 语言：简体中文
- 强调色：蓝色 (`#339cff`)
- 当前状态：已禁用（`config.toml` 中 `enabled = false`）
