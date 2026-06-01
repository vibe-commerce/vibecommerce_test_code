# Ozon — basics

Last Updated: 2026-05-29
Источник: [Ozon API documentation](https://docs.ozon.ru/api/seller/)

## Модели работы

| Модель | Описание | Когда выбирать |
|--------|----------|----------------|
| **FBO** | Товар на складе Ozon | Большие объёмы, отлаженные SKU |
| **FBS** | Товар на складе селлера, Ozon забирает | Средний оборот |
| **realFBS Standard** | Селлер сам доставляет (до клиента или ПВЗ) | Уникальные товары |
| **realFBS Express** | Селлер доставляет < 24ч (LBM Last-Mile-Buy) | Город-локально, premium |

## Базовые тарифы (2026, ориентировочно)

- **Комиссия Ozon:** 7-25% по категории (схема `reward = базовая ставка × коэффициент`)
- **Логистика FBO:** ~35-70 руб/единица (зависит от веса/габаритов)
- **Размещение FBO:** ~0.3-1.5 руб/единица/день
- **Эквайринг:** ~1.5%
- **Возвраты:** ~50-100 руб/возврат

⚠️ Тарифы регулярно меняются. Актуальные → seller.ozon.ru → API → Тарифы.

## API

### Базовые группы

| Группа | Назначение | URL |
|--------|------------|-----|
| **Seller API** | Каталог, цены, остатки, заказы | `api-seller.ozon.ru` |
| **Performance API** | Реклама, продвижение | `performance.ozon.ru` |
| **Chat API** | Чат с покупателями | `api-seller.ozon.ru/v1/chat` |

### Аутентификация

Ozon использует **Client-Id + Api-Key** в HTTP headers:

```http
GET /v3/product/list HTTP/1.1
Host: api-seller.ozon.ru
Client-Id: 1234567
Api-Key: 3b8f1537-6ee3-42f7-9270-66f5a508e031
```

- `Client-Id` — числовой ID продавца из ЛК
- `Api-Key` — UUID-токен из ЛК → API → Сертификаты

### Rate limits

- Standard: **2 RPS** на эндпоинт
- Бурст: до **10 RPS** в течение 10 секунд
- Большие выгрузки — пагинация через `cursor` или `offset`

См. правило `marketplace-data-freshness.md` про обновление кеша.

## Особенности

- **Карточка товара:** до 12 фото + видео + 3D-модели (на отдельных категориях)
- **Маркировка ЧЗ:** обязательна (как и WB)
- **Сертификация:** проверка через `_modules/06-certification-legal/scripts/check_ozon_requirements.py`
- **Возвраты:** ~15-40% (выше, чем WB по некоторым категориям из-за ЯДоставки)
- **Спецусловия Ozon:** «Скидка от продавца» (аналог СПП), Premium-программы, кобрендинг

## Best practices (FREE basics)

1. **Заполняй все атрибуты** — Ozon ранжирует по полноте карточки
2. **Используй A+ контент** (доступно из Premium-тарифа) — рост конверсии до 25%
3. **Reviews stimulation:** программа лояльности Ozon Premium даёт бонусы за отзывы
4. **Rich-text описание** — Ozon разрешает HTML в описании (в отличие от WB)
5. **Управление остатками** через Seller API + cron

## 📈 Углубление в `vibecommerce_vip_code`

- Полные стратегии под каждую категорию Ozon
- A+ контент best practices
- **`marketplace-discounts-guide.md`** — Скидка от продавца, соинвест, Премиум-программа
- Особенности Ozon Performance API для рекламы

## Связанные

- Модуль: [`../../_modules/02-unit-economics/`](../../_modules/02-unit-economics/)
- Модуль: [`../../_modules/06-certification-legal/`](../../_modules/06-certification-legal/)
- Rule: [`../../.claude/rules/marketplace-data-freshness.md`](../../.claude/rules/marketplace-data-freshness.md)
