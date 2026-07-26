# Codex Conversation Archive Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Automatically summarize quiet Codex sessions into traceable Obsidian notes, index them through the existing Ollama/Qdrant pipeline, and report transcript storage growth without deleting source data.

**Architecture:** A fast Codex `Stop` hook coalesces session events into SQLite. A launchd-managed worker parses normalized conversational messages, asks the existing DeepSeek endpoint for validated JSON, and atomically updates one Markdown note per session. The existing indexer is corrected to use persistent state and replace stale per-file vectors before launchd manages both workers.

**Tech Stack:** Python 3.11+, stdlib SQLite/JSON/urllib, DeepSeek Chat Completions API, Ollama `nomic-embed-text`, Qdrant, pytest, macOS launchd.

## Global Constraints

- Store summaries under `02 Projects/Codex Conversations/YYYY/MM/`; never copy full transcripts into Obsidian or Qdrant.
- Never compress, move, modify, or delete files under `~/.codex/sessions`.
- Reuse `DEEPSEEK_API_*`, Ollama `nomic-embed-text`, and Qdrant collection `ai-brain`.
- Preserve unrelated Vault and Git changes.
- Treat transcript text as untrusted data and never log transcript bodies or secrets.

---

### Task 1: Archive configuration and durable queue

**Files:**
- Create: `ai-brain-rag/conversation_archive/__init__.py`
- Create: `ai-brain-rag/conversation_archive/config.py`
- Create: `ai-brain-rag/conversation_archive/store.py`
- Create: `ai-brain-rag/tests/conversation_archive/test_store.py`
- Modify: `ai-brain-rag/.gitignore`

**Interfaces:**
- Produces: `ArchiveConfig.from_env() -> ArchiveConfig`
- Produces: `ArchiveStore.enqueue(event: HookEvent)`, `eligible(now)`, `mark_success(...)`, and `mark_failure(...)`.

- [ ] Write failing pytest cases proving repeated session events coalesce, the newest turn wins, 60-second quiet-period eligibility works, and retry state survives reopening SQLite.
- [ ] Run `ai-brain-rag/.venv/bin/pytest tests/conversation_archive/test_store.py -q`; expect failures because the package does not exist.
- [ ] Implement typed configuration with explicit Vault, session-root, SQLite, quiet-period, DeepSeek, and report-threshold settings; implement schema creation and transactional upserts in `ArchiveStore`.
- [ ] Add `data/conversation-archive/`, `data/indexer/`, and `data/logs/` to `.gitignore` while keeping code and tests tracked.
- [ ] Re-run the focused test and expect all cases to pass.
- [ ] Commit with `feat: add durable conversation archive queue`.

### Task 2: Codex hook ingestion and safe configuration merge

**Files:**
- Create: `ai-brain-rag/conversation_archive/hook.py`
- Create: `ai-brain-rag/scripts/install-codex-hook.py`
- Create: `ai-brain-rag/tests/conversation_archive/test_hook.py`
- Create: `ai-brain-rag/tests/conversation_archive/test_install_hook.py`

**Interfaces:**
- Consumes: `ArchiveConfig`, `ArchiveStore`.
- Produces: `HookEvent.from_json(value) -> HookEvent` and CLI exit code `0` for accepted or safely ignored events.
- Produces: `merge_stop_hook(existing: dict, command: str) -> dict` without modifying unrelated hooks.

- [ ] Write failing tests for valid `Stop` input, missing transcript paths, malformed JSON, duplicate events, preservation of existing hook entries, and idempotent installation.
- [ ] Run both test files and verify they fail because hook modules are missing.
- [ ] Implement stdin ingestion that logs metadata only and returns promptly; implement a JSON merger that adds exactly one absolute command to the user-level `Stop` hooks.
- [ ] Re-run focused tests and expect all cases to pass.
- [ ] Commit with `feat: enqueue Codex stop hook events`.

### Task 3: Version-isolated transcript normalization

**Files:**
- Create: `ai-brain-rag/conversation_archive/transcript.py`
- Create: `ai-brain-rag/tests/fixtures/codex-session.jsonl`
- Create: `ai-brain-rag/tests/conversation_archive/test_transcript.py`

