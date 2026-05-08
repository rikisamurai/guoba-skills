#!/usr/bin/env python3
"""Create a new canonical skill and discovery symlinks."""

from __future__ import annotations

import argparse
import os
import re
import shutil
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
RESOURCE_DIRS = {"scripts", "references", "assets"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def validate_kebab_case(value: str, label: str) -> None:
    if not NAME_RE.fullmatch(value):
        raise ValueError(f"{label} must be lowercase kebab-case: {value}")


def title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def escape_yaml_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def render_template(template: str, values: dict[str, str]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def parse_resources(resources: str | tuple[str, ...] | list[str] | None) -> tuple[str, ...]:
    if resources is None:
        return ()
    if isinstance(resources, str):
        values = [item.strip() for item in resources.split(",") if item.strip()]
    else:
        values = list(resources)
    unknown = sorted(set(values) - RESOURCE_DIRS)
    if unknown:
        raise ValueError(f"Unknown resource directories: {', '.join(unknown)}")
    return tuple(dict.fromkeys(values))


def planned_paths(
    root: Path,
    skill_dir: Path,
    resource_dirs: tuple[str, ...],
    with_references: bool,
) -> list[Path]:
    paths = [skill_dir / "SKILL.md"]
    for resource in resource_dirs:
        paths.append(skill_dir / resource / ".gitkeep")
    if with_references and "references" not in resource_dirs:
        paths.append(skill_dir / "references/.gitkeep")
    for discovery in DISCOVERY_DIRS:
        paths.append(root / discovery / skill_dir.name)
    return paths


def create_relative_symlink(target: Path, link: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"Would link {link} -> {target}")
        return
    if link.exists() or link.is_symlink():
        if link.is_symlink() and link.resolve() == target.resolve():
            return
        raise FileExistsError(f"Discovery entry already exists: {link}")
    relative = Path(os.path.relpath(target, start=link.parent))
    link.symlink_to(relative, target_is_directory=True)


def cleanup_partial_skill(root: Path, skill_dir: Path) -> None:
    for discovery in DISCOVERY_DIRS:
        link = root / discovery / skill_dir.name
        if link.is_symlink():
            link.unlink()
    if skill_dir.exists():
        shutil.rmtree(skill_dir)


def create_skill(
    *,
    root: Path,
    name: str,
    domain: str,
    description: str,
    with_references: bool = False,
    resources: str | tuple[str, ...] | list[str] | None = None,
    dry_run: bool = False,
) -> Path:
    root = Path(root)
    validate_kebab_case(name, "skill name")
    validate_kebab_case(domain, "domain")
    resource_dirs = parse_resources(resources)

    domain_dir = root / "skills" / domain
    if not domain_dir.is_dir():
        raise FileNotFoundError(f"Unknown domain: {domain}")

    skill_dir = domain_dir / name
    if skill_dir.exists():
        raise FileExistsError(f"Skill already exists: {skill_dir}")

    template_name = (
        "SKILL.with-references.template.md"
        if with_references
        else "SKILL.template.md"
    )
    skill_template = (root / "templates" / template_name).read_text(encoding="utf-8")
    values = {
        "name": name,
        "description": escape_yaml_string(description),
        "title": title_from_name(name),
    }

    if dry_run:
        for path in planned_paths(root, skill_dir, resource_dirs, with_references):
            print(f"Would create {path}")
        return skill_dir

    try:
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            render_template(skill_template, values),
            encoding="utf-8",
        )

        all_resource_dirs = set(resource_dirs)
        if with_references:
            all_resource_dirs.add("references")
        for resource in sorted(all_resource_dirs):
            resource_dir = skill_dir / resource
            resource_dir.mkdir()
            (resource_dir / ".gitkeep").write_text("", encoding="utf-8")

        for discovery in DISCOVERY_DIRS:
            discovery_dir = root / discovery
            discovery_dir.mkdir(parents=True, exist_ok=True)
            create_relative_symlink(skill_dir, discovery_dir / name, dry_run=False)

        refresh_index.refresh_index(root)
    except Exception:
        cleanup_partial_skill(root, skill_dir)
        raise
    return skill_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_name")
    parser.add_argument("--domain", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--with-references", action="store_true")
    parser.add_argument(
        "--resources",
        default="",
        help="Comma-separated optional resource dirs: scripts,references,assets",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--root", type=Path, default=repo_root(), help=argparse.SUPPRESS)
    args = parser.parse_args()

    try:
        skill_dir = create_skill(
            root=args.root,
            name=args.skill_name,
            domain=args.domain,
            description=args.description,
            with_references=args.with_references,
            resources=args.resources,
            dry_run=args.dry_run,
        )
    except (FileExistsError, FileNotFoundError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    action = "Would create" if args.dry_run else "Created"
    print(f"{action} {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
