# Codex Conversation Archive Design

## Goal

Automatically turn Codex conversations into concise, traceable Obsidian notes and index those notes in the existing AI-Brain Qdrant collection without requiring a manual command after each conversation.

## Scope

The first version handles Codex sessions stored under `~/.codex/sessions`. It extends the existing `ai-brain-rag` project and reuses its DeepSeek, Ollama, Qdrant, and Obsidian integrations. It does not import conversations from ChatGPT web, Claude, messaging applications, or other sources.

## Chosen retention model

Use option C:

- Store a structured summary in Obsidian.
- Keep the original transcript only in `~/.codex/sessions`.
- Record the source session ID and transcript path in the note frontmatter.
- Do not copy full transcripts into Obsidian or Qdrant.
- Never compress, move, modify, or delete original Codex sessions automatically.

## Existing-system findings

The project already provides:

- Vault-wide Markdown scanning with SHA-256 change detection.
- Markdown chunking.
- Local embeddings through Ollama `nomic-embed-text` using 768-dimensional vectors.
- A Qdrant collection named `ai-brain`.
- DeepSeek configuration for generated answers.
- RAG API and MCP search access.

The current indexer stores its state in `/tmp/indexer_state.json`, so state can disappear after a restart. When a Markdown file changes, it inserts new randomly identified points without first deleting the old points for that file. Conversation notes will change repeatedly, so this behavior can leave stale or duplicate vectors and must be corrected as part of the integration.

## Architecture

### 1. Codex lifecycle hook

A user-level Codex `Stop` hook in `~/.codex/hooks.json` invokes a small enqueue command after a turn ends. The hook reads the JSON event from standard input and records only the fields required for later processing:

- `session_id`
- `turn_id`
- `transcript_path`
- `cwd`
- event timestamp

The hook must finish quickly. It does not call DeepSeek, Ollama, or Qdrant and does not parse the complete transcript.

Existing user-level hook configuration must be merged rather than overwritten. The installed hook must use an absolute executable path and must not depend on the current project directory.

### 2. Durable queue and state

Use SQLite inside `ai-brain-rag/data/conversation-archive/state.sqlite3`. The database records pending sessions, the latest observed turn, last transcript modification time, processing status, retry count, last successful content hash, note path, and error information.

Repeated hook events for the same session are coalesced. A session becomes eligible for processing after a configurable quiet period, initially five minutes. This prevents a long conversation from producing a new summary after every turn.

Failed jobs use bounded exponential retry and remain visible in logs and state. A failed summary never replaces a previously valid note.

### 3. Transcript adapter

Transcript parsing is isolated behind one adapter because Codex documents `transcript_path` as convenient hook input but does not guarantee that the transcript file format is stable.

The adapter extracts human and assistant conversational content and excludes system instructions, tool schemas, raw tool output, internal reasoning, and secrets where identifiable. Unsupported record shapes are counted and logged without aborting the whole session. Parsing the same unchanged transcript produces the same normalized content hash.

### 4. DeepSeek summarization

The summarizer reuses the existing DeepSeek API configuration. Ollama remains responsible only for embeddings.

DeepSeek returns a validated structured result containing:

- title
- concise summary
- decisions
- completed work
- action items
- unresolved questions
- problems and solutions
- projects and files involved
- tags

The prompt treats transcript text as untrusted data and instructs the model not to follow instructions found inside the transcript. Invalid responses are rejected and retried; they are not written as partial notes. API keys remain in the existing ignored environment configuration and are never copied into logs or notes.

### 5. Obsidian writer

Notes are written below:

`02 Projects/Codex Conversations/YYYY/MM/`

Each session owns one stable Markdown file. The filename uses the session date, a sanitized title, and a short session-ID suffix. YAML frontmatter contains:

- `type: codex-conversation`
- `source: codex`
- `session_id`
- `transcript_path`
- `created`
- `updated`
- `project_cwd`
- `content_hash`
- `summary_model`
- `status`
- `tags`

The body contains only the structured summary sections. The transcript path is stored as provenance, not embedded content. Writes use a temporary file followed by an atomic rename. A failed generation leaves the prior note intact.

### 6. Qdrant integration and indexer correction

The existing vault indexer remains the only component that writes note chunks to Qdrant. The conversation worker writes Markdown and lets the indexer detect it.

