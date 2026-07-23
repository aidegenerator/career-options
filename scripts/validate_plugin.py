#!/usr/bin/env python3
"""Dependency-free structural and behavioral checks for career-ops."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


EXPECTED_REPOSITORY = (
    "https://github.com/andrew-shwetzer/"
    "career-ops-plugin-do-not-fork-currently-updating-v2-"
)
STALE_REPOSITORY_FRAGMENTS = (
    "github.com/andrewshwetzer",
    "github.com/andrew-shwetzer/career-ops-plugin.git",
)
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
RESOURCE_REF = re.compile(r"references/[a-z0-9][a-z0-9._/-]*\.(?:md|html)")
FRONTMATTER_NAME = re.compile(r"^name:\s*[\"']?([^\"'\n]+)", re.MULTILINE)
FRONTMATTER_DESCRIPTION = re.compile(
    r"^description:\s*(?:[\"'].*[\"']|\|.*)$", re.MULTILINE
)


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.checks = 0

    def require(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.errors.append(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(text: str, path: Path, validation: Validation) -> str:
    validation.require(text.startswith("---\n"), f"{path}: missing frontmatter")
    parts = text.split("---\n", 2)
    validation.require(len(parts) == 3, f"{path}: unclosed frontmatter")
    return parts[1] if len(parts) == 3 else ""


def validate_component(
    path: Path, expected_name: str, validation: Validation
) -> None:
    text = read_text(path)
    header = frontmatter(text, path, validation)
    name_match = FRONTMATTER_NAME.search(header)
    validation.require(name_match is not None, f"{path}: missing name")
    if name_match:
        validation.require(
            name_match.group(1).strip() == expected_name,
            f"{path}: name must be {expected_name!r}",
        )
    validation.require(
        FRONTMATTER_DESCRIPTION.search(header) is not None,
        f"{path}: missing description",
    )


def validate_resources(root: Path, validation: Validation) -> None:
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        for reference in RESOURCE_REF.findall(read_text(path)):
            validation.require(
                (root / reference).is_file(),
                f"{path}: missing referenced resource {reference}",
            )


def validate_text_invariants(root: Path, validation: Validation) -> None:
    text_files = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and "dist" not in path.parts
        and "tests" not in path.parts
        and path.suffix in {".md", ".json", ".yml", ".yaml", ".py"}
        and path.name != "validate_plugin.py"
    ]
    corpus = "\n".join(read_text(path) for path in text_files)

    for fragment in STALE_REPOSITORY_FRAGMENTS:
        validation.require(
            fragment not in corpus,
            f"stale repository reference remains: {fragment}",
        )

    apply_text = read_text(root / "skills/apply/SKILL.md")
    for required in (
        "references/workflow-gates.md",
        "Resume Draft",
        "Resume Ready",
        "Application Ready",
        "NEEDS USER INPUT",
        "never auto-submit",
    ):
        validation.require(
            required.lower() in apply_text.lower(),
            f"apply workflow is missing gate language: {required}",
        )

    tailor_text = read_text(root / "skills/tailor-resume/SKILL.md")
    for required in (
        "claim audit",
        "reverse chronological",
        "Resume Draft",
        "explicitly approves",
    ):
        validation.require(
            required.lower() in tailor_text.lower(),
            f"resume workflow is missing invariant: {required}",
        )

    scan_text = read_text(root / "skills/scan/SKILL.md")
    for required in (
        "references/job-identity.md",
        "Possible Duplicate",
        "snippet-only",
        "not exhaustive",
    ):
        validation.require(
            required.lower() in scan_text.lower(),
            f"scan workflow is missing duplicate/freshness rule: {required}",
        )

    screen_description = frontmatter(
        read_text(root / "skills/screen/SKILL.md"),
        root / "skills/screen/SKILL.md",
        validation,
    )
    evaluation_description = frontmatter(
        read_text(root / "skills/evaluate/SKILL.md"),
        root / "skills/evaluate/SKILL.md",
        validation,
    )
    validation.require(
        "pastes a job description" in screen_description,
        "screen must own default pasted-JD routing",
    )
    validation.require(
        "pastes what looks like a job description" not in evaluation_description,
        "evaluate must not compete with screen for default pasted-JD routing",
    )

    tracker_header = (
        "| Date Added | Date Applied | Company | Role | Job Key | Posting URL | "
        "Score | Status | Evaluation | Resume | Notes |"
    )
    for relative in (
        "commands/setup.md",
        "skills/evaluate/SKILL.md",
        "skills/track/SKILL.md",
    ):
        validation.require(
            tracker_header in read_text(root / relative),
            f"{relative}: tracker schema drift",
        )


def validate_root(root: Path) -> Validation:
    validation = Validation()
    manifest_path = root / ".claude-plugin/plugin.json"
    validation.require(manifest_path.is_file(), "missing plugin manifest")

    try:
        manifest = json.loads(read_text(manifest_path))
    except (OSError, json.JSONDecodeError) as exc:
        validation.errors.append(f"invalid plugin manifest: {exc}")
        return validation

    validation.require(manifest.get("name") == "career-ops", "wrong plugin name")
    validation.require(
        bool(SEMVER.match(str(manifest.get("version", "")))),
        "manifest version is not semantic versioning",
    )
    validation.require(
        manifest.get("repository") == EXPECTED_REPOSITORY,
        "manifest repository does not match the live repository",
    )
    validation.require(
        manifest.get("homepage") == EXPECTED_REPOSITORY,
        "manifest homepage does not match the live repository",
    )

    marketplace_path = root / ".claude-plugin/marketplace.json"
    validation.require(marketplace_path.is_file(), "missing marketplace manifest")
    try:
        marketplace = json.loads(read_text(marketplace_path))
    except (OSError, json.JSONDecodeError) as exc:
        validation.errors.append(f"invalid marketplace manifest: {exc}")
        marketplace = {}

    plugins = marketplace.get("plugins", [])
    validation.require(
        isinstance(plugins, list) and len(plugins) == 1,
        "marketplace must contain exactly one plugin",
    )
    if isinstance(plugins, list) and plugins:
        entry = plugins[0]
        validation.require(
            entry.get("name") == manifest.get("name"),
            "marketplace and plugin names differ",
        )
        validation.require(entry.get("source") == "./", "marketplace source must be ./")
        validation.require(
            entry.get("repository") == EXPECTED_REPOSITORY,
            "marketplace repository does not match the live repository",
        )
        validation.require(
            entry.get("homepage") == EXPECTED_REPOSITORY,
            "marketplace homepage does not match the live repository",
        )
        validation.require(
            entry.get("description") == manifest.get("description"),
            "marketplace and plugin descriptions differ",
        )

    skills = sorted((root / "skills").glob("*/SKILL.md"))
    validation.require(len(skills) >= 11, "expected at least 11 skills")
    seen_names: set[str] = set()
    for path in skills:
        expected_name = path.parent.name
        validate_component(path, expected_name, validation)
        validation.require(
            expected_name not in seen_names, f"duplicate skill name: {expected_name}"
        )
        seen_names.add(expected_name)

    for path in sorted((root / "commands").glob("*.md")):
        validate_component(path, path.stem, validation)
    for path in sorted((root / "agents").glob("*.md")):
        validate_component(path, path.stem, validation)

    validate_resources(root, validation)
    validate_text_invariants(root, validation)
    return validation


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    validation = validate_root(root)
    if validation.errors:
        print(f"FAILED: {len(validation.errors)} error(s)")
        for error in validation.errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {validation.checks} plugin checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
