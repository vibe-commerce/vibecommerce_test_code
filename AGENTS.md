# AGENTS.md — vibecommerce_test_code

> Этот файл — **канон для OpenAI Codex** (agents.md spec).
> Эквивалент для Claude Code → [CLAUDE.md](CLAUDE.md).
> Общая часть для обоих → [_shared/INSTRUCTIONS.md](_shared/INSTRUCTIONS.md).

Last Updated: 2026-06-02
Version: 0.3.2 (lifecycle EMPTY_code 0.5.4 + FREE/VIP + cross-agent compat)

## TL;DR для Codex

- **Что это:** шаблонный стартер для селлеров на МП/e-com, форкается студентом
- **Workflow:** только `local` + `main`, без deploy
- **Принцип №0:** в репо НЕТ персональных/клиентских данных
- **Plan Before Act:** перед нетривиальной правкой план в файл + согласование
- **Tagging:** `[CANONICAL]`, `[REF:]`, `[CONFIRMED:]`, `[PLACEHOLDER:]`, `[VIP]`
- **Память:** [`_shared/MEMORY.md`](_shared/MEMORY.md)

## Стек

| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.11+ |
| Аналитика | pandas, openpyxl, numpy |
| AI-агенты | Claude Code + OpenAI Codex (cross-agent через `AGENTS.md` + `.agents/`) |
| MCP | context7 (документация), playwright (web QA) |

См. полный стек и проекты → [README.md](README.md).

## Структура (краткая карта)

```
├── CLAUDE.md / AGENTS.md (этот) / _shared/INSTRUCTIONS.md   ← AI инструкции
├── README.md / FACTS.md / ROADMAP.md / AGENDA.md / HANDOFF.md
├── _modules/<NN>-<name>/   ← методические модули (read-only)
├── my-project/             ← рабочая зона студента (data/ gitignored)
├── _knowledge/{marketplaces,legal,suppliers}/
├── _prompts/{roles,jtbd,library}/
├── _practices/             ← 8-этапный workflow
├── _specs/templates/       ← brief, plan, ADR, tech-spec
├── backlog/{ideas,briefs,plans,archive/{done,rejected}}/
├── _changelogs/CHANGELOG.md
├── _status/PROJECT_STATUS.md
├── _private/               ← gitignored: secrets, docs, data
├── documentation/onboarding/
├── .claude/                ← Claude-only (skills, agents, rules, hooks, settings.json)
├── .codex/                 ← Codex-only (skills, agents, prompts, hooks, config.toml)
├── .agents/                ← общая папка (skills + subagents через симлинки)
└── _shared/                ← общие инструкции + MCP + hooks
```

## Что прочитать первым делом

При старте сессии Codex должен прочитать:

1. **[`_shared/INSTRUCTIONS.md`](_shared/INSTRUCTIONS.md)** — общие правила (Принцип №0, Plan Before Act, git, security, KISS/YAGNI)
2. **[`_shared/MEMORY.md`](_shared/MEMORY.md)** — стабильные факты + decisions
3. **[`AGENDA.md`](AGENDA.md)** — текущий фокус сессии
4. **[`_practices/00-WORKFLOW.md`](_practices/00-WORKFLOW.md)** — 8-этапный workflow

## Codex-specific особенности

### Slash-команды
Codex использует skills из `.codex/skills/` (симлинки на `.agents/skills/`).
После реализации `scripts/sync-agents-config.sh` все skills работают одинаково в обоих агентах.

### MCP
Конфиг MCP-серверов — в [`_shared/mcp.yaml`](_shared/mcp.yaml). Генератор
создаёт `.codex/.mcp.toml` из этого файла.

Текущие MCP:
- `context7` — актуальная документация SDK
- `playwright` — браузерная автоматизация

### Хуки
Codex hooks — реальные адаптеры в `.codex/hooks/` (`auto-ruff.sh`,
`memory-bank-check.sh`, apply_patch-aware). Монтируются через `.codex/hooks.json`
+ `[features] hooks = true` в `.codex/config.toml`.

### Permissions / Config
- `.codex/config.toml.template` — шаблон конфига. Скопируй в `~/.codex/config.toml` или подкорректируй для project-local.

### Что НЕ работает в Codex (Claude-only)
- Slash plugins (agent-teams, frontend-design, etc.) — пометить в скиллах как `claude-only: true`
- Расширенные hooks (`PostToolBatch`, `TaskCreated`, `WorktreeCreate`) — пока Claude-only

## Git Workflow

```
local → push → main (GitHub)
```

Подробности — в [`_shared/INSTRUCTIONS.md`](_shared/INSTRUCTIONS.md#git-workflow).

## Quick start для Codex-пользователя

```bash
# 1. Установка Codex
# https://github.com/openai/codex или VS Code extension

# 2. Открой репо
code .  # или открой через codex CLI

# 3. Заполни ~/.codex/config.toml (см. .codex/config.toml.template)

# 4. В Codex чате:
# "Прочитай AGENTS.md и _shared/INSTRUCTIONS.md, расскажи структуру проекта"

# 5. Дальше — workflow по _practices/00-WORKFLOW.md
```

Подробности → [`documentation/onboarding/codex-setup.md`](documentation/onboarding/codex-setup.md).

## Связанные

- Claude канон: [CLAUDE.md](CLAUDE.md)
- Общие инструкции: [_shared/INSTRUCTIONS.md](_shared/INSTRUCTIONS.md)
- Общая память: [_shared/MEMORY.md](_shared/MEMORY.md)
- MCP конфиг: [_shared/mcp.yaml](_shared/mcp.yaml)
- Cross-agent skills: [.agents/](.agents/)
- Codex specific: [.codex/](.codex/)
- Onboarding: [documentation/onboarding/README.md](documentation/onboarding/README.md)
