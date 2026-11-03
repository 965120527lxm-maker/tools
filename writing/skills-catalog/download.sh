#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
rm -f *.SKILL.md

download() {
  local name="$1"
  local url="$2"
  local out="${name}.SKILL.md"
  echo "=== ${out} ==="
  if ! curl -fsSL --connect-timeout 30 --max-time 120 "$url" -o "$out"; then
    echo "FAIL ${url}"
    rm -f "$out"
    return 1
  fi
  if head -c 80 "$out" | grep -Eiq '<!DOCTYPE|<html|404: Not Found|Not Found'; then
    echo "BAD content from ${url}"
    head -c 200 "$out"; echo
    rm -f "$out"
    return 1
  fi
  wc -l -c "$out"
}

# 使用前请先: source ~/.bashrc && proxy_on
download "blader-humanizer" "https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md"
download "op7418-Humanizer-zh" "https://raw.githubusercontent.com/op7418/Humanizer-zh/main/SKILL.md"
download "Aboudjem-humanizer-skill" "https://raw.githubusercontent.com/Aboudjem/humanizer-skill/main/skills/humanizer/SKILL.md"
download "hannsxpeter-humanizer" "https://raw.githubusercontent.com/hannsxpeter/humanizer/main/SKILL.md"
download "milock-humanizer" "https://raw.githubusercontent.com/milock/humanizer/main/SKILL.md"
download "Shirhussain-humanize" "https://raw.githubusercontent.com/Shirhussain/humanize/main/SKILL.md"
download "fendouai-humanize-text-skill" "https://raw.githubusercontent.com/fendouai/humanize-text-skill/main/SKILL.md"
download "daniel-bogale-anti-ai-writing-humanizer" "https://raw.githubusercontent.com/daniel-bogale/anti-ai-writing-humanizer/main/skills/anti-ai-writing-humanizer/SKILL.md"
download "ai-zixun-humanizer-zh" "https://raw.githubusercontent.com/ai-zixun/humanizer-zh/main/SKILL.md"
download "avikbal-dm-anti-ai-writing-claude-skill" "https://raw.githubusercontent.com/avikbal-dm/anti-ai-writing-claude-skill/main/anti-ai-writing-style-avikbal-SKILL.md"

echo
ls -la *.SKILL.md
echo
for f in *.SKILL.md; do
  echo "---- ${f} ----"
  head -n 6 "$f"
  echo
done
