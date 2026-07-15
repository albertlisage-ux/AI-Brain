---
type: design
topics: [obsidian, knowledge-graph, design]
status: approved
aliases: [霓虹力导向星图设计, Neon Force-Directed Star Map Design]
---

# 霓虹力导向星图设计 / Neon Force-Directed Star Map Design

## 中文

### 目标

在现有 Neon Observatory 动态主题上构建平衡型霓虹力导向星图。图谱应呈现开放、可辨认的主题星群，同时保持文字、语义颜色和连接方向清晰，不依赖社区插件。

### 当前基础

真实 Obsidian Vault 位于 `/Users/yuanzhe/Knowledge`，AI-Brain 是其中的 Git 仓库。外层 Vault 已启用图谱专用 CSS，包含深海军蓝背景、星云漂移、扫描线、激活面板呼吸光和六组语义颜色。当前图谱约覆盖 58 个 Markdown 文件中的可见知识笔记。

### 力导向布局

- 将 `repelStrength` 从 `14` 调整为 `18`，使主题簇之间形成更清楚的空间边界。
- 将 `linkDistance` 从 `205` 调整为 `230`，减少标签和连线重叠。
- 将 `centerStrength` 从 `0.42` 调整为 `0.32`，避免所有主题过度挤向中心。
- 将 `linkStrength` 从 `1` 调整为 `0.9`，让节点保持关联但允许主题簇自然展开。
- 将 `nodeSizeMultiplier` 从 `1.3` 调整为 `1.4`，让核心节点更像星体。
- 将 `lineSizeMultiplier` 从 `0.9` 调整为 `0.78`，降低交叉连线的视觉噪声。
- 保留方向箭头、隐藏孤立节点和现有排除规则。

### 视觉层

1. 在图谱背景加入低密度静态星点，使用纯 CSS 径向渐变，不加载图片或网络资源。
2. 保留 12 秒星云漂移、18 秒扫描线和 8 秒激活面板呼吸光；不增加高频闪烁。
3. 将画布饱和度和对比度轻微提高，并加入低半径青色 `drop-shadow`，让节点和高亮连线呈现霓虹星体效果。
4. 保留 MOC 金色、LinkTech 青绿、AI RAG 紫色、Security 红色、Design 粉色和 Codex 电光蓝，不用 CSS 覆盖属性颜色组。
5. 控制面板继续使用半透明 HUD 样式，且不遮挡图谱交互。

### 性能与无障碍

- 仅修改全局图谱和局部图谱，不影响编辑器、Canvas 或其他面板。
- 星点保持静态，动态只使用已有低频动画，避免额外持续重绘。
- 在 `prefers-reduced-motion: reduce` 下关闭星云、扫描线和呼吸光动画；静态星点与语义颜色保留。
- 不安装 3D Graph、Juggl 或其他社区插件。

### 实现位置

- 力参数：`/Users/yuanzhe/Knowledge/.obsidian/graph.json`
- 图谱视觉：`/Users/yuanzhe/Knowledge/.obsidian/snippets/ai-brain-neon-observatory.css`
- Git 记录：AI-Brain 中的设计说明和实施计划；外层 Vault 配置保持为本机未跟踪设置。

### 验收标准

- 六组语义颜色和现有图谱过滤规则保持不变。
- 力参数精确匹配设计值：`18`、`230`、`0.32`、`0.9`、`1.4`、`0.78`。
- CSS 包含低密度星点层和轻量画布辉光，且只作用于 `graph` 与 `localgraph`。
- CSS 无外部资源，括号配对，减少动态效果回退仍有效。
- `appearance.json` 与 `graph.json` 可解析，`git diff --check` 通过。

---

## English

### Goal

Build a balanced neon force-directed star map on top of the existing Neon Observatory dynamic theme. The graph should form open, recognizable topic constellations while keeping labels, semantic colors, and link direction clear, without relying on community plugins.

### Current Foundation

The active Obsidian Vault is `/Users/yuanzhe/Knowledge`, with AI-Brain nested inside it as the Git repository. The outer Vault already enables graph-scoped CSS with a deep navy background, drifting nebulae, scanlines, an active-panel focus pulse, and six semantic color groups. The graph currently selects visible knowledge notes from an inventory of approximately 58 Markdown files.

### Force-Directed Layout

- Change `repelStrength` from `14` to `18` so topic clusters gain clearer spatial boundaries.
- Change `linkDistance` from `205` to `230` to reduce label and edge overlap.
- Change `centerStrength` from `0.42` to `0.32` so topics do not collapse into the center.
- Change `linkStrength` from `1` to `0.9` so connected nodes remain related while clusters can expand naturally.
- Change `nodeSizeMultiplier` from `1.3` to `1.4` so important nodes read more like stars.
- Change `lineSizeMultiplier` from `0.9` to `0.78` to reduce visual noise from crossing edges.
- Preserve directional arrows, hidden orphan nodes, and the existing exclusion rules.

### Visual Layers

1. Add a low-density static star field to the graph background using CSS radial gradients only, with no images or network resources.
2. Preserve the 12-second nebula drift, 18-second scanline motion, and 8-second active-panel pulse; add no high-frequency flashing.
3. Slightly increase canvas saturation and contrast and apply a small-radius cyan `drop-shadow` so nodes and highlighted edges read as neon stars.
4. Preserve gold for MOCs, teal for LinkTech, violet for AI RAG, red for Security, pink for Design, and electric blue for Codex. CSS must not override property-driven color groups.
5. Keep the translucent HUD-style control panel without blocking graph interaction.

### Performance and Accessibility

- Modify only global and local graph views, not editors, Canvas, or other panes.
- Keep the star field static. Use only the existing low-frequency animations to avoid additional continuous repainting.
- Under `prefers-reduced-motion: reduce`, disable nebula, scanline, and focus-pulse animation while retaining the static star field and semantic colors.
- Do not install 3D Graph, Juggl, or any other community plugin.

### Implementation Locations

- Force settings: `/Users/yuanzhe/Knowledge/.obsidian/graph.json`
- Graph visuals: `/Users/yuanzhe/Knowledge/.obsidian/snippets/ai-brain-neon-observatory.css`
- Git record: the design specification and implementation plan in AI-Brain; outer Vault configuration remains local and untracked.

### Acceptance Criteria

- The six semantic colors and existing graph filters remain unchanged.
- Force values exactly match the design: `18`, `230`, `0.32`, `0.9`, `1.4`, and `0.78`.
- CSS includes a low-density star field and lightweight canvas glow scoped only to `graph` and `localgraph`.
- CSS uses no external resources, has balanced braces, and preserves the reduced-motion fallback.
- `appearance.json` and `graph.json` parse successfully, and `git diff --check` passes.
