---
type: design
topics: [obsidian, knowledge-graph, design]
status: approved
aliases: [霓虹 3D 核心知识星群设计, Neon 3D Core Knowledge Constellation Design]
---

# 霓虹 3D 核心知识星群设计 / Neon 3D Core Knowledge Constellation Design

## 中文

### 目标

使用已安装并启用的 New 3D Graph `2.5.2`，将 AI-Brain 的核心知识笔记呈现为可旋转、缩放和聚焦的霓虹三维星群。原生二维 Neon Observatory 保留为快速、稳定的备用图谱。

### 数据范围

3D 图谱只选择以下路径，过滤器之间使用“或”关系：

- `AI-Brain/AI-Brain.md`
- `AI-Brain/02 Projects/LinkTech-hydraulic/linktech-project.md`
- `AI-Brain/03 Skills`
- `AI-Brain/05 Architecture`
- `AI-Brain/06 Decisions`
- `AI-Brain/07 Lessons`

关闭邻居扩展，避免外层 Vault 或被排除目录重新进入图谱。隐藏附件、标签节点和孤立节点；不显示 Daily、Templates、Archive、Prompt、README、代码和 `docs/superpowers`。

### 语义颜色

插件不读取原生图谱的属性查询，因此使用它支持的文件名和正文匹配规则重建颜色组。规则按优先级排列：

1. `file:AI-Brain.md` 与 `file:*-moc.md`：金色 `#FBBF24`
2. `topics: [linktech`：青绿 `#2DD4BF`
3. `topics: [ai-rag`：紫色 `#A78BFA`
4. `topics: [security`：红色 `#FB7185`
5. `topics: [design`：粉色 `#F472B6`
6. `topics: [codex`：电光蓝 `#38BDF8`

未匹配节点使用青色 `#38BDF8`，连线使用低亮度蓝 `#1E3A5F`，焦点使用近白色 `#F8FAFC`，背景使用深海军蓝 `#020617`。

### 节点、标签与交互

- 使用球形节点，节点大小 `1.8`，连线粗细 `0.6`。
- 显示节点标签，距离 `180`，淡出阈值 `0.7`，文字大小 `2.5`。
- 标签背景使用 `#020617`、透明度 `0.5`，开启遮挡检测。
- 开启单击缩放和 WASD 相机控制；旋转速度 `0.7`、平移速度 `0.8`、缩放速度 `1.0`。
- 保持性能模式关闭，因为核心星群规模较小且需要标签与曲线。

### 物理布局

- 中心力 `0.07`：保持整体可见，同时避免主题全部挤在中心。
- 排斥力 `12`：形成可分辨的主题星群。
- 连接力 `0.012`：维持知识关系但保留三维空间。

插件设置实时生效；首次打开后若布局尚未稳定，使用插件的 Reset 按钮重新加热模拟，不修改笔记内容。

### HUD 样式

新增独立 CSS snippet `ai-brain-neon-3d-graph.css`，只作用于 `.graph-3d-*` 类：

- 设置按钮、Reset 按钮、设置面板和节点计数器使用半透明深蓝 HUD。
- 使用青色细边框、低亮度外发光和等宽标题。
- 不覆盖 WebGL 节点颜色，不使用高频动画，不接收图谱画布事件。
- 保留 `prefers-reduced-motion` 兼容性。

### 实现位置

- 插件配置：`/Users/yuanzhe/Knowledge/.obsidian/plugins/new-3d-graph/data.json`
- HUD snippet：`/Users/yuanzhe/Knowledge/.obsidian/snippets/ai-brain-neon-3d-graph.css`
- snippet 启用：`/Users/yuanzhe/Knowledge/.obsidian/appearance.json`
- 插件启用状态：`/Users/yuanzhe/Knowledge/.obsidian/community-plugins.json`

不修改插件的 `main.js`、`manifest.json` 或 `styles.css`，以免升级时丢失改动。

### 打开方式

使用左侧栏网络图标，或在命令面板执行 `New 3D Graph: Open 3d graph`。macOS 当前未授权 `osascript` 发送按键，因此自动化只能打开 Vault，不能代替用户触发命令。

### 验收标准

- New 3D Graph `2.5.2` 保持启用，插件代码未修改。
- `data.json` 包含六个语义主题、六个核心路径过滤器和精确物理参数。
- Daily、Templates、Archive、附件、标签节点和孤立节点不进入 3D 图谱。
- HUD snippet 已启用，选择器只作用于 `.graph-3d-*`。
- 所有 JSON 可解析，CSS 括号配对，无外部资源，`git diff --check` 通过。
- 二维 Neon Observatory 配置保持可用。

