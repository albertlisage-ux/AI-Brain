# AI-Brain Vault 全库整合设计

## 目标

消除图谱中的同名入口、减少职责重叠、让 Codex、LinkTech、AI RAG 三个主题簇以不同颜色呈现，同时保留具有独立用途的技术事实源。

## 命名与入口

- 根入口由 `codex.md` 重命名为 `AI-Brain.md`。
- 四个分类入口改为唯一名称：`skills-moc.md`、`architecture-moc.md`、`decisions-moc.md`、`lessons-moc.md`。
- LinkTech 项目主页改为 `linktech-project.md`；项目 Skill 改为 `linktech-workflow.md`，从文件名和内容上区分“项目导航”与“执行规则”。
- 使用 `aliases` 保留常用称呼，所有 WikiLink 更新为唯一的 Vault 路径。

## 内容整合

- LinkTech 项目主页保留项目身份、仓库关系和跨类型导航；工作流笔记只保留执行规则、命令和按任务查阅路径。
- `ai-brain-rag/README.md` 收敛为代码目录快速启动说明；完整配置、API、MCP 和排障知识以 `ai-rag-setup-guide.md` 为事实源。
- Codex 导入记录移到 `99 Archive/`；Daily 仅保留时间线摘要并链接归档记录。
- Architecture、Decision、Lesson、Changelog、Troubleshooting 保持独立，因为它们服务不同阅读任务。
- 不合并仓库 `README.md`、项目 `AGENTS.md` 或流程文档；它们从知识图谱排除。

## 属性与图谱

- 为全部知识笔记补齐 `type`、`topics`、`status`；模板、README、AGENTS 和流程文档除外。
- 图谱颜色组按以下顺序匹配：
  1. AI-Brain 总入口：金色
  2. Codex：蓝色
  3. LinkTech：绿色
  4. AI RAG：紫色
  5. Security：红色
  6. Design：粉色
- Daily、Archive、Templates、README、AGENTS、代码、缓存和流程文档默认隐藏。
- Bases 继续按 `type` 提供动态清单，并显式排除 `08 Templates/`。

## 验收

- 不再存在同名 `codex.md` 或含义重叠的 LinkTech 项目/工作流内容。
- 全库 WikiLink 断链与歧义均为 0。
- 每篇进入全局图谱的知识笔记都匹配至少一个主题颜色组。
- JSON、YAML、Base 文件全部可解析，`git diff --check` 通过。
- 只修改 Markdown、Base、Obsidian 配置和设计/计划文档，不触碰代码、缓存或凭证。