**Interfaces:**
- Produces: `NormalizedTranscript(session_id, created_at, messages, content_hash)`.
- Produces: `parse_transcript(path: Path, sessions_root: Path) -> NormalizedTranscript`.

- [ ] Build a synthetic JSONL fixture containing `session_meta`, user and assistant messages, tool output, system instructions, reasoning records, malformed records, and prompt-injection text.
- [ ] Write failing tests proving only user/assistant visible text is retained, tool/system/reasoning data is excluded, unsupported records are tolerated, root escape is rejected, and hashes are deterministic.
- [ ] Run the focused test and verify the expected missing implementation failure.
- [ ] Implement a streaming adapter for the observed `session_meta`, `event_msg`, and `response_item` envelopes. Validate resolved paths remain inside the configured sessions root and never log message contents.
- [ ] Re-run focused tests and expect all cases to pass.
- [ ] Commit with `feat: normalize Codex transcripts safely`.

### Task 4: DeepSeek structured summary and atomic Obsidian notes

**Files:**
- Create: `ai-brain-rag/conversation_archive/summarizer.py`
- Create: `ai-brain-rag/conversation_archive/note_writer.py`
- Create: `ai-brain-rag/tests/conversation_archive/test_summarizer.py`
- Create: `ai-brain-rag/tests/conversation_archive/test_note_writer.py`

**Interfaces:**
- Consumes: `NormalizedTranscript`, existing `DEEPSEEK_API_KEY`, `DEEPSEEK_API_BASE`, `DEEPSEEK_MODEL` semantics.
- Produces: `ConversationSummary` with title, summary, decisions, completed work, actions, unresolved questions, solutions, projects/files, and tags.
- Produces: `write_note(summary, transcript, config) -> Path`.

- [ ] Write failing tests for prompt-injection isolation, JSON code-fence cleanup, schema rejection, HTTP errors, deterministic session filenames, YAML escaping, and preservation of an existing note when generation fails.
- [ ] Run focused tests and verify failures occur before implementation.
- [ ] Implement DeepSeek Chat Completions through stdlib HTTP with a system instruction that treats transcript content as data. Validate every field and cap list/text sizes.
- [ ] Implement Markdown rendering and atomic same-directory temporary-file replacement under `02 Projects/Codex Conversations/YYYY/MM/`.
- [ ] Re-run focused tests and expect all cases to pass.
- [ ] Commit with `feat: summarize sessions into Obsidian notes`.

### Task 5: Worker retries and read-only capacity reports

**Files:**
- Create: `ai-brain-rag/conversation_archive/capacity.py`
- Create: `ai-brain-rag/conversation_archive/worker.py`
- Create: `ai-brain-rag/tests/conversation_archive/test_capacity.py`
- Create: `ai-brain-rag/tests/conversation_archive/test_worker.py`

**Interfaces:**
- Consumes: queue, transcript parser, summarizer, and note writer interfaces from Tasks 1–4.
- Produces: `collect_capacity(root) -> CapacitySnapshot`, `write_monthly_report(...) -> Path`, and `process_once(...) -> ProcessResult`.

- [ ] Write failing tests for unchanged-hash no-op, successful note update, bounded exponential retry, prior-note preservation, monthly report idempotency, 5-GiB/20% warnings, unsummarized counts, and no filesystem mutation calls against transcripts.
- [ ] Run focused tests and verify failures occur because worker modules are absent.
- [ ] Implement one-pass processing and a polling CLI loop with signal handling. Keep missing dependencies retryable and write reports atomically.
- [ ] Re-run focused tests and expect all cases to pass.
- [ ] Commit with `feat: process conversation queue and report capacity`.

### Task 6: Correct stale Qdrant vectors and persistent index state

**Files:**
- Modify: `ai-brain-rag/indexer/config.py`
- Modify: `ai-brain-rag/indexer/indexer.py`
- Create: `ai-brain-rag/tests/indexer/test_indexer_updates.py`

**Interfaces:**
- Produces: `_delete_file_points(client, rel_path)` using payload key `filepath`.
- Produces: deterministic UUID point IDs from relative path and chunk index.
- Produces: `INDEXER_STATE_FILE` configurable under `data/indexer/state.json`.

