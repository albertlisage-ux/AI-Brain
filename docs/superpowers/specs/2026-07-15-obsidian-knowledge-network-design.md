# Obsidian 知识网络优化设计

## 目标

在保留现有 PARA 目录结构的前提下，把 AI-Brain 从“按目录存放、局部互链”的笔记集合，优化为以入口页（MOC）导航、以语义链接表达真实关系、以少量属性支持筛选的知识网络。

优化后的图谱应形成 Projects、Skills、Architecture、Decisions、Lessons 五个清晰主题簇，并通过项目、能力、设计、决策和复盘之间的真实知识路径建立跨簇连接。图谱密度不是目标；每条新增链接都必须对阅读或追溯有帮助。

## 已确认的设计选择

采用“入口页（MOC）+ 语义交叉链接”为主、轻量属性为辅的方案。

- 不采用标签主导：标签适合筛选，但不能解释两篇笔记为何相关。
- 不采用高密度自动互链：共同关键词不足以证明存在值得阅读的关系。
- 不改变 PARA 目录，不批量重命名文件，不引入新的 Obsidian 插件依赖。
- 根目录 `README.md` 是仓库欢迎页，不纳入 Obsidian 知识网络，不向其添加知识图谱链接。

## 当前状态与问题

仓库已经具备分类入口页：`03 Skills/codex.md`、`05 Architecture/codex.md`、`06 Decisions/codex.md`、`07 Lessons/codex.md`，项目入口为 `02 Projects/LinkTech-hydraulic/linktec.md`，总入口为根目录 `codex.md`。

现有基础可继续沿用，但有四类问题：

1. 根入口 `codex.md` 的知识图谱存在重复边，部分导航直接指向空目录，统计数字也容易过时。
2. 分类入口的链接多为文件索引，缺少主题分组和“从这里继续到哪里”的知识路径。
3. 一部分详情页已有“相关”链接，但多为并列罗列，语义理由不稳定；另一些核心页缺少跨类型入口。
4. 当前没有 `.obsidian` 图谱配置，无法持久化过滤条件和颜色分组。

## 信息架构

### 1. 总入口

继续使用根目录 `codex.md` 作为唯一 Vault MOC，承担三项职责：

- 按 Projects、Skills、Architecture、Decisions、Lessons 导航到分类入口或项目主页。
- 展示当前核心主题：Codex、LinkTech、AI RAG。
- 提供跨类型阅读路径，例如“AI RAG 配置指南 → 系统架构 → 配置决策 → 开发经验”。

总入口不重复维护详细文件清单；详细清单留在分类 MOC，以降低数字和条目过时的概率。空目录不使用不可解析的 WikiLink；尚无内容的分类用普通文本标示。

### 2. 分类入口

以下文件继续作为分类 MOC：

- `03 Skills/codex.md`
- `05 Architecture/codex.md`
- `06 Decisions/codex.md`
- `07 Lessons/codex.md`

各 MOC 使用一致但不过度模板化的结构：用途说明、按主题分组的笔记索引、建议阅读路径、跨分类入口。每个链接的说明回答“这篇笔记解决什么问题”或“为什么下一步读它”。

项目知识不额外创建总目录页；当前仅有一个活跃项目，`02 Projects/LinkTech-hydraulic/linktec.md` 直接承担项目 MOC。未来出现第二个项目时，再新增 `02 Projects/codex.md`，避免提前制造空入口。

### 3. 主题簇与桥接规则

核心主题簇及其桥接方式如下：

| 主题簇 | 主要入口 | 合理的跨簇关系 |
|---|---|---|
| Projects | LinkTech 项目主页 | 项目使用的 Skill、实现架构、安全决策、变更与故障经验 |
| Skills | Skills MOC | Skill 依赖的架构、产生的设计决策、使用经验 |
| Architecture | Architecture MOC | 架构服务的项目、约束它的决策、对应的排障经验 |
| Decisions | Decisions MOC | 决策作用的项目或架构、验证或推翻它的经验 |
| Lessons | Lessons MOC | 经验来源的项目、涉及的架构、后续形成的决策 |

新增链接必须使用带语义的上下文句或表格说明。允许使用紧凑的“相关”区块，但链接显示文本应表明关系，例如“安全基线来源”“对应排障记录”“实现所依赖的架构”，而不是只列标题。

不因以下理由单独建立链接：两个文件出现相同关键词、属于相同目录、都与 Codex 泛相关、仅为了让局部图谱更密集。

## 属性策略

只给核心入口和核心主题笔记添加少量、稳定、可维护的 YAML 属性：

```yaml
---
type: moc | project | skill | architecture | decision | lesson
topic:
  - codex | linktech | ai-rag | security | design
status: active | reference | archived
project: linktech | ai-brain
---
```

约束：

- `type` 必填且为单值。
- `topic` 为列表，只填写正文明确涉及的主题；不追求穷举。
- `status` 必填，用于区分活跃入口、长期参考和归档内容。
- `project` 仅在笔记明确归属于某项目时添加；不使用空值。
- 第一轮只覆盖总 MOC、四个分类 MOC、LinkTech 项目 MOC，以及为核心阅读路径提供桥接的少量笔记，不全库批量添加。

## Obsidian 图谱配置

