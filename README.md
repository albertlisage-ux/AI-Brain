# AI-Brain 🧠

> 个人知识管理系统 · PARA 结构 · Git Submodule 多项目管理

## 快速开始

```bash
git clone --recursive git@github.com:albertlisage-ux/AI-Brain.git
```

如果已 clone 但未拉子模块：

```bash
git submodule update --init --recursive
```

## 目录结构

```
AI-Brain/
├── 00 Inbox/        ← 临时想法、待处理资料
├── 01 Daily/        ← 每日记录
├── 02 Projects/     ← 项目笔记 + Git Submodule
│   └── LinkTech-hydraulic/
│       ├── linktech-project.md ← 项目入口（本仓库管理）
│       └── code/         ← Git Submodule（实际代码仓库）
├── 03 Skills/       ← 可复用技能/工作流知识
├── 04 Prompts/      ← 提示词库
├── 05 Architecture/ ← 系统架构设计
├── 06 Decisions/    ← 技术决策记录
├── 07 Lessons/      ← 经验教训
├── 08 Templates/    ← 模板
├── 99 Archive/      ← 归档
├── Attachments/     ← 附件文件
├── AI-Brain.md      ← Obsidian 知识总入口
└── README.md        ← 本文件
```

## 核心设计

### PARA 分类

| 类别 | 说明 |
|------|------|
| **Projects** | 有明确目标、截止日期的项目笔记 |
| **Areas** | 长期负责的领域（通过 Skills/Architecture 体现） |
| **Resources** | 兴趣/参考主题（Inbox/Attachments） |
| **Archives** | 已完成/冷存储（99 Archive） |

### Git Submodule 策略

```
AI-Brain（父仓库）
  ├── 02 Projects/Project-A/
  │   ├── linktech-project.md ← 项目笔记（Markdown，在 AI-Brain 中管理）
  │   └── code/            ← Git Submodule → 实际代码仓库
  └── 02 Projects/Project-B/
      └── ...
```

- **笔记**在 AI-Brain 仓库中版本管理
- **代码**通过 `git submodule` 关联到独立仓库的特定 commit
- 克隆时加 `--recursive` 即可拉取所有子模块

## Obsidian 使用

本仓库设计为 Obsidian Vault，支持：

- `[[WikiLinks]]` — 笔记间双向链接
- `Cmd+O` — 快速跳转
- `Cmd+Shift+G` — 图谱视图查看知识网络
- Properties 与 Bases — 按主题、类型和状态筛选知识
- Backlinks、Outgoing Links 与局部图谱 — 沿真实关系探索笔记
- 从 AI-Brain.md 进入总 MOC，再进入分类 MOC 或项目主页

## 许可

私有知识库
