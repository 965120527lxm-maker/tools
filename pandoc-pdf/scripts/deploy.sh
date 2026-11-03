#!/usr/bin/env bash
# One-click install of pandoc-pdf templates into the Pandoc data directory.
#
#   ./scripts/deploy.sh              # → ~/.local/share/pandoc
#   ./scripts/deploy.sh /custom/dir  # → custom data-dir
#   PANDOC_DATA_DIR=... ./scripts/deploy.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="${1:-${PANDOC_DATA_DIR:-${HOME}/.local/share/pandoc}}"

echo "[pandoc-pdf] root     = ${ROOT}"
echo "[pandoc-pdf] data-dir = ${DATA_DIR}"

mkdir -p "${DATA_DIR}/defaults/academic" "${DATA_DIR}/headers/academic"

# Sync style files (no delete of unrelated user defaults)
cp -f "${ROOT}/defaults/academic/default.yaml" "${DATA_DIR}/defaults/academic/default.yaml"
cp -f "${ROOT}/headers/academic/"*.tex "${DATA_DIR}/headers/academic/"

# Backward-compatible flat name: --defaults=academic
cp -f "${DATA_DIR}/defaults/academic/default.yaml" "${DATA_DIR}/defaults/academic.yaml"

# Optional: system font hints (no binary fonts vendored)
mkdir -p "${DATA_DIR}/pandoc-pdf"
cp -f "${ROOT}/fonts/README.md" "${DATA_DIR}/pandoc-pdf/FONTS.md"
if [[ -f "${ROOT}/fonts/manifest.txt" ]]; then
  cp -f "${ROOT}/fonts/manifest.txt" "${DATA_DIR}/pandoc-pdf/manifest.txt"
fi

echo "[pandoc-pdf] installed:"
echo "  defaults/academic/default.yaml"
echo "  defaults/academic.yaml  (alias)"
echo "  headers/academic/*.tex"

# Dependency check (non-fatal warnings)
if command -v pandoc >/dev/null 2>&1; then
  echo "[pandoc-pdf] pandoc: $(pandoc --version | head -1)"
else
  echo "[pandoc-pdf] WARN: pandoc not on PATH" >&2
fi
if command -v xelatex >/dev/null 2>&1; then
  echo "[pandoc-pdf] xelatex: ok"
else
  echo "[pandoc-pdf] WARN: xelatex missing (need texlive-xetex)" >&2
fi

if command -v fc-list >/dev/null 2>&1; then
  missing=0
  for fam in "Noto Serif CJK SC" "TeX Gyre Termes" "Noto Sans Mono"; do
    if fc-list ":family=${fam}" | head -1 | grep -q .; then
      echo "[pandoc-pdf] font ok: ${fam}"
    else
      # TeX Gyre may only be visible to XeTeX, not fontconfig
      if [[ "${fam}" == "TeX Gyre Termes" ]]; then
        echo "[pandoc-pdf] font note: ${fam} (often TeX-only; ok if xelatex finds it)"
      else
        echo "[pandoc-pdf] WARN: font not in fontconfig: ${fam}" >&2
        missing=1
      fi
    fi
  done
  if [[ "${missing}" -ne 0 ]]; then
    echo "[pandoc-pdf] hint: sudo apt install fonts-noto-cjk fonts-noto-mono texlive-fonts-recommended" >&2
  fi
fi

cat <<EOF

Done. Try:

  pandoc ${ROOT}/examples/sample.md -o /tmp/pandoc-pdf-sample.pdf --defaults=academic/default

If pandoc looks in the wrong data-dir:

  pandoc ... --data-dir=${DATA_DIR} --defaults=academic/default

EOF
