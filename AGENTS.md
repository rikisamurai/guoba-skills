# Agent Instructions

This repository stores reusable Agent Skills.

- Keep canonical skills in `skills/<domain>/<skill-name>/`.
- Keep discovery directories flat and symlinked to canonical skill folders.
- Use lowercase kebab-case skill names.
- Every skill must include `SKILL.md` with `name` and `description` frontmatter.
- Refresh `README.md` with `python3 scripts/refresh_index.py` after skill changes.
- Run `python3 scripts/validate_repo.py` before committing.
