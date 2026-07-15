---
type: skill
topics: [codex, automation]
status: reference
---

# Playwright CLI Skill

**来源**: `~/.codex/skills/playwright/`  
**用途**: 从终端驱动真实浏览器（导航、填表、截图、数据提取、UI 调试）

## 核心原则

- CLI 优先自动化，**不**使用 `@playwright/test`（除非用户明确要求测试文件）
- 优先使用 `scripts/playwright_cli.sh` 包装脚本

## 必备检查

```bash
command -v npx >/dev/null 2>&1
```

若无 npx，需用户安装 Node.js/npm 并全局安装：
```bash
npm install -g @playwright/cli@latest
```

## 核心工作流

```
1. open → 2. snapshot → 3. click/type/fill → 4. re-snapshot → 5. screenshot
```

## 关键命令

| 命令 | 用途 |
|------|------|
| `"$PWCLI" open <url> --headed` | 打开页面 |
| `"$PWCLI" snapshot` | 获取 DOM 快照（稳定元素引用） |
| `"$PWCLI" click <ref>` | 点击元素 |
| `"$PWCLI" type <text>` | 输入文本 |
| `"$PWCLI" fill <ref> <value>` | 填写表单 |
| `"$PWCLI" screenshot` | 截屏 |
| `"$PWCLI" press <key>` | 按键 |

## 何时重新 snapshot

- 导航后
- 点击导致 UI 大幅变化后
- 打开/关闭弹窗或菜单后
- 标签页切换后
- 元素引用失效时

## 路径设置

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"
```

---

**相关：** [[03 Skills/skills-moc|← 返回 Skills 索引]] · [[screenshot-skill|Screenshot]] · [[../05 Architecture/codex-system-architecture|系统架构]]
