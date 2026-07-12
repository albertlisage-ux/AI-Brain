# System: Plugin Creator Skill

**来源**: `~/.codex/skills/.system/plugin-creator/`  
**用途**: 创建和脚手架 Codex 插件

## 快速开始

```bash
# 创建基本插件（默认 ~/plugins/<plugin-name>/）
python3 scripts/create_basic_plugin.py <plugin-name>

# 创建并生成 marketplace 条目
python3 scripts/create_basic_plugin.py my-plugin --with-marketplace

# 指定路径和更多选项
python3 scripts/create_basic_plugin.py my-plugin \
  --path <parent-dir> \
  --with-skills --with-hooks --with-scripts --with-assets --with-mcp --with-apps \
  --with-marketplace
```

## 插件名称规范

- 自动转换为小写连字符格式
- `My Plugin` → `my-plugin`
- 最大 64 字符

## 插件结构

```
<plugin-name>/
├── .codex-plugin/
│   └── plugin.json     # 必需
├── skills/             # 可选
├── hooks/              # 可选
├── scripts/            # 可选
├── assets/             # 可选
└── mcp/               # 可选
```

## 验证与更新

```bash
# 验证插件
python3 scripts/validate_plugin.py <plugin-path>

# 开发时更新 cachebuster
python3 scripts/update_plugin_cachebuster.py <plugin-path>
```

## Marketplace

- 个人 marketplace: `~/.agents/plugins/marketplace.json`
- 默认创建到个人 marketplace
- 可通过 `--marketplace-name` 指定其他名称

---

**相关：** [[_index|← 返回 Skills 索引]] · [[system-skill-creator-skill|Skill Creator]] · [[system-skill-installer-skill|Skill Installer]] · [[system-openai-docs-skill|OpenAI Docs]]
