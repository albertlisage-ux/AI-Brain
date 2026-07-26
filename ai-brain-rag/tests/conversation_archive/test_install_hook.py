from copy import deepcopy

from conversation_archive.hook import merge_stop_hook


def test_merge_preserves_existing_hook_entries() -> None:
    existing = {
        "version": 1,
        "hooks": {
            "Stop": [{"type": "command", "command": "/existing/hook"}],
            "Start": [{"type": "command", "command": "/existing/start"}],
        },
        "unrelated": {"keep": True},
    }
    original = deepcopy(existing)

    merged = merge_stop_hook(existing, "/absolute/archive-hook")

    assert existing == original
    assert merged["hooks"]["Start"] == original["hooks"]["Start"]
    assert merged["unrelated"] == original["unrelated"]
    assert {
        handler["command"]
        for group in merged["hooks"]["Stop"]
        for handler in group["hooks"]
    } == {
        "/existing/hook",
        "/absolute/archive-hook",
    }


def test_merge_is_idempotent() -> None:
    once = merge_stop_hook({}, "/absolute/archive-hook")
    twice = merge_stop_hook(once, "/absolute/archive-hook")

    assert twice == once
    assert len(twice["hooks"]["Stop"]) == 1


def test_merge_requires_absolute_command() -> None:
    try:
        merge_stop_hook({}, "relative-command")
    except ValueError as exc:
        assert "absolute" in str(exc)
    else:
        raise AssertionError("relative command was accepted")


def test_merge_writes_codex_matcher_group_schema() -> None:
    merged = merge_stop_hook({}, "/absolute/archive-hook")

    assert merged["hooks"]["Stop"] == [
        {
            "hooks": [
                {"type": "command", "command": "/absolute/archive-hook"}
            ]
        }
    ]
