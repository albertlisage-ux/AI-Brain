---
type: plan
topics: [obsidian, knowledge-graph, design]
status: completed
aliases: [3D 银河图谱可读性优化实施计划, 3D Galaxy Legibility Optimization Plan]
---

# 3D 银河图谱可读性优化实施计划 / 3D Galaxy Legibility Optimization Plan

## 中文

### 目标

在不修改 New 3D Graph `2.5.2` 插件源码、不改动笔记内容的前提下，把现有 3D 图谱优化为更易识别、可动态聚焦的银河图谱。保留六个语义星系和核心路径过滤器。

### 任务 1：建立失败基线

- [x] 验证当前 `data.json` 尚未使用目标节点、标签、连线与物理参数。
- [x] 验证当前 HUD 尚未包含银河背景、画布拖动光标与键盘焦点样式。

### 任务 2：优化图谱参数

文件：`/Users/yuanzhe/Knowledge/.obsidian/plugins/new-3d-graph/data.json`

- [x] 将背景设为 `#050816`，节点大小设为 `2.8`，连线粗细设为 `0.45`。
- [x] 将标签距离、淡出阈值、字号设为 `420 / 0.75 / 4.0`。
- [x] 将标签背景设为 `#071426`、透明度设为 `0.72`，保留遮挡检测。
- [x] 将中心力、排斥力、连接力设为 `0.05 / 14 / 0.012`。
- [x] 保留六个路径过滤器、语义颜色、球形节点、点击聚焦和 WASD 控制。

### 任务 3：优化银河 HUD

文件：`/Users/yuanzhe/Knowledge/.obsidian/snippets/ai-brain-neon-3d-graph.css`

- [x] 更新主画布背景与 `16px` 控制面板圆角。
- [x] 添加 `grab` / `grabbing` 光标和清晰的 `:focus-visible` 焦点环。
- [x] 保留选择器作用域、克制辉光、短过渡和 `prefers-reduced-motion`。

### 任务 4：验证

- [x] 验证目标参数精确匹配，六个过滤器与颜色规则未丢失。
- [x] 验证所有 JSON 可解析、CSS 括号平衡且无外部资源。
- [x] 验证插件 `main.js`、`manifest.json`、`styles.css` 哈希未改变。
- [x] 运行 `git diff --check`，复核只包含预期仓库文档改动。

## English

### Goal

Optimize the current 3D graph into a more legible galaxy map with dynamic focus, without modifying New 3D Graph `2.5.2` source or note content. Preserve the six semantic galaxies and core path filters.

### Task 1: Establish a Failing Baseline

- [x] Confirm that the current `data.json` does not yet use the target node, label, link, and physics values.
- [x] Confirm that the current HUD does not yet include the galaxy background, canvas drag cursors, and keyboard focus treatment.

### Task 2: Optimize Graph Parameters

File: `/Users/yuanzhe/Knowledge/.obsidian/plugins/new-3d-graph/data.json`

- [x] Set the background to `#050816`, node size to `2.8`, and link thickness to `0.45`.
- [x] Set label distance, fade threshold, and text size to `420 / 0.75 / 4.0`.
- [x] Set the label background to `#071426` at `0.72` opacity and preserve occlusion detection.
- [x] Set center, repel, and link forces to `0.05 / 14 / 0.012`.
- [x] Preserve six path filters, semantic colors, spherical nodes, click focus, and WASD controls.

### Task 3: Refine the Galaxy HUD

File: `/Users/yuanzhe/Knowledge/.obsidian/snippets/ai-brain-neon-3d-graph.css`

- [x] Update the main-canvas background and use `16px` control-panel radii.
- [x] Add `grab` / `grabbing` cursors and a clear `:focus-visible` focus ring.
- [x] Preserve selector scope, restrained glow, short transitions, and `prefers-reduced-motion`.

### Task 4: Verify

- [x] Verify exact target values and ensure that six filters and color rules remain intact.
- [x] Verify that all JSON parses, CSS braces balance, and no external resources are used.
- [x] Verify that plugin `main.js`, `manifest.json`, and `styles.css` hashes are unchanged.
- [x] Run `git diff --check` and confirm that only intended repository documentation changed.
