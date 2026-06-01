#!/usr/bin/env bash
# memory-bank-check.sh — PostToolUse hook для Edit/Write
#
# Проверяет: при изменении файла обновлён ли README.md в его папке.
# Если нет — выводит warning (НЕ блокирует действие).
#
# Реализует правило MEMORY BANK из CLAUDE.md.

set -u

INPUT=$(cat)

FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

# Проверяем только Edit/Write
case "$TOOL" in
  Edit|Write|MultiEdit) ;;
  *) exit 0 ;;
esac

# Если путь пустой или не файл — пропускаем
[[ -z "$FILE" ]] && exit 0

# Получаем абсолютный путь и относительный к корню проекта
PROJECT_ROOT=$(git -C "$(dirname "$FILE")" rev-parse --show-toplevel 2>/dev/null || echo "")
[[ -z "$PROJECT_ROOT" ]] && exit 0

# Если файл вне проекта — пропускаем
case "$FILE" in
  "$PROJECT_ROOT"/*) ;;
  *) exit 0 ;;
esac

REL_PATH="${FILE#$PROJECT_ROOT/}"

# Whitelist: пути и расширения, для которых README обновлять не нужно
case "$REL_PATH" in
  README.md|*/README.md) exit 0 ;;
  CLAUDE.md|AGENDA.md|HANDOFF.md|FACTS.md|ROADMAP.md|VERSION|MEMORY.md) exit 0 ;;
  _private/*|.git/*|.claude/data/*|.claude/settings.local.json) exit 0 ;;
  data/raw/*|data/processed/*|data/cache/*) exit 0 ;;
  node_modules/*|.venv/*|venv/*|__pycache__/*|.pytest_cache/*|.ruff_cache/*) exit 0 ;;
  dist/*|build/*|.next/*|.ipynb_checkpoints/*) exit 0 ;;
  *.log|*.lock|*.pyc|*.swp|*.swo|.DS_Store|Thumbs.db) exit 0 ;;
  uv.lock|package-lock.json|yarn.lock|pnpm-lock.yaml) exit 0 ;;
esac

# Находим ближайший README.md вверх по дереву
DIR=$(dirname "$FILE")
README=""
while [[ "$DIR" == "$PROJECT_ROOT"* ]]; do
  if [[ -f "$DIR/README.md" ]]; then
    README="$DIR/README.md"
    break
  fi
  [[ "$DIR" == "$PROJECT_ROOT" ]] && break
  DIR=$(dirname "$DIR")
done

[[ -z "$README" ]] && exit 0

# Проверяем, был ли README изменён в текущем git-индексе или незакоммиченных правках
README_REL="${README#$PROJECT_ROOT/}"
GIT_STATUS=$(git -C "$PROJECT_ROOT" status --porcelain "$README_REL" 2>/dev/null)

if [[ -z "$GIT_STATUS" ]]; then
  # README не менялся в этой сессии — выводим warning
  >&2 echo ""
  >&2 echo "⚠️  MEMORY BANK: ты изменил $REL_PATH,"
  >&2 echo "    но $README_REL не обновлён в этой сессии."
  >&2 echo "    Обнови README по правилу MEMORY BANK (см. CLAUDE.md)."
  >&2 echo ""
fi

exit 0
