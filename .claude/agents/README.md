# `.claude/agents/` — субагенты Claude Code

Last Updated: 2026-05-02

## Что здесь

Описания восьми специализированных субагентов (все с `model: inherit` —
наследуют модель родительской сессии):

**Quality / Testing:**
- `code-reviewer.md` — ревью кода на баги, логику, security, конвенции
- `test-runner.md` — автотесты (lint, types, unit, build, pytest markers, data pipeline)
- `techdebt-scanner.md` — поиск технического долга (TODO/FIXME, размеры, deps, дубли)

**Documentation / Design:**
- `docs-generator.md` — генерация документации после деплоя (5 файлов: status, pending, dev-status, error-registry, changelog)
- `design-critic.md` — ревью дизайн-системы (consistency, a11y)

**Domain experts:**
- `lawyer.md` — юрист РФ (коммерция+IT), B2C/ЗоЗПП/152-ФЗ
- `seo-auditor.md` — SEO+AEO аудит (technical + on-page + Schema.org)
- `web-researcher.md` — структурированный интернет-ресёрч с источниками

## Зачем

Субагенты — это «специалисты», которые Claude Code запускает в отдельном
контексте. Их роль — изолировать узкую задачу (ревью, деплой, тесты)
от основного диалога, чтобы не загрязнять контекст.

## Как пользоваться

- Файлы в формате `<name>.md` с YAML-фронтматтером и описанием
- Запуск через `subagent_type: "<name>"` в Agent tool
- Триггеры описаны в каждом файле в секции `description`

## Связанные

- Родитель: [`../README.md`](../README.md)
- Скиллы: [`../skills/README.md`](../skills/README.md)
- Правила: [`../rules/README.md`](../rules/README.md)
