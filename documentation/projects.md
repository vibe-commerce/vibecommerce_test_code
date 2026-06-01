# Структура проектов

Last Updated: 2026-06-02

> С версии 0.3.0 старые папки `PRJ_*` (личные проекты автора) **удалены** по
> Принципу №0 (pure template) и заменены на структуру EMPTY_code:
> **`_modules/`** (методички, read-only) + **`my-project/`** (рабочая зона студента).
> Ниже — куда переехало содержимое прежних `PRJ_*`.

## Где теперь что (миграция PRJ_* → _modules/)

| Было (`PRJ_*`) | Стало | Что внутри |
|----------------|-------|------------|
| `PRJ_ВЫБОР_НИШИ` | [`_modules/01-niche-selection/`](../_modules/01-niche-selection/) | план выбора ниши, демо-CSV Ozon, `add_buyback_rate.py` |
| `PRJ_MARKETPLACE` | [`_modules/05-ads-optimization/`](../_modules/05-ads-optimization/) | ABCDX, воронка, генераторы демо-данных (`data-demo/`) |
| `PRJ_ANALYTICS` | [`_modules/03-marketplace-analytics/`](../_modules/03-marketplace-analytics/) | MPStats-клиент (`mpstats/`), модель ДДС (`cashflow/`) |
| `PRJ_ВОРОНКА` | [`_modules/04-funnel-jtbd/`](../_modules/04-funnel-jtbd/) + [`_prompts/jtbd/`](../_prompts/jtbd/) | JTBD-методика и промпт-карточки |
| `PRJ_DEMO` / `PRJ_DTC` | — | демо-финмодели и D2C-заготовки убраны (личные данные автора) |

## Как работать со своим проектом

Один форк = **один проект селлера** в [`my-project/`](../my-project/). Подпапки
`00-niche`…`06-finance` соответствуют 7 модулям. Методику бери из `_modules/`,
результаты складывай в `my-project/` (свои выгрузки — в `my-project/data/`,
gitignored).

См. [`../my-project/README.md`](../my-project/README.md) — карта рабочей зоны.

## Связанные

- Методические модули: [`../_modules/README.md`](../_modules/README.md)
- Рабочая зона студента: [`../my-project/README.md`](../my-project/README.md)
- История миграции: [`../_changelogs/CHANGELOG.md`](../_changelogs/CHANGELOG.md) (0.3.0)
