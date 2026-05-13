# Guoba Skills

Personal Agent Skills repository scaffold.

Canonical skill sources live under `skills/<domain>/<skill-name>/`. Agent discovery
directories expose flat symlinks back to those canonical folders:

- `.agents/skills` for Codex and other Agent Skills compatible tools.
- `.claude/skills` for Claude-compatible discovery.

This repository starts with structure, templates, and maintenance scripts only. Real
skills can be added with `scripts/new_skill.py`.

## Layout

```text
skills/
  automation/
  content/
  infrastructure/
  research/
  writing/
templates/
scripts/
.agents/skills/
.claude/skills/
```

## Install

Install all skills into your local agent (Claude Code, Codex, or any [Agent Skills](https://skills.sh)-compatible agent):

```bash
# from GitHub
npx skills add rikisamurai/guoba-skills

# or from a local clone
npx skills add /path/to/guoba-skills
```

Discovery layout: `.claude/skills/` for Claude Code, `.agents/skills/` for Codex.

## Usage

Create a skill:

```bash
python3 scripts/new_skill.py example-skill --domain automation --description "Example trigger text"
```

Create a skill with reference guidance and resource folders:

```bash
python3 scripts/new_skill.py research-helper --domain research --description "Use for repeatable research workflows" --with-references --resources scripts,references,assets
```

Refresh the generated index:

```bash
python3 scripts/refresh_index.py
```

Validate the repository:

```bash
python3 scripts/validate_repo.py
```

## Skills Index

<!-- skills-index:start -->
### automation

- [gb-handoff](skills/automation/gb-handoff/) - Produce a self-contained handoff prompt for another agent (Codex, a fresh Claude session, a teammate) when the user wants to delegate continued work. Triggers on: "写一个 prompt 给 codex"、"交接一下"、"让 xxx 跟进"、"summary 一下再写个 prompt"、"handoff to another agent"、"write a prompt so X can continue", or any request to capture the current session state for continuation elsewhere.
- [quick-commit](skills/automation/quick-commit/) - Stage tracked changes and create a Conventional Commits commit in one shot — no message-drafting back-and-forth, no confirmation prompts. Trigger on: "quick commit"、"qc"、"快速提交"、"提个 commit"、"commit 一下"、"帮我 commit"、"提交一下"、"ship it"、"commit & push (without push)", or any short request to capture current changes as a single commit. Skip when the user wants to (a) review/edit the message before committing, (b) only stage files, or (c) split the changes across multiple commits.

### research

- [gb-grill-me](skills/research/gb-grill-me/) - Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
<!-- skills-index:end -->
