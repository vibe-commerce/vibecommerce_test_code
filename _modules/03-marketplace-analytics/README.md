# 03 — Marketplace-аналитика

Last Updated: 2026-05-29

## Главный вопрос

«Что происходит на рынке?» — анализ категории, конкурентов, динамики
продаж, сезонности через MPStats API.

## Что внутри (FREE)

### Демо-данные

- `mpstats/sleep_market_research.xlsx` — открытый MPStats research товарной категории «для сна»
- `mpstats/march8_gift_research.xlsx` — открытый MPStats research категории подарков к 8 марта
- `cashflow/cashflow_model.xlsx` — модель cashflow для селлера

> `# DEMO DATA — открытые MPStats research-выгрузки. Рыночные данные категорий,
> не привязано к конкретному селлеру.`

### Скрипты (basic)

- `mpstats/research_*.py` — скрипты для базового MPStats research (single-niche).
  ⚠️ Требуют `MPSTATS_API_KEY` в `.env`.
- `cashflow/build_cashflow.py` *(в работе)* — построение cashflow-модели
  по продажам и расходам

## Skill

- `/mpstats-analyst` (basic) — 2 базовых метода: `get_category_summary`, `get_top_products`
- `/mpstats-research` (basic) — single-niche analysis (top-10 конкурентов + базовая статистика)

## Чек-лист «модуль закрыт»

- [ ] Запущен `/mpstats-research` для своей категории → получен top-10 конкурентов
- [ ] Построен cashflow-модель за прошлые 12 месяцев + прогноз 6 месяцев вперёд
- [ ] Найдены сезонные пики (по неделям)
- [ ] Сохранён результат в `../my-project/02-analytics/`

## 📈 Углубление в `vibecommerce_vip_code`

- **`mpstats-analyst` PRO** — полные ~80 методов: ABCDX, cohort-анализ,
  сезонность multi-year, репрайсинг
- **`mpstats-research` PRO** — batch pipeline для multi-niche, конкурентный
  landscape, retention-метрики
- **Cashflow advanced** — multi-currency, FX-риски, налоговая оптимизация cashflow
- **Sub-agent `niche-researcher`** + `shopping-researcher` (batch поиск товаров)

## Связанные

- Skill: `/mpstats-analyst` (basic, hybrid), `/mpstats-research` (basic, hybrid)
- Rule: [`../../.claude/rules/marketplace-data-freshness.md`](../../.claude/rules/marketplace-data-freshness.md)
- Рабочая зона: [`../../my-project/02-analytics/`](../../my-project/02-analytics/)
