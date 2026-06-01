# Wildberries — basics

Last Updated: 2026-05-29
Источник: [WB Открытая API documentation](https://docs.wildberries.ru/openapi)

## Модели работы

| Модель | Описание | Когда выбирать |
|--------|----------|----------------|
| **FBO** (Fulfillment By Operator) | Товар на складе WB, WB упаковывает и отправляет | Большой ассортимент, отлаженные продажи |
| **FBS** (Fulfillment By Seller) | Товар на складе селлера, селлер упаковывает, WB забирает курьером | Тестирование новых SKU, небольшой стартовый ассортимент |
| **realFBS** | Селлер сам доставляет до клиента | Уникальные / габаритные товары |

## Базовые тарифы (2026, ориентировочно)

- **Комиссия WB:** 14-19% от цены товара (зависит от категории)
- **Логистика FBO:** ~30-50 руб/единица в одну сторону
- **Логистика FBS приёмка:** ~5-15 руб/единица
- **Хранение FBO:** 0.5-2 руб/единица/день (выше для крупногабарита)
- **Эквайринг:** ~1.5% (стандарт для маркетплейсов)
- **Возвраты:** 40-80 руб/возврат (логистика обратно + переупаковка)

⚠️ Тарифы регулярно меняются. Актуальные → [тарифы WB Seller](https://seller.wildberries.ru/) → Финансы → Тарифы.

## API

### Базовые группы

| Группа | Назначение | Документация |
|--------|------------|---------------|
| **Seller API** | Управление товарами, заказами | [docs.wildberries.ru](https://docs.wildberries.ru/openapi) |
| **Statistics API** | Продажи, остатки, история | [Statistics API](https://openapi.wildberries.ru/statistics/api/ru/) |
| **Advertising API** | Управление рекламными кампаниями | [Advertising API](https://dev.wildberries.ru/openapi/advertisement) |
| **Content API** | Управление карточками | [Content API](https://dev.wildberries.ru/openapi/api-information) |
| **Marketplace API** | FBS-заказы | [Marketplace API](https://openapi.wildberries.ru/marketplace/api/ru/) |

### Аутентификация

WB использует **JWT-токены** в HTTP header `Authorization`:

```http
GET /api/v1/supplier/sales HTTP/1.1
Host: statistics-api.wildberries.ru
Authorization: eyJhbGciOiJFUzI1NiIs...
```

Токен генерируется в ЛК WB → Профиль → Доступ к API. Один токен — все API.

### Rate limits

- Statistics API: **1 запрос/секунду** на токен
- Seller API: **до 10 RPS** (зависит от эндпоинта)
- Большие выгрузки — пагинация через `dateFrom`/`dateTo`

См. правило `marketplace-data-freshness.md` про обновление кеша.

## Особенности

- **Карточка товара:** 5 фото + 3 видео + описание (до 5000 символов)
- **Маркировка ЧЗ:** обязательна для одежды/обуви/парфюма/шин/духов/фотокамер
- **Сертификация:** проверять через `_modules/06-certification-legal/`
- **Возвраты:** ~40-60% в категории одежда, ~10-20% в FMCG (зависит от категории)
- **СПП (скидка постоянного покупателя):** 4-20% от продажи. Влияет на маржу!

## Best practices (FREE basics)

1. **A/B-тест фото №1** — рост CTR с первой фотки на 30-50%
2. **Описание SEO** — насыщенное ключами + читаемое (использовать `/lawyer` для соответствия ЗоЗПП)
3. **Управление остатками** — не дать товару попасть в категорию «нет в наличии» > 3 дня (падение рейтинга)
4. **Реклама:** для нового SKU — рекламируй первые 30 дней (поднять позицию органики)

## 📈 Углубление в `vibecommerce_vip_code`

- Полные стратегии под каждую категорию
- Бенчмарки маржинальности
- **`marketplace-discounts-guide.md`** — детально про СПП, соинвест, спецусловия WB
- Особенности API workaround'ы, неочевидные эндпоинты

## Связанные

- Модуль: [`../../_modules/02-unit-economics/`](../../_modules/02-unit-economics/) (юнит-экономика WB)
- Модуль: [`../../_modules/03-marketplace-analytics/`](../../_modules/03-marketplace-analytics/) (MPStats аналитика)
- Rule: [`../../.claude/rules/marketplace-data-freshness.md`](../../.claude/rules/marketplace-data-freshness.md)
