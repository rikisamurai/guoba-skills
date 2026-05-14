---
name: quick-commit
description: >
  Stage tracked changes and ship a Conventional Commits commit in one shot,
  WITHOUT previewing the message or asking the user to confirm. Invoking
  this skill IS the user's authorization — they don't want a round-trip.
  Trigger ONLY when the request explicitly contains a "quick" signal:
  "qc"、"quick commit"、"quick commit it"、"快速 commit"、"快速提交". Do
  NOT trigger on bare "commit 一下"、"帮我 commit"、"提交一下"、"ship it" or
  any other generic commit phrasing — those leave room for message review,
  use the normal git workflow there. Also skip when the user wants to
  (a) review/edit the message before committing, (b) only stage files, or
  (c) split the changes across multiple commits.
metadata:
  author: riki
  version: "0.2.0"
---

# Quick Commit

One-shot autonomous commit. The user has already decided to commit; your job
is to look at what changed, write a faithful Conventional Commits message in
the repo's existing style, and ship it.

## Contract: pre-authorized, no confirmation

The user typing `qc` (or another trigger phrase from the description above)
**is** the confirmation. They picked this skill specifically because they do
not want to look at the message before it lands. Asking "does this look
good?" / "shall I commit?" / "请确认一下" defeats the entire point — if they
wanted that, they would have asked you to draft a message instead.

Concretely, in the same turn you receive the trigger phrase you must:

- **Not** preview the message back to the user before running `git commit`.
- **Not** ask "is this OK?" / "shall I proceed?" / "可以提交吗".
- **Not** pause after staging to wait for input.
- **Not** present multiple message options for the user to pick from.
- **Not** split the work across turns ("I'll analyze the diff first, then
  commit on your next reply").

Run snapshot → stage → diff → message → `git commit` → report, all in one
turn, with no user-facing message until the report at the end.

A `git commit` is **reversible** (`git reset HEAD~1`, `git commit --amend`,
`git reflog`). It does **not** qualify as a "hard-to-reverse action" under
Claude Code's default confirmation rules. Confirmation here is friction, not
safety.

The only legitimate reasons to stop and talk to the user before the commit
lands are the edge cases listed at the bottom of this file (mid-rebase,
clean tree, likely-secret detected, etc.). If you find yourself drafting a
"just to confirm…" sentence for any other reason, stop and reread this
section.

## When to invoke

- The user's message contains an explicit "quick" signal: `qc`,
  `quick commit`, `quick commit it`, `快速 commit`, `快速提交`.
- The user is clearly handing the commit step off to you because they trust
  the diff is in a committable state.

Do **not** invoke when:

- The user says "draft a commit message" / "想个 commit message" / "提个
  commit"、"commit 一下"、"帮我 commit"、"提交一下"、"ship it" — these are
  generic commit asks where the user may still want to see the message
  first. Use the plain commit workflow there, not this skill.
- The user wants to split the working tree into multiple commits.
- There are merge conflicts, rebase in progress, or detached HEAD — bail out
  and tell the user.
- The user asked to push, tag, or open a PR. This skill only commits;
  mention that follow-ups need a separate request.

## Workflow

Run these steps in order. Steps 1–3 can be parallelized in one tool call.

### 1. Snapshot repo state (parallel)

Run in a single Bash batch:

```bash
git status --short
git diff --stat
git log -n 5 --pretty=format:'%h %s'
```

Inspect the output:

- **`git status --short`** — find tracked modifications (`M`/`MM`), tracked
  deletions (`D`), tracked renames (`R`), and untracked files (`??`).
- **`git diff --stat`** — gauge size and which files dominate the change.
- **`git log -n 5`** — capture the repo's commit message dialect (subject
  case, scope conventions, language). You will mimic it.

### 2. Decide what to stage

Default policy:

- **Stage all tracked modifications/deletions/renames** (`git add -u`).
- **Skip untracked files by default.** Untracked files are the most common
  source of accidental commits (debug scratch, secrets, editor backups).

Stage an untracked file only when **both** are true:

- It is clearly part of the same logical change as the tracked edits (e.g.
  the user just had you create a new module that the tracked edits import
  from).
- It is not a likely-secret or junk path. Always skip:
  - `.env`, `.env.*`, `*.pem`, `*.key`, `*.p12`, `id_rsa*`, `credentials*`,
    `secrets*`, anything under a `secrets/` or `.secret/` directory
  - `node_modules/`, `dist/`, `build/`, `.next/`, `target/`, `__pycache__/`,
    `*.log`, `*.tmp`, `.DS_Store`
  - Anything in `.gitignore` (git already filters these, but double-check)

If you skip something the user might have wanted, mention it in your final
report so they can re-run with explicit instructions.

**Never** use `git add -A` or `git add .` — too easy to sweep in secrets.
Stage by path or use `git add -u` (modifications only).

### 3. Read the actual diff

```bash
git diff --cached
```

You need this to write a faithful message. The `--stat` from step 1 told you
*what files*; the cached diff tells you *what changed*.

If the diff is huge (>500 lines), focus on:

