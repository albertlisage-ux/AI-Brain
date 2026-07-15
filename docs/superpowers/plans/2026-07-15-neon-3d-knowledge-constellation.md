# 霓虹 3D 核心知识星群实施计划 / Neon 3D Core Knowledge Constellation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 使用 New 3D Graph 2.5.2 构建经过过滤、语义着色且具有霓虹 HUD 的 AI-Brain 三维核心知识星群。 / Build a filtered, semantically colored AI-Brain 3D core knowledge constellation with a neon HUD using New 3D Graph 2.5.2.

**Architecture:** 插件的 `data.json` 负责数据范围、颜色、标签、交互和物理参数；独立 CSS snippet 只负责 `.graph-3d-*` HUD 元素。原生二维 Neon Observatory 与插件源文件保持不变。 / The plugin `data.json` owns scope, colors, labels, interaction, and physics; a separate CSS snippet styles only `.graph-3d-*` HUD elements. The native 2D Neon Observatory and plugin source files remain unchanged.

**Tech Stack:** Obsidian, New 3D Graph 2.5.2, JSON, CSS.

## Global Constraints / 全局约束

- 真实 Vault 是 `/Users/yuanzhe/Knowledge`；Git 仓库是 `/Users/yuanzhe/Knowledge/AI-Brain`。 / The active Vault is `/Users/yuanzhe/Knowledge`; the Git repository is `/Users/yuanzhe/Knowledge/AI-Brain`.
- 不修改插件的 `main.js`、`manifest.json` 或 `styles.css`。 / Do not modify the plugin’s `main.js`, `manifest.json`, or `styles.css`.
- 保留原生二维 Neon Observatory。 / Preserve the native 2D Neon Observatory.
- 只显示核心知识目录，隐藏附件、标签和孤立节点。 / Show only core knowledge directories and hide attachments, tags, and orphan nodes.
- 新增的文档保持完整中英双语。 / Keep newly created documentation fully bilingual.

---

## 中文实施步骤

### 任务 1：写入 New 3D Graph 配置

**文件：**
- 新建：`/Users/yuanzhe/Knowledge/.obsidian/plugins/new-3d-graph/data.json`
- 读取但不修改：`/Users/yuanzhe/Knowledge/.obsidian/plugins/new-3d-graph/manifest.json`

**接口：**
- 输入：New 3D Graph 2.5.2 的设置结构和 AI-Brain 核心路径。
- 输出：插件启动时通过 `loadData()` 读取的完整 JSON 设置。

- [x] **步骤 1：运行预检查并确认失败**

运行：

```bash
test -f /Users/yuanzhe/Knowledge/.obsidian/plugins/new-3d-graph/data.json \
  && jq -e '.centerForce == 0.07 and .repelForce == 12 and .linkForce == 0.012' \
    /Users/yuanzhe/Knowledge/.obsidian/plugins/new-3d-graph/data.json
```

预期：失败，因为 `data.json` 尚不存在或没有目标设置。

- [x] **步骤 2：使用 `apply_patch` 新建完整配置**

写入：

