import json
from pathlib import Path
import sys
import uuid

INDEXER_DIR = Path(__file__).parents[2] / "indexer"
sys.path.insert(0, str(INDEXER_DIR))

import indexer as module  # noqa: E402


class FakeClient:
    def __init__(self, fail_delete: set[str] | None = None):
        self.operations = []
        self.fail_delete = fail_delete or set()

    def delete(self, collection_name, points_selector, wait=True):
        condition = points_selector.filter.must[0]
        rel = condition.match.value
        self.operations.append(("delete", rel, condition.key))
        if rel in self.fail_delete:
            raise RuntimeError("delete failed")

    def upsert(self, collection_name, points, wait=True):
        self.operations.append(("upsert", list(points)))


def configure(monkeypatch, tmp_path: Path, current: dict, previous: dict):
    state = tmp_path / "data/indexer/state.json"
    state.parent.mkdir(parents=True)
    state.write_text(json.dumps(previous))
    vault = tmp_path / "vault"
    vault.mkdir()
    for rel in current:
        path = vault / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("content for " + rel)
    monkeypatch.setattr(module, "STATE_FILE", str(state))
    monkeypatch.setattr(module, "OBSIDIAN_VAULT", str(vault))
    monkeypatch.setattr(module, "scan_vault", lambda: current)
    monkeypatch.setattr(
        module,
        "chunk_markdown",
        lambda path: [{"heading": "H", "content": Path(path).name + " content long enough"}],
    )
    monkeypatch.setattr(module, "embed_texts", lambda texts: [[0.1, 0.2] for _ in texts])
    return state


def test_changed_and_deleted_files_remove_all_prior_points(monkeypatch, tmp_path: Path) -> None:
    current = {"changed.md": {"hash": "new"}}
    previous = {"changed.md": {"hash": "old"}, "deleted.md": {"hash": "old"}}
    configure(monkeypatch, tmp_path, current, previous)
    client = FakeClient()

    module.index_vault(client)

    deletes = [operation for operation in client.operations if operation[0] == "delete"]
    assert deletes == [
        ("delete", "deleted.md", "filepath"),
        ("delete", "changed.md", "filepath"),
    ]


def test_changed_file_uses_deterministic_uuid_ids(monkeypatch, tmp_path: Path) -> None:
    current = {"changed.md": {"hash": "new"}}
    configure(monkeypatch, tmp_path, current, {})
    client = FakeClient()

    module.index_vault(client)
    point = next(op[1][0] for op in client.operations if op[0] == "upsert")

    assert point.id == module._point_id("changed.md", 0)
    assert point.id == module._point_id("changed.md", 0)
    assert str(uuid.UUID(str(point.id))) == str(point.id)
    assert point.payload["filepath"] == "changed.md"


def test_failed_file_stays_pending_while_successful_file_advances(monkeypatch, tmp_path: Path) -> None:
    current = {"bad.md": {"hash": "new-bad"}, "good.md": {"hash": "new-good"}}
    previous = {"bad.md": {"hash": "old-bad"}, "good.md": {"hash": "old-good"}}
    state = configure(monkeypatch, tmp_path, current, previous)

    def embed(texts):
        if texts[0].startswith("bad.md"):
            raise RuntimeError("embedding failed")
        return [[0.1, 0.2]]

    monkeypatch.setattr(module, "embed_texts", embed)
    module.index_vault(FakeClient())

    saved = json.loads(state.read_text())
    assert saved["bad.md"]["hash"] == "old-bad"
    assert saved["good.md"]["hash"] == "new-good"


def test_failed_deleted_file_remains_in_state_for_retry(monkeypatch, tmp_path: Path) -> None:
    state = configure(monkeypatch, tmp_path, {}, {"deleted.md": {"hash": "old"}})
    module.index_vault(FakeClient(fail_delete={"deleted.md"}))
    assert "deleted.md" in json.loads(state.read_text())