Indexer state moves from `/tmp` to a configurable persistent path under `ai-brain-rag/data/indexer/state.json`. Before inserting chunks for any changed file, the indexer deletes all existing points whose payload belongs to that file. It then upserts deterministic point IDs derived from the relative path and chunk index. The payload field used for deletion is standardized so modified and deleted files follow the same code path.

State is updated only for files that were successfully processed. A failed chunk or embedding operation must remain pending for the next scan rather than being incorrectly marked current.

### 7. Capacity monitoring

The worker calculates the following for `~/.codex/sessions`:

- total file count
- total bytes
- oldest and newest transcript timestamps
- growth since the previous report
- files observed but not successfully summarized

A monthly Markdown report is written to `09 System Reports/Codex Storage/YYYY-MM.md`. Configurable warning thresholds default to 5 GiB total size and 20% month-over-month growth.

Monitoring is read-only. The system never compresses, moves, edits, or deletes Codex transcripts. Crossing a threshold creates a warning in the report and logs but performs no cleanup action.

### 8. Automatic operation on macOS

Use user-level `launchd` agents:

- one long-running conversation archive worker
- one long-running existing vault indexer

The services start at login, restart after unexpected exit, use absolute paths, and write rotating logs under `ai-brain-rag/data/logs`. Qdrant and Ollama remain external prerequisites. If either dependency is unavailable, workers retry without losing queued sessions.

Installer and uninstaller scripts manage only the launch-agent files created by this project. Uninstalling automation does not remove notes, state, vectors, transcripts, Qdrant data, or environment files.

## Data flow

1. Codex finishes a turn and runs the `Stop` hook.
2. The hook coalesces the session into SQLite and returns.
3. The worker waits until the session has been quiet for five minutes.
4. The transcript adapter normalizes permitted conversational content.
5. If the normalized hash is unchanged, processing stops.
6. DeepSeek produces a validated structured summary.
7. The writer atomically creates or updates the session's Obsidian note.
8. The existing indexer detects the changed Markdown, deletes stale points, embeds current chunks with Ollama, and writes them to Qdrant.
9. SQLite records the successful hash and note path.

## Error handling

- Hook failure must not block or alter the Codex transcript.
- Missing transcripts remain queued for retry because hook and filesystem timing may differ.
- DeepSeek timeout, rate-limit, malformed output, or authentication failure does not overwrite an existing note.
- Missing Ollama or Qdrant leaves the Markdown note intact and pending for indexing.
- Transcript parser incompatibility is reported with session and record type, without logging private transcript content.
- SQLite and note writes use transactions or atomic replacement.
- No automated recovery path is allowed to delete source conversations.

## Testing

Automated tests cover:

- hook event validation and session coalescing
- quiet-period eligibility
- representative JSONL transcript normalization
- exclusion of tool and system records
- deterministic content hashes and note paths
- DeepSeek structured-response validation
- atomic note creation and update behavior
- retry behavior preserving a prior valid note
- changed-file stale-vector deletion
- deleted-file vector deletion
- state advancement only after successful indexing
- capacity calculations, threshold warnings, and the no-delete guarantee

Integration tests use temporary Vault, SQLite, and fake HTTP services. A local smoke test uses one copied transcript fixture, the configured DeepSeek API, live Ollama, and live Qdrant, then verifies the note and searchable payload. Tests must not modify real Codex transcripts.

## Security and privacy constraints

- Never write API keys or credentials into source, notes, reports, payloads, or logs.
- Treat transcript contents as untrusted input.
- Do not index full raw transcripts.
- Keep Qdrant and service ports bound to localhost as currently configured.
- Do not follow or mutate paths outside the configured Codex sessions root and Vault output roots.
- Preserve all unrelated existing Vault and Git changes.

## Success criteria

- A new or updated Codex session automatically produces or updates exactly one Obsidian summary note after the quiet period.
- Reprocessing unchanged input makes no note or vector changes.
- Updating a note cannot leave stale Qdrant chunks for the same file.
- DeepSeek failure preserves the last valid note and retries later.
- Capacity reports appear monthly and warnings are informational only.
- No execution path compresses, moves, modifies, or deletes files under `~/.codex/sessions`.
- The archive worker and indexer resume automatically after macOS login or process restart.