---

## English

### Goal

Use the installed and enabled New 3D Graph `2.5.2` to present AI-Brain’s core knowledge notes as a neon three-dimensional constellation that can be rotated, zoomed, and focused. Preserve the native two-dimensional Neon Observatory as a fast and stable fallback graph.

### Data Scope

The 3D graph selects only the following paths, with filters combined using OR semantics:

- `AI-Brain/AI-Brain.md`
- `AI-Brain/02 Projects/LinkTech-hydraulic/linktech-project.md`
- `AI-Brain/03 Skills`
- `AI-Brain/05 Architecture`
- `AI-Brain/06 Decisions`
- `AI-Brain/07 Lessons`

Disable neighboring-node expansion so the outer Vault and excluded directories cannot re-enter the graph. Hide attachments, tag nodes, and orphan nodes. Exclude Daily, Templates, Archive, prompts, README files, code, and `docs/superpowers`.

### Semantic Colors

The plugin does not read native graph property queries, so rebuild the color groups using its supported filename and content-matching rules. Apply the rules in priority order:

1. `file:AI-Brain.md` and `file:*-moc.md`: gold `#FBBF24`
2. `topics: [linktech`: teal `#2DD4BF`
3. `topics: [ai-rag`: violet `#A78BFA`
4. `topics: [security`: red `#FB7185`
5. `topics: [design`: pink `#F472B6`
6. `topics: [codex`: electric blue `#38BDF8`

Use cyan `#38BDF8` for unmatched nodes, low-luminance blue `#1E3A5F` for links, near-white `#F8FAFC` for focus, and deep navy `#020617` for the background.

### Nodes, Labels, and Interaction

- Use spherical nodes with node size `1.8` and link thickness `0.6`.
- Show node labels with distance `180`, fade threshold `0.7`, and text size `2.5`.
- Use `#020617` label backgrounds at `0.5` opacity and enable occlusion detection.
- Enable click-to-zoom and WASD camera controls with rotation speed `0.7`, pan speed `0.8`, and zoom speed `1.0`.
- Keep performance mode disabled because the core constellation is small and requires labels and curved links.

### Physics Layout

- Center force `0.07`: keep the whole graph visible without collapsing every topic into the center.
- Repel force `12`: produce distinguishable topic constellations.
- Link force `0.012`: preserve knowledge relationships while retaining three-dimensional space.

Plugin settings apply live. If the layout has not stabilized after the first open, use the plugin’s Reset button to reheat the simulation without changing note content.

### HUD Styling

Add a separate CSS snippet named `ai-brain-neon-3d-graph.css`, scoped only to `.graph-3d-*` classes:

- Give the Settings button, Reset button, settings panel, and node counter a translucent deep-blue HUD treatment.
- Use thin cyan borders, low-intensity outer glow, and monospaced headings.
- Do not override WebGL node colors, add high-frequency animation, or intercept graph-canvas events.
- Preserve `prefers-reduced-motion` compatibility.

### Implementation Locations

- Plugin configuration: `/Users/yuanzhe/Knowledge/.obsidian/plugins/new-3d-graph/data.json`
- HUD snippet: `/Users/yuanzhe/Knowledge/.obsidian/snippets/ai-brain-neon-3d-graph.css`
- Snippet enablement: `/Users/yuanzhe/Knowledge/.obsidian/appearance.json`
- Plugin enablement: `/Users/yuanzhe/Knowledge/.obsidian/community-plugins.json`

Do not modify the plugin’s `main.js`, `manifest.json`, or `styles.css`, so plugin upgrades cannot overwrite custom changes.

### How to Open

Use the network icon in the left ribbon or run `New 3D Graph: Open 3d graph` from the Command Palette. macOS currently does not authorize `osascript` to send keystrokes, so automation can open the Vault but cannot trigger the command for the user.

### Acceptance Criteria

- New 3D Graph `2.5.2` remains enabled and plugin code is unchanged.
- `data.json` contains six semantic themes, six core path filters, and the exact physics values.
- Daily, Templates, Archive, attachments, tag nodes, and orphan nodes do not enter the 3D graph.
- The HUD snippet is enabled and selectors are scoped only to `.graph-3d-*`.
- All JSON parses, CSS braces are balanced, no external resources are used, and `git diff --check` passes.
- The two-dimensional Neon Observatory configuration remains available.
