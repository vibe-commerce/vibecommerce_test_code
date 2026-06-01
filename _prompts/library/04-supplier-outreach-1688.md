# Промпт: Письмо поставщику на 1688 / Alibaba

## Когда использовать

- Первое обращение к китайскому B2B поставщику
- Запрос sample order для тестирования качества
- Переговоры по объёму и цене

## Промпт (English version — для 1688/Alibaba/международных)

```
You are an experienced procurement manager for an e-commerce seller from Russia.

Write a professional outreach email to a Chinese supplier on 1688/Alibaba.

Input: product type + target quantity + key requirements (certification, delivery time, payment terms).

Email structure:
1. Subject: clear, specific (≤ 60 chars)
2. Greeting + brief intro (1-2 sentences who you are)
3. Specific request:
   - Product name + spec
   - Target quantity (MOQ check)
   - Price range you're working with
4. Specific questions (3-5 max):
   - Lead time for production?
   - Available certifications?
   - Sample order possibility (free / paid)?
   - Payment terms (T/T, L/C)?
   - Logistics options (CIF, FOB, EXW)?
5. Trade Assurance / professional posture:
   - Years in business of your company (даже если 1)
   - Volume you handle monthly
   - Goal: long-term partnership, not one-off
6. Closing with timeline (when you need response by)

Style:
- Professional but warm
- Short sentences (Chinese-friendly English)
- Specific numbers, not vague terms
- No emojis in business correspondence
- Sign with full name + WeChat ID (if available)
```

## Пример

### Вход
```
Товар: TWS наушники с активным шумоподавлением (ANC)
Объём: 1000 шт стартовый заказ + потенциал 5000 шт/мес
Требования: CE + EAC, гарантия 1 год, Bluetooth 5.3, IPX4
Опыт: первый импорт, ИП, оборот ~3 млн ₽/мес
```

### Выход
```
Subject: TWS ANC headphones — 1000 units order + monthly potential

Hello {Supplier Name},

I'm {Your Name} from {Your Brand}, an e-commerce seller from Russia.
We focus on premium audio accessories sold on Wildberries and Ozon
(top Russian marketplaces, 30M+ monthly users each).

We're looking for a long-term supplier for the following:

Product: TWS earbuds with active noise cancellation (ANC)
Specs:
  - Bluetooth 5.3
  - ANC ≥ -25 dB
  - IPX4 water resistance
  - Battery: 6h+ standalone, 30h+ with charging case
  - AAC / AptX HD codec support

Quantity: 1000 units initial order + monthly potential 3000-5000 units

Key questions:
1. What's the lead time for 1000 units after PO confirmation?
2. Do you provide CE + EAC certifications? Can we receive copies?
3. Is a sample order possible? Paid sample is OK — please send price + lead time
   for 3-5 samples to evaluate quality.
4. What payment terms do you offer? T/T 30/70 preferred.
5. Can you quote both CIF Moscow and FOB Shenzhen?

Our company:
- 2 years of marketplace experience in Russia
- Monthly revenue: 2-3M RUB
- We handle imports through certified customs brokers
- Goal: long-term partnership, not one-off purchase

Could you send pricing breakdown + your standard contract template
by {DATE +7 days}? We're evaluating 3-4 suppliers and aim to decide
within 14 days.

Looking forward to your reply.

Best regards,
{Your Name}
{Your Brand}
WeChat: {your wechat id}
Email: {you@yourbrand.ru}
```

## Связанные

- Knowledge: [`../../_knowledge/suppliers/`](../../_knowledge/suppliers/)
- Модуль: [`../../_modules/02-unit-economics/`](../../_modules/02-unit-economics/) (расчёт себестоимости с импортом)

## 📈 VIP

- Полные шаблоны под все этапы переговоров (sample → PO → пред-производственный контроль → отгрузка)
- Стандартный контракт T/T 30/70 с китайским поставщиком (на английском)
- WeChat-скрипты для оперативной переписки
- Sub-agent `shopping-researcher` — батчевый поиск поставщиков с автогенерацией обращений
