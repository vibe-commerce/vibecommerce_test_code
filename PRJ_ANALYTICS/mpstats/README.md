# MPStats API Integration

Аналитика товаров и категорий маркетплейсов через MPStats API.

## Поддерживаемые маркетплейсы

| Маркетплейс | Статус | Флаг `--platform` |
|---|---|---|
| Ozon | Готов | `oz` (по умолчанию) |
| Wildberries | Готов | `wb` |
| Яндекс Маркет | Экспериментальный | `ym` |

## Настройка

1. Получи API-ключ на [mpstats.io](https://mpstats.io)
2. Добавь в `.env` в корне проекта:
```
MPSTATS_API_KEY=your_key_here
```
3. Проверь подключение:
```bash
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/check_limit.py
```

## Скрипты

### `check_limit.py` — проверка API
```bash
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/check_limit.py
```

### `analyze_sku.py` — анализ товара по ID
```bash
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/analyze_sku.py 123456789
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/analyze_sku.py 123456789 --platform wb
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/analyze_sku.py 123456789 --niche
uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/analyze_sku.py 123456789 --xlsx report.xlsx
```

### `analyze_category.py` — анализ категории
```bash
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/analyze_category.py "Электроника/Смартфоны"
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/analyze_category.py "Электроника" --platform wb --days 60
uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/analyze_category.py "Электроника" --xlsx report.xlsx
```

### `explore_ym.py` — исследование Яндекс Маркет
```bash
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/explore_ym.py
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/explore_ym.py --item 12345
```

### `research_sleep.py` — исследование рынка товаров для сна
```bash
# Полный анализ WB + Ozon → Excel + JSON + консоль
uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/research_sleep.py

# Только WB
uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/research_sleep.py --platforms wb

# Только показать категории (без API-запросов)
uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/research_sleep.py --discover

# Другой период (60 дней)
uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/research_sleep.py --days 60
```

## Структура

```
mpstats/
├── PLAN.md              # План интеграции и справка по API
├── README.md            # Этот файл
├── client.py            # HTTP-клиент (sync, httpx, retry, мультиплатформа)
├── models.py            # Модели данных (ItemSummary, CategoryMetrics, NicheContext)
├── check_limit.py       # Проверка лимитов API
├── analyze_sku.py       # Анализ товара по ID
├── analyze_category.py  # Анализ категории
├── explore_ym.py        # Исследование YM-эндпоинтов
├── research_sleep.py    # Исследование рынка товаров для сна
├── sleep_market_research.xlsx  # Результат: Excel-отчёт
├── sleep_market_research.json  # Результат: JSON-сводка
└── reports/             # Отчёты исследований
    └── sleep_2026-02-20.md     # Отчёт: товары для сна
```

## Зависимости

```
httpx>=0.28        # HTTP-клиент
python-dotenv>=1.0 # Загрузка .env
openpyxl>=3.1      # Excel-экспорт (опционально)
```

Не требуют установки — `uv run --with` подтягивает на лету.

## Как провести новое исследование рынка

1. Скопируй `research_sleep.py` → `research_{тема}.py`
2. Замени `SLEEP_CATEGORIES` на категории для своей ниши (найди через `client.get_categories_tree()`)
3. Запусти: `uv run --with httpx,python-dotenv,openpyxl PRJ_ANALYTICS/mpstats/research_{тема}.py`
4. Задокументируй результат в `reports/{тема}_{дата}.md`

Подробная инструкция: [REF: .claude/skills/mpstats-research/SKILL.md]

## Связанные ресурсы

- [REF: .env.example] — шаблон переменных окружения
- [REF: .claude/skills/mpstats-analyst/SKILL.md] — скилл анализа товара/категории
- [REF: .claude/skills/mpstats-research/SKILL.md] — скилл исследования рынка
- [REF: PLAN.md] — детальный план и справка по API
