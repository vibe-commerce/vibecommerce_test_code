# `_specs/templates/` — шаблоны спецификаций и lifecycle-документов

Last Updated: 2026-05-02

## Что здесь

Шаблоны для двух разных слоёв:

1. **Lifecycle-документы** в `backlog/`: `brief.md`, `plan.md`,
   `rejected.md` — для прохождения цепочки `ideas → briefs → plans →
   archive`.
2. **Spec-driven документы** в `_specs/<feature>/`: `user-spec.md`,
   `tech-spec.md`, `task.md`, `ADR-template.md` — для крупных фич,
   когда план уже согласован и нужны архитектурные спецификации.

Копируй нужный шаблон, заполняй.

### Lifecycle-документы (для `backlog/`)

| Шаблон | Куда копировать | Когда использовать |
|--------|-----------------|--------------------|
| `brief.md` | `backlog/briefs/<date>-<slug>.md` | Идея созрела до приоритизации (зачем / scope / AC) |
| `plan.md` | `backlog/plans/<date>-<slug>.md` | Бриф согласован, пора расписывать как делать (подход / чек-лист / риски) |
| `rejected.md` | `backlog/archive/rejected/<slug>.md` | Решили не делать — фиксируем «почему» и триггеры пересмотра |

### Spec-driven документы (для `_specs/<feature>/`)

| Шаблон | Назначение | Когда использовать |
|--------|------------|--------------------|
| `user-spec.md` | Требования глазами пользователя (русский, для людей) | Крупная фича: после плана, перед tech-spec |
| `tech-spec.md` | Технический план (для агентов) | Крупная фича: после одобрения user-spec |
| `task.md` | Атомарная единица работы с TDD-якорями | После декомпозиции tech-spec |
| `task-decomposition.md` | Разбивка большой задачи на task-ы | Когда task > 1 дня работы |
| `skill-playbook.md` | Шаблон для нового skill | Перед созданием skill |
| `design-system.md` | Шаблон для дизайн-токенов | При создании новой темы |
| `ADR-template.md` | Architecture Decision Record | При значимом архитектурном решении |

## Workflow

```
backlog/ideas/ → brief.md (приоритизация) → plan.md (исполнение) → код
                                                  ↓ если фича крупная
                                       _specs/<feature>/{user-spec, tech-spec, task-N}
```

Чек-лист задач живёт **только** в `plan.md` (или в `task-N.md` для крупных
фич). В `brief.md` чек-листа быть не должно — это сигнал, что пора
создавать `plan.md`.

## Связанные

- Родитель: [`../README.md`](../README.md)
- Источник: адаптировано из [molyanov-ai-dev](https://github.com/nickspaargaren/molyanov-ai-dev) (MIT)
