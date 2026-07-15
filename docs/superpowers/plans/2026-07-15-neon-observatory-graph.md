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

- [ ] Create the snippets directory.
- [ ] Add graph-only dark surface, grid, scanlines, labels, node defaults, connection colors, and focus states.
- [ ] Validate CSS brace balance and absence of external imports.

### Task 2: Enable and tune

- [ ] Enable `ai-brain-neon-observatory` in `appearance.json` without removing other enabled snippets.
- [ ] Keep six semantic groups and tune node size, line size, repulsion, and link distance.
- [ ] Parse both JSON files and confirm the snippet exists.

### Task 3: Verify

- [ ] Confirm the active Vault root is the outer Knowledge directory.
- [ ] Confirm graph search is scoped to `AI-Brain`.
- [ ] Confirm six unique packed RGB colors.
- [ ] Commit the repository design record; leave the user-local outer Vault settings untracked.
