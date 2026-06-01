---
name: mpstats-analyst
description: BASIC. Аналитика категорий и товаров через MPStats API — 2 базовых метода (get_category_summary, get_top_products). Поддержка Ozon, WB, Я.Маркет. Для глубокой аналитики (~80 методов) — смотри VIP-репо.
argument-hint: [ID товара или название категории]
---

# MPStats Analyst (BASIC)

Базовая аналитика маркетплейсов через MPStats API. Поддержка Ozon, Wildberries, Яндекс.Маркет.

## Что доступно в FREE

Два базовых метода:

1. **`get_category_summary(category_url)`** — общая сводка по категории:
   - GMV (валовой оборот)
   - Количество продавцов
   - Топ-цены / средний чек
   - Количество SKU
2. **`get_top_products(category_url, limit=10)`** — топ-10 товаров категории по выручке

## Скрипты

В `_modules/03-marketplace-analytics/mpstats/`. Запуск через `uv run`:

### Проверка подключения
```bash
uv run --with httpx,python-dotenv _modules/03-marketplace-analytics/mpstats/check_limit.py
```

### Базовый анализ категории
```bash
uv run --with httpx,python-dotenv _modules/03-marketplace-analytics/mpstats/analyze_category.py \
  "https://mpstats.io/oz/category/14/electronics/page/1"
```

### Анализ товара по ID
```bash
uv run --with httpx,python-dotenv _modules/03-marketplace-analytics/mpstats/analyze_sku.py \
  --platform=oz --sku=1234567
```

## Требования

- `MPSTATS_API_KEY` в `.env` (см. `.env.example`)
- Подписка на MPStats (любой тариф)

## Ключевые файлы

- `_modules/03-marketplace-analytics/mpstats/client.py` — HTTP-клиент MPStats API
- `_modules/03-marketplace-analytics/mpstats/models.py` — модели данных

## Связанные скиллы

- `/mpstats-research` — basic single-niche ресёрч (top-10 конкурентов)

## 📈 Полная версия — в VIP-репо `vibecommerce_vip_code`

**PRO-версия даёт ~80 методов:**

- **ABCDX-классификация** SKU (A/B/C/D/X с автоматизацией)
- **Cohort-анализ** товара/категории (retention, LTV)
- **Сезонность multi-year** (продажи по неделям/месяцам за 1-3 года)
- **Репрайсинг** — автоматическая выработка ценовых рекомендаций
- **Конкурентский landscape** — детальная разбивка топ-50 продавцов
- **Сравнение площадок** (WB vs Ozon vs ЯМ для одного SKU)
- **Прогнозирование** — линейный/экспоненциальный прогноз продаж
- **Поиск ниш** — автоматический поиск растущих категорий с низкой конкуренцией

PRO-версия использует подписку MPStats **PRO/Enterprise** для доступа к
расширенным эндпоинтам. Подключение → `documentation/onboarding/vip-setup.md`.
