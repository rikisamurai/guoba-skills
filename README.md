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

A skill folder holds one `SKILL.md` plus optional `scripts/`, `references/`, `assets/`,
and an optional `agents/openai.yaml` for Codex-only settings (display name, invocation
policy). Claude-only settings live in the `SKILL.md` frontmatter itself:

```text
skills/automation/deploy/
  SKILL.md            # name, description, workflow + Claude frontmatter fields
  agents/openai.yaml  # Codex interface + policy
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

Create a manual-trigger skill (Claude `/name` or Codex `$name` only, never auto-invoked):

```bash
python3 scripts/new_skill.py deploy --domain automation --description "Deploy the app" --manual
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

- [clean-worktree](skills/automation/clean-worktree/) - Clean up the current completed task worktree and local branch, then return to the updated main branch. Manual only: Claude /clean-worktree, Codex $clean-worktree.
- [gb-handoff](skills/automation/gb-handoff/) - Produce a self-contained handoff prompt for another agent (Codex, a fresh Claude session, a teammate) when the user wants to delegate continued work. Triggers on: "写一个 prompt 给 codex"、"交接一下"、"让 xxx 跟进"、"summary 一下再写个 prompt"、"handoff to another agent"、"write a prompt so X can continue", or any request to capture the current session state for continuation elsewhere.
- [gb-neat](skills/automation/gb-neat/) - Use when explicitly invoked as `/gb-neat` or `/neat`, or when the user clearly asks to sync project docs or agent memory. Do not use for ordinary summaries, handoffs, wrap-up, or generic tidy-up requests.
- [locate-frontend-code](skills/automation/locate-frontend-code/) - 探索某个前端功能的代码,产出一份「功能地图」(结构树 + 速查表 + 数据流), 帮你快速了解它的代码位置和结构。手动触发:Claude `/locate-frontend-code`, Codex `$locate-frontend-code`。
- [qcp](skills/automation/qcp/) - One-shot commit and push, same turn, no preview or authorization. Manual only: Claude `/qcp`, Codex `$qcp`.
- [quick-commit](skills/automation/quick-commit/) - One-shot commit, same turn, no preview. Manual only: Claude `/quick-commit`, Codex `$quick-commit`.

### content

- [gb-ai-hot](skills/content/gb-ai-hot/) - Use when the user asks for current AI news, AI HOT, AI daily reports, model/product launches, AI papers, or recent OpenAI/Anthropic/Google updates. 中文触发语同样适用："AI 日报"、"今天 AI 圈有什么"、"过去 24 小时 大新闻"、"最近的模型发布"、"最近的 AI 论文"、"OpenAI/Anthropic 最近有 什么动态"。

### research

- [gb-grill-me](skills/research/gb-grill-me/) - Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
<!-- skills-index:end -->