- [ ] Write failing fake-Qdrant tests proving changed and deleted files remove all prior points, successful changed files receive deterministic IDs, failures remain pending, and successful unrelated files advance state.
- [ ] Run the focused test and verify existing code fails duplicate/stale-vector expectations.
- [ ] Standardize all filters on payload `filepath`, delete stale points before changed-file upsert, replace random UUIDs with UUIDv5 IDs, save state atomically, and merge only successfully processed file states.
- [ ] Re-run focused tests and the existing archive suite; expect all tests to pass.
- [ ] Commit with `fix: replace stale vectors during vault updates`.

### Task 7: launchd automation, dependency setup, and documentation

**Files:**
- Create: `ai-brain-rag/scripts/run-conversation-archive.sh`
- Create: `ai-brain-rag/scripts/install-automation.sh`
- Create: `ai-brain-rag/scripts/uninstall-automation.sh`
- Create: `ai-brain-rag/launchd/com.yuanzhe.ai-brain-conversation-archive.plist.template`
- Create: `ai-brain-rag/launchd/com.yuanzhe.ai-brain-indexer.plist.template`
- Create: `ai-brain-rag/tests/scripts/test_installation.py`
- Modify: `ai-brain-rag/indexer/requirements.txt`
- Modify: `ai-brain-rag/README.md`
- Modify: `03 Skills/ai-rag-setup-guide.md`

**Interfaces:**
- Consumes: worker and indexer CLIs.
- Produces: idempotent installer that merges the Codex hook and loads exactly two user LaunchAgents.
- Produces: uninstaller that unloads only project-owned agents and never removes data.

- [ ] Write failing tests that render plist templates in a temporary home, verify absolute paths and environment loading, verify installer idempotency, and assert uninstall scripts contain no transcript/data deletion operations.
- [ ] Run the focused installation test and verify expected failures.
- [ ] Implement scripts with `set -euo pipefail`, explicit project paths, launchd log paths, and safe `bootout/bootstrap` behavior; document prerequisites, configuration, start/stop/status, reports, privacy, and recovery.
- [ ] Re-run focused and full tests; expect all to pass.
- [ ] Commit with `feat: automate conversation archive on macOS`.

### Task 8: Controlled installation and end-to-end verification

**Files:**
- Modify only generated user config: `~/.codex/hooks.json` and `~/Library/LaunchAgents/com.yuanzhe.ai-brain-*.plist` through reviewed installers.
- Create runtime state only under ignored `ai-brain-rag/data/` and summary/report destinations in the Vault.

**Interfaces:**
- Verifies the complete production data flow without changing any original transcript.

- [ ] Run the full test suite with `ai-brain-rag/.venv/bin/pytest -q` and record exact pass/fail totals.
- [ ] Run `python -m compileall conversation_archive indexer rag-api mcp-server` and expect exit code 0.
- [ ] Inspect `.env.local` variable names without printing values and verify DeepSeek configuration is present.
- [ ] With approval for local services, verify live Qdrant and Ollama health, then install the hook and LaunchAgents.
- [ ] Copy one transcript into a temporary fixture directory, enqueue it, process it with the configured DeepSeek endpoint, and verify exactly one note is written and searchable in Qdrant.
- [ ] Reprocess unchanged content and verify note mtime and Qdrant point count do not change.
- [ ] Run capacity reporting and verify no file metadata or content under `~/.codex/sessions` changed.
- [ ] Inspect `git diff --check`, `git status --short`, launchd status, worker logs, and Qdrant results; report any external-service limitation explicitly.
- [ ] Commit final documentation or verification adjustments with `docs: complete conversation archive setup`.

## Plan self-review

- Every design requirement maps to a task: ingestion (2), state/debounce (1), parsing (3), DeepSeek/notes (4), retries/capacity (5), Qdrant correction (6), automation/docs (7), production verification (8).
- Production behavior is introduced only after a failing test in each task.
- Source transcript deletion is absent from every interface and explicitly asserted in tests.
- Runtime files and unrelated Vault notes remain untracked and untouched.
