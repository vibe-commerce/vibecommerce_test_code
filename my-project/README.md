# `my-project/` — рабочая зона студента

Last Updated: 2026-05-29

## Что здесь

Это твоя личная песочница для применения методик из [`_modules/`](../_modules/)
к **своему проекту селлера** (своя ниша, ассортимент, экономика).

Все 7 подпапок соответствуют 7 модулям. Складывай туда результаты работы.

## Структура

| Подпапка | Соответствует модулю | Что складывать |
|----------|----------------------|----------------|
| [`00-niche/`](00-niche/) | `_modules/01-niche-selection/` | Гипотезы ниш, скоринг, отобранная ниша |
| [`01-unit-economy/`](01-unit-economy/) | `_modules/02-unit-economics/` | Расчёты по своим SKU, юнит-калькулятор |
| [`02-analytics/`](02-analytics/) | `_modules/03-marketplace-analytics/` | Аналитика своей категории / своих конкурентов |
| [`03-funnel/`](03-funnel/) | `_modules/04-funnel-jtbd/` | JTBD-карточки своих сегментов, воронки |
| [`04-ads/`](04-ads/) | `_modules/05-ads-optimization/` | ABCDX по своему ассортименту, рекламные кампании |
| [`05-legal/`](05-legal/) | `_modules/06-certification-legal/` | Сертификация своих товаров, юридические требования |
| [`06-finance/`](06-finance/) | `_modules/07-financial-reporting/` | Свой P&L, ДДС, баланс |
| [`data/`](data/) | для всех модулей | Твои выгрузки (CSV, xlsx) — **gitignored по умолчанию** |
| [`reports/`](reports/) | для всех модулей | Финальные отчёты по проекту |

## Правила работы

1. **Не редактируй `_modules/`** — копируй файлы оттуда сюда и работай с копией
2. **Свои данные** (выгрузки WB/Ozon, отчёты MPStats, продажи) — кладёшь только
   в `my-project/data/` или `my-project/<номер>/data/`. Это gitignored — не уйдёт в публику.
3. **Реквизиты и токены** — НИКОГДА не сюда. Это [`../_private/secrets/`](../_private/)
   (gitignored полностью).
4. **Личные данные** — файлы с префиксом `personal-` тоже gitignored
   (`my-project/**/personal-*`).

## Quick start: первая итерация

```
1. Прочитай _modules/README.md — выбери первый модуль (обычно 01-niche-selection)
2. Прочитай _modules/01-niche-selection/README.md — методика 3-фазная (FREE)
3. Скопируй шаблон скоринг-матрицы из _modules/01-.../templates/ → my-project/00-niche/
4. Запусти скоринг по своим гипотезам ниш
5. Сохрани результат в my-project/reports/01-niche-selection-{date}.md
```

## Что НЕ кладётся в `my-project/`

- ❌ Боевые API-токены → [`../_private/secrets/`](../_private/)
- ❌ Личные документы (паспорта, договоры) → [`../_private/docs/`](../_private/)
- ❌ Реквизиты клиентов / партнёров → [`../_private/docs/`](../_private/)
- ❌ Промпты-роли (это общий контент) → [`../_prompts/`](../_prompts/)
- ❌ Справочники по WB/Ozon/закону (общий контент) → [`../_knowledge/`](../_knowledge/)

## Связанные

- Методические модули: [`../_modules/README.md`](../_modules/README.md)
- Knowledge base: [`../_knowledge/`](../_knowledge/)
- Промпты: [`../_prompts/`](../_prompts/)
- Приватные данные: [`../_private/`](../_private/)
