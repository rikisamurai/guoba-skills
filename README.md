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

- [session-handoff](skills/automation/session-handoff/) - Produce a self-contained handoff prompt for another agent (Codex, a fresh Claude session, a teammate) when the user wants to delegate continued work. Triggers on: "写一个 prompt 给 codex"、"交接一下"、"让 xxx 跟进"、"summary 一下再写个 prompt"、"handoff to another agent"、"write a prompt so X can continue", or any request to capture the current session state for continuation elsewhere.

### infrastructure

- [ci-smoke-needs-real-deps](skills/infrastructure/ci-smoke-needs-real-deps/) - Use when a CI release/build pipeline runs a smoke test that boots the project's bundled binary against an external dependency stack (PostgreSQL, MySQL, Redis, MongoDB, S3, etc.) and the test fails with connection refused, missing-required-env, or migration errors. The fix is to declare the dep as a CI service container AND inject the matching env vars on the smoke step. Common after a stack migration leaves the release workflow out of sync with the new ci.yml/code reality.

### research

- [chat-export-report](skills/research/chat-export-report/) - Use when user provides exported chat history (WeChat / Telegram / iMessage / QQ exports as .md / .txt / .json) and asks "我和 X 聊了啥"、"看完整个 md"、"细说 XX"、"是不是有 Y"、"what did I and X talk about", wants topical breakdown, requests detail on specific themes (relationships / work / health / events), or seeks honest interpretation of conversation dynamics. Triggers on large chat dumps (>1000 lines) where direct full read is impractical.

### writing

- [generate-design-md](skills/writing/generate-design-md/) - Generate a DESIGN.md file for any brand or website by analyzing its visual design system. Use when the user asks to "generate a DESIGN.md for [brand/URL]", "create a design system doc for [site]", "extract the design tokens from [URL]", or "make a DESIGN.md like [brand]". Triggers on any request to document a website's design language in DESIGN.md format.
- [holding-analytical-judgment](skills/writing/holding-analytical-judgment/) - Use when delivering analysis, assessment, or diagnosis to the person whose work/behavior/decisions are being analyzed, and they push back emotionally, contradict conclusions, or express discomfort — prevents flipping the conclusion to match their mood while staying open to new factual evidence. Covers code review, architecture review, performance diagnosis, root-cause analysis, decision post-mortems, behavior/relationship analysis — any task where the reader is the subject.
<!-- skills-index:end -->
