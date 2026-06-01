# `_specs/` — спецификации крупных фич

Last Updated: 2026-05-29

## Что здесь

Архитектурные и продуктовые спецификации **крупных фич** (>3 дней
работы, нужны tech-spec / user-spec / ADR).

С 0.5.0 `_specs/` **больше не подменяет** план реализации. План-чек-лист
живёт только в [`backlog/plans/<slug>.md`](../backlog/plans/) — даже
для крупных фич; рядом с ним в `_specs/<feature>/` живут спецификации.

## Когда заводить `_specs/<feature>/`

- Фича достаточно крупная, чтобы потребовать tech-spec, user-spec или ADR.
- Или есть значимое архитектурное решение, которое нужно зафиксировать
  в ADR.

Признаки, что `_specs/<feature>/` **не нужен**:
- План вмещается в чек-лист `backlog/plans/<slug>.md` (≤3 дней работы).
- Архитектурные решения тривиальны или уже описаны в `documentation/`.
- Изменение касается одного слоя без новых интеграций.

## Структура

| Файл / папка | Описание |
|--------------|----------|
| [`templates/`](templates/) | Шаблоны user-spec, tech-spec, task, ADR + lifecycle-шаблоны brief / plan / rejected |
| [`design/`](design/) | Цветовые темы и `THEMES.md` |
| [`codex-compat/`](codex-compat/) | Спецификация cross-agent совместимости Claude Code + OpenAI Codex |

## Связь с `backlog/`

```
backlog/briefs/<slug>.md   ← зачем / стоит ли делать
backlog/plans/<slug>.md    ← как делать (чек-лист, риски)
_specs/<feature>/          ← архитектура (tech-spec, user-spec, ADR)
   ├── user-spec.md
   ├── tech-spec.md
   ├── ADR-001-<topic>.md
   └── task-N.md (если декомпозиция)
```

План в `backlog/plans/` ссылается на `_specs/<feature>/`. Спецификации
**не дублируют** «зачем» из брифа и «чек-лист» из плана — только
архитектура и решения.

## Жёсткие правила

```
❌ НЕ держи в _specs/ план реализации (plan.md, чек-лист, шаги)
   — это только в backlog/plans/<slug>.md
❌ НЕ держи в _specs/ то, что ещё в backlog/ без одобрения
✅ Реализованное — переноси факты в documentation/
✅ Старые / заменённые спеки — в _specs/archive/
```

## Связанные

- Родитель: [`../README.md`](../README.md)
- Идеи / брифы / планы: [`../backlog/README.md`](../backlog/README.md)
- Шаблоны (lifecycle + spec): [`templates/README.md`](templates/README.md)
- Реализованные факты: [`../documentation/`](../documentation/)
- Cross-agent spec: [`codex-compat/README.md`](codex-compat/README.md)