- File-level groupings (which directories / packages changed together)
- Exported API changes (function/type signatures)
- New files and their purpose
- Removed code (often the strongest signal)

### 4. Draft the message

Conventional Commits format:

```
<type>(<scope>): <subject>

<optional body>
```

**Type** — pick the single best fit:

| Type       | Use for                                                     |
|------------|-------------------------------------------------------------|
| `feat`     | new user-visible feature or capability                      |
| `fix`      | bug fix (production behavior was wrong)                     |
| `refactor` | code change that doesn't alter behavior                     |
| `chore`    | tooling, deps, config, repo housekeeping                    |
| `docs`     | documentation only                                          |
| `test`     | tests only (or test fixtures)                               |
| `style`    | whitespace, formatting, semicolons — no logic               |
| `perf`     | performance improvement                                     |
| `build`    | build system, packaging, CI scaffolding                     |
| `ci`       | CI config (`.github/`, pipelines)                           |
| `revert`   | reverts a prior commit                                      |

If a single change touches multiple types, pick the **dominant** one (the
one a reader would most want to see first). Don't invent compound types.

**Scope** — optional but encouraged when there's an obvious one. Look at the
file paths:

- Single package/module touched → use its name (`auth`, `api`, `cli`,
  `parser`).
- Multiple packages but one is dominant → use that one.
- Genuinely cross-cutting → omit the scope.

Match scope casing/style to recent commits in `git log` (lowercase is most
common; some repos use the directory name verbatim).

**Subject** — one line, imperative mood, no trailing period:

- ≤ 72 chars ideally; hard cap 100.
- Imperative ("add", "fix", "rename"), not past tense ("added") or
  gerund ("adding"). Mirrors how git itself phrases its own messages.
- Describe **what changed and why it matters**, not the mechanical action.
  - ✘ `update file foo.ts`
  - ✘ `add 3 lines to parser`
  - ✓ `feat(parser): support trailing commas in object literals`
- **Match the language of recent commits.** If the last 5 commits are
  Chinese, write the subject in Chinese; if mixed/English, use English. Do
  not switch styles mid-history.

**Body** — only include when the subject can't carry the full story:

- Why the change was made (motivation, bug being fixed)
- Non-obvious trade-offs
- Breaking changes → prefix the body with `BREAKING CHANGE:` per spec

For most quick commits, **no body is needed**. Don't pad.

### 5. Commit (immediately, no preview)

Run `git commit` in the same turn. Do **not** show the drafted message to
the user first and wait — re-read the Contract section if you're tempted.

Use a HEREDOC so the message renders correctly even with special chars or
multi-line bodies:

```bash
git commit -m "$(cat <<'EOF'
feat(parser): support trailing commas in object literals
EOF
)"
```

Do **not** pass `--no-verify`. If a pre-commit hook fails, that is the
correct outcome — surface the failure and stop. Do not retry with hooks
disabled, do not amend the previous commit. Tell the user what failed and
let them decide.

After the commit, run `git status` to confirm a clean tree (or note any
intentionally-skipped untracked files).

### 6. Report back

Reply concisely. Include:

- The exact commit message used (one fenced block)
- Files committed (counts are fine if many: `12 files, +203/-87`)
- Anything you intentionally skipped (untracked files, etc.) and why
- The new commit hash (`git log -1 --pretty=format:'%h'`)

Do **not** narrate the workflow steps. The user wanted a quick commit; the
report should be quick too.

## Edge cases

- **Nothing staged after `git add -u`** (only untracked files exist) — tell
  the user: "Working tree only has untracked files; tell me which to stage."
  Don't invent a commit out of thin air.
- **Working tree is clean** — say so, do nothing.
- **Already in the middle of a rebase/merge/cherry-pick** — bail. Detect
  via `git status` ("rebase in progress", "All conflicts fixed: run 'git
  rebase --continue'", etc.).
- **Detached HEAD** — bail. The user almost certainly doesn't want a commit
  they'll lose.
- **Pre-commit hook modifies files** (formatter rewrites, etc.) — the
  commit will fail with the formatter's exit code or succeed with new
  unstaged changes. Surface the resulting state honestly; don't auto-amend.
- **Likely-secret detected in staged diff** (anything matching `AKIA[0-9A-Z]{16}`,
  `-----BEGIN .* PRIVATE KEY-----`, `password\s*=\s*['"][^'"]{8,}`,
  `Bearer [A-Za-z0-9-_]{20,}`) — **stop**, unstage, warn the user. A leaked
  secret is much worse than a delayed commit.

## Quality bar

Before reporting success, check:

- [ ] You actually ran `git commit` this turn — no "let me confirm first"
      pause, no preview-then-wait.
- [ ] The commit message's type matches what the diff actually does (no
      `chore:` for a real bugfix, no `feat:` for a refactor).
- [ ] The subject line reads like a sentence the user would write — not
      "update files" or "various changes".
- [ ] Language and casing match the last 5 commits in `git log`.
- [ ] No `--no-verify`, no `--amend`, no `git add -A`.
- [ ] No secrets in the diff (eyeball-check, plus the regex screen above).

If any answer is "no", fix it before replying.
