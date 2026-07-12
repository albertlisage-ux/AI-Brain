# Rules 默认规则

**来源**: `~/.codex/rules/default.rules`  
**参考**: [[../05 Architecture/codex-system-architecture|Codex 系统架构]] · [[codex-config-decisions|配置决策]]

## 当前规则

```python
prefix_rule(pattern=["git", "switch"], decision="allow")
```

仅有一条规则：允许执行 `git switch` 命令。

这是一个前缀匹配规则 — 任何以 `git switch` 开头的命令都被允许。
