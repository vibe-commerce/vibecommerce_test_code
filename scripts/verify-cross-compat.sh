#!/usr/bin/env bash
# verify-cross-compat.sh — smoke-проверка cross-agent компатибильности.
#
# Что проверяет:
#   1. Симлинки .claude/skills и .codex/skills указывают на .agents/skills
#   2. AGENTS.md ≤ 32 KB (Codex limit)
#   3. CLAUDE.md / AGENTS.md / _shared/INSTRUCTIONS.md существуют
#   4. _shared/mcp.yaml валидный YAML
#   5. Все sub-agents в .agents/subagents/ имеют валидный YAML
#   6. Все generated TOML (.codex/agents/*, .mcp.toml, config.template) парсятся
#   7. .claude/.mcp.json — валидный JSON
#   8. Симлинки skills указывают на правильный target
#
# Триггер: `make verify-agents` или pre-commit hook.

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
    rel_target="../../.agents/skills/$skill_name"
    for base in .claude .codex; do
      link="$base/skills/$skill_name"
      if [ -L "$link" ] && [ "$(readlink "$link")" = "$rel_target" ]; then
        echo "✅ Symlink $link → $rel_target"
      else
        echo "❌ Symlink $link (ожидался target $rel_target)"
        errors=$((errors+1))
      fi
    done
  done
else
  echo "ℹ️  .agents/skills/ пуста — symlink checks пропущены"
fi

# 5-7. Парсинг всех cross-agent конфигов (YAML / JSON / TOML)
if command -v python3 >/dev/null; then
  if python3 - <<'PYEOF'
import glob
import json
import sys
import tomllib

errors = []

try:
    import yaml
    for f in ["_shared/mcp.yaml", *glob.glob(".agents/subagents/*.yaml")]:
        try:
            yaml.safe_load(open(f, encoding="utf-8"))
        except Exception as e:
            errors.append(f"YAML {f}: {e}")
except ImportError:
    print("  ℹ️  PyYAML не установлен — YAML-проверка пропущена")

for f in [*glob.glob(".codex/agents/*.toml"), ".codex/.mcp.toml", ".codex/config.toml.template"]:
    try:
        tomllib.load(open(f, "rb"))
    except FileNotFoundError:
        pass
    except Exception as e:
        errors.append(f"TOML {f}: {e}")

for f in [".claude/.mcp.json"]:
    try:
        json.load(open(f, encoding="utf-8"))
    except FileNotFoundError:
        pass
    except Exception as e:
        errors.append(f"JSON {f}: {e}")

if errors:
    print("\n".join("  " + e for e in errors))
    sys.exit(1)
PYEOF
  then
    echo "✅ Все cross-agent конфиги (YAML/JSON/TOML) валидны"
  else
    echo "❌ Невалидные cross-agent конфиги (см. выше)"
    errors=$((errors+1))
  fi
fi

echo ""
if [ "$errors" -gt 0 ]; then
  echo "❌ verify-cross-compat.sh FAILED ($errors errors)"
  exit 1
else
  echo "✅ verify-cross-compat.sh PASSED"
fi
