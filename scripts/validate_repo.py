#!/usr/bin/env python3
"""Validate canonical skills, discovery links, and the README index."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import refresh_index  # noqa: E402


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DISCOVERY_DIRS = (
    ".agents/skills",
    ".claude/skills",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def expected_readme(root: Path, readme_text: str) -> str:
    return refresh_index.replace_index(readme_text, refresh_index.build_index(root))


def validate_frontmatter(root: Path, errors: list[str]) -> list[Path]:
    skill_paths: list[Path] = []
    for skill_md in sorted((root / "skills").glob("*/*/SKILL.md")):
        skill_dir = skill_md.parent
        name = skill_dir.name
        domain = skill_dir.parent.name
        skill_paths.append(skill_dir)

        if not NAME_RE.fullmatch(name):
            errors.append(f"{skill_dir}: folder name must be lowercase kebab-case")
        if not NAME_RE.fullmatch(domain):
            errors.append(f"{skill_dir}: domain must be lowercase kebab-case")

        frontmatter = refresh_index.parse_frontmatter(skill_md)
        if frontmatter.get("name") != name:
            errors.append(
                f"{skill_md}: frontmatter name must match folder name '{name}'"
            )
        if not frontmatter.get("description"):
            errors.append(f"{skill_md}: frontmatter description is required")
    return skill_paths


def validate_discovery_links(root: Path, skill_paths: list[Path], errors: list[str]) -> None:
    skills_by_name = {path.name: path.resolve() for path in skill_paths}
    for discovery in DISCOVERY_DIRS:
        discovery_dir = root / discovery
        if not discovery_dir.is_dir():
            errors.append(f"{discovery_dir}: missing discovery directory")
            continue

        for name, target in skills_by_name.items():
            link = discovery_dir / name
            if not link.is_symlink():
                errors.append(f"{link}: missing discovery symlink")
                continue
            if link.resolve() != target:
                errors.append(f"{link}: symlink points to {link.resolve()}, expected {target}")

        for entry in discovery_dir.iterdir():
            if entry.name == ".gitkeep":
                continue
            if not entry.is_symlink():
                errors.append(f"{entry}: discovery entries must be symlinks")
                continue
            if entry.name not in skills_by_name:
                errors.append(f"{entry}: discovery symlink has no matching skill")


def validate_readme_index(root: Path, errors: list[str]) -> None:
    readme = root / "README.md"
    if not readme.is_file():
        errors.append(f"{readme}: missing README.md")
        return
    text = readme.read_text(encoding="utf-8")
    if refresh_index.START_MARKER not in text or refresh_index.END_MARKER not in text:
        errors.append(f"{readme}: missing generated skills index markers")
        return
    expected = expected_readme(root, text)
    if text != expected:
        errors.append(
            f"{readme}: generated skills index is stale; run scripts/refresh_index.py"
        )


def validate_repo(root: Path | None = None) -> int:
    root = (root or repo_root()).resolve()
    errors: list[str] = []
    skill_paths = validate_frontmatter(root, errors)
    validate_discovery_links(root, skill_paths, errors)
    validate_readme_index(root, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Repository scaffold is valid.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root(), help=argparse.SUPPRESS)
    args = parser.parse_args()
    return validate_repo(args.root)


if __name__ == "__main__":
    raise SystemExit(main())
