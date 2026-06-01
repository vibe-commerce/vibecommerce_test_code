# Настройка Claude Code

Last Updated: 2026-05-29

## Шаг 1 — Установка Claude Code

Варианты:
1. **VS Code Extension** — самый простой (Marketplace → `Claude Code`)
2. **Desktop app** (Mac/Windows) — https://claude.com/claude-code
3. **CLI** — https://claude.com/claude-code/cli

## Шаг 2 — Проверка настроек репо

Открой репо в Claude Code. Должно подгрузиться:

- `CLAUDE.md` — главные инструкции (в разделе «Context» Claude видит этот файл)
- `.claude/settings.json` — permissions, hooks, enabledPlugins
- `.claude/skills/*` — slash-команды
- `.claude/agents/*` — sub-агенты
- `.claude/rules/*` — правила сессии

Проверь: в чате Claude напиши `/help` — должен показать список slash-команд:
- `/architect`, `/commit`, `/push`, `/git-status`, `/docs`, `/handoff`, `/test`, ...

## Шаг 3 — Permissions

По умолчанию `.claude/settings.json` разрешает:
- `WebFetch(domain:docs.anthropic.com)` — для документации Claude
- Enabled plugins: context7, playwright, agent-teams, и др.

Если хочешь добавить permission на свой домен (например, твой Shopify):
```bash
# Запусти в Claude Code чате:
/config

# Или вручную отредактируй .claude/settings.json:
{
  "permissions": {
    "allow": [
      "WebFetch(domain:docs.anthropic.com)",
      "WebFetch(domain:my-shop.com)"
    ]
  }
}
```

## Шаг 4 — MCP context7

`context7` MCP сервер уже включён в `enabledPlugins`. Он даёт актуальную
документацию библиотек (`use context7` в промптах).

Проверка: в чате
```
use context7. Покажи актуальный API pandas read_excel.
```

## Шаг 5 — Hooks

Активный хук — `memory-bank-check.sh` (срабатывает после Edit/Write).
Проверяет, что при изменении файла обновлён `README.md` в его папке.

```bash
# Проверка хука:
chmod +x .claude/hooks/memory-bank-check.sh
bash .claude/hooks/memory-bank-check.sh  # должен запуститься без ошибок
```

## Шаг 6 — Глобальные skills/agents

Если хочешь подключить глобальные skills/agents из `~/.claude/` (например,
`webapp-testing`), ставь их вручную — список и pinned-SHA в
`.claude/EXTERNAL-TOOLS.md` (bootstrap-скрипт запланирован, но ещё не реализован).

## Шаг 7 — Первый тест

В Claude Code чате:
```
/architect

Задача: добавить README для своего проекта селлера в my-project/.
```

Должен запуститься skill `/architect` → создать план в `backlog/plans/{date}-{slug}.md`.

## Полезные slash-команды

| Команда | Что делает |
|---------|-----------|
| `/architect` | Планирование → backlog/plans/ |
| `/commit` | AI-генерация commit message |
| `/push` | Безопасный push с подтверждением |
| `/handoff` | Сохранение состояния сессии в HANDOFF.md |
| `/docs` | Обновление документации после крупных изменений |
| `/test` | lint + types + unit tests |
| `/lawyer` | Юридический вопрос РФ |
| `/qa-tester` | QA через Playwright |
| `/project-knowledge` | База знаний по структуре/конвенциям |

## Связанные

- Codex setup (опционально): [`codex-setup.md`](codex-setup.md)
- VIP-настройка: [`vip-setup.md`](vip-setup.md)
- Workflow студента: [`student-workflow.md`](student-workflow.md)
