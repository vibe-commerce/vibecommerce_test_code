# `_knowledge/` — справочники и база знаний

Last Updated: 2026-05-29

## Что здесь

Общие справочники, актуальные для **любого** селлера на МП и e-commerce.
В отличие от `_modules/` (методики работы), `_knowledge/` — это **факты
о рынке/законах/инструментах**.

## Структура

- [`marketplaces/`](marketplaces/) — тарифы, комиссии, API площадок (WB, Ozon, ЯМ, Avito)
- [`legal/`](legal/) — резюме законов (152-ФЗ, ЗоЗПП, маркировка, сертификация, налоги)
- [`suppliers/`](suppliers/) — где искать поставщиков (overview Alibaba, 1688, локальные)

## Принципы

- `[CANONICAL]` — первоисточник факта в этом репо (один на факт)
- `[REF: path#section]` — кросс-ссылка вместо дублирования
- `[CONFIRMED: source-url-or-date]` — проверенная информация с источником
- `[PLACEHOLDER: owner]` — информация для заполнения (если ещё не собрано)
- `[VIP]` — углублённая версия живёт в `vibecommerce_vip_code`

## Maintenance

- Раз в квартал — пройди по всем `[CONFIRMED:]` отметкам и проверь, не устарели ли
- Правила `legal-data-freshness.md` и `marketplace-data-freshness.md` напоминают
  о необходимости проверки изменений

## 📈 Углубление в `vibecommerce_vip_code`

Полные knowledge-наборы в VIP:
- `marketplace-discounts-guide.md` (СПП/соинвест/спецусловия по площадкам)
- Полные `marketplaces/` — стратегии, бенчмарки, особенности API
- Полные `suppliers/` — OEM/ODM, 1688 deep, импорт, проверка контрагентов

## Связанные

- Родитель: [`../README.md`](../README.md)
- Промпты: [`../_prompts/`](../_prompts/)
- Модули: [`../_modules/`](../_modules/)
