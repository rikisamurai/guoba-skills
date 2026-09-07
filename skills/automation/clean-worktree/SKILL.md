---
name: clean-worktree
description: "Clean up the current completed task worktree and local branch, then return to the updated main branch. Manual only: Claude /clean-worktree, Codex $clean-worktree."
disable-model-invocation: true
---

# Clean Worktree

Clean only the current task's linked worktree and local branch after proving its
commits were merged. Explicit invocation authorizes this workflow; do not add a
confirmation round-trip when all checks pass. Stop on ambiguity or a failed check.

## 1. Identify and preflight

- Read `git rev-parse --show-toplevel`, `git symbolic-ref --quiet --short HEAD`,
  `git rev-parse HEAD`, `git rev-parse --path-format=absolute --git-common-dir`,
  and `git worktree list --porcelain`. Record the exact task path, branch, and SHA.
  Identify the main working directory from Git metadata and the worktree list;
  do not infer identity from directory names. Stop for a bare repository, detached
  HEAD, or invocation from the main working directory.
- Resolve the remote from the repository's configured upstreams and the remote
  default branch using `git ls-remote --symref <remote> HEAD`. Do not assume
  `origin` or `main`. Stop if the intended remote, default branch, or corresponding
  local main branch cannot be resolved unambiguously, or the task is on that branch.
- Inspect both worktrees with
  `git status --porcelain=v1 --untracked-files=all --ignore-submodules=none`,
  including submodule changes. Stop for any staged, unstaged, or untracked content.
  Check worktree-specific Git paths for `MERGE_HEAD`, `CHERRY_PICK_HEAD`,
  `REVERT_HEAD`, `rebase-merge`, `rebase-apply`, and `sequencer`; stop if any exist.
  Stop if either worktree is locked or prunable, or the main branch is checked out
  in a worktree other than the main working directory.

Use quoted absolute paths and exact refs in subsequent commands. Never use
`reset --hard`, `clean`, automatic stash, forced worktree removal, or `rm -rf`.
Never delete the main working directory, remote branches, or other task worktrees.

## 2. Prove completion against the latest main branch

Fetch the resolved remote main branch explicitly into its remote-tracking ref
(`git fetch <remote> refs/heads/<main>:refs/remotes/<remote>/<main>`). Stop if fetch
fails. Record the fetched SHA; all checks below refer to this fresh state.

- Normal merge: require `git merge-base --is-ancestor <task-sha> <fetched-main-sha>`.
- If ancestry fails, inspect the corresponding PR/CR merge record using an
  available connector or CLI. Require a merged status, the exact repository and
  target branch, the source SHA matching the current task SHA, and the resulting
  merge/squash/rebased commit present in fetched main's history. A closed request,
  matching title, similar diff, or a merged older revision is insufficient.
- If that record is unavailable or cannot prove the current task was merged,
  stop and report the missing evidence. Do not infer completion from invocation.

Require the local main tip to be an ancestor of fetched main as well. Local-only
commits or divergence block cleanup; do not merge, rebase, or push to resolve them.

## 3. Return to main and update before deleting

Move command execution to the retained main working directory before removing
anything. Use an explicit shell working directory or `git -C` for every subsequent
command; a `cd` in one tool call may not persist into another. If the runtime cannot
run outside the task directory, stop before deletion and explain the limitation.

From the main working directory, switch to the resolved local main branch and run
`git merge --ff-only <fetched-main-sha>`. Check each exit status separately. Require
HEAD to equal the fetched SHA and the directory to remain clean. An update failure
must leave the task worktree and branch intact.

## 4. Remove only the verified task

Immediately before deletion, recheck task path registration, branch, SHA,
cleanliness, in-progress operations, and worktree locks against the snapshot.
Stop if anything changed. Ensure no other worktree checks out the task branch.

From the retained directory:

1. Run `git worktree remove -- <absolute-task-path>` without force. If it fails
   (including refusal due to ignored files or submodules), stop and retain the branch.
2. Recheck that the local task branch still points to the verified SHA and is not
   checked out elsewhere, then run `git branch -d -- <task-branch>`.
3. If ordinary deletion fails specifically because Git cannot recognize the
   verified squash/rebase merge, recheck the same branch SHA and worktree occupancy
   and use `git branch -D -- <task-branch>`. This exception requires the merge-record
   evidence from step 2; never force-delete for a different error or uncertain state.

Do not automatically commit, merge the task, push, delete remote branches, prune
unrelated worktrees, or archive the agent task. Stop on partial failure; do not
recreate a removed worktree or broaden the cleanup to recover automatically.

## 5. Verify and report

Verify that the task path is absent from both disk and `git worktree list`, the local
task branch no longer exists, and the retained directory is clean on the resolved
main branch at the fetched SHA. Report the removed path and local branch, retained
directory, and main SHA. “Latest” means the remote state fetched during this run.

On failure, report the failed step, what already changed, and what remains. For
example, if branch deletion fails after worktree removal, say the directory was
removed but the branch remains. Do not claim the Claude/Codex session or app
workspace moved: only Git state and subsequent command execution changed.
