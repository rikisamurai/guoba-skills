---
name: quick-commit
description: >
  One-shot commit, same turn, no preview. Trigger ONLY on: `qc`,
  `quick commit`, `快速 commit`, `快速提交`.
metadata:
  author: riki
  version: "0.4.0"
---

# Quick Commit

Stage everything, write `<type>: <subject>`, commit with `--no-verify`. Same
turn. No preview, no confirmation, no scope, no body.

## Why no confirmation

Typing `qc` *is* the confirmation — the user picked this skill to skip the
round-trip. `git commit` is reversible (`git reset HEAD~1`, `--amend`,
`reflog`), so it doesn't trigger the default "ask before hard-to-reverse
actions" rule. Confirmation here is friction, not safety. Speed wins.

## Skip when

- User wants to draft/review the message → use the plain commit workflow.
- User wants to split the working tree across multiple commits.
- Mid rebase/merge/cherry-pick, or detached HEAD → bail and surface state.

## Workflow (single turn)

### 1. Snapshot (one bash batch)

```bash
git status --short
git log -n 5 --pretty=format:'%h %s'
```

The log line is critical — you'll mirror its language and casing. Skip
`git diff` unless `git status` is too vague to pick a type. Speed first.

### 2. Stage

```bash
git add -A
```

No allow/deny list, no per-file judgment, no secret scan. The user is
responsible for `.gitignore`. If they wanted curation, they wouldn't have
typed `qc`.

### 3. Pick a type

One of: `feat fix refactor chore docs test style perf build ci revert`.
Pick the dominant intent. No scope. No body.

### 4. Write the subject

- Imperative, ≤72 chars, no trailing period.
- Concrete — not "update files" / "various changes".
- **Match the language of the last 5 commits** (English vs Chinese — never
  switch mid-history).

### 5. Commit immediately

```bash
git commit --no-verify -m "feat: support trailing commas in object literals"
```

Always `--no-verify`. Never `--amend`.

### 6. Report

Concise: short hash + the message in a fenced block. Don't narrate.

## Edge cases (the only legit pauses)

- **Working tree clean** → say so, do nothing.
- **Only untracked files** → still `git add -A` and commit. Only bail if the
  user explicitly said "don't commit untracked".
- **Rebase/merge/cherry-pick in progress** → bail, surface state.
- **Detached HEAD** → bail.

## Quality bar

- [ ] You ran `git commit` this turn — no preview-then-wait.
- [ ] Used `git add -A` and `--no-verify`.
- [ ] Message is `<type>: <subject>` — no scope, no body.
- [ ] Type matches what the diff did (no `chore:` for a bugfix).
- [ ] Subject reads natural, not "update files" / "various changes".
- [ ] Language matches recent log.
- [ ] No `--amend`.
