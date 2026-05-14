#!/usr/bin/env bash
# Build the two sandbox git repos used by quick-commit's eval set.
#
# Usage:
#   bash setup.sh [TARGET_DIR]
#
# TARGET_DIR defaults to ./_sandbox (relative to cwd). Each fixture lives at
# TARGET_DIR/<fixture-name>/repo/. The script wipes any existing fixture dir
# under TARGET_DIR before recreating it, so reruns are idempotent.

set -euo pipefail

TARGET_DIR="${1:-./_sandbox}"
TARGET_DIR="$(cd "$(dirname "$TARGET_DIR")" && pwd)/$(basename "$TARGET_DIR")"

mkdir -p "$TARGET_DIR"

git_init_repo() {
  local dir="$1"
  rm -rf "$dir"
  mkdir -p "$dir"
  git -C "$dir" init -q -b main
  git -C "$dir" config user.email "eval@local"
  git -C "$dir" config user.name "Quick-Commit Eval"
}

# ---------------------------------------------------------------------------
# eval-1-feat-simple
#   English Conventional Commits log; one tracked file modification adding
#   trailing-comma support and a new exported function.
# ---------------------------------------------------------------------------
F1="$TARGET_DIR/eval-1-feat-simple/repo"
git_init_repo "$F1"
mkdir -p "$F1/src"
cat > "$F1/src/parser.ts" <<'EOF'
export function parse(input: string): Record<string, unknown> {
  return JSON.parse(input);
}
EOF
git -C "$F1" add -A
git -C "$F1" commit -q -m "feat(parser): initial JSON parser"
git -C "$F1" commit -q --allow-empty -m "chore: scaffold repo"
git -C "$F1" commit -q --allow-empty -m "docs: add README"
git -C "$F1" commit -q --allow-empty -m "test(parser): cover empty input"
git -C "$F1" commit -q --allow-empty -m "refactor(parser): extract helper"
cat > "$F1/src/parser.ts" <<'EOF'
export function parse(input: string): Record<string, unknown> {
  const cleaned = input.replace(/,(\s*[}\]])/g, '$1');
  return JSON.parse(cleaned);
}

export function parseArray(input: string): unknown[] {
  const cleaned = input.replace(/,(\s*[\]])/g, '$1');
  return JSON.parse(cleaned);
}
EOF

# ---------------------------------------------------------------------------
# eval-2-fix-chinese
#   Chinese Conventional Commits log; one tracked file modification that
#   adds a None guard preventing a null-pointer attribute access.
# ---------------------------------------------------------------------------
F2="$TARGET_DIR/eval-2-fix-chinese/repo"
git_init_repo "$F2"
cat > "$F2/auth.py" <<'EOF'
def get_user_name(user):
    return user.profile.name
EOF
git -C "$F2" add -A
git -C "$F2" commit -q -m "feat(auth): 增加用户名读取"
git -C "$F2" commit -q --allow-empty -m "chore: 初始化项目脚手架"
git -C "$F2" commit -q --allow-empty -m "docs: 补充 README 安装步骤"
git -C "$F2" commit -q --allow-empty -m "refactor(auth): 拆分 profile 模块"
git -C "$F2" commit -q --allow-empty -m "test(auth): 覆盖匿名用户场景"
cat > "$F2/auth.py" <<'EOF'
def get_user_name(user):
    if user is None or user.profile is None:
        return None
    return user.profile.name
EOF

echo "Fixtures ready under: $TARGET_DIR"
for f in eval-1-feat-simple eval-2-fix-chinese; do
  echo "  $f:"
  git -C "$TARGET_DIR/$f/repo" status --short | sed 's/^/    /'
done
