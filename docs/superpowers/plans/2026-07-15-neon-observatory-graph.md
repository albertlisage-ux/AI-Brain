# Neon Observatory Graph Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply a readable sci-fi visual system to the active Obsidian Vault graph.

**Architecture:** Property-driven graph groups retain semantic colors, while a graph-scoped CSS snippet supplies the dark observatory surface, grid, scanlines, labels, and connection styling.

**Tech Stack:** Obsidian Graph JSON, CSS snippet, JSON appearance settings.

## Global Constraints

- Modify the active outer Vault at `/Users/yuanzhe/Knowledge`.
- Do not style note editors or other Obsidian panes.
- Do not load external fonts or install community plugins.
- Preserve reduced-motion behavior.

### Task 1: Graph surface

- [x] Create the snippets directory.
- [x] Add graph-only dark surface, grid, scanlines, labels, node defaults, connection colors, and focus states.
- [x] Validate CSS brace balance and absence of external imports.

### Task 2: Enable and tune

- [x] Enable `ai-brain-neon-observatory` in `appearance.json` without removing other enabled snippets.
- [x] Keep six semantic groups and tune node size, line size, repulsion, and link distance.
- [x] Parse both JSON files and confirm the snippet exists.

### Task 3: Verify

- [x] Confirm the active Vault root is the outer Knowledge directory.
- [x] Confirm graph search is scoped to `AI-Brain`.
- [x] Confirm six unique packed RGB colors.
- [x] Commit the repository design record; leave the user-local outer Vault settings untracked.

### Task 4: Native light motion

**Files:**
- Modify: `/Users/yuanzhe/Knowledge/.obsidian/snippets/ai-brain-neon-observatory.css`
- Modify: `docs/superpowers/specs/2026-07-15-neon-observatory-graph-design.md`

- [x] Run a pre-change CSS check that requires `ai-brain-aurora-drift`, `ai-brain-scanline-drift`, `ai-brain-focus-pulse`, and a reduced-motion static fallback; expect failure because the animations are absent.
- [x] Add a pointer-transparent `::before` aurora layer with a 12-second slow drift.
- [x] Animate the existing scanline layer over 18 seconds and add an 8-second low-intensity focus pulse to the active graph leaf.
- [x] Disable all three decorative animations under `prefers-reduced-motion: reduce`.
- [x] Validate selector scope, animation durations, CSS brace balance, JSON configuration, snippet enablement, and six unique graph colors.
