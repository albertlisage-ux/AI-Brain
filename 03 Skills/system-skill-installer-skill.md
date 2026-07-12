# System: Skill Installer Skill

**来源**: `~/.codex/skills/.system/skill-installer/`  
**用途**: 从 curated 列表或 GitHub 仓库安装 Codex Skills

## 技能来源

| 来源 | 路径 |
|------|------|
| 官方 curated skills | `https://github.com/openai/skills/tree/main/skills/.curated` |
| 实验性 skills | `https://github.com/openai/skills/tree/main/skills/.experimental` |
| 其他 GitHub 仓库 | 用户提供 repo/path |

## 安装脚本

```bash
# 列出可用 skills
python3 scripts/list-skills.py
python3 scripts/list-skills.py --format json
python3 scripts/list-skills.py --path skills/.experimental

# 从 GitHub 安装
python3 scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path <path/to/skill>

# 使用 URL
python3 scripts/install-skill-from-github.py \
  --url https://github.com/<owner>/<repo>/tree/<ref>/<path>
```

## 行为说明

- 默认直接下载（公有仓库）
- 认证失败时回退到 git sparse checkout
- 目标目录已存在则中止
- 安装到 `$CODEX_HOME/skills/<skill-name>`（默认 `~/.codex/skills/`）
- 支持私仓（需 `GITHUB_TOKEN`/`GH_TOKEN`）

## 注意事项

- `.system` 下的 skills 是预装的，无需用户安装
- 安装完成后，下次对话生效
- 网络操作，沙箱中运行时需请求权限提升

---

**相关：** [[codex|← 返回 Skills 索引]] · [[system-skill-creator-skill|Skill Creator]] · [[system-plugin-creator-skill|Plugin Creator]] · [[../05 Architecture/codex-system-architecture|系统架构]]
