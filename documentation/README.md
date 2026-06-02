# `documentation/` — живая документация проекта

Last Updated: 2026-06-02

## Что здесь

Только **факты о реализованном**. Не пиши сюда нереализованные планы — для них
есть `_specs/` и `backlog/`.

| # | Документ | Описание |
|---|----------|----------|
| 00 | [FORKING-GUIDE](00-FORKING-GUIDE.md) | Как форкать шаблон — чек-лист placeholder'ов |
| 01 | [OVERVIEW](01-OVERVIEW.md) | Обзор проекта, стек, ключевые решения |
| 10 | [ARCHITECTURE](10-ARCHITECTURE.md) | Архитектура системы, слои, компоненты |
| 20 | [GIT-WORKFLOW](20-GIT-WORKFLOW.md) | Ветки (только `local` + `main`), commit правила |
| 30 | [TESTING](30-TESTING.md) | Стратегия, уровни, запуск тестов |
| 50 | [TROUBLESHOOTING](50-TROUBLESHOOTING.md) | Типовые проблемы и их решения |
| 80 | [ERROR-REGISTRY](80-ERROR-REGISTRY.md) | Реестр ошибок с root cause |
| 90 | [AI-AGENT-BEST-PRACTICES](90-AI-AGENT-BEST-PRACTICES.md) | Работа с AI-агентами + anti-patterns |
| — | [onboarding/](onboarding/) | Гайды для студента-форкера |

⚠️ **Этот шаблон без deploy:** `40-DEPLOY.md` оставлен от EMPTY_code,
но для test_code не релевантен (workflow `local` + `main`, без боевого окружения).
MCP-конфиг — в `_shared/mcp.yaml` (см. также `onboarding/claude-code-setup.md` и
`onboarding/codex-setup.md`).

## Жёсткое правило

```
❌ НЕ пиши в documentation/ то, что ещё не реализовано
   Используй _specs/ (для запланированного) или backlog/ (для идей)
```

## Связанные

- Родитель: [`../README.md`](../README.md)
- Что планируется: [`../_specs/`](../_specs/)
- Что в работе: [`../backlog/`](../backlog/)
- История релизов: [`../_changelogs/`](../_changelogs/)
- Состояние окружений: [`../_status/`](../_status/)
