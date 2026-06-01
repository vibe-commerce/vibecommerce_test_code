# План интеграции MPStats API

**Статус:** IMPLEMENTED — код готов, требуется API-ключ для тестирования
**Дата:** 2026-02-20
**Источник:** kolos_code (`src/app/clients/mpstats.py` + сервисный слой), MPStats API docs

---

## Цель

Подключить MPStats API к рабочему пространству vibecommerce_test_code для аналитики товаров и категорий на **трёх маркетплейсах: Ozon, Wildberries, Яндекс Маркет**. Синхронные CLI-скрипты, без бота и Redis.

## Покрытие маркетплейсов

| Маркетплейс | MPStats prefix | Готовность API | Приоритет |
|---|---|---|---|
| **Ozon** | `/oz/` | Полностью задокументирован, реализован в kolos_code | P0 — делаем первым |
| **Wildberries** | `/wb/` | Полностью задокументирован (API-03-wb.md в kolos_code), но клиент НЕ реализован | P0 — делаем вместе с Ozon |
| **Яндекс Маркет** | `/ym/` (предположительно) | На платформе MPStats есть, но API-эндпоинты плохо задокументированы | P1 — исследуем эндпоинты, затем реализуем |

## Архитектура результата

```
PRJ_ANALYTICS/
└── mpstats/
    ├── PLAN.md                # Этот файл
    ├── README.md              # Документация по использованию
    ├── client.py              # MPStatsClient (sync, httpx, retry, мультиплатформа)
    ├── models.py              # ItemSummary, NicheContext, CategoryMetrics (dataclass)
    ├── analyze_sku.py         # CLI: анализ товара по ID (--platform oz|wb|ym)
    ├── analyze_category.py    # CLI: анализ категории (--platform oz|wb|ym)
    ├── check_limit.py         # CLI: проверка лимитов API
    └── explore_ym.py          # CLI: исследование эндпоинтов Яндекс Маркет
```

---

## Этапы реализации

### Этап 1. Инфраструктура

| # | Действие | Файл | Статус |
|---|----------|------|--------|
| 1.1 | Создать папку `PRJ_ANALYTICS/mpstats/` | — | DONE |
| 1.2 | Добавить `MPSTATS_API_KEY` в `.env` | `.env` | TODO (требуется ключ) |
| 1.3 | Создать `.env.example` с шаблоном (без секретов) | `.env.example` | DONE |

### Этап 2. HTTP-клиент (ядро)

| # | Действие | Файл | Статус |
|---|----------|------|--------|
| 2.1 | Портировать `MPStatsClient` — синхронная версия на `httpx` | `client.py` | DONE |
| 2.2 | Retry 3x, exponential backoff (1s → 2s → 4s) | — | DONE |
| 2.3 | Rate-limit: обработка 429 с Retry-After | — | DONE |
| 2.4 | Заголовок авторизации: `X-Mpstats-TOKEN` | — | DONE |
| 2.5 | Параметр `platform` в методах (`oz`, `wb`, `ym`) для выбора prefix | — | DONE |

**Подход к мультиплатформенности:**
Клиент один (`MPStatsClient`), но каждый метод принимает `platform: str = "oz"`. Внутри метод подставляет нужный prefix (`/oz/`, `/wb/`, `/ym/`). Структура эндпоинтов у Ozon и WB одинаковая — отличается только prefix.

**Эндпоинты — Ozon (`/oz/`):**

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/oz/get/item/{id}` | Базовая информация о товаре |
| GET | `/oz/get/item/{id}/by_date` | Товар за период |
| GET | `/oz/get/category/by_date` | Категория за период |
| POST | `/oz/get/category` | Товары категории (с пагинацией) |
| GET | `/oz/get/category/sellers` | Продавцы категории |
| GET | `/oz/get/category/brands` | Бренды категории |
| GET | `/oz/get/categories` | Дерево категорий (~3500) |
| GET | `/user/report_api_limit` | Проверка лимитов |

**Эндпоинты — Wildberries (`/wb/`):**

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/wb/get/item/{id}/summary` | Базовая информация о товаре |
| GET | `/wb/get/item/{id}/by_date` | Товар за период |
| GET | `/wb/get/item/{id}/keywords` | Ключевые слова товара |
| GET | `/wb/get/item/{id}/seo` | SEO-анализ товара |
| GET | `/wb/get/item/{id}/by_size` | Данные по размерам |
| GET | `/wb/get/category/by_date` | Категория за период |
| POST | `/wb/get/category` | Товары категории (с пагинацией) |
| GET | `/wb/get/category/sellers` | Продавцы категории (тариф Professional) |
| GET | `/wb/get/category/brands` | Бренды категории |
| GET | `/wb/get/category/subcategories` | Подкатегории |
| GET | `/wb/get/category/price_segmentation` | Ценовые сегменты |
| GET | `/wb/get/categories` | Дерево категорий |
| POST | `/wb/get/brand` | Товары бренда |
| POST | `/wb/get/seller` | Товары продавца |

