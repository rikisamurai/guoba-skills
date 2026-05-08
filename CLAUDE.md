# Claude Notes

Claude-compatible skills are exposed through `.claude/skills` as symlinks to the
canonical folders under `skills/`.

Do not edit discovery symlinks directly. Edit the canonical skill folder, then run
`python3 scripts/validate_repo.py`.
