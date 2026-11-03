#!/usr/bin/env bash
# Build PDF with academic/default. Uses deployed data-dir, or this repo as data-dir.
#
#   ./scripts/build.sh note.md
#   ./scripts/build.sh note.md out.pdf
#   ./scripts/build.sh note.md out.pdf academic/default
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${1:?usage: build.sh <input.md> [output.pdf] [defaults-name]}"
OUT="${2:-${SRC%.md}.pdf}"
STYLE="${3:-academic/default}"

DATA_DIR="${PANDOC_DATA_DIR:-${HOME}/.local/share/pandoc}"
if [[ ! -f "${DATA_DIR}/defaults/academic/default.yaml" ]]; then
  echo "[pandoc-pdf] templates not deployed; using repo as --data-dir" >&2
  DATA_DIR="${ROOT}"
fi

echo "[pandoc-pdf] $(pandoc --version | head -1)"
echo "[pandoc-pdf] data-dir=${DATA_DIR}  defaults=${STYLE}"
echo "[pandoc-pdf] ${SRC} → ${OUT}"

pandoc "${SRC}" -o "${OUT}" --data-dir="${DATA_DIR}" --defaults="${STYLE}"
echo "[pandoc-pdf] wrote ${OUT}"
