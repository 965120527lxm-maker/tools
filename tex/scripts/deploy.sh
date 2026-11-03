#!/usr/bin/env bash
# Deploy TeX environment hints + lxm local packages into TEXMFHOME.
#
#   ./scripts/deploy.sh           # check + install sty to ~/texmf
#   ./scripts/deploy.sh --apt     # also print (or run) apt install lines
#   TEXMFHOME=/path ./scripts/deploy.sh
#
# Pipeline roles: see ../PIPELINE.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEXMFHOME="${TEXMFHOME:-${HOME}/texmf}"
DO_APT=0
RUN_APT=0

for arg in "$@"; do
  case "${arg}" in
    --apt) DO_APT=1 ;;
    --apt-install) DO_APT=1; RUN_APT=1 ;;
    -h|--help)
      sed -n '2,12p' "$0" | sed 's/^# \?//'
      exit 0
      ;;
    *)
      echo "unknown arg: ${arg}" >&2
      exit 2
      ;;
  esac
done

APT_PACKAGES=(
  texlive-xetex
  texlive-lang-chinese
  texlive-lang-cjk
  texlive-latex-extra
  texlive-fonts-recommended
  texlive-science
  texlive-pictures
  latexmk
  fonts-noto-cjk
  fonts-noto-mono
)

echo "[tex] root      = ${ROOT}"
echo "[tex] TEXMFHOME = ${TEXMFHOME}"
echo "[tex] pipeline  = ${ROOT}/../PIPELINE.md"

# --- local packages (TDS) ---
mkdir -p "${TEXMFHOME}"
# Copy package trees: packages/<name>/tex/... → $TEXMFHOME/tex/...
for pkg_dir in "${ROOT}/packages"/*; do
  [[ -d "${pkg_dir}" ]] || continue
  name="$(basename "${pkg_dir}")"
  echo "[tex] install package: ${name}"
  # rsync-like: copy contents under package root into TEXMFHOME
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude '.git' "${pkg_dir}/" "${TEXMFHOME}/"
  else
    cp -a "${pkg_dir}/." "${TEXMFHOME}/"
  fi
done

if command -v mktexlsr >/dev/null 2>&1; then
  mktexlsr "${TEXMFHOME}" >/dev/null 2>&1 || true
elif command -v texhash >/dev/null 2>&1; then
  texhash "${TEXMFHOME}" >/dev/null 2>&1 || true
fi

# Record deploy meta
mkdir -p "${TEXMFHOME}/lxm-tex"
cp -f "${ROOT}/fonts/README.md" "${TEXMFHOME}/lxm-tex/FONTS.md"
cp -f "${ROOT}/../PIPELINE.md" "${TEXMFHOME}/lxm-tex/PIPELINE.md" 2>/dev/null || true
date -Iseconds > "${TEXMFHOME}/lxm-tex/DEPLOYED_AT"

echo "[tex] sty tree installed under ${TEXMFHOME}"

# --- engine / font check ---
missing_cmd=0
for c in xelatex latexmk; do
  if command -v "${c}" >/dev/null 2>&1; then
    echo "[tex] ok cmd: ${c} ($("${c}" --version 2>/dev/null | head -1))"
  else
    echo "[tex] MISSING cmd: ${c}" >&2
    missing_cmd=1
  fi
done

if command -v kpsewhich >/dev/null 2>&1; then
  export TEXMFHOME
  for f in beamer.cls ctex.sty fontspec.sty xeCJK.sty lxm-academic.sty; do
    p="$(kpsewhich "${f}" 2>/dev/null || true)"
    if [[ -n "${p}" ]]; then
      echo "[tex] ok kpse: ${f} → ${p}"
    else
      echo "[tex] MISSING kpse: ${f}" >&2
      missing_cmd=1
    fi
  done
else
  echo "[tex] WARN: kpsewhich not found" >&2
  missing_cmd=1
fi

if command -v fc-list >/dev/null 2>&1; then
  if fc-list "Noto Serif CJK SC" | head -1 | grep -q .; then
    echo "[tex] ok font: Noto Serif CJK SC"
  else
    echo "[tex] MISSING font: Noto Serif CJK SC (apt: fonts-noto-cjk)" >&2
    missing_cmd=1
  fi
fi

# --- apt ---
apt_line="sudo apt install -y ${APT_PACKAGES[*]}"
if [[ "${DO_APT}" -eq 1 ]]; then
  echo "[tex] apt packages:"
  printf '  %s\n' "${APT_PACKAGES[@]}"
  if [[ "${RUN_APT}" -eq 1 ]]; then
    echo "[tex] running: ${apt_line}"
    # shellcheck disable=SC2086
    sudo apt install -y "${APT_PACKAGES[@]}"
  else
    echo "[tex] dry-run. To install:"
    echo "  ${apt_line}"
    echo "  # or: $0 --apt-install"
  fi
elif [[ "${missing_cmd}" -ne 0 ]]; then
  echo "[tex] some checks failed. Install deps with:" >&2
  echo "  ${apt_line}" >&2
  echo "  # or: $0 --apt" >&2
fi

cat <<EOF

Done.
  Check:  ${ROOT}/scripts/check.sh
  Sample: cd ${ROOT}/examples && latexmk -xelatex hello-academic.tex
  Roles:  ${ROOT}/../PIPELINE.md

EOF

exit 0
