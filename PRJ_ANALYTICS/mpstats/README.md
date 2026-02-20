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
└── explore_ym.py        # Исследование YM-эндпоинтов
```

## Зависимости

```
httpx>=0.28        # HTTP-клиент
python-dotenv>=1.0 # Загрузка .env
openpyxl>=3.1      # Excel-экспорт (опционально)
```

Не требуют установки — `uv run --with` подтягивает на лету.

## Связанные ресурсы

- [REF: .env.example] — шаблон переменных окружения
- [REF: .claude/skills/mpstats-analyst/SKILL.md] — скилл для Claude
- [REF: PLAN.md] — детальный план и справка по API
