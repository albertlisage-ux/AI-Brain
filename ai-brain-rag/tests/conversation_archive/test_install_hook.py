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
    assert {entry["command"] for entry in merged["hooks"]["Stop"]} == {
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
