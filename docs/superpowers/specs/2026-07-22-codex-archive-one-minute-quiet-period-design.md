# Codex Archive One-Minute Quiet Period Design

## Goal

Change the Codex conversation archive quiet period from five minutes to one minute so completed turns are summarized sooner.

## Design

- Change the `ArchiveConfig.from_env()` default for `CONVERSATION_QUIET_SECONDS` from `300` to `60`.
- Set `CONVERSATION_QUIET_SECONDS=60` in the existing ignored `.env.local` without reading, printing, or changing any secret value.
- Preserve the current SQLite eligibility, coalescing, retry, transcript parsing, summarization, note writing, and indexing behavior.
- Update user-facing documentation to describe a one-minute quiet period.
- Add a regression test proving the default configuration resolves to 60 seconds. Existing store tests continue to verify eligibility at an explicitly supplied quiet period.
- Restart only `com.yuanzhe.ai-brain-conversation-archive`; the indexer does not depend on this setting.

## Verification

- Run the focused configuration and store tests, then the complete pytest suite.
- Source `.env.local` without printing values and report only the effective quiet-period duration.
- Verify the conversation archive LaunchAgent returns to the `running` state after restart.

## Safety

No transcript, summary, SQLite record, vector, credential, or unrelated Vault note is deleted or rewritten by this configuration change.
