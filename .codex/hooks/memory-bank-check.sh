#!/usr/bin/env bash
# .codex/hooks/memory-bank-check.sh — Codex PostToolUse adapter.
#
# Напоминает обновить README.md папки при изменении файла (правило MEMORY BANK
# из AGENTS.md / CLAUDE.md). НЕ блокирует действие.
#
# Codex-специфика vs Claude-вариант (.claude/hooks/memory-bank-check.sh):
#   - правки Codex идут через apply_patch → tool_name может быть "apply_patch";
#   - путь файла берём из tool_input (file_path/path), а если его нет
#     (apply_patch), определяем изменённые файлы из git diff (defensive —
#     точная схема tool_input для apply_patch официально не зафиксирована);
#   - предупреждение отдаём Codex-нативно через JSON {"systemMessage": ...}.
set -u

INPUT="$(cat)"

command -v jq  >/dev/null 2>&1 || exit 0
command -v git >/dev/null 2>&1 || exit 0

TOOL="$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)"
case "$TOOL" in
  apply_patch|Edit|Write|MultiEdit) ;;
  *) exit 0 ;;
esac

PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "")"
[ -z "$PROJECT_ROOT" ] && exit 0

# Затронутые файлы: сначала из tool_input, иначе (apply_patch) из git diff.
F="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)"
if [ -n "$F" ]; then
  FILES="$F"
else
  # apply_patch: tool_name=apply_patch, пути — в tool_input.command
  # (маркеры "*** Add/Update/Delete File: <path>"). Затем fallback на git status,
  # который (в отличие от git diff) видит и НОВЫЕ untracked-файлы.
  CMD="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)"
  FILES="$(printf '%s\n' "$CMD" | sed -n -E 's/^\*\*\* (Add|Update|Delete) File: //p')"
  [ -z "$FILES" ] && FILES="$(git -C "$PROJECT_ROOT" status --porcelain 2>/dev/null | sed -E 's/^.. //')"
fi
[ -z "$FILES" ] && exit 0

is_whitelisted() {
  case "$1" in
    README.md|*/README.md) return 0 ;;
    CLAUDE.md|AGENTS.md|AGENDA.md|HANDOFF.md|FACTS.md|ROADMAP.md|VERSION|MEMORY.md) return 0 ;;
    _private/*|.git/*|.claude/data/*|.claude/settings.local.json) return 0 ;;
    data/raw/*|data/processed/*|data/cache/*) return 0 ;;
    node_modules/*|.venv/*|venv/*|__pycache__/*|.pytest_cache/*|.ruff_cache/*) return 0 ;;
    dist/*|build/*|.next/*|.ipynb_checkpoints/*) return 0 ;;
    *.log|*.lock|*.pyc|*.swp|*.swo|.DS_Store|Thumbs.db) return 0 ;;
    uv.lock|package-lock.json|yarn.lock|pnpm-lock.yaml) return 0 ;;
  esac
  return 1
}

find_readme() {
  d="$1"
  while :; do
    [ -f "$d/README.md" ] && { printf '%s' "$d/README.md"; return; }
    [ "$d" = "$PROJECT_ROOT" ] && return
    parent="$(dirname "$d")"
    [ "$parent" = "$d" ] && return
    d="$parent"
  done
}

WARN=""
while IFS= read -r REL; do
  [ -z "$REL" ] && continue
  case "$REL" in "$PROJECT_ROOT"/*) REL="${REL#"$PROJECT_ROOT"/}" ;; esac
  is_whitelisted "$REL" && continue
  [ -e "$PROJECT_ROOT/$REL" ] || continue
  README="$(find_readme "$PROJECT_ROOT/$(dirname "$REL")")"
  [ -z "$README" ] && continue
  README_REL="${README#"$PROJECT_ROOT"/}"
  if [ -z "$(git -C "$PROJECT_ROOT" status --porcelain "$README_REL" 2>/dev/null)" ]; then
    WARN="${WARN}  - ${REL} → обнови ${README_REL}"$'\n'
  fi
done < <(printf '%s\n' "$FILES" | sort -u)

if [ -n "$WARN" ]; then
  MSG="⚠️ MEMORY BANK: изменены файлы, но README их папок не обновлён в этой сессии:"$'\n'"${WARN}(правило MEMORY BANK — см. AGENTS.md)"
  jq -cn --arg m "$MSG" '{systemMessage: $m}'
fi

exit 0
