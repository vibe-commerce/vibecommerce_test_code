# `_knowledge/marketplaces/` — справочник по маркетплейсам

Last Updated: 2026-05-29

## Покрытие (FREE)

Базовые факты по российским маркетплейсам:

| Площадка | Что есть | Подробности |
|----------|----------|-------------|
| **Wildberries (WB)** | Тарифы, базовые API | `wb-basics.md` |
| **Ozon** | Тарифы, базовые API | `ozon-basics.md` |
| **Яндекс.Маркет (ЯМ)** | Базовая информация | `yandex-market-basics.md` |
| **Avito** | Базовая информация | `avito-basics.md` |

## Что важно знать (быстрая шпаргалка)

### Wildberries
- Комиссия: 14-19% от категории
- Логистика FBO: ~30-50 руб/единица
- Эквайринг: ~1.5%
- Возвраты: ~40-60 руб/возврат
- API: docs.wildberries.ru/openapi (Seller API + Statistics API + Advertising API)

### Ozon
- Комиссия: 7-25% по категории (схема reward = `базовая ставка × коэффициент`)
- Логистика FBO/FBS/realFBS — разные тарифы
- Эквайринг: ~1.5%
- API: api-seller.ozon.ru/v1/* (нужен Client-Id + Api-Key)

### Яндекс.Маркет
- Модели: FBY / FBS / Express / DBS
- Комиссия: 0-19% по категории
- API: api.partner.market.yandex.ru (OAuth)

### Avito
- Модели: классифайд (без выкупа продаж Avito), Avito Доставка
- Тарифы за пакеты услуг (продвижение объявлений)

## Источники

- [WB Открытая API documentation](https://docs.wildberries.ru/openapi)
- [Ozon API documentation](https://docs.ozon.ru/api/seller/)
- [Я.Маркет Partner API](https://yandex.ru/dev/market/partner-api/)
- [MPStats](https://mpstats.io) — paid analytics

## 📈 Углубление в `vibecommerce_vip_code`

- **`marketplace-discounts-guide.md`** — детальный гайд по СПП (скидке продавца),
  соинвестированию, спецусловиям, акциям WB/Ozon
- **Полные стратегии** под каждую категорию (одежда, FMCG, электроника, мебель)
- **Бенчмарки** по марже, ДРР, оборачиваемости запасов
- **Особенности API** — workaround'ы, неочевидные эндпоинты, rate-limit стратегии

## Связанные

- Модуль: [`../../_modules/02-unit-economics/`](../../_modules/02-unit-economics/)
- Модуль: [`../../_modules/03-marketplace-analytics/`](../../_modules/03-marketplace-analytics/)
- Rule: [`../../.claude/rules/marketplace-data-freshness.md`](../../.claude/rules/marketplace-data-freshness.md)
