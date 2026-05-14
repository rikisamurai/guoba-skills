# quick-commit · evals

Lightweight regression set for the `quick-commit` skill. Two sandbox repos,
two short prompts, deterministic pass criteria.

## Files

- `evals.json` — canonical eval definitions: prompts, scenarios, and typed
  assertions (`must` = hard requirement, `should` = graded, `qualitative` =
  human review). Includes a `check_types` registry and `result_schema` so any
  grader can produce a result file the assertions can run against.
- `grade.py` — runs every assertion in `evals.json` against
  `baseline-results/<eval-name>.json` and prints PASS / FAIL / MANUAL per
  check, plus an overall score. Exit code 0 when every `must` passes.
- `fixtures/setup.sh` — recreates the two sandbox git repos from scratch.
  Idempotent — wipes and rebuilds each fixture on every run.
- `timing.sh` — drives headless Claude against each fixture N times,
  records the mean wall-clock into the baseline JSON. Speed is
  quick-commit's #1 priority, so wall-clock is graded as `must`.
- `baseline-results/` — frozen snapshots of subagent runs from the iteration
  that shipped the v0.1.0 skill, kept as a "this is what passing looks like"
  reference. Not a contract — re-runs may legitimately produce different
  wording as long as `evals.json` `must` rules hold.

## Scoring model

- A single `must` failure means the eval failed. All evals must pass for the
  overall run to pass.
- `should` items don't block; the grader reports `passed/total` for nuance
  and to flag drift over time.
- `qualitative` checks (e.g. "subject is concrete, not generic") aren't
  amenable to regex and surface as `MANUAL` — eyeball them.

The numeric "score" is intentionally just `must_passed / must_total` and
`should_passed / should_total` — no weighted aggregate. Quick-commit has a
narrow surface; if you're tempted to write a single overall percentage,
that's a signal to add more evals instead.

## How to run

### 1. Build the fixtures

```bash
cd skills/automation/quick-commit/evals
bash fixtures/setup.sh /tmp/quick-commit-eval
```

This produces `/tmp/quick-commit-eval/<fixture-name>/repo/` for each of the
two evals. Each repo has the right git log and the right dirty state.

### 2. Run the skill against each fixture

For each eval in `evals.json`, dispatch a fresh agent with:

- The skill loaded (read `../SKILL.md`).
- `cwd` (or `git -C`) pointing at the fixture's `repo/` directory.
- The `prompt` field as the literal user message.

The reference subagent prompt template lives in any iteration's transcript;
the gist is: "read the skill, follow it, commit to this repo, then write a
JSON report to outputs/result.json".

### 3. Grade the results

Save each subagent's `result.json` as
`<some-results-dir>/<eval-name>.json` (filename matches the `name` field in
`evals.json`, e.g. `feat-simple.json`). Then:

```bash
python3 grade.py --results-dir <some-results-dir>
# defaults to baseline-results/ if --results-dir is omitted
python3 grade.py --json > grades.json   # machine-readable
```

Output looks like:

```
[feat-simple]
  PASS   (must ) type-is-feat        Commit type is feat (no scope).
  PASS   (must ) no-scope            Message has no scope (no `type(scope):` form).
  ...
  --- PASS  must=7/7  should=1/1  manual=1
============================================================
OVERALL: PASS
  must:   14/14
  should: 2/2
  manual: 2  (qualitative — review by hand)
```

Exit code is `0` when every `must` passes across every eval, `1` otherwise.
Wire that into CI when you want it.

### 4. Re-baseline wall-clock (`timing.sh`)

Speed is the whole point of `qc`. `timing.sh` drives `claude -p` headlessly
against each fixture, captures wall-clock per run, and merges the mean into
`baseline-results/<eval>.json` as `wall_clock_seconds_avg5`. The grader's
`numeric_le` check enforces the per-eval ceiling (set in `evals.json` at
~1.4× the measured baseline mean — generous enough for network jitter,
tight enough to break if a regression adds an extra tool round-trip).

```bash
bash timing.sh all                        # both fixtures, 5 runs each
bash timing.sh feat-simple                # one fixture
MODEL=opus RUNS=3 bash timing.sh all      # override model / sample count
```

Defaults: `MODEL=sonnet`, `RUNS=5`, `TARGET_DIR=/tmp/quick-commit-eval`.
The wrapper resets the fixture between runs and stages a discovery
symlink (`<fixture>/.claude/skills/quick-commit -> <repo canonical>`) so
headless Claude resolves *this* repo's `SKILL.md`, not whatever the user
has globally installed.

**Cost / why not in CI.** Each run is one `claude -p` invocation; default
`all` is 10 invocations (5 × 2 fixtures), roughly $0.10–0.50 on Sonnet
and ~3 minutes wall-clock total. Run before shipping a skill change, not
on every push. If you tighten the threshold and CI flaps, raise it rather
than chasing tail-latency noise — you only need to catch *real* slowdowns
(extra tool calls, restored diff reads), not 1-second jitter.

When you change `SKILL.md` in a way that intentionally affects speed,
re-run `timing.sh all`, eyeball the new mean, and update the per-eval
`max` in `evals.json` (and the matching `_threshold_basis` note).

### 5. Compare to baseline

If a run regresses something the baseline got right, that is the signal to
either fix the skill or update the baseline (with a note in the commit
explaining why the change is intentional). The baseline files live under
`baseline-results/` and are graded by `grade.py` with no flags — useful as a
sanity check that the eval definitions themselves still parse.

## Adding a new eval

1. Add a new fixture block to `fixtures/setup.sh` with a comment header
   explaining the scenario.
2. Add a new entry to `evals.json` with `id`, `name`, `fixture`, `prompt`,
   `scenario`, and `assertions[]` — each assertion has `id`, `weight`
   (`must` / `should`), `human` (one-line description for the grader to
   print), and `check` (one of the types in the `check_types` registry, or
   `qualitative` for human review).
3. Run it against the current skill, save the snapshot to
   `baseline-results/<name>.json` (filename = the `name` field).
4. Run `python3 grade.py` — should print PASS for the new eval. Commit.

If you need a check type the grader doesn't yet support, add it to both
`grade.py` (the `run_check` switch) and the `check_types` registry in
`evals.json` so the schema stays self-documenting.

## Why this set is small on purpose

The skill has a narrow surface (stage → message → commit → report), so two
well-chosen scenarios cover the high-value branches:

- happy path with English log and a real new feature (eval-1)
- language switching + correct fix-vs-refactor classification (eval-2)

If the skill grows new behavior (e.g. handling `--amend` requests, multi-file
splits, hooks-failed recovery), add an eval per behavior. Don't bloat for
coverage's sake.