新增 `.obsidian/graph.json`，保存全局图谱的过滤和颜色配置。

过滤查询排除：

- `path:"02 Projects/LinkTech-hydraulic/code"`
- `path:"ai-brain-rag/.venv"`
- `path:"ai-brain-rag/data/model-cache"`
- `path:"ai-brain-rag/data/qdrant"`
- `path:"ai-brain-rag/indexer/__pycache__"`
- `path:"docs/superpowers"`
- `file:README`

颜色组优先使用稳定的 `type` 属性，而不是依赖目录名称：

- Projects：`[type:project]`
- Skills：`[type:skill]`
- Architecture：`[type:architecture]`
- Decisions：`[type:decision]`
- Lessons：`[type:lesson]`
- MOC：`[type:moc]`

颜色选择以相互可辨识、深浅背景均有足够对比为准；不修改用户的主题或其他界面偏好。

## 具体改动范围

### 新建

- `.obsidian/graph.json`：全局图谱过滤及颜色组。

### 修改

- `codex.md`：精简并重构总 MOC，删除重复关系，修复空目录导航表达，加入三个核心主题的知识路径。
- `03 Skills/codex.md`：按 Codex 平台、内容处理、自动化、安全、设计、项目专用能力分组，并解释跨分类去向。
- `05 Architecture/codex.md`：按 Codex、LinkTech、AI RAG 相关架构分组，并建立决策与经验入口。
- `06 Decisions/codex.md`：按平台配置、安全、设计和项目决策分组，并标明决策作用范围。
- `07 Lessons/codex.md`：按 Codex、LinkTech、AI RAG 经验分组，并回链到来源项目或架构。
- `02 Projects/LinkTech-hydraulic/linktec.md`：增加核心属性，强化项目到 Skills、Architecture、Decisions、Lessons 的语义关系。
- `05 Architecture/codex-system-architecture.md`、`06 Decisions/codex-config-decisions.md`、`07 Lessons/codex-lessons.md`：组成 Codex 的“架构—决策—经验”路径。
- `03 Skills/linktec-skill.md`、`05 Architecture/linktech-user-system.md`、`06 Decisions/linktech-security.md`、`07 Lessons/linktech-troubleshooting.md`：组成 LinkTech 的“项目能力—实现架构—安全决策—排障经验”路径。

上述七篇桥接笔记只增加核心属性，并在现有相关区块无法解释链接语义时调整该区块；不改写技术正文。AI RAG 路径通过总 MOC 和分类 MOC 连接现有的配置指南、Codex 架构与开发日志，受保护的两篇 RAG 笔记保持不变。

### 明确不修改

- `README.md`。
- `ai-brain-rag/playground.html`。
- 用户当前正在修改的 `03 Skills/ai-rag-setup-guide.md`。
- 用户新建的 `07 Lessons/rag-playground-dev-log.md`。
- `02 Projects/LinkTech-hydraulic/code/` 子模块内容。
- RAG 虚拟环境、模型缓存、Qdrant 数据和工具生成文件。

`ai-rag-setup-guide.md` 与 `rag-playground-dev-log.md` 已经互链，因此可由分类 MOC 指向它们，但本轮不编辑这两个文件，以避免与用户未提交改动重叠。

## 实施安全策略

1. 实施前记录 `git status --short`，将现有三项工作树变化作为保护基线。
2. 所有修改使用逐文件补丁，不进行全库格式化或批量替换。
3. 每批修改后再次检查工作树差异，确认受保护文件的 diff 未被本任务改变。
4. 设计、计划和实现分别提交；提交时显式列出文件，不使用 `git add .`。
5. 若发现目标文件在实施期间出现新的外部修改，暂停该文件修改并保留其当前内容。

## 验证与验收标准

### 自动检查

- 所有新增 WikiLink 的目标文件存在；明确标注为空目录的普通文本不计入链接。
- 核心笔记 YAML 可解析，属性值符合本设计限定集合。
- `.obsidian/graph.json` 是合法 JSON，包含全部排除规则和六个颜色组。
- `git diff --check` 无空白错误。
- 受保护的三项用户改动与实施前基线一致。

### 人工验收

- 从 `codex.md` 最多两次跳转可到达任一分类 MOC 或 LinkTech 项目主页。
- Codex、LinkTech、AI RAG 各自至少形成一条跨越三种笔记类型的可解释阅读路径。
- 每条新增跨类型链接在上下文中能说明关系，而非仅显示“相关笔记”。
- 全局图谱默认看不到代码、虚拟环境、缓存、RAG 数据、流程文档和根欢迎页。
- Projects、Skills、Architecture、Decisions、Lessons、MOC 在图谱中显示为可区分颜色组。

## 回滚方式

本优化使用独立提交。未推送时可通过 `git revert <commit>` 生成安全的反向提交；不使用 `git reset --hard` 或覆盖工作树的方式回滚。由于受保护文件不会进入优化提交，回滚不会影响用户现有的 RAG 指南、Playground 或开发日志改动。

## 非目标

- 不追求为每篇笔记添加属性。
- 不安装 Dataview 或其他社区插件。
- 不自动生成反向链接区块；Obsidian 已提供反向链接能力。
- 不重构正文技术内容，不修复与知识网络无关的历史问题。
- 不把图谱视觉密度作为质量指标。
