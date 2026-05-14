---
name: quick-commit
description: >
  One-shot Conventional Commits commit — stage, message, commit in the same
  turn, no preview, no "shall I commit?". Trigger ONLY on explicit "quick"
  signals: `qc`, `quick commit`, `快速 commit`, `快速提交`. Skip generic
  asks ("commit 一下", "ship it") — those leave room for review.
metadata:
  author: riki
  version: "0.3.0"
---

# Quick Commit

Stage tracked changes, write a Conventional Commits message in the repo's
existing style, commit. Same turn. No preview, no confirmation.

## Why no confirmation

Typing `qc` *is* the confirmation — the user picked this skill to skip the
round-trip. `git commit` is reversible (`git reset HEAD~1`, `--amend`,
`reflog`), so it doesn't trigger the default "ask before hard-to-reverse
actions" rule. Confirmation here is friction, not safety.

The only legitimate reasons to pause and ask are the Edge cases below
(clean tree, mid-rebase, likely-secret). Anything else: commit, then
report.

## Skip when

- User wants to draft/review the message → use the plain commit workflow.
- Splitting the working tree across multiple commits.
- Mid rebase/merge/cherry-pick, or detached HEAD → bail and surface state.
- User asked to push/tag/open PR → that's a separate request.

## Workflow (single turn)

### 1. Snapshot (one bash batch)

```bash
git status --short
git diff --stat
git log -n 5 --pretty=format:'%h %s'
```

The log line is critical — you'll mirror its language, casing, and scope
style.

### 2. Stage

- `git add -u` for tracked changes.
- For untracked files: stage only when clearly part of the same logical
  change AND not in the skip list.
  - Skip: `.env*`, `*.pem`, `*.key`, `id_rsa*`, `credentials*`, `secrets*`,
    `node_modules/`, `dist/`, `build/`, `.next/`, `__pycache__/`, `*.log`,
    `.DS_Store`.
- Never `git add -A` / `git add .` — too easy to sweep in secrets.
- Mention skipped files in the report.

### 3. Read the diff

```bash
git diff --cached
```

You need this to write a faithful message — `--stat` only tells you which
files. For huge diffs (>500 lines): focus on file groupings, exported API
changes, new files, deletions.

### 4. Draft `<type>(<scope>): <subject>`

- **Type**: pick the dominant intent. `feat` (new capability), `fix` (bug),
  `refactor` (no behavior change), `chore` (tooling/deps), `docs`, `test`,
  `style`, `perf`, `build`, `ci`, `revert`. Don't invent compound types.
- **Scope**: optional, use the touched module name when obvious; omit when
  cross-cutting.
- **Subject**: imperative, ≤72 chars, no trailing period. Concrete, not
  "update files". **Match the language of the last 5 commits** (English vs
  Chinese — never switch mid-history).
- **Body**: only when subject can't carry the story. Most quick commits
  don't need one.

### 5. Commit immediately

Do **not** preview the message to the user first. Same turn, run:

```bash
git commit -m "$(cat <<'EOF'
feat(parser): support trailing commas in object literals
EOF
)"
```

No `--no-verify`. If a hook fails, surface the error and stop — don't
retry without hooks, don't `--amend`.

### 6. Report

Concise: commit hash, message in a fenced block, file count or list,
anything skipped + why. Don't narrate the workflow.

## Edge cases (the only legit pauses)

- **Working tree clean** → say so, do nothing.
- **Only untracked files** → ask which to stage; don't invent a commit.
- **Rebase/merge/cherry-pick in progress** → bail, surface state.
- **Detached HEAD** → bail.
- **Hook modifies files** (formatter) → surface the new state, don't
  auto-amend.
- **Likely-secret in staged diff** (`AKIA[0-9A-Z]{16}`, `BEGIN .* PRIVATE
  KEY`, `password\s*=\s*['"][^'"]{8,}`, `Bearer [A-Za-z0-9-_]{20,}`) →
  unstage, warn, do not commit.

## Quality bar

- [ ] You ran `git commit` this turn — no preview-then-wait.
- [ ] Type matches what the diff does (no `chore:` for a bugfix).
- [ ] Subject reads natural, not "update files" / "various changes".
- [ ] Language matches recent log.
- [ ] No `--no-verify` / `--amend` / `git add -A`.
- [ ] No secrets in the diff.
