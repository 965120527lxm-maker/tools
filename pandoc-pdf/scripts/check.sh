#!/usr/bin/env bash
# Verify pandoc / xelatex / fonts / deployed templates.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="${PANDOC_DATA_DIR:-${HOME}/.local/share/pandoc}"
ok=0

check() {
  local label="$1"; shift
  if "$@"; then
    echo "OK  ${label}"
  else
    echo "FAIL ${label}" >&2
    ok=1
  fi
}

check "pandoc on PATH" bash -c 'command -v pandoc >/dev/null'
check "xelatex on PATH" bash -c 'command -v xelatex >/dev/null'
check "defaults in repo" test -f "${ROOT}/defaults/academic/default.yaml"
check "defaults deployed" test -f "${DATA_DIR}/defaults/academic/default.yaml"

if command -v fc-list >/dev/null; then
  check "Noto Serif CJK SC" bash -c 'fc-list "Noto Serif CJK SC" | grep -q .'
fi

# Smoke: markdown → latex with defaults (no full PDF if engine broken)
tmp="$(mktemp -d)"
trap 'rm -rf "${tmp}"' EXIT
printf '# Smoke 中文\n\nHello.\n' > "${tmp}/t.md"
if pandoc "${tmp}/t.md" -t latex --data-dir="${ROOT}" --defaults=academic/default -o "${tmp}/t.tex" 2>"${tmp}/err"; then
  echo "OK  defaults→latex smoke"
else
  echo "FAIL defaults→latex smoke" >&2
  cat "${tmp}/err" >&2
  ok=1
fi

exit "${ok}"
