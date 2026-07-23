from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from package_plugin import included_files  # noqa: E402
from validate_plugin import validate_root  # noqa: E402


class PluginValidationTests(unittest.TestCase):
    def test_repository_passes_all_invariants(self) -> None:
        validation = validate_root(ROOT)
        self.assertEqual([], validation.errors)
        self.assertGreaterEqual(validation.checks, 140)

    def test_packaged_files_exclude_local_and_development_data(self) -> None:
        relative = {path.relative_to(ROOT).as_posix() for path in included_files(ROOT)}
        self.assertIn(".claude-plugin/plugin.json", relative)
        self.assertIn(".claude-plugin/marketplace.json", relative)
        self.assertIn("skills/apply/SKILL.md", relative)
        self.assertFalse(any(path.startswith("data/") for path in relative))
        self.assertFalse(any(path.startswith("tests/") for path in relative))
        self.assertFalse(any(path.startswith(".git/") for path in relative))

    def test_stale_repository_url_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "plugin"
            shutil.copytree(
                ROOT,
                copy,
                ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"),
            )
            readme = copy / "README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8")
                + "\nhttps://github.com/andrewshwetzer/career-ops-plugin\n",
                encoding="utf-8",
            )
            validation = validate_root(copy)
            self.assertTrue(
                any("stale repository reference" in error for error in validation.errors)
            )

    def test_missing_application_gate_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "plugin"
            shutil.copytree(
                ROOT,
                copy,
                ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"),
            )
            apply_skill = copy / "skills/apply/SKILL.md"
            apply_skill.write_text(
                apply_skill.read_text(encoding="utf-8").replace(
                    "NEEDS USER INPUT", "MISSING FACT"
                ),
                encoding="utf-8",
            )
            validation = validate_root(copy)
            self.assertIn(
                "apply workflow is missing gate language: NEEDS USER INPUT",
                validation.errors,
            )


if __name__ == "__main__":
    unittest.main()
