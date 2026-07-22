import os
from pathlib import Path
import plistlib
import subprocess


ROOT = Path(__file__).parents[2]


def test_installer_renders_absolute_plists_and_is_idempotent(tmp_path: Path) -> None:
    home = tmp_path / "home"
    environment = {
        **os.environ,
        "AI_BRAIN_TARGET_HOME": str(home),
        "AI_BRAIN_SKIP_LAUNCHD": "1",
        "AI_BRAIN_SKIP_HOOK": "1",
    }
    command = ["bash", str(ROOT / "scripts/install-automation.sh")]

    subprocess.run(command, check=True, cwd=ROOT, env=environment)
    first = {
        path.name: path.read_bytes()
        for path in (home / "Library/LaunchAgents").glob("com.yuanzhe.ai-brain-*.plist")
    }
    subprocess.run(command, check=True, cwd=ROOT, env=environment)
    second = {
        path.name: path.read_bytes()
        for path in (home / "Library/LaunchAgents").glob("com.yuanzhe.ai-brain-*.plist")
    }

    assert first == second
    assert len(first) == 2
    for content in first.values():
        plist = plistlib.loads(content)
        arguments = plist["ProgramArguments"]
        assert any(str(ROOT.resolve()) in argument for argument in arguments)
        assert Path(plist["StandardOutPath"]).is_absolute()
        assert str(ROOT.resolve() / "data/logs") in plist["StandardOutPath"]
        assert "__PROJECT_ROOT__" not in content.decode()


def test_worker_wrapper_loads_env_and_uses_absolute_project_paths() -> None:
    script = (ROOT / "scripts/run-conversation-archive.sh").read_text()
    assert ".env.local" in script
    assert "set -a" in script
    assert "conversation_archive.worker" in script
    assert "conversation_archive.hook" in script


def test_uninstaller_never_deletes_transcripts_or_runtime_data() -> None:
    script = (ROOT / "scripts/uninstall-automation.sh").read_text()
    assert ".codex/sessions" not in script
    assert "data/" not in script
    assert "rm -rf" not in script
