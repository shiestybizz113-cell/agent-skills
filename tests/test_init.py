from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INIT = ROOT / "scripts" / "init"


class InitScriptTests(unittest.TestCase):
    def run_init(self, workspace: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["AGENT_SKILLS_ROOT"] = str(ROOT)
        return subprocess.run(
            ["python3", str(INIT), "--workspace", str(workspace), *extra],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_merges_settings_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            settings = workspace / ".claude" / "settings.local.json"
            settings.parent.mkdir(parents=True)
            settings.write_text(
                json.dumps({"permissions": {"allow": ["Read"]}}),
                encoding="utf-8",
            )

            first = self.run_init(workspace)
            self.assertEqual(first.returncode, 0, first.stderr)
            installed = json.loads(settings.read_text(encoding="utf-8"))
            self.assertEqual(installed["permissions"], {"allow": ["Read"]})
            self.assertEqual(len(installed["hooks"]["PreToolUse"]), 1)
            self.assertEqual(len(installed["hooks"]["PostToolUse"]), 1)
            self.assertTrue((workspace / ".claude/hooks/agent-skills-pre-edit-guard.sh").exists())
            self.assertTrue((workspace / ".claude/hooks/agent-skills-post-edit-validate.py").exists())
            self.assertEqual(len(list(settings.parent.glob("settings.local.json.backup-*"))), 1)

            second = self.run_init(workspace)
            self.assertEqual(second.returncode, 0, second.stderr)
            installed_again = json.loads(settings.read_text(encoding="utf-8"))
            self.assertEqual(installed_again, installed)
            self.assertEqual(len(list(settings.parent.glob("settings.local.json.backup-*"))), 1)

    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            result = self.run_init(workspace, "--dry-run")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("DRY RUN", result.stdout)
            self.assertFalse((workspace / ".claude").exists())

    def test_invalid_json_is_preserved_and_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            settings = workspace / ".claude" / "settings.local.json"
            settings.parent.mkdir(parents=True)
            settings.write_text("{broken", encoding="utf-8")

            result = self.run_init(workspace)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(settings.read_text(encoding="utf-8"), "{broken")
            self.assertFalse((workspace / ".claude/hooks").exists())


if __name__ == "__main__":
    unittest.main()
