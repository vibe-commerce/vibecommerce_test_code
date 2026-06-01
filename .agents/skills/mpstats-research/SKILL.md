---
name: mpstats-research
description: "BASIC. Single-niche ресёрч через MPStats API — топ-10 конкурентов + базовая статистика категории. Поддержка Ozon, WB, ЯМ. Для multi-niche batch pipeline — VIP-репо."
argument-hint: "[название ниши/рынка для исследования]"
---

# MPStats Market Research (BASIC)

Базовое исследование рынка по **одной категории** на маркетплейсе.

## Что доступно в FREE

Single-niche анализ:

1. **Базовая статистика категории** (GMV, кол-во продавцов, медианная цена)
2. **Топ-10 конкурентов** (по выручке)
3. **Базовый отчёт** в Markdown (.md)

## Скрипты

В `_modules/03-marketplace-analytics/mpstats/`:

```bash
# Single-niche basic research
uv run --with httpx,python-dotenv _modules/03-marketplace-analytics/mpstats/research_sleep.py
```

Адаптируй `research_*.py` под свою категорию: замени URL категории и название.

## Требования

- `MPSTATS_API_KEY` в `.env`
- Подписка MPStats (любой тариф)

## Связанные

- `/mpstats-analyst` — basic анализ конкретного товара/категории
- `_modules/03-marketplace-analytics/` — методический модуль

## 📈 Полная версия — в VIP-репо `vibecommerce_vip_code`

**PRO-версия даёт:**

- **Batch pipeline** для multi-niche (десятки категорий одновременно)
- **Конкурентский landscape** — детальная разбивка топ-50 продавцов с историей
- **Retention-метрики** по когортам товаров
- **Pivot-сравнения** между площадками (WB vs Ozon vs ЯМ)
- **Автоматический поиск** растущих ниш с низкой конкуренцией
- **Sub-agent `niche-researcher`** — полный цикл от лонг-листа до решения

Подключение → `documentation/onboarding/vip-setup.md`.
