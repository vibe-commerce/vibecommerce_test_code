# `_specs/codex-compat/` — Cross-agent compatibility

Last Updated: 2026-05-29

## Что здесь

Спецификации архитектуры cross-agent совместимости (Claude Code + OpenAI Codex).

Полная методология + ресёрч + готовый пример живут в **EMPTY_code** (это
наш «исходник истины» для cross-agent методологии):

- **План:** [`EMPTY_code/backlog/plans/2026-05-08-codex-compatibility.md`](/Users/vadimbakanov/Documents/_CODE/EMPTY_code/backlog/plans/2026-05-08-codex-compatibility.md)
  — 6 фаз, ~12-18 часов работы
- **Ресёрч (~80 KB):** [`EMPTY_code/_specs/codex-compat/`](/Users/vadimbakanov/Documents/_CODE/EMPTY_code/_specs/codex-compat/)
  - `research-claude-code.md` — Claude Code детально
  - `research-codex.md` — OpenAI Codex детально
  - `research-cross-agent.md` — agents.md spec + межагентские паттерны
  - `research.md` — синтез
- **Готовый пример:** [`vadim-bakanov-ai-dev/.agents/skills/`](/Users/vadimbakanov/Documents/_CODE/vadim-bakanov-ai-dev/.agents/skills/) — 22 skill уже в кросс-формате

## Что реализовано в test_code (фаза C base)

✅ **Структура папок:**
- `AGENTS.md` (канон для Codex, agents.md spec)
- `CLAUDE.md` (канон для Claude Code) — обновлён с указанием cross-agent
- `_shared/INSTRUCTIONS.md` — общая часть (Принцип №0, Plan Before Act, git, security)
- `_shared/MEMORY.md` — общая память репо
- `_shared/memory-policy.md` — политика памяти
- `_shared/mcp.yaml` — единый источник для MCP-серверов
- `_shared/hooks/README.md`
- `.agents/skills/` (пусто — будет наполнено в C12)
- `.agents/subagents/` (пусто — будет наполнено в C14)
- `.codex/{skills,agents,prompts,hooks}/` (пусто, симлинки появятся после C12)
- `.codex/config.toml.template`

✅ **Скрипты:**
- `scripts/sync-agents-config.sh` (stub — пока проверяет структуру)
- `scripts/verify-cross-compat.sh` (работает: smoke-проверка)

✅ **Makefile targets:**
- `make sync-agents`
- `make verify-agents`

## Что НЕ реализовано (open tasks)

❌ **C7** — полная реализация генератора `sync-agents-config.sh`:
- YAML → Markdown (Claude agent format)
- YAML → TOML (Codex agent format)
- mcp.yaml → .mcp.json (Claude) + .mcp.toml (Codex)

❌ **C12** — массовый порт skills:
- Move `.claude/skills/<name>/` → `.agents/skills/<name>/` + симлинки
- Проверка SKILL.md frontmatter на совместимость с agentskills.io
- ~14-16 skills FREE

❌ **C13** — пометка Claude-only skills в frontmatter

❌ **C14** — порт subagents (~6-8 агентов) через rip-конвертер

❌ **C15** — аудит плагинов (`agent-teams`, `pr-review-toolkit`, etc.)

❌ **C18-C19** — обновление README + onboarding для обоих агентов

❌ **C21** — финальный smoke в VS Code (оба агента работают параллельно)

❌ **C22** — применение архитектуры к `vibecommerce_vip_code` (после фазы V)

## Архитектурное решение (вариант C)

```
test_code/
├── AGENTS.md                # Codex канон
├── CLAUDE.md                # Claude канон
├── _shared/
│   ├── INSTRUCTIONS.md      # общая часть (@-импортируется обоими)
│   ├── MEMORY.md
│   ├── mcp.yaml             # один источник для MCP
│   └── hooks/
├── .agents/
│   ├── skills/<name>/SKILL.md     # источник истины
│   └── subagents/<name>.yaml      # источник истины
├── .claude/
│   ├── skills/<name> → симлинк
│   └── agents/<name>.md           # генерируется
└── .codex/
    ├── skills/<name> → симлинк
    └── agents/<name>.toml         # генерируется
```

## Источники

- **agents.md spec** — https://agents.md (индустриальный стандарт 2026, 60+k репо)
- **agentskills.io** — https://agentskills.io (кросс-совместимые skills, ~32 инструмента)

## Связанные

- План апгрейда test_code: [`../../backlog/plans/2026-05-28-upgrade-test-code-from-best-practices.md`](../../backlog/plans/2026-05-28-upgrade-test-code-from-best-practices.md) — раздел 3.12 «Фаза C»
- AGENTS.md канон: [`../../AGENTS.md`](../../AGENTS.md)
- CLAUDE.md канон: [`../../CLAUDE.md`](../../CLAUDE.md)
- Общие инструкции: [`../../_shared/INSTRUCTIONS.md`](../../_shared/INSTRUCTIONS.md)
