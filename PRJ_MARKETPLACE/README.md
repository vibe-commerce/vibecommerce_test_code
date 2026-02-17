# PRJ_MARKETPLACE — Работа с маркетплейсами

Last Updated: 2026-02-17

## Описание
Проект по работе с маркетплейсами: WB, OZON, Яндекс.Маркет и др.

## Структура
- [FACTS.md](FACTS.md) — ключевые метрики, контакты, реквизиты
- [sales_data_v1.0.xlsx](sales_data_v1.0.xlsx) — тестовый датасет продаж (50 SKU, 12 недель, WB+Ozon) [CANONICAL]
- [ads_data_v1.0.xlsx](ads_data_v1.0.xlsx) — рекламные и трафиковые данные v1 [CANONICAL]
- [ads_data_v2.0.xlsx](ads_data_v2.0.xlsx) — рекламные и трафиковые данные v2
- [abcdx_analysis.py](abcdx_analysis.py) — скрипт ABCDX-анализа ассортимента
- [generate_sales_data.py](generate_sales_data.py) — скрипт генерации датасета продаж
- [generate_ads_data.py](generate_ads_data.py) — скрипт генерации рекламных данных
- [funnel_analysis.py](funnel_analysis.py) — анализ воронки продаж (Показы→Клики→Корзина→Заказы)
- [analysis_output/](analysis_output/) — результаты анализов (графики PNG, отчёты Excel)

## Связь между файлами
Файлы `sales_data` и `ads_data` связаны по ключу **(Неделя, SKU, Площадка)**.
Совпадающие поля: Заказы (шт), Цена (₽), Выручка (₽), Расход на рекламу (₽).

## Анализ воронки продаж

Скрипт `funnel_analysis.py` анализирует воронку Показы → Клики → Корзина → Заказы по 50 SKU на WB и Ozon за 12 недель. Результат:
- `analysis_output/funnel_report.xlsx` — Excel-отчёт (8 листов: воронка по SKU, WB vs Ozon, категории, рекламная эффективность, динамика, трафик vs прибыль, проблемные SKU, рекомендации)
- `analysis_output/06-13_*.png` — 8 графиков (воронка, тепловая карта, scatter-плоты, тренды)

Запуск: `uv run --with openpyxl --with matplotlib PRJ_MARKETPLACE/funnel_analysis.py`

## Связанные проекты
- [REF: PRJ_ANALYTICS/] — общая аналитика
- [REF: backlog/Backlog.txt] — задачи по проекту (PRJ = MARKETPLACE)