```json
{
  "searchQuery": "",
  "showNeighboringNodes": false,
  "performanceMode": false,
  "filters": [
    { "type": "path", "value": "AI-Brain/AI-Brain.md", "enabled": true },
    { "type": "path", "value": "AI-Brain/02 Projects/LinkTech-hydraulic/linktech-project.md", "enabled": true },
    { "type": "path", "value": "AI-Brain/03 Skills", "enabled": true },
    { "type": "path", "value": "AI-Brain/05 Architecture", "enabled": true },
    { "type": "path", "value": "AI-Brain/06 Decisions", "enabled": true },
    { "type": "path", "value": "AI-Brain/07 Lessons", "enabled": true }
  ],
  "showAttachments": false,
  "hideOrphans": true,
  "showTags": false,
  "groups": [
    { "query": "file:AI-Brain.md", "color": "#FBBF24" },
    { "query": "file:*-moc.md", "color": "#FBBF24" },
    { "query": "topics: [linktech", "color": "#2DD4BF" },
    { "query": "topics: [ai-rag", "color": "#A78BFA" },
    { "query": "topics: [security", "color": "#FB7185" },
    { "query": "topics: [design", "color": "#F472B6" },
    { "query": "topics: [codex", "color": "#38BDF8" }
  ],
  "useThemeColors": false,
  "colorNode": "#38BDF8",
  "colorTag": "#A78BFA",
  "colorAttachment": "#64748B",
  "colorLink": "#1E3A5F",
  "colorHighlight": "#F8FAFC",
  "backgroundColor": "#020617",
  "nodeSize": 1.8,
  "tagNodeSize": 1.2,
  "attachmentNodeSize": 1.2,
  "linkThickness": 0.6,
  "nodeShape": "Sphere",
  "tagShape": "Tetrahedron",
  "attachmentShape": "Cube",
  "showNodeLabels": true,
  "showLabelsOnHoverOnly": false,
  "labelDistance": 180,
  "labelFadeThreshold": 0.7,
  "labelTextSize": 2.5,
  "labelTextColorLight": "#0F172A",
  "labelTextColorDark": "#E2E8F0",
  "labelBackgroundColor": "#020617",
  "labelBackgroundOpacity": 0.5,
  "labelOcclusion": true,
  "useKeyboardControls": true,
  "keyboardMoveSpeed": 2,
  "zoomOnClick": true,
  "rotateSpeed": 0.7,
  "panSpeed": 0.8,
  "zoomSpeed": 1,
  "centerForce": 0.07,
  "repelForce": 12,
  "linkForce": 0.012
}
```

- [x] **步骤 3：验证配置通过**

运行 `jq empty`，并断言六个过滤器、七条颜色规则、隐藏项、节点外观和三项力参数精确匹配。预期：全部通过。

### 任务 2：添加并启用霓虹 3D HUD

**文件：**
- 新建：`/Users/yuanzhe/Knowledge/.obsidian/snippets/ai-brain-neon-3d-graph.css`
- 修改：`/Users/yuanzhe/Knowledge/.obsidian/appearance.json`

**接口：**
- 输入：插件稳定的 `.graph-3d-*` UI 类。
- 输出：只作用于 3D 设置按钮、面板和计数器的 CSS snippet。

- [x] **步骤 1：运行预检查并确认失败**

运行：

```bash
test -f /Users/yuanzhe/Knowledge/.obsidian/snippets/ai-brain-neon-3d-graph.css \
  && jq -e '.enabledCssSnippets | index("ai-brain-neon-3d-graph") != null' \
    /Users/yuanzhe/Knowledge/.obsidian/appearance.json
```

预期：失败，因为 snippet 尚不存在且未启用。

- [x] **步骤 2：使用 `apply_patch` 新建 HUD CSS**

CSS 只使用 `.graph-3d-view-content`、`.graph-3d-settings-toggle`、`.graph-3d-reset-toggle`、`.graph-3d-settings-panel` 和 `.graph-3d-counter`，提供深蓝半透明背景、青色细边框、低亮度辉光、等宽标题、Hover 状态和减少动态效果回退。

- [x] **步骤 3：启用 snippet**

在 `appearance.json` 的 `enabledCssSnippets` 中保留 `ai-brain-neon-observatory`，并追加 `ai-brain-neon-3d-graph`。

- [x] **步骤 4：验证 HUD**

验证 CSS 括号配对、不含 `@import` 或网络 URL、不包含编辑器选择器，并确认两个 snippets 同时启用。

### 任务 3：完整验收与打开

**文件：**
- 验证：`/Users/yuanzhe/Knowledge/.obsidian/community-plugins.json`
- 验证：`/Users/yuanzhe/Knowledge/.obsidian/plugins/new-3d-graph/{main.js,manifest.json,styles.css}`
- 更新：`docs/superpowers/plans/2026-07-15-neon-3d-knowledge-constellation.md`

- [x] **步骤 1：验证插件状态与源码哈希**

确认 `new-3d-graph` 已启用、版本为 `2.5.2`，并验证三个插件文件哈希仍为：

```text
main.js      f537ff8b6d2cbec39ab71e0c6eee77d55f095664dd10d8cdcb1a386c0bae9fba
manifest.json f291983db746277596d5a95e20dcddc03fee5be9325db53c05440d8ce238adef
styles.css   80e25925feeac6403ef703ee60aac6b4c58bfa37a2dfd47d49f9c6f907fd03c6
```

