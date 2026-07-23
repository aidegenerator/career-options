#!/usr/bin/env python3
"""Build and verify a Claude custom-plugin ZIP with files at archive root."""

from __future__ import annotations

import json
import stat
import sys
import zipfile
from pathlib import Path

from validate_plugin import validate_root


INCLUDE = (
    ".claude-plugin",
    "agents",
    "commands",
    "references",
    "skills",
    "ATTRIBUTION.md",
    "LICENSE",
    "README.md",
)
MAX_ZIP_BYTES = 50 * 1024 * 1024


def included_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for entry in INCLUDE:
        path = root / entry
        if path.is_dir():
            files.extend(candidate for candidate in path.rglob("*") if candidate.is_file())
        elif path.is_file():
            files.append(path)
    return sorted(files)


def verify_zip(path: Path) -> None:
    if path.stat().st_size >= MAX_ZIP_BYTES:
        raise ValueError("ZIP exceeds Claude's 50 MB custom-plugin limit")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if ".claude-plugin/plugin.json" not in names:
            raise ValueError("manifest is not at ZIP root")
        if any(name.startswith("/") or ".." in Path(name).parts for name in names):
            raise ValueError("ZIP contains an unsafe path")
        if any(name.startswith((".git/", "data/", "config/", "dist/")) for name in names):
            raise ValueError("ZIP contains excluded local data")
        for info in archive.infolist():
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise ValueError(f"ZIP contains symlink: {info.filename}")


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    validation = validate_root(root)
    if validation.errors:
        for error in validation.errors:
            print(f"ERROR: {error}")
        return 1

    manifest = json.loads((root / ".claude-plugin/plugin.json").read_text())
    output_dir = root / "dist"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / f"career-ops-{manifest['version']}.zip"

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in included_files(root):
            archive.write(path, path.relative_to(root).as_posix())

    verify_zip(output)
    print(f"PASS: {output} ({output.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
