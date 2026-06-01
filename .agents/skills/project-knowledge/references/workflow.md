# workflow.md — Git и deploy workflow

Last Updated: 2026-05-01

## Структура веток

```
local (разработка) → cherry-pick → dev (тестирование) → merge → prod (production)

main — заморожен (архив)
```

| Ветка | Назначение | Что коммитить |
|-------|------------|---------------|
| `local` | Рабочая ветка разработчика | Всё: код, specs, планы, TODO |
| `dev` | Тестовое окружение | Только рабочий код (завершённые фичи) |
| `prod` | Production | Только протестированный код |

## Critical-правило

**После ЛЮБОЙ операции (deploy, push, merge, cherry-pick) ВСЕГДА возвращайся на ветку `local`.**

Это гарантирует, что разработчик не «застрянет» на `dev`/`prod` после операционной задачи.

## 8 этапов разработки

| # | Этап | Артефакт | Где |
|---|------|----------|-----|
| 1 | Идея | сырая заметка | `backlog/ideas/` |
| 2 | План | бриф / спека | `backlog/briefs/` → `_specs/` |
| 3 | Разработка | код | `src/` |
| 4 | Feedback loop | lint + test (max 3 итерации) | `_practices/04-feedback-loop.md` |
| 5 | Ревью | агенты `code-reviewer` / `design-critic` | `.claude/agents/` |
| 6 | Документация | README, CHANGELOG | `_changelogs/`, `_status/` |
| 7 | Коммит | conventional message | skill `/commit` |
| 8 | Бэкап | push в GitHub | skill `/push` или `/backup` |

Подробности — в [`_practices/00-WORKFLOW.md`](../../../../_practices/00-WORKFLOW.md).

## Правила коммитов (для AI и разработчика)

1. **НЕ** делать commit/push/merge без подтверждения пользователя
2. **НЕ** делать force-push, `reset --hard`, rebase без явного запроса
3. **НЕ** коммитить секреты (`.env`, credentials, ключи)
4. **НЕ** использовать `git add -A` или `git add .` — добавлять файлы по отдельности
5. Conventional commits: `<type>(<scope>): <description>`
   - `feat:` новая фича
   - `fix:` исправление бага
   - `docs:` документация
   - `refactor:` рефакторинг без изменения поведения
   - `chore:` рутинные изменения
   - `release:` релиз с обновлением VERSION

## Деплой

### На DEV
```bash
./scripts/deploy-dev.sh
```
- Можно деплоить без явного подтверждения, если ветка `local` чистая
- После деплоя: `/qa-tester` → `/docs`

### На PROD
1. **НИКОГДА напрямую на PROD** — сначала DEV
2. Требуется ЯВНОЕ подтверждение пользователя
3. Workflow: `local → DEV → тест → PROD`
4. После деплоя: smoke-test + `/docs` + обновление `VERSION` + changelog

```bash
./scripts/deploy-prod.sh
```

## После каждого деплоя

1. Протестируй, что деплой работает (`./scripts/smoke-test.sh dev|prod`)
2. Запусти `/docs` для обновления документации
3. Обнови `VERSION` при значимых изменениях (semver)
4. Обнови changelog (`_changelogs/`)
5. Проверь синхронизацию веток
6. Вернись на `local`

## Связанные slash-команды

| Команда | Назначение |
|---------|-----------|
| `/commit` | AI-генерация commit message |
| `/push` | Безопасный push с превью |
| `/backup` | Быстрый бэкап (commit + push) |
| `/cherry-pick` | local → dev |
| `/merge-to-prod` | dev → prod (с подтверждением) |
| `/deploy-dev` | Деплой на DEV |
| `/deploy-prod` | Деплой на PROD (с safety checklist) |
| `/rollback` | Откат деплоя |
| `/git-status` | Статус всех веток |
| `/logs` | Логи DEV/PROD через SSH |

## Anti-patterns

- ❌ Force-push в `main` или в чужую ветку
- ❌ `git reset --hard` без бэкапа
- ❌ Коммит без сверки `git status`
- ❌ Деплой на PROD без предварительного тестирования на DEV
- ❌ Считать деплой завершённым, пока не выполнены все 6 шагов «после деплоя»
