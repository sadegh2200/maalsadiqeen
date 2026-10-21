#!/usr/bin/env bash
# Install (or re-sync) the maalsadiqeen-reel skill from this repository into the standard
# skill locations. Idempotent: run it again after any change to the master copy.
#
#   bash install-skill.sh            install / refresh every target
#   bash install-skill.sh --check    verify the installed copies are identical to the master
#
# Master copy (edit here only): maalsadiqeen-reel-maker/maalsadiqeen-reel/
# Targets:
#   <repo>/.claude/skills/maalsadiqeen-reel   project-scoped (Claude Code and compatible agents)
#   ~/.claude/skills/maalsadiqeen-reel        user-scoped (Claude Code)
#   ~/.agents/skills/maalsadiqeen-reel        shared user path (Codex / Copilot / Gemini CLI / ...)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$ROOT/maalsadiqeen-reel-maker/maalsadiqeen-reel"

[ -f "$SRC/SKILL.md" ] || { echo "✗ master copy not found: $SRC" >&2; exit 1; }

NAME="$(awk -F': *' '/^name:[[:space:]]*/{print $2; exit}' "$SRC/SKILL.md")"
[ -n "$NAME" ] || { echo "✗ could not read name: from $SRC/SKILL.md" >&2; exit 1; }

TARGETS=(
  "$ROOT/.claude/skills/$NAME"
  "$HOME/.claude/skills/$NAME"
  "$HOME/.agents/skills/$NAME"
)

CHECK=0
case "${1:-}" in
  --check) CHECK=1 ;;
  "" ) ;;
  * ) echo "usage: bash install-skill.sh [--check]" >&2; exit 2 ;;
esac

src_files=$(find "$SRC" -type f | wc -l | tr -d ' ')
echo "skill : $NAME"
echo "master: $SRC ($src_files files)"

status=0
for dst in "${TARGETS[@]}"; do
  if [ "$CHECK" = 1 ]; then
    if [ -d "$dst" ] && diff -r "$SRC" "$dst" >/dev/null 2>&1; then
      echo "✓ $dst"
    else
      echo "✗ $dst (missing or out of sync)"
      status=1
    fi
    continue
  fi

  mkdir -p "$(dirname "$dst")"
  rm -rf "$dst"
  cp -a "$SRC" "$dst"
  if diff -r "$SRC" "$dst" >/dev/null 2>&1; then
    echo "✓ installed → $dst"
  else
    echo "✗ copy mismatch → $dst" >&2
    status=1
  fi
done

if [ "$status" = 0 ] && [ "$CHECK" = 0 ]; then
  echo
  echo "Next: source \"$ROOT/.claude/skills/$NAME/scripts/env.sh\" and follow SKILL.md."
fi
exit "$status"
