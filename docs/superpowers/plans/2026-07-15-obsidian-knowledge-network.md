# Obsidian Knowledge Network Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair the Vault's navigation and build a maintainable Obsidian knowledge network using semantic MOCs, lightweight properties, Bases, templates, and core-plugin configuration.

**Architecture:** Markdown MOCs remain the narrative navigation layer, while YAML properties provide structured metadata for Graph groups and Bases. Vault configuration uses only Obsidian core features and excludes code, caches, process documents, and repository-only files.

**Tech Stack:** Obsidian Markdown/WikiLinks, YAML properties, Obsidian Bases, JSON configuration, Git.

## Global Constraints

- Preserve the existing PARA directory structure.
- Do not install community plugins.
- Do not edit technical body content unrelated to navigation or metadata.
- Use Vault-root-relative WikiLink paths where duplicate names or relative-depth errors are possible.
- Keep `README.md`, `AGENTS.md`, source code, virtual environments, model caches, Qdrant data, and `docs/superpowers` outside the knowledge graph.
- Work only in the isolated `codex/obsidian-knowledge-network` branch.

---

### Task 1: Link integrity and root navigation

**Files:**
- Modify: `codex.md`
- Modify: `03 Skills/linktec-skill.md`
- Modify: `03 Skills/linktec-frontend-taste.md`
- Modify: `05 Architecture/linktech-deployment.md`
- Modify: `05 Architecture/linktech-product-system.md`
- Modify: `05 Architecture/linktech-user-system.md`
- Modify: `06 Decisions/linktech-security.md`
- Modify: `07 Lessons/linktech-changelog.md`
- Modify: `07 Lessons/linktech-troubleshooting.md`
- Modify: thirteen Skill notes containing ambiguous `[[codex]]` links

**Interfaces:**
- Consumes: Current Vault file paths.
- Produces: WikiLinks that resolve to exactly one existing Markdown file.

- [ ] **Step 1: Record the failing link baseline**

Run the repository link-audit command and retain the expected baseline: 28 unresolved links and 13 ambiguous `codex` links.

- [ ] **Step 2: Replace broken relative links**

Use Vault-root-relative destinations such as `[[07 Lessons/linktech-changelog|变更日志]]` and `[[03 Skills/codex|Skills 索引]]`.

- [ ] **Step 3: Replace empty-directory WikiLinks**

In `codex.md`, render Daily, Prompts, and Archive as plain folder labels until real MOCs exist.

- [ ] **Step 4: Verify link resolution**

Run the link audit. Expected: 0 unresolved links and 0 ambiguous links, excluding literal WikiLink examples in documentation.

- [ ] **Step 5: Commit**

```bash
git add -- codex.md "03 Skills" "05 Architecture" "06 Decisions" "07 Lessons"
git commit -m "fix: repair Obsidian knowledge links"
```

### Task 2: Semantic MOCs and reading paths

**Files:**
- Modify: `codex.md`
- Modify: `03 Skills/codex.md`
- Modify: `05 Architecture/codex.md`
- Modify: `06 Decisions/codex.md`
- Modify: `07 Lessons/codex.md`
- Modify: `02 Projects/LinkTech-hydraulic/linktec.md`

**Interfaces:**
- Consumes: Validated WikiLinks from Task 1.
- Produces: One root MOC, four category MOCs, and one project MOC with semantic navigation.

- [ ] **Step 1: Rewrite the root MOC**

Replace stale counts and duplicated Mermaid edges with topic entry points for Codex, LinkTech, and AI RAG plus three cross-type reading paths.

- [ ] **Step 2: Group each category MOC**

Group Skills by capability; Architecture by system; Decisions by scope; Lessons by source. Explain why each linked note is useful.

- [ ] **Step 3: Strengthen the project MOC**

Retain existing operational content while making Skills, Architecture, Decisions, and Lessons explicit project knowledge paths.

- [ ] **Step 4: Verify two-hop navigation**

Confirm the root MOC directly reaches all category MOCs and the LinkTech project MOC, and every category MOC links back to the root.

- [ ] **Step 5: Commit**

```bash
git add -- codex.md "03 Skills/codex.md" "05 Architecture/codex.md" "06 Decisions/codex.md" "07 Lessons/codex.md" "02 Projects/LinkTech-hydraulic/linktec.md"
git commit -m "docs: build semantic Obsidian MOCs"
```

