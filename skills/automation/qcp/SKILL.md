---
name: qcp
description: >
  One-shot commit and push, same turn, no preview or authorization. Manual
  only: Claude `/qcp`, Codex `$qcp`.
disable-model-invocation: true
metadata:
  author: riki
  version: "0.2.0"
---

# QCP

Stage everything, write `<type>: <subject>`, commit with `--no-verify`, then
push with `--no-verify`. Same turn. No preview, no confirmation, no scope, no
body.

## Why no authorization

Typing `qcp` *is* the authorization for both the commit and the push. The user
picked this skill to skip the round-trip. Use the local git state and recent
commit language to make the best commit, then push immediately.

## Skip when

- User wants to draft/review the message -> use the plain commit workflow.
- User wants to split the working tree across multiple commits.
- Mid rebase/merge/cherry-pick, or detached HEAD -> bail and surface state.
- No push target can be inferred: no upstream and no `origin` remote.

## Workflow (single turn)

### 1. Snapshot (one bash batch)

```bash
git status --short --branch
git log -n 5 --pretty=format:'%h %s'
```

The log line is critical: mirror its language and casing. Skip `git diff`
unless `git status` is too vague to pick a type. Speed first.

### 2. Stage

```bash
git add -A
```

No allow/deny list, no per-file judgment, no secret scan. The user is
responsible for `.gitignore`. If they wanted curation, they would not have
typed `qcp`.

### 3. Commit if needed

If the working tree has staged or unstaged changes after the snapshot, commit
them. If the tree is clean, skip commit and proceed to push only if the branch
is ahead of its upstream.

Pick one type: `feat fix refactor chore docs test style perf build ci revert`.
Pick the dominant intent. No scope. No body.

Subject rules:

- Imperative, <=72 chars, no trailing period.
- Concrete, not "update files" or "various changes".
- Match the language of the last 5 commits: English vs Chinese, never switch
  mid-history.

```bash
git commit --no-verify -m "feat: support trailing commas in object literals"
```

Always `--no-verify`. Never `--amend`.

### 4. Push immediately

If an upstream exists:

```bash
GIT_TERMINAL_PROMPT=0 git push --no-verify
```

If no upstream exists but `origin` exists:

```bash
GIT_TERMINAL_PROMPT=0 git push --no-verify -u origin HEAD
```

Do not ask before pushing. Do not pull, rebase, merge, or force-push. If push
is rejected or credentials are missing, surface the exact failure and stop.

### 5. Report

Concise: short hash + the message + push destination if available. Use a fenced
block for the commit message. Do not narrate.

## Edge cases (the only legit pauses)

- **Working tree clean and nothing ahead** -> say so, do nothing.
- **Working tree clean but branch ahead** -> push only.
- **Only untracked files** -> still `git add -A`, commit, and push. Only bail
  if the user explicitly said "don't commit untracked".
- **Rebase/merge/cherry-pick in progress** -> bail, surface state.
- **Detached HEAD** -> bail.
- **No upstream and no `origin` remote** -> bail, surface state.
- **Push rejected or auth unavailable** -> stop; never force-push or repair
  history automatically.

## Quality bar

- [ ] You ran `git push` this turn when there was a commit to push or the
      branch was already ahead.
- [ ] Used `git add -A`, `git commit --no-verify`, and `git push --no-verify`.
- [ ] Message is `<type>: <subject>`: no scope, no body.
- [ ] Type matches what the diff did, no `chore:` for a bugfix.
- [ ] Subject reads natural, not "update files" or "various changes".
- [ ] Language matches recent log.
- [ ] No `--amend`, no pull/rebase/merge, no force-push.
