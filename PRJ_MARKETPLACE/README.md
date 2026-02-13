# PRJ_MARKETPLACE — Работа с маркетплейсами

Last Updated: 2026-02-13

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

## Связь между файлами
Файлы `sales_data` и `ads_data` связаны по ключу **(Неделя, SKU, Площадка)**.
Совпадающие поля: Заказы (шт), Цена (₽), Выручка (₽), Расход на рекламу (₽).

## Связанные проекты
- [REF: PRJ_ANALYTICS/] — общая аналитика
- [REF: backlog/Backlog.txt] — задачи по проекту (PRJ = MARKETPLACE)
