# PRJ_ANALYTICS — Аналитика и отчёты

Last Updated: 2026-02-20

## Описание
Проект по аналитике: сводные отчёты, дашборды, unit-экономика, когортный анализ.

## Структура
```
PRJ_ANALYTICS/
├── README.md
└── mpstats/                  # Интеграция с MPStats API (Ozon, WB, YM)
    ├── PLAN.md               # План интеграции и справка по API
    ├── README.md             # Документация по использованию
    ├── client.py             # HTTP-клиент (sync, httpx, retry)
    ├── models.py             # Модели данных
    ├── check_limit.py        # Проверка API
    ├── analyze_sku.py        # Анализ товара по ID
    ├── analyze_category.py   # Анализ категории
    └── explore_ym.py         # Исследование YM-эндпоинтов
```

## Связанные проекты
- [REF: PRJ_MARKETPLACE/FACTS.md] — метрики маркетплейсов
- [REF: PRJ_DTC/FACTS.md] — метрики D2C
- [REF: backlog/Backlog.txt] — задачи по проекту (PRJ = ANALYTICS)
