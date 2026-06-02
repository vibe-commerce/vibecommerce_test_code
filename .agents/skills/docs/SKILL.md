---
name: docs
description: Обновление документации после деплоя — _status/ файлы, changelogs, architecture docs, error registry. Используй при docs, обновить документацию, после деплоя, update docs.
---

# /docs — Documentation Update (entry-point)

> ⚠️ DEV/PROD-режим ниже — для форков с боевым деплоем. В **базовом шаблоне**
> деплой-окружений нет (CLAUDE.md: «В шаблоне НЕТ DEV/PROD»); тогда `/docs`
> обновляет только `_status/PROJECT_STATUS.md`, `_changelogs/CHANGELOG.md`, `documentation/`.

Тонкий entry-point. Полный workflow обновления документации живёт в саб-агенте
`docs-generator` — он читает много файлов (коммиты, status-файлы, registry)
и поэтому изолируется в отдельный контекст.

## Instructions

### 1. Определи окружение

Спроси пользователя или выведи из контекста:
- `DEV` — обновить `_status/DEV.md`, `PENDING_RELEASE.md`, `DEVELOPMENT_STATUS.md`
- `PROD` — то же + `_status/PROD.md` + `_changelogs/prod.md`
- `both` — обновить оба окружения

При деплое только что — env обычно ясен из контекста (последняя команда
`/deploy-dev` → DEV, `/deploy-prod` → PROD).

### 2. Узнай был ли багфикс

Проверь коммиты с прошлого релиза:
```bash
git log $(cat VERSION)..HEAD --oneline 2>/dev/null | grep -iE "fix|bugfix"
```

Если есть — передай агенту флаг «обновить ERROR_REGISTRY».

### 3. Делегируй `docs-generator` через Agent tool

```
Agent tool:
  subagent_type: docs-generator
  description: Update docs for <env> deploy
  prompt: "env=<DEV|PROD|both>, bugfix=<true|false>, version=<VERSION>"
```

Агент обновит до 5 файлов: `_status/{ENV}.md`, `PENDING_RELEASE.md`,
`DEVELOPMENT_STATUS.md`, `ERROR_REGISTRY.md` (если bugfix), `_changelogs/{env}.md`
(если PROD).

### 4. Передай отчёт пользователю

Перепиши кратко:
```
## Documentation Updated

| File | Changes |
|------|---------|
| _status/{ENV}.md | <one-line> |
| ... | ... |
```

## Правила

1. Перед делегацией убедись, что `VERSION` обновлён (это ответственность
   `/deploy-prod` или вручную) — иначе changelog получит неправильную метку
2. Не предлагай делать deploy и docs одновременно — это два шага
3. Если агент сообщил, что нет изменений с прошлого деплоя — не создавай
   пустых записей