**Эндпоинты — Яндекс Маркет (`/ym/`):**

| Метод | Endpoint | Описание |
|-------|----------|----------|
| ? | `/ym/get/item/{id}` | Предположительно — нужно исследовать |
| ? | `/ym/get/category/...` | Предположительно — нужно исследовать |

> **Важно:** API-эндпоинты MPStats для Яндекс Маркет не задокументированы публично. Этап 4.4 (`explore_ym.py`) — скрипт для исследования доступных эндпоинтов методом проб.

### Этап 3. Модели данных

| # | Действие | Файл | Статус |
|---|----------|------|--------|
| 3.1 | `ItemSummary` — универсальный dataclass с `from_api(data, platform)` | `models.py` | DONE |
| 3.2 | `NicheContext` — dataclass для контекста категории | `models.py` | DONE |
| 3.3 | `CategoryMetrics` — метрики категории (тренды, концентрация) | `models.py` | DONE |

**Подход:** Модели платформо-независимые. Маппинг полей API → модель происходит в `from_api()` с учётом platform. Разные маркетплейсы возвращают похожие данные, но с разными именами полей.

**Поля ItemSummary** (общие для всех платформ):
- platform, id, name, brand, seller, seller_id, category
- final_price, price, rating, reviews_count
- balance (остатки)

**Дополнительные поля по платформам:**
- **Ozon:** delivery_scheme (FBO/FBS), discount
- **WB:** supplier_id, pics_count, feedbacks_count

**Поля NicheContext:**
- platform, category_name, total_revenue, total_sales, avg_check
- sellers_count, brands_count, trend_pct, trend_label

### Этап 4. Аналитические скрипты

| # | Действие | Файл | Статус |
|---|----------|------|--------|
| 4.1 | Анализ товара по ID — сводка + рыночный контекст | `analyze_sku.py` | DONE |
| 4.2 | Анализ категории — топ товары, выручка, тренды | `analyze_category.py` | DONE |
| 4.3 | Проверка лимитов API | `check_limit.py` | DONE |
| 4.4 | Исследование эндпоинтов Яндекс Маркет | `explore_ym.py` | DONE |

**Формат запуска:**
```bash
# Ozon (по умолчанию)
uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/analyze_sku.py 123456789

# Wildberries
uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/analyze_sku.py 123456789 --platform wb

# Яндекс Маркет
uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/analyze_sku.py 123456789 --platform ym

# Категория на WB
uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/analyze_category.py "Электроника/Смартфоны" --platform wb

# Проверка лимитов
uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/check_limit.py

# Исследование YM эндпоинтов
uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/explore_ym.py
```

**Каждый скрипт:**
- Принимает `--platform oz|wb|ym` (по умолчанию `oz`)
- Загружает ключ из `.env` через `python-dotenv`
- Выводит результат в консоль (форматированная таблица)
- Опциональный флаг `--xlsx` — экспорт в Excel

### Этап 5. Скилл для Claude

| # | Действие | Файл | Статус |
|---|----------|------|--------|
| 5.1 | Создать скилл `mpstats-analyst` | `.claude/skills/mpstats-analyst/` | DONE |
| 5.2 | Триггеры: mpstats, аналитика ozon/wb/ym, анализ товара, анализ категории | — | DONE |

### Этап 6. Документация

