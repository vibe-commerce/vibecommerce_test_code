---
name: mpstats-analyst
description: Аналитика товаров и категорий через MPStats API (Ozon, Wildberries, Яндекс Маркет). Анализ товара по ID, анализ категории, проверка лимитов API, исследование эндпоинтов.
argument-hint: [ID товара или название категории]
---

# MPStats Analyst

Аналитика маркетплейсов через MPStats API. Поддержка Ozon, Wildberries, Яндекс Маркет.

## Скрипты

Все скрипты в `PRJ_ANALYTICS/mpstats/`. Запуск через `uv run`.

### Проверка подключения
```bash
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/check_limit.py
```

### Анализ товара по ID
```bash
# Ozon (по умолчанию)
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/analyze_sku.py <ID>

# Wildberries
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/analyze_sku.py <ID> --platform wb

# С контекстом ниши
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/analyze_sku.py <ID> --niche

# Экспорт в Excel
uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/analyze_sku.py <ID> --xlsx report.xlsx
```

### Анализ категории
```bash
# Ozon
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/analyze_category.py "Электроника/Смартфоны"

# WB с периодом 60 дней
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/analyze_category.py "Электроника" --platform wb --days 60

# Экспорт в Excel
uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/analyze_category.py "Электроника" --xlsx report.xlsx
```

### Исследование Яндекс Маркет
```bash
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/explore_ym.py
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/explore_ym.py --item 12345
```

## Процесс работы

1. Убедись что `MPSTATS_API_KEY` задан в `.env` (проверь через `check_limit.py`)
2. Определи задачу: анализ товара или категории
3. Выбери платформу: `oz` (Ozon), `wb` (Wildberries), `ym` (Яндекс Маркет)
4. Запусти соответствующий скрипт
5. Интерпретируй результат для пользователя

## Ключевые файлы

- `PRJ_ANALYTICS/mpstats/client.py` — HTTP-клиент MPStats API
- `PRJ_ANALYTICS/mpstats/models.py` — модели данных
- `PRJ_ANALYTICS/mpstats/PLAN.md` — план интеграции и справка по API

## Связанные скиллы

- `/mpstats-research` — исследование рынка (несколько категорий на нескольких МП, сводный отчёт)
