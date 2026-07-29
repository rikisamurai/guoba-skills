#!/usr/bin/env bash
# aihot.sh — aihot.virxact.com API 的 curl 包装。
# 自动附加浏览器 UA（/api/public/* 有 UA 黑名单，默认 curl UA 会被 403），
# 非 2xx 时把 HTTP 状态码和响应体打到 stderr 并以非零退出。
# 网络层失败（DNS / 连接 / 超时）由 curl 自己把原因打到 stderr。
#
# 用法: aihot.sh '/api/public/items?mode=selected&take=50'
set -euo pipefail

BASE="https://aihot.virxact.com"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

path="${1:?usage: aihot.sh '/api/public/...'}"

body=$(mktemp)
trap 'rm -f "$body"' EXIT

status=$(curl -sS --max-time 30 -o "$body" -w '%{http_code}' -H "User-Agent: $UA" "$BASE$path")

if [ "$status" -ge 200 ] && [ "$status" -lt 300 ]; then
  cat "$body"
else
  echo "HTTP $status from $BASE$path" >&2
  cat "$body" >&2
  exit 1
fi
