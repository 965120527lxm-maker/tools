#!/usr/bin/env bash
# Fetch the approved Chinese academic-writing calibration corpus.
#
# Only official samples, institution-hosted teaching materials, and
# open-licensed sources belong here. This script intentionally does not fetch
# full commercial books from third-party mirrors.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WRITING_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CORPUS_ROOT="${WRITING_ROOT}/corpus/zh-academic"
PDF_ROOT="${CORPUS_ROOT}/pdfs"
TEXT_ROOT="${CORPUS_ROOT}/text"
OPENMLSYS_ROOT="${CORPUS_ROOT}/open-textbooks/openmlsys"

mkdir -p "${PDF_ROOT}" "${TEXT_ROOT}" "${OPENMLSYS_ROOT}"

fetch() {
  local url="$1"
  local target="$2"

  if [[ -s "${target}" ]]; then
    echo "[corpus] present: ${target}"
    return
  fi

  echo "[corpus] fetch: ${url}"
  curl --location --fail --silent --show-error \
    --user-agent 'Mozilla/5.0 (writing-corpus-fetcher)' \
    --output "${target}.part" "${url}"
  mv "${target}.part" "${target}"
}

fetch \
  'https://www.tup.tsinghua.edu.cn/upload/books/yz/064027-01.pdf' \
  "${PDF_ROOT}/zhou-zhihua-machine-learning-sample.pdf"
fetch \
  'https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/Book2016toc.pdf' \
  "${PDF_ROOT}/zhou-zhihua-machine-learning-preface-toc.pdf"
fetch \
  'https://jwc.fudan.edu.cn/_upload/article/files/4b/39/489071da4c2a9f56492ae9ecfc59/4cff14a9-818d-4f38-8e14-3cd7ab94ea11.pdf' \
  "${PDF_ROOT}/fudan-probability-introduction.pdf"

OPENMLSYS_REV='9c289782ccbb165ac8ad7c960ecffc12942a5560'
OPENMLSYS_BASE="https://raw.githubusercontent.com/openmlsys/openmlsys/${OPENMLSYS_REV}"
fetch \
  "${OPENMLSYS_BASE}/v1/zh_chapters/chapter_preface/index.md" \
  "${OPENMLSYS_ROOT}/preface.md"
fetch \
  "${OPENMLSYS_BASE}/v1/zh_chapters/appendix_machine_learning_introduction/classic_machine_learning.md" \
  "${OPENMLSYS_ROOT}/classic-machine-learning.md"

if command -v pdftotext >/dev/null 2>&1; then
  for pdf in "${PDF_ROOT}"/*.pdf; do
    name="$(basename "${pdf}" .pdf)"
    pdftotext -layout "${pdf}" "${TEXT_ROOT}/${name}.txt"
  done
else
  echo '[corpus] pdftotext not found; PDFs downloaded without text extraction' >&2
fi

(
  cd "${CORPUS_ROOT}"
  find pdfs open-textbooks -type f -print0 \
    | sort -z \
    | xargs -0 sha256sum > SHA256SUMS
)

echo "[corpus] ready: ${CORPUS_ROOT}"
