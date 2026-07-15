# Security Ownership Map Skill

**来源**: `~/.codex/skills/security-ownership-map/`  
**用途**: 分析 Git 仓库构建安全所有权拓扑（人→文件映射），计算 bus factor 和敏感代码所有权

## 前置依赖

```bash
pip install networkx
```

## 快速开始

```bash
python scripts/run_ownership_map.py \
  --repo . \
  --out ownership-map-out \
  --since "12 months ago" \
  --emit-commits
```

## 核心参数

| 参数 | 说明 |
|------|------|
| `--since/--until` | 时间窗口 |
| `--sensitive-config` | 敏感规则配置 CSV |
| `--cochange-max-files` | 忽略超大 commit 的噪音 |
| `--cochange-exclude` | 排除文件模式（如 `**/Cargo.lock`） |
| `--no-communities` | 禁用社区检测 |
| `--graphml` | 输出 GraphML 格式 |
| `--include-merges` | 包含合并提交 |

## 默认排除

- 锁定文件（lockfiles）
- `.github/*` 配置
- 编辑器配置
- Dependabot 提交

## 敏感规则默认配置

| 模式 | 标签 | 权重 |
|------|------|------|
| `**/auth/**` | auth | 1.0 |
| `**/crypto/**` | crypto | 1.0 |
| `**/*.pem` | secrets | 1.0 |

## 输出产物

| 文件 | 内容 |
|------|------|
| `people.csv` | 人员节点 |
| `files.csv` | 文件节点 |
| `edges.csv` | 人→文件边 |
| `cochange_edges.csv` | 文件间共变边（Jaccard 权重） |
| `summary.json` | 安全所有权发现 |
| `commits.jsonl` | 提交明细（可选） |
| `communities.json` | 社区检测结果（含 maintainers） |

---

**相关：** [[03 Skills/codex|← 返回 Skills 索引]] · [[security-best-practices-skill|Security Best Practices]] · [[security-threat-model-skill|Security Threat Model]] · [[../06 Decisions/security-tools-decision-log|安全工具决策]]
