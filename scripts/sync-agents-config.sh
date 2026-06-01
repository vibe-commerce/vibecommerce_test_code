#!/usr/bin/env bash
# sync-agents-config.sh — синхронизация cross-agent конфига (Claude Code + OpenAI Codex)
#
# Что делает:
#   1. Симлинкует .claude/skills/<name> ↔ .agents/skills/<name> ↔ .codex/skills/<name>
#   2. Генерирует .claude/agents/<name>.md из .agents/subagents/<name>.yaml
#   3. Генерирует .codex/agents/<name>.toml из .agents/subagents/<name>.yaml
#   4. Генерирует .claude/.mcp.json из _shared/mcp.yaml
#   5. Генерирует .codex/.mcp.toml из _shared/mcp.yaml
#
# Идемпотентен — запускается многократно без побочных эффектов.
#
# Триггер: `make sync-agents` или вручную перед коммитом.
#
# Требования: bash 4+, python3 (для YAML/JSON парсинга)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# --- Helpers ---
ok()    { echo "  ✅ $1"; }
warn()  { echo "  ⚠️  $1"; }
note()  { echo "  ℹ️  $1"; }
fail()  { echo "  ❌ $1"; exit 1; }

# --- 1. Structure check ---
echo "📦 sync-agents-config.sh"
echo "Repo root: $REPO_ROOT"
echo ""

for dir in .agents/skills .agents/subagents _shared/hooks _shared; do
  [ -d "$dir" ] || fail "Missing directory: $dir"
done
for f in _shared/INSTRUCTIONS.md _shared/MEMORY.md _shared/mcp.yaml; do
  [ -f "$f" ] || fail "Missing file: $f"
done

# Ensure target dirs exist
mkdir -p .claude/skills .claude/agents .codex/skills .codex/agents

# --- 2. Symlinks для skills ---
echo "📎 Symlinking skills (.agents/skills/ → .claude/skills/ + .codex/skills/)..."
linked=0; existed=0; conflicted=0
for skill_dir in .agents/skills/*/; do
  [ -d "$skill_dir" ] || continue
  skill_name=$(basename "$skill_dir")

  for target in .claude/skills .codex/skills; do
    link_path="$target/$skill_name"
    rel_target="../../.agents/skills/$skill_name"
    if [ -L "$link_path" ]; then
      # already a symlink — check if points to correct location
      current=$(readlink "$link_path")
      if [ "$current" = "$rel_target" ]; then
        existed=$((existed+1))
      else
        rm "$link_path" && ln -s "$rel_target" "$link_path"
        ok "Re-linked: $link_path"
        linked=$((linked+1))
      fi
    elif [ -e "$link_path" ]; then
      warn "$link_path exists but is not a symlink — skipping (move to .agents/ first)"
      conflicted=$((conflicted+1))
    else
      ln -s "$rel_target" "$link_path"
      ok "Linked: $link_path → $rel_target"
      linked=$((linked+1))
    fi
  done
done
note "Skills: $linked new/updated, $existed unchanged, $conflicted conflicts"

# --- 3. Sub-agents: YAML → .claude/agents/<name>.md + .codex/agents/<name>.toml ---
echo ""
echo "🤖 Generating sub-agents from YAML..."
generated_md=0; generated_toml=0
if compgen -G ".agents/subagents/*.yaml" > /dev/null 2>&1; then
  for yaml_file in .agents/subagents/*.yaml; do
    [ -f "$yaml_file" ] || continue
    name=$(basename "$yaml_file" .yaml)

    # Use Python to parse YAML and generate
    python3 - "$yaml_file" "$name" <<'PYEOF'
import sys, os
try:
    import yaml
except ImportError:
    print(f"  ⚠️  PyYAML not installed — skipping {sys.argv[2]}")
    sys.exit(0)

yaml_file, name = sys.argv[1], sys.argv[2]
with open(yaml_file) as f:
    data = yaml.safe_load(f)

# .claude/agents/<name>.md (Markdown with YAML frontmatter)
md_path = f".claude/agents/{name}.md"
desc = data.get("description", "")
model = data.get("model", "inherit")
tools = data.get("tools", [])
prompt = data.get("prompt", "")

md_content = f"""---
name: {name}
description: {desc}
model: {model}
"""
if tools:
    if isinstance(tools, list):
        md_content += f"tools: [{', '.join(tools)}]\n"
    else:
        md_content += f"tools: {tools}\n"
md_content += "---\n\n"
md_content += prompt + "\n"

with open(md_path, "w") as f:
    f.write(md_content)
print(f"  ✅ Generated: {md_path}")

# .codex/agents/<name>.toml
toml_path = f".codex/agents/{name}.toml"
toml_content = f'''# Generated from .agents/subagents/{name}.yaml — do not edit manually
name = "{name}"
description = """{desc}"""
model = "{model}"
'''
if tools and isinstance(tools, list):
    toml_content += f'tools = [{", ".join(f"\"{t}\"" for t in tools)}]\n'

toml_content += f'''
[prompt]
content = """{prompt}"""
'''

with open(toml_path, "w") as f:
    f.write(toml_content)
print(f"  ✅ Generated: {toml_path}")
PYEOF
    generated_md=$((generated_md+1))
    generated_toml=$((generated_toml+1))
  done
else
  note "No subagents YAML files in .agents/subagents/ yet (use C14 to port)"
fi

# --- 4. MCP config generation ---
echo ""
echo "🔌 Generating MCP configs from _shared/mcp.yaml..."

python3 - <<'PYEOF'
import sys, json
try:
    import yaml
except ImportError:
    print("  ⚠️  PyYAML not installed — skipping MCP generation")
    sys.exit(0)

with open("_shared/mcp.yaml") as f:
    cfg = yaml.safe_load(f)

servers = cfg.get("servers", {})

# .claude/.mcp.json
claude_mcp = {"mcpServers": {}}
for name, server in servers.items():
    cl = server.get("claude", {})
    if cl.get("builtin"):
        # Built-in plugin — listed in settings.json, no .mcp.json entry needed
        continue
    entry = cl.get("config", {})
    if entry:
        claude_mcp["mcpServers"][name] = entry

with open(".claude/.mcp.json", "w") as f:
    json.dump(claude_mcp, f, indent=2, ensure_ascii=False)
print(f"  ✅ Generated: .claude/.mcp.json ({len(claude_mcp['mcpServers'])} servers)")

# .codex/.mcp.toml
toml_lines = ["# Generated from _shared/mcp.yaml — do not edit manually\n"]
for name, server in servers.items():
    cx = server.get("codex", {})
    if not cx:
        continue
    toml_lines.append(f"\n[mcp_servers.{name}]")
    for k, v in cx.items():
        if isinstance(v, str):
            toml_lines.append(f'{k} = "{v}"')
        elif isinstance(v, list):
            toml_lines.append(f'{k} = [{", ".join(f"\"{x}\"" for x in v)}]')
        else:
            toml_lines.append(f"{k} = {v}")

with open(".codex/.mcp.toml", "w") as f:
    f.write("\n".join(toml_lines) + "\n")
codex_count = sum(1 for s in servers.values() if s.get("codex"))
print(f"  ✅ Generated: .codex/.mcp.toml ({codex_count} servers)")
PYEOF

echo ""
echo "✅ sync-agents-config.sh finished."
