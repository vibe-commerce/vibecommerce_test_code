# `_shared/` — общие инструкции для AI-агентов

Last Updated: 2026-05-29

## Что здесь

Общая часть инструкций, которая одинакова для Claude Code и OpenAI Codex.

- `INSTRUCTIONS.md` — главные общие инструкции (импортируется обоими через `@`)
- `MEMORY.md` — общая память репо (читается обоими)
- `memory-policy.md` — политика памяти
- `mcp.yaml` — единый источник для MCP-серверов (генератор → `.claude/.mcp.json` + Codex TOML)
- `hooks/` — общие хуки (симлинки из `.claude/hooks/` и `.codex/hooks/`)

## Зачем

Без `_shared/`:
- Каждый агент читает свой файл (`CLAUDE.md` для Claude, `AGENTS.md` для Codex)
- Общие правила дублируются → разъезжаются со временем
- Не понятно, какой источник истины

С `_shared/`:
- `CLAUDE.md` импортирует `_shared/INSTRUCTIONS.md` через `@`
- `AGENTS.md` тоже импортирует
- Общая часть — в одном месте, не дублируется

## Импорты

В `CLAUDE.md`:
```markdown
@ _shared/INSTRUCTIONS.md
@ AGENTS.md
```

В `AGENTS.md` (если Codex поддерживает import):
```markdown
@ _shared/INSTRUCTIONS.md
```

Если Codex не поддерживает `@`-import → дублирование переносится в скрипт
`scripts/sync-agents-config.sh` (после реализации).

## Связанные

- Claude канон: [`../CLAUDE.md`](../CLAUDE.md)
- Codex канон: [`../AGENTS.md`](../AGENTS.md)
- Cross-agent skills/subagents: [`../.agents/`](../.agents/)
