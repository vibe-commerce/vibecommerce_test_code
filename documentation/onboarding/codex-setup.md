# Настройка OpenAI Codex

Last Updated: 2026-05-29

## Что такое Codex

OpenAI Codex — AI-агент от OpenAI (VS Code extension + CLI). Этот шаблон
работает в обоих агентах: Claude Code и Codex. Главный канон для Codex —
[`../../AGENTS.md`](../../AGENTS.md) в корне репо (agents.md spec).

## Шаг 1 — Установка Codex

Варианты:
1. **VS Code Extension** — самый простой (Marketplace → ищи `OpenAI Codex` или `Cursor`)
2. **CLI** — https://github.com/openai/codex (если опубликован)
3. **Других платформ** — Aider, Continue.dev, etc. — все совместимы с agents.md spec

## Шаг 2 — Project-local config

Скопируй шаблон конфига:

```bash
cp .codex/config.toml.template ~/.codex/config.toml
# Подкорректируй под свои нужды (см. комментарии внутри)
```

Или для project-local конфига:

```bash
cp .codex/config.toml.template ./.codex/config.toml
```

## Шаг 3 — Проверка чтения AGENTS.md

После открытия репо Codex должен подгрузить:
- `AGENTS.md` — главный канон (≤ 32 KB по spec)
- `_shared/INSTRUCTIONS.md` — общая часть с Claude
- `_shared/MEMORY.md` — общая память

В Codex чате проверь:
```
Прочитай AGENTS.md и _shared/INSTRUCTIONS.md, расскажи структуру проекта.
```

Если Codex не видит файлы — проверь, что они на корне и `AGENTS.md` ≤ 32 KB.

## Шаг 4 — Skills (после фазы C12)

Изначально `.codex/skills/` пуста. После реализации
`scripts/sync-agents-config.sh` (фаза C7-C12) сюда появятся симлинки на
`.agents/skills/`, и Codex будет видеть те же команды что и Claude Code.

Текущий статус: stub. Полная реализация — задача отдельной сессии.

См. историю реализации cross-agent слоя в [`../../_changelogs/CHANGELOG.md`](../../_changelogs/CHANGELOG.md)
(записи 0.3.0 / 0.3.1).

## Шаг 5 — MCP

MCP-конфиг живёт в [`../../_shared/mcp.yaml`](../../_shared/mcp.yaml).
Генератор `scripts/sync-agents-config.sh` создаст `.codex/.mcp.toml` для Codex.

Текущие MCP:
- `context7` — актуальная документация SDK
- `playwright` — браузерная автоматизация

## Шаг 6 — Hooks

Codex hooks — в `.codex/hooks/` (симлинки на `_shared/hooks/`).
Текущий хук: `memory-bank-check.sh` (предупреждает об отсутствии README updates).

## Шаг 7 — Проверка cross-agent компатибильности

```bash
bash scripts/verify-cross-compat.sh
```

Должно выдать ✅ PASSED:
- AGENTS.md ≤ 32 KB
- _shared/{INSTRUCTIONS,MEMORY}.md существуют
- _shared/mcp.yaml валидный YAML
- .agents/, .codex/ папки существуют
- (после C12) симлинки skills работают

## Что НЕ работает в Codex (Claude-only)

- Claude plugins (`agent-teams`, `frontend-design`, `claude-md-management` etc.)
  — пометить в skill frontmatter как `claude-only: true`
- Расширенные Claude hooks (`PostToolBatch`, `TaskCreated`, `WorktreeCreate`)
- Some MCP servers могут не поддерживать Codex без обёртки

## Связанные

- Главный канон для Codex: [`../../AGENTS.md`](../../AGENTS.md)
- Общие инструкции: [`../../_shared/INSTRUCTIONS.md`](../../_shared/INSTRUCTIONS.md)
- Cross-agent spec: [`../../_specs/codex-compat/README.md`](../../_specs/codex-compat/README.md)
- Установка Claude Code: [`claude-code-setup.md`](claude-code-setup.md)
