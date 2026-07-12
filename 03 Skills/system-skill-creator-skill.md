# System: Skill Creator Skill

**来源**: `~/.codex/skills/.system/skill-creator/`  
**用途**: 创建和更新 Codex Skill 的指南

## 核心原则

### 1. 简洁是关键
- Codex 已经很聪明，只添加它还不知道的信息
- 每段文字都要问自己："这值得它的 token 成本吗？"
- 用简洁示例替代冗长解释

### 2. 设置合适的自由度

| 自由度 | 适用场景 |
|--------|---------|
| 🟢 高（文字指令） | 多种方法可行、依赖上下文判断 |
| 🟡 中（伪代码/参数脚本） | 有推荐模式、允许变体 |
| 🔴 低（特定脚本） | 操作脆弱易错、一致性关键 |

### 3. 保护验证完整性
- 可使用 subagent 独立验证 skill
- 传递最小上下文，不泄露预期答案

## Skill 结构

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter
│   │   ├── name: (必需)
│   │   └── description: (必需)
│   └── Markdown 指令 (必需)
├── agents/
│   └── openai.yaml (推荐 — UI 元数据)
├── scripts/    (可选 — 可执行代码)
├── references/ (可选 — 参考文档)
└── assets/     (可选 — 模板/图标/字体)
```

## SKILL.md 要求

- **Frontmatter** — `name` 和 `description` 是 Codex 判断何时使用此 skill 的唯一依据
- **Body** — 仅当 skill 被触发后才加载到上下文中

## Skill 能提供的价值

1. 专业化工作流 — 特定领域的多步骤流程
2. 工具集成 — 特定文件格式或 API 的使用指南
3. 领域知识 — 公司特定知识、模式、业务逻辑
4. 捆绑资源 — 脚本、参考、资产

---

**相关：** [[_index|← 返回 Skills 索引]] · [[system-skill-installer-skill|Skill Installer]] · [[system-plugin-creator-skill|Plugin Creator]] · [[../08 Templates/skill-analysis-template|Skill 导入模板]]
