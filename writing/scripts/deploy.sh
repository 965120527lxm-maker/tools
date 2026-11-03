#!/usr/bin/env bash
# Install lxm-general-writing into the user-level Kimi and Cursor skill roots.
#
# Usage:
#   tools/writing/scripts/deploy.sh
#   tools/writing/scripts/deploy.sh --dry-run
#   tools/writing/scripts/deploy.sh --kimi-only
#   tools/writing/scripts/deploy.sh --cursor-only
#
# Test or customize without changing HOME:
#   KIMI_SKILLS_DIR=/tmp/kimi-skills \
#   CURSOR_SKILLS_DIR=/tmp/cursor-skills \
#     tools/writing/scripts/deploy.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WRITING_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_NAME="lxm-general-writing"
SOURCE_DIR="${WRITING_ROOT}/${SKILL_NAME}"
USER_HOME="${HOME:?HOME is required}"
KIMI_ROOT="${KIMI_SKILLS_DIR:-${USER_HOME}/.kimi/skills}"
CURSOR_ROOT="${CURSOR_SKILLS_DIR:-${USER_HOME}/.cursor/skills}"

DRY_RUN=0
INSTALL_KIMI=1
INSTALL_CURSOR=1

usage() {
  sed -n '2,13p' "$0" | sed 's/^# \?//'
}

for arg in "$@"; do
  case "${arg}" in
    --dry-run)
      DRY_RUN=1
      ;;
    --kimi-only)
      INSTALL_KIMI=1
      INSTALL_CURSOR=0
      ;;
    --cursor-only)
      INSTALL_KIMI=0
      INSTALL_CURSOR=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[writing] unknown argument: ${arg}" >&2
      usage >&2
      exit 2
      ;;
  esac
done

SKILL_FILES=(
  'SKILL.md'
  'references/blader-humanizer.md'
  'references/chinese-academic-prose.md'
)

for relative_path in "${SKILL_FILES[@]}"; do
  if [[ ! -f "${SOURCE_DIR}/${relative_path}" ]]; then
    echo "[writing] missing source skill file: ${SOURCE_DIR}/${relative_path}" >&2
    exit 1
  fi
done

install_skill() {
  local client="$1"
  local root="$2"
  local target_dir="${root}/${SKILL_NAME}"
  local changed=0

  echo "[writing] ${client}: ${SOURCE_DIR} -> ${target_dir}"
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    return
  fi

  for relative_path in "${SKILL_FILES[@]}"; do
    local source_file="${SOURCE_DIR}/${relative_path}"
    local target_file="${target_dir}/${relative_path}"

    mkdir -p "$(dirname "${target_file}")"
    if [[ -f "${target_file}" ]] && cmp -s "${source_file}" "${target_file}"; then
      continue
    fi
    install -m 0644 "${source_file}" "${target_file}"
    cmp -s "${source_file}" "${target_file}" || {
      echo "[writing] ${client}: verification failed: ${relative_path}" >&2
      exit 1
    }
    changed=1
  done

  if [[ "${changed}" -eq 1 ]]; then
    echo "[writing] ${client}: installed"
  else
    echo "[writing] ${client}: already up to date"
  fi
}

if [[ "${INSTALL_KIMI}" -eq 1 ]]; then
  install_skill "Kimi" "${KIMI_ROOT}"
fi
if [[ "${INSTALL_CURSOR}" -eq 1 ]]; then
  install_skill "Cursor" "${CURSOR_ROOT}"
fi

if [[ "${DRY_RUN}" -eq 1 ]]; then
  echo "[writing] dry run complete; no files changed"
else
  echo "[writing] done"
fi
