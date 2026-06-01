# `.claude/` — AI Brain (Claude Code)

Last Updated: 2026-05-02

## Что здесь

Конфигурация и расширения Claude Code: skills (slash-команды), sub-агенты,
правила сессии, хуки, settings.

## Структура

| Папка / файл | Назначение |
|--------------|-----------|
| [`skills/`](skills/) | Slash-команды (commit, deploy, test, architect, ...) |
| [`agents/`](agents/) | Sub-агенты для делегирования (deployer, test-runner, code-reviewer, ...) |
| [`rules/`](rules/) | Поведенческие правила сессии (advisory) |
| [`hooks/`](hooks/) | Bash-хуки (deterministic, выполняются всегда) |
| [`data/`](data/) | Skill memory (error-log.md и др., gitignored если нужно) |
| `settings.json` | Permissions, hooks, enabled plugins |
| `settings.local.json` | Личные настройки разработчика (gitignored) |
| [`EXTERNAL-TOOLS.md`](EXTERNAL-TOOLS.md) | Внешние агенты/скиллы, ожидаемые **глобально** в `~/.claude/` (ставятся через `make install-claude-tools`) |

## Skills vs Agents vs Rules vs Hooks

| Артефакт | Когда использовать |
|----------|--------------------|
| **Skill** | Многократно используемая команда с domain knowledge (`/commit`, `/deploy-dev`) |
| **Agent** | Делегирование подзадачи в отдельный контекст (code review, тесты, исследование) |
| **Rule** | Поведенческая привычка для AI (advisory, может быть проигнорирована) |
| **Hook** | Детерминированное действие на событие (auto-lint, MEMORY BANK warning) |

## Связанные

- Родитель: [`../README.md`](../README.md)
- AI best practices: [`../documentation/90-AI-AGENT-BEST-PRACTICES.md`](../documentation/90-AI-AGENT-BEST-PRACTICES.md)
- Forking guide: [`../documentation/00-FORKING-GUIDE.md`](../documentation/00-FORKING-GUIDE.md)
