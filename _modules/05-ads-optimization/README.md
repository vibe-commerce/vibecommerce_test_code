# 05 — Оптимизация рекламы

Last Updated: 2026-05-29

## Главный вопрос

«Куда вкладывать рекламный бюджет?» — приоритизация SKU по ABCDX, анализ
воронки рекламной кампании, оптимизация ставок.

## Что внутри (FREE)

### Демо-данные

- `data-demo/sales_data_v1.0.xlsx` — синтетические продажи 50 SKU «товары для сна»
- `data-demo/ads_data_v1.0.xlsx` — синтетические рекламные данные (показы/клики/расходы)
- `data-demo/ads_data_v2.0.xlsx` — обновлённая версия v2

> `# DEMO DATA — synthetic via generate_*.py with random.seed(42). 50 SKU
> "товары для сна" × 2 площадки (WB+Ozon) × 12 недель. Not real seller data.`

### Скрипты

- `scripts/abcdx_analysis.py` — ABCDX-классификация SKU:
  - **A** — топ-20% по выручке (звёзды)
  - **B** — следующие 30% (стабильные)
  - **C** — длинный хвост 50% (массовые)
  - **D** — убыточные (отрицательная маржа)
  - **X** — мёртвый сток (без продаж >30 дней)
- `scripts/funnel_analysis.py` — анализ воронки конверсии: показы → клики → корзина → продажа
- `scripts/generate_sales_data.py` — генератор синтетических продаж (`random.seed(42)`)
- `scripts/generate_ads_data.py` — генератор синтетических рекламных данных

## Базовый workflow

Все скрипты пишут/читают в `data-demo/` (рядом со `scripts/`). Порядок важен:
ABCDX читает `ads_data_v1.0.xlsx`, funnel читает `ads_data_v2.0.xlsx`
(результат ABCDX) + `sales_data_v1.0.xlsx`.

```
1. python scripts/generate_sales_data.py  # → data-demo/sales_data_v1.0.xlsx
2. python scripts/generate_ads_data.py    # → data-demo/ads_data_v1.0.xlsx
3. python scripts/abcdx_analysis.py       # ads_data_v1.0 → data-demo/ads_data_v2.0.xlsx (ABCDX)
4. python scripts/funnel_analysis.py      # ads_data_v2.0 + sales → data-demo/analysis_output/
5. Перенести логику на свои данные → my-project/04-ads/
```

## Чек-лист «модуль закрыт»

- [ ] Своя продажная история разложена по ABCDX
- [ ] Идентифицированы 5-10 SKU группы A для усиления рекламы
- [ ] Идентифицированы SKU группы X для распродажи/выноса
- [ ] План перераспределения рекламного бюджета
- [ ] Сохранён результат в `../my-project/04-ads/`

## 📈 Углубление в `vibecommerce_vip_code`

- **ABCDX advanced** — с учётом сезонности, оборачиваемости остатков, риска
- **Сценарии репрайсинга** — что будет с маржой при разных уровнях ДРР
- **Multi-SKU оптимизация** — портфельный подход к рекламному бюджету
- **Интеграция с `mpstats-pricing-logic`** rule

## Связанные

- Skill: `/mpstats-analyst` (для интеграции с MPStats)
- Модуль: [`../02-unit-economics/`](../02-unit-economics/) (для расчёта BEP по группам)
- Рабочая зона: [`../../my-project/04-ads/`](../../my-project/04-ads/)
