---
type: skill
topics: [codex, automation]
status: reference
---

# Screenshot Capture Skill

**来源**: `~/.codex/skills/screenshot/`  
**用途**: 桌面/系统截图（全屏、指定窗口、区域）

## 保存位置规则

1. 用户指定路径 → 保存到该路径
2. 用户未指定 → OS 默认截图位置
3. Codex 自检用 → 保存到 temp 目录

## 工具优先级

- 优先使用工具本身的截图能力（如 Figma MCP、Playwright）
- 无法获取时回退到此 Skill

## macOS 权限预处理

```bash
bash <skill-path>/scripts/ensure_macos_permissions.sh
```

合并权限检查 + 截图：
```bash
bash <skill-path>/scripts/ensure_macos_permissions.sh && \
python3 <skill-path>/scripts/take_screenshot.py --app "<App>"
```

## 常见使用模式

| 场景 | 命令 |
|------|------|
| 默认位置截图 | `python3 <path>/take_screenshot.py` |
| Temp 截图（Codex 检查用） | `python3 <path>/take_screenshot.py --mode temp` |
| 指定路径 | `python3 <path>/take_screenshot.py --path output/screen.png` |
| 指定应用窗口 | `python3 <path>/take_screenshot.py --app "Codex"` |
| 指定窗口标题 | `python3 <path>/take_screenshot.py --app "Codex" --window-name "Settings"` |
| 像素区域 | `python3 <path>/take_screenshot.py --mode temp --region 100,200,800,600` |

---

**相关：** [[03 Skills/skills-moc|← 返回 Skills 索引]] · [[playwright-skill|Playwright]] · [[system-imagegen-skill|ImageGen]]
| 列出匹配窗口 | `python3 <path>/take_screenshot.py --list-windows --app "Codex"` |
