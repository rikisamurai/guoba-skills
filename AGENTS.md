# Agent Instructions

This repository stores reusable Agent Skills.

- Keep canonical skills in `skills/<domain>/<skill-name>/`.
- Keep discovery directories flat and symlinked to canonical skill folders.
- Use lowercase kebab-case skill names.
- Every skill must include `SKILL.md` with `name` and `description` frontmatter.
- Claude-specific fields go in the `SKILL.md` frontmatter top level (not under
  `metadata:`); Codex-specific fields go in the optional `agents/openai.yaml`.
- A manual-trigger skill must say so on both runtimes:
  `disable-model-invocation: true` in `SKILL.md` and
  `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Configuring only
  one side fails validation.
- Refresh `README.md` with `python3 scripts/refresh_index.py` after skill changes.
- Run `python3 scripts/validate_repo.py` before committing.
