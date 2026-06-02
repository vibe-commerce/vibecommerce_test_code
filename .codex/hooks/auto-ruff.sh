#!/usr/bin/env bash
# .codex/hooks/auto-ruff.sh — Codex PostToolUse adapter: ruff --fix по изменённым .py.
#
# Аналог Claude-хука (PostToolUse matcher Write → ruff). Codex-специфика: правки
# идут через apply_patch, поэтому если путь не пришёл в tool_input — берём
# изменённые .py из git diff. Тихо выходит, если ruff/jq/git недоступны.
set -u

INPUT="$(cat)"

command -v ruff >/dev/null 2>&1 || exit 0
command -v jq   >/dev/null 2>&1 || exit 0
command -v git  >/dev/null 2>&1 || exit 0

TOOL="$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)"
case "$TOOL" in
  apply_patch|Edit|Write|MultiEdit) ;;
  *) exit 0 ;;
esac

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "")"
[ -z "$ROOT" ] && exit 0

F="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)"
if [ -n "$F" ]; then
  FILES="$F"
else
  # apply_patch: пути из tool_input.command; иначе fallback на git status
  # (ловит НОВЫЕ untracked .py, которые git diff не показывает).
  CMD="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)"
  FILES="$(printf '%s\n' "$CMD" | sed -n -E 's/^\*\*\* (Add|Update|Delete) File: //p')"
  [ -z "$FILES" ] && FILES="$(git -C "$ROOT" status --porcelain 2>/dev/null | sed -E 's/^.. //')"
fi

while IFS= read -r f; do
  [ -z "$f" ] && continue
  case "$f" in
    *.py)
      if [ -f "$f" ]; then ruff check --fix "$f" >/dev/null 2>&1 || true
      elif [ -f "$ROOT/$f" ]; then ruff check --fix "$ROOT/$f" >/dev/null 2>&1 || true
      fi
      ;;
  esac
done < <(printf '%s\n' "$FILES")

exit 0
