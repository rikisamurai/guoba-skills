#!/usr/bin/env bash
# Time the quick-commit skill end-to-end against eval fixtures.
#
# Speed is quick-commit's #1 priority, so the eval set treats wall-clock as a
# `must` — not just a nice-to-have. This wrapper drives headless Claude
# against each fixture N times and records the mean into the baseline JSON,
# where grade.py's numeric_le check picks it up.
#
# Usage:
#   bash timing.sh [FIXTURE_OR_NAME | all]
#
# Env knobs:
#   MODEL       claude model alias (default: sonnet)
#   TARGET_DIR  fixture sandbox dir   (default: /tmp/quick-commit-eval)
#   RUNS        number of timed runs  (default: 5)
#
# Each run resets the fixture, stages a discovery symlink so headless Claude
# loads THIS repo's SKILL.md (not the user's globally-installed copy), and
# times a fresh `claude -p` invocation from inside the fixture's repo.

set -euo pipefail

EVALS_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$EVALS_DIR/../../../.." && pwd)"
SKILL_CANONICAL="$REPO_ROOT/skills/automation/quick-commit"
EVALS_JSON="$EVALS_DIR/evals.json"
RESULTS_DIR="$EVALS_DIR/baseline-results"
SETUP_SH="$EVALS_DIR/fixtures/setup.sh"

TARGET_DIR="${TARGET_DIR:-/tmp/quick-commit-eval}"
MODEL="${MODEL:-sonnet}"
RUNS="${RUNS:-5}"

WHICH="${1:-all}"

if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found on PATH" >&2
  exit 1
fi

TRIPLES=()
while IFS= read -r line; do
  TRIPLES+=("$line")
done < <(python3 - "$EVALS_JSON" <<'PY'
import json, sys
with open(sys.argv[1]) as f:
    doc = json.load(f)
for e in doc["evals"]:
    print(f'{e["fixture"]}\t{e["name"]}\t{e["prompt"]}')
PY
)

time_one_invocation() {
  # $1 fixture_repo  $2 prompt
  python3 - "$1" "$2" "$MODEL" <<'PY'
import subprocess, sys, time
fixture_repo, prompt, model = sys.argv[1], sys.argv[2], sys.argv[3]
t0 = time.monotonic()
subprocess.run(
    [
        "claude", "-p",
        "--dangerously-skip-permissions",
        "--no-session-persistence",
        "--setting-sources", "project",
        "--model", model,
        prompt,
    ],
    cwd=fixture_repo,
    check=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
t1 = time.monotonic()
print(f"{t1 - t0:.3f}")
PY
}

run_one_fixture() {
  local fixture="$1" name="$2" prompt="$3"
  local fixture_repo="$TARGET_DIR/$fixture/repo"
  local result_path="$RESULTS_DIR/$name.json"

  if [[ ! -f "$result_path" ]]; then
    echo "result file missing for eval '$name': $result_path" >&2
    exit 1
  fi

  echo ">>> Timing $name (fixture=$fixture, prompt='$prompt', runs=$RUNS, model=$MODEL)"

  local samples=()
  for i in $(seq 1 "$RUNS"); do
    bash "$SETUP_SH" "$TARGET_DIR" >/dev/null
    mkdir -p "$fixture_repo/.claude/skills"
    ln -sfn "$SKILL_CANONICAL" "$fixture_repo/.claude/skills/quick-commit"

    local elapsed
    elapsed="$(time_one_invocation "$fixture_repo" "$prompt")"
    echo "  run $i: ${elapsed}s"
    samples+=("$elapsed")
  done

  python3 - "$result_path" "${samples[@]}" <<'PY'
import json, sys
result_path = sys.argv[1]
samples = [float(x) for x in sys.argv[2:]]
mean = round(sum(samples) / len(samples), 3)
samples_rounded = [round(s, 3) for s in samples]
with open(result_path) as f:
    doc = json.load(f)
doc["wall_clock_seconds_avg5"] = mean
doc["wall_clock_samples"] = samples_rounded
with open(result_path, "w") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"  -> {result_path}: avg5={mean}s, samples={samples_rounded}")
PY
}

matched=0
for triple in "${TRIPLES[@]}"; do
  IFS=$'\t' read -r fixture name prompt <<< "$triple"
  if [[ "$WHICH" == "all" || "$WHICH" == "$name" || "$WHICH" == "$fixture" ]]; then
    run_one_fixture "$fixture" "$name" "$prompt"
    matched=1
  fi
done

if [[ "$matched" == 0 ]]; then
  echo "No eval matching '$WHICH'" >&2
  exit 1
fi