- [x] **步骤 2：运行完整检查**

解析全部 JSON，检查配置计数、精确数值、CSS 作用域、括号、外部资源和 `git diff --check`。确认旧二维设计文件中的未提交 `ç` 改动未被覆盖或暂存。

- [x] **步骤 3：打开 Vault 并交付打开方式**

运行 `open "obsidian://open?vault=Knowledge"`。由于 macOS 不允许自动发送按键，提示用户点击左侧网络图标或运行 `New 3D Graph: Open 3d graph`。

---

## English Implementation Steps

### Task 1: Write the New 3D Graph Configuration

**Files:**
- Create: `/Users/yuanzhe/Knowledge/.obsidian/plugins/new-3d-graph/data.json`
- Read only: `/Users/yuanzhe/Knowledge/.obsidian/plugins/new-3d-graph/manifest.json`

**Interfaces:**
- Consumes: the New 3D Graph 2.5.2 settings schema and AI-Brain core paths.
- Produces: complete JSON settings loaded by the plugin through `loadData()`.

- [x] **Step 1: Run the pre-check and confirm failure**

Require `data.json` to exist and contain forces `0.07`, `12`, and `0.012`. Expected: failure because the file or target configuration is absent.

- [x] **Step 2: Create the complete configuration with `apply_patch`**

Write the exact JSON shown in the Chinese Task 1. It contains six path filters, seven ordered color rules representing six semantic themes, custom neon colors, spherical nodes sized `1.8`, link thickness `0.6`, labels at distance `180` with fade threshold `0.7` and text size `2.5`, WASD controls, click-to-zoom, and the approved forces `0.07`, `12`, and `0.012`.

- [x] **Step 3: Verify the configuration passes**

Run `jq empty` and assert exact filter counts, group counts, hidden content, node appearance, and physics values. Expected: all checks pass.

### Task 2: Add and Enable the Neon 3D HUD

**Files:**
- Create: `/Users/yuanzhe/Knowledge/.obsidian/snippets/ai-brain-neon-3d-graph.css`
- Modify: `/Users/yuanzhe/Knowledge/.obsidian/appearance.json`

**Interfaces:**
- Consumes: stable `.graph-3d-*` plugin UI classes.
- Produces: a CSS snippet scoped to 3D settings controls, panel, and counter.

- [x] **Step 1: Run the pre-check and confirm failure**

Require the snippet to exist and be enabled. Expected: failure because neither condition is currently true.

- [x] **Step 2: Create the HUD CSS with `apply_patch`**

Use only `.graph-3d-view-content`, `.graph-3d-settings-toggle`, `.graph-3d-reset-toggle`, `.graph-3d-settings-panel`, and `.graph-3d-counter`. Add a translucent deep-blue surface, thin cyan border, low-intensity glow, monospaced headings, hover states, and a reduced-motion fallback.

- [x] **Step 3: Enable the snippet**

Preserve `ai-brain-neon-observatory` in `appearance.json` and append `ai-brain-neon-3d-graph`.

- [x] **Step 4: Verify the HUD**

Check balanced CSS braces, absence of imports or network URLs, absence of editor selectors, and simultaneous enablement of both snippets.

### Task 3: Full Acceptance and Open

**Files:**
- Verify: `/Users/yuanzhe/Knowledge/.obsidian/community-plugins.json`
- Verify: `/Users/yuanzhe/Knowledge/.obsidian/plugins/new-3d-graph/{main.js,manifest.json,styles.css}`
- Update: `docs/superpowers/plans/2026-07-15-neon-3d-knowledge-constellation.md`

- [x] **Step 1: Verify plugin state and source hashes**

Confirm that `new-3d-graph` is enabled, the version is `2.5.2`, and all three plugin-file hashes match the values recorded in the Chinese Task 3.

- [x] **Step 2: Run the full check**

Parse every JSON file; check counts, exact settings, CSS scope, braces, external resources, and `git diff --check`. Confirm that the uncommitted `ç` changes in the older 2D design are neither overwritten nor staged.

- [x] **Step 3: Open the Vault and hand off the graph command**

Run `open "obsidian://open?vault=Knowledge"`. Because macOS blocks automated keystrokes, tell the user to click the left-ribbon network icon or run `New 3D Graph: Open 3d graph`.