| # | Действие | Файл | Статус |
|---|----------|------|--------|
| 6.1 | README для mpstats | `PRJ_ANALYTICS/mpstats/README.md` | DONE |
| 6.2 | Обновить README проекта PRJ_ANALYTICS | `PRJ_ANALYTICS/README.md` | DONE |
| 6.3 | Обновить корневой README — навигация | `README.md` | DONE |
| 6.4 | Обновить CLAUDE.md — переменная MPSTATS_API_KEY | `CLAUDE.md` | DONE |

---

## Порядок реализации

```
Этап 1 (инфраструктура)
  └→ Этап 2 (клиент: сначала OZ + WB, потом YM)
       └→ Этап 3 (модели)
            └→ Этап 4.3 (check_limit — проверяем что API работает)
                 └→ Этап 4.4 (explore_ym — исследуем YM эндпоинты)
                      └→ Этап 4.1 (analyze_sku)
                           └→ Этап 4.2 (analyze_category)
                                └→ Этап 5 (скилл)
                                     └→ Этап 6 (документация)
```

## Зависимости

```
httpx>=0.28        # HTTP-клиент (sync режим)
python-dotenv>=1.0 # Загрузка .env
openpyxl>=3.1      # Excel-экспорт (уже используется)
```

Устанавливать не нужно — используем `uv run --with`.

## Что НЕ переносим из kolos_code

- **Redis-кеширование** — нет Redis, скрипты разовые
- **Async/await** — нет async-фреймворка в проекте
- **Telegram handlers/keyboards** — нет бота
- **aiogram** — не нужен
- **Pydantic Settings** — избыточно для CLI-скриптов

## Ключевые решения

1. **Sync вместо async** — в проекте нет async-инфраструктуры, скрипты запускаются разово
2. **Без кеша** — для разовых запросов кеш не нужен; если понадобится — добавим файловый кеш (JSON)
3. **uv run** — не создаём venv, зависимости подтягиваются на лету
4. **Мультиплатформа через prefix** — один клиент, параметр `platform` определяет prefix эндпоинта
5. **YM — сначала исследуем** — эндпоинты не задокументированы, нужен скрипт-разведчик

## Различия WB vs Ozon в API

| Аспект | Ozon (`/oz/`) | Wildberries (`/wb/`) |
|---|---|---|
| Товар (base) | `GET /oz/get/item/{id}` | `GET /wb/get/item/{id}/summary` |
| Keywords | нет | `GET /wb/get/item/{id}/keywords` |
| SEO | нет | `GET /wb/get/item/{id}/seo` |
| Размеры | нет | `GET /wb/get/item/{id}/by_size` |
| Ценовые сегменты | нет | `GET /wb/get/category/price_segmentation` |
| Продавцы категории | все тарифы | только тариф Professional |
| AI-прогнозы | нет | `GET /wb/get/ds/category/yhat` |
| Тренды (ML) | нет | `GET /wb/get/ds/category/trend` |

> WB API богаче — есть keywords, SEO, price segmentation, ML-прогнозы. Эти фичи можно добавить как расширения после базовой интеграции.

## Plan B

Если MPStats API станет недоступен или дорогим:
- **MarketDB** — аналогичный API, похожая структура данных
- **SellerBoard** — альтернатива с другим форматом ответа

Замена потребует: изменить URL + заголовок в `client.py` + маппинг полей в `models.py`. Структура скриптов не меняется.

## Справка по API

- **Авторизация:** заголовок `X-Mpstats-TOKEN: <api_key>`
- **Base URL:** `https://mpstats.io/api`
- **Rate limit:** при 429 — ждать `Retry-After` или backoff
- **Таймаут:** 30 секунд
- **Ошибки:** 404 = не найдено, 5xx = retry, 429 = rate limit

## Источники

- kolos_code: `src/app/clients/mpstats.py` — async-клиент (Ozon)
- kolos_code: `_specs/BF-MPstats/API-03-wb.md` — документация WB-эндпоинтов
- kolos_code: `_specs/BF-MPstats/API-03-ozon.md` — документация Ozon-эндпоинтов
- [MPStats интеграции](https://mpstats.io/integrations) — официальная страница API
- [MPStats Яндекс Маркет](https://mpstats.io/instruments/yandex-market/analytics) — YM на платформе (API не задокументирован)
