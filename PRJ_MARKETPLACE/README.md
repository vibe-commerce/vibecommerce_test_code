# PRJ_MARKETPLACE — Работа с маркетплейсами

Last Updated: 2026-02-12

## Описание
Проект по работе с маркетплейсами: WB, OZON, Яндекс.Маркет и др.

## Структура
- [FACTS.md](FACTS.md) — ключевые метрики, контакты, реквизиты
- [sales_data_v1.0.xlsx](sales_data_v1.0.xlsx) — тестовый датасет продаж (50 SKU, 12 недель, WB+Ozon)
- [ads_data_v1.0.xlsx](ads_data_v1.0.xlsx) — рекламные и трафиковые данные (мэтчатся с sales_data)
- [generate_sales_data.py](generate_sales_data.py) — скрипт генерации датасета продаж
- [generate_ads_data.py](generate_ads_data.py) — скрипт генерации рекламных данных

## Ключевые файлы
- [FACTS.md](FACTS.md) — факты и цифры по маркетплейсам
- [sales_data_v1.0.xlsx](sales_data_v1.0.xlsx) — история продаж за 3 месяца [CANONICAL]
- [ads_data_v1.0.xlsx](ads_data_v1.0.xlsx) — трафик, реклама, ДРР, ROAS [CANONICAL]

## Связь между файлами
Файлы `sales_data` и `ads_data` связаны по ключу **(Неделя, SKU, Площадка)**.
Совпадающие поля: Заказы (шт), Цена (₽), Выручка (₽), Расход на рекламу (₽).

## Связанные проекты
- [REF: PRJ_ANALYTICS/] — общая аналитика
- [REF: backlog/Backlog.txt] — задачи по проекту (PRJ = MARKETPLACE)
