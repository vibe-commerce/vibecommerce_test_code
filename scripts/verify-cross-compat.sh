#!/usr/bin/env bash
# verify-cross-compat.sh — smoke-проверка cross-agent компатибильности.
#
# Что проверяет:
#   1. Симлинки .claude/skills и .codex/skills указывают на .agents/skills
#   2. AGENTS.md ≤ 32 KB (Codex limit)
#   3. CLAUDE.md / AGENTS.md / _shared/INSTRUCTIONS.md существуют
#   4. _shared/mcp.yaml валидный YAML
#   5. Все sub-agents в .agents/subagents/ имеют валидный YAML
#
# Триггер: `make verify-agents` или pre-commit hook.
#
# STATUS: stub. Полная реализация — пункт C8 плана.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

errors=0

check() {
  local name="$1"
  shift
  if "$@"; then
    echo "✅ $name"
  else
    echo "❌ $name"
    errors=$((errors+1))
  fi
}

echo "🔍 verify-cross-compat.sh"
echo ""

# 1. Файлы существуют
check "CLAUDE.md exists" test -f CLAUDE.md
check "AGENTS.md exists" test -f AGENTS.md
check "_shared/INSTRUCTIONS.md exists" test -f _shared/INSTRUCTIONS.md
check "_shared/MEMORY.md exists" test -f _shared/MEMORY.md
check "_shared/mcp.yaml exists" test -f _shared/mcp.yaml

# 2. AGENTS.md ≤ 32 KB
agents_size=$(wc -c < AGENTS.md)
check "AGENTS.md ≤ 32KB (current: ${agents_size}B)" test "$agents_size" -le 32768

# 3. Папки cross-agent
check ".agents/skills/ exists" test -d .agents/skills
check ".agents/subagents/ exists" test -d .agents/subagents
check ".codex/ exists" test -d .codex
check ".codex/config.toml.template exists" test -f .codex/config.toml.template

# 4. Симлинки (если уже синкнули)
if [ -d .agents/skills ] && [ "$(ls -A .agents/skills 2>/dev/null)" ]; then
  for skill_dir in .agents/skills/*/; do
    skill_name=$(basename "$skill_dir")
    check "Symlink .claude/skills/$skill_name" test -L ".claude/skills/$skill_name"
    check "Symlink .codex/skills/$skill_name" test -L ".codex/skills/$skill_name"
  done
else
  echo "ℹ️  .agents/skills/ пуста — symlink checks пропущены"
fi

# 5. YAML валидность (если есть python)
if command -v python3 >/dev/null; then
  if python3 -c "import yaml" 2>/dev/null; then
    check "_shared/mcp.yaml is valid YAML" python3 -c "import yaml; yaml.safe_load(open('_shared/mcp.yaml'))"
  else
    echo "ℹ️  PyYAML не установлен, YAML-проверка пропущена"
  fi
fi

echo ""
if [ "$errors" -gt 0 ]; then
  echo "❌ verify-cross-compat.sh FAILED ($errors errors)"
  exit 1
else
  echo "✅ verify-cross-compat.sh PASSED"
fi
