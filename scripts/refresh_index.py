#!/usr/bin/env python3
"""Refresh the generated skills index in README.md."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path


START_MARKER = "<!-- skills-index:start -->"
END_MARKER = "<!-- skills-index:end -->"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    lines = parts[1].splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in {">", "|"}:
            block_lines: list[str] = []
            while index < len(lines):
                next_line = lines[index]
                if next_line and not next_line.startswith((" ", "\t")):
                    break
                block_lines.append(next_line.strip())
                index += 1
            if value == ">":
                data[key] = " ".join(part for part in block_lines if part).strip()
            else:
                data[key] = "\n".join(block_lines).strip()
            continue
        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {'"', "'"}
        ):
            value = value[1:-1]
        data[key] = value
    return data


def iter_skills(root: Path) -> list[dict[str, str]]:
    skills: list[dict[str, str]] = []
    for skill_md in sorted((root / "skills").glob("*/*/SKILL.md")):
        skill_dir = skill_md.parent
        domain = skill_dir.parent.name
        name = skill_dir.name
        frontmatter = parse_frontmatter(skill_md)
        skills.append(
            {
                "domain": domain,
                "name": frontmatter.get("name", name),
                "folder_name": name,
                "description": frontmatter.get("description", ""),
                "path": skill_dir.relative_to(root).as_posix(),
            }
        )
    return skills


def build_index(root: Path) -> str:
    skills = iter_skills(root)
    if not skills:
        return "_No skills yet._\n"

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for skill in skills:
        grouped[skill["domain"]].append(skill)

    lines: list[str] = []
    for domain in sorted(grouped):
        lines.append(f"### {domain}")
        lines.append("")
        for skill in sorted(grouped[domain], key=lambda item: item["name"]):
            description = skill["description"] or "No description provided."
            lines.append(
                f"- [{skill['name']}]({skill['path']}/) - {description}"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def replace_index(readme_text: str, index_text: str) -> str:
    block = f"{START_MARKER}\n{index_text.rstrip()}\n{END_MARKER}"
    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        return readme_text.rstrip() + "\n\n## Skills Index\n\n" + block + "\n"

    start = readme_text.index(START_MARKER)
    end = readme_text.index(END_MARKER, start) + len(END_MARKER)
    return readme_text[:start] + block + readme_text[end:]


def refresh_index(root: Path | None = None) -> str:
    root = (root or repo_root()).resolve()
    readme = root / "README.md"
    original = readme.read_text(encoding="utf-8") if readme.exists() else ""
    updated = replace_index(original, build_index(root))
    readme.write_text(updated, encoding="utf-8")
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root(), help=argparse.SUPPRESS)
    args = parser.parse_args()
    refresh_index(args.root)
    print("README.md skills index refreshed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