### Task 3: Properties, templates, and Bases

**Files:**
- Modify: the six MOCs from Task 2
- Modify: `05 Architecture/codex-system-architecture.md`
- Modify: `06 Decisions/codex-config-decisions.md`
- Modify: `07 Lessons/codex-lessons.md`
- Modify: `03 Skills/linktec-skill.md`
- Modify: `05 Architecture/linktech-user-system.md`
- Modify: `06 Decisions/linktech-security.md`
- Modify: `07 Lessons/linktech-troubleshooting.md`
- Modify: `08 Templates/skill-analysis-template.md`
- Create: `08 Templates/architecture-template.md`
- Create: `08 Templates/decision-template.md`
- Create: `08 Templates/lesson-template.md`
- Create: `08 Templates/project-template.md`
- Create: `08 Templates/daily-template.md`
- Create: `03 Skills/skills.base`
- Create: `06 Decisions/decisions.base`
- Create: `07 Lessons/lessons.base`

**Interfaces:**
- Consumes: MOC and bridge-note paths.
- Produces: Consistent `type`, `topics`, `status`, and optional `project` properties; reusable templates; dynamic Bases.

- [ ] **Step 1: Add parsable YAML properties**

Use single-value `type`, list `topics`, single-value `status`, and linked-list `project` only where applicable.

- [ ] **Step 2: Add core templates**

Each template must contain valid properties and focused sections appropriate to its note type.

- [ ] **Step 3: Add Bases**

Create table/list views filtered by `type`, with useful columns and sorting; keep narrative context in MOCs rather than duplicating it in Bases.

- [ ] **Step 4: Validate metadata**

Parse all touched YAML and Base files. Expected: no syntax errors and all required fields present.

- [ ] **Step 5: Commit**

```bash
git add -- "02 Projects" "03 Skills" "05 Architecture" "06 Decisions" "07 Lessons" "08 Templates"
git commit -m "feat: add Obsidian properties templates and Bases"
```

### Task 4: Core-plugin and graph configuration

**Files:**
- Create: `.obsidian/app.json`
- Create: `.obsidian/core-plugins.json`
- Create: `.obsidian/daily-notes.json`
- Create: `.obsidian/templates.json`
- Create: `.obsidian/graph.json`

**Interfaces:**
- Consumes: Properties and template paths from Task 3.
- Produces: A portable Vault configuration using core plugins only.

- [ ] **Step 1: Configure file behavior**

Enable automatic internal-link updates, Wikilinks, the `Attachments` attachment folder, and excluded-file patterns for code, caches, process docs, README, and AGENTS files.

- [ ] **Step 2: Enable useful core plugins**

Enable Graph, Backlinks, Outgoing Links, Properties, Bases, Templates, Daily Notes, Bookmarks, Canvas, Page Preview, File Recovery, Search, and Command Palette.

- [ ] **Step 3: Configure Templates and Daily Notes**

Point Templates to `08 Templates`; point Daily Notes to `01 Daily` using `YYYY-MM-DD` and the daily template.

- [ ] **Step 4: Configure graph groups**

Exclude non-knowledge files and create distinct groups for MOCs, Projects, Skills, Architecture, Decisions, and Lessons.

- [ ] **Step 5: Validate JSON and commit**

Parse every new JSON file. Expected: valid JSON and no community-plugin configuration.

```bash
git add -- .obsidian
git commit -m "feat: configure Obsidian core knowledge tools"
```

### Task 5: Full verification

**Files:**
- Verify: all files changed in Tasks 1–4

**Interfaces:**
- Consumes: Complete implementation.
- Produces: Evidence that the Vault is internally consistent and scoped correctly.

- [ ] **Step 1: Run the complete link audit**

Expected: 0 unresolved or ambiguous knowledge links.

- [ ] **Step 2: Parse structured files**

Expected: all JSON, YAML frontmatter, and Base files parse successfully.

- [ ] **Step 3: Verify configuration coverage**

Expected: six graph groups, required excluded paths, five template types, three Bases, and required core plugins.

- [ ] **Step 4: Inspect the diff**

Run `git diff --check`, confirm no source/code/cache files changed, and review the full diff for accidental technical-content rewrites.

- [ ] **Step 5: Report completion**

Summarize commits, verification evidence, and any optional manual Obsidian actions such as arranging Bookmarks or creating a Canvas.
