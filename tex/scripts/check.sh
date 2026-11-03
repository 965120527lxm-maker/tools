#!/usr/bin/env bash
# Verify TeX engine, fonts, and lxm-academic.sty.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export TEXMFHOME="${TEXMFHOME:-${HOME}/texmf}"
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

check "xelatex" bash -c 'command -v xelatex >/dev/null'
check "latexmk" bash -c 'command -v latexmk >/dev/null'
check "kpsewhich" bash -c 'command -v kpsewhich >/dev/null'
check "beamer.cls" bash -c '[[ -n "$(kpsewhich beamer.cls)" ]]'
check "lxm-academic.sty" bash -c '[[ -n "$(kpsewhich lxm-academic.sty)" ]]'
check "Noto Serif CJK SC" bash -c 'fc-list "Noto Serif CJK SC" | grep -q .'

tmp="$(mktemp -d)"
trap 'rm -rf "${tmp}"' EXIT
cp "${ROOT}/examples/hello-academic.tex" "${tmp}/"
if (
  cd "${tmp}"
  latexmk -xelatex -interaction=nonstopmode -halt-on-error hello-academic.tex \
    >"${tmp}/build.log" 2>&1
); then
  echo "OK  xelatex sample → $(ls "${tmp}"/hello-academic.pdf 2>/dev/null)"
else
  echo "FAIL xelatex sample (see log)" >&2
  tail -n 40 "${tmp}/build.log" >&2 || true
  ok=1
fi

exit "${ok}"
