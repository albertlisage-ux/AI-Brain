# AI-Brain Vault Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate duplicate knowledge responsibilities and produce topic-colored, uniquely named Obsidian graph clusters.

**Architecture:** Unique narrative MOCs provide navigation, note properties assign topic membership, and Graph groups visualize primary themes. Repository instructions and operational README files remain separate from the knowledge layer.

**Tech Stack:** Markdown, WikiLinks, YAML properties, Obsidian Bases, JSON, Git.

## Global Constraints

- Preserve independent Architecture, Decision, Lesson, Changelog, and Troubleshooting notes.
- Do not modify source code, credentials, caches, or the LinkTech submodule.
- Keep all links resolvable after every rename.
- Merge to `main` only after complete verification.

---

### Task 1: Unique entry names

**Files:** Rename the root MOC, four category MOCs, LinkTech project MOC, LinkTech workflow note, and the archived import record; update all Markdown references.

- [ ] Record the current duplicate stems and link baseline.
- [ ] Rename files to `AI-Brain.md`, category-specific MOC names, `linktech-project.md`, and `linktech-workflow.md`.
- [ ] Update all WikiLinks and aliases.
- [ ] Run link audit; expect 0 broken and 0 ambiguous links.
- [ ] Commit with `docs: give knowledge entries unique names`.

### Task 2: Content responsibility consolidation

**Files:** Rewrite `linktech-project.md`, `linktech-workflow.md`, `ai-brain-rag/README.md`, the archived import record, and Daily summary.

- [ ] Keep project identity and repository structure only in the project MOC.
- [ ] Keep operational rules and task routing only in the workflow note.
- [ ] Reduce the RAG README to developer quick start and link to the complete guide.
- [ ] Move historical import detail to Archive and make Daily a concise timeline index.
- [ ] Re-run similarity and link checks, then commit with `docs: consolidate overlapping vault content`.

### Task 3: Complete topic metadata

**Files:** Every knowledge Markdown file in Projects, Skills, Architecture, Decisions, and Lessons that is not a template or repository instruction.

- [ ] Add valid `type`, `topics`, and `status`.
- [ ] Assign Codex, LinkTech, AI RAG, Security, or Design topic membership.
- [ ] Update Bases to exclude `08 Templates/`.
- [ ] Parse YAML and Bases; expect no errors.
- [ ] Commit with `feat: classify vault knowledge by topic`.

### Task 4: Topic-first graph

**Files:** `.obsidian/graph.json`, `.obsidian/app.json`, root and category MOCs.

- [ ] Replace type-first colors with AI-Brain, Codex, LinkTech, AI RAG, Security, and Design groups.
- [ ] Exclude Daily, Archive, Templates, README, AGENTS, process docs, code, and caches.
- [ ] Validate six distinct groups and verify every visible knowledge note matches a group.
- [ ] Commit with `feat: color Obsidian graph by knowledge theme`.

### Task 5: Verify and merge

- [ ] Confirm 0 broken links, 0 ambiguous links, and no duplicate MOC stems.
- [ ] Parse all YAML, Base, and JSON files.
- [ ] Run `git diff --check` and verify only authorized files changed.
- [ ] Confirm both the feature worktree and main checkout are clean.
- [ ] Merge `codex/obsidian-knowledge-network` into `main`, rerun verification, remove the owned worktree, and delete the merged branch.
