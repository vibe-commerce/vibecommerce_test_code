# Архитектура репозитория

Last Updated: 2026-02-12

## Назначение
Рабочее пространство e-commerce менеджера (ИП Баканов Вадим). Это НЕ кодовый проект — это структурированное хранилище для проектов, аналитики, бэклога задач и автоматизации рутины с помощью Claude Code.

## Структура

```
vibecommerce_test_code/
├── CLAUDE.md                    # Главная инструкция для Claude Code
├── README.md                    # Навигация и обзор репозитория
├── VERSION                      # Текущая версия (semver)
│
├── documentation/               # Документация (этот раздел)
│   ├── README.md
│   ├── architecture.md          # Архитектура и структура
│   ├── projects.md              # Описание проектов
│   └── skills-and-roles.md      # Скиллы и роли
│
├── PRJ_MARKETPLACE/             # Проект: маркетплейсы (WB, Ozon)
│   ├── README.md
│   ├── FACTS.md                 # Метрики, контакты, реквизиты
│   ├── sales_data_v1.0.xlsx     # Датасет продаж (50 SKU, 12 недель)
│   └── generate_sales_data.py   # Скрипт генерации датасета
│
├── PRJ_DTC/                     # Проект: собственный e-com (D2C)
│   ├── README.md
│   └── FACTS.md                 # Метрики, конверсии, трафик
│
├── PRJ_ANALYTICS/               # Проект: аналитика и отчёты
│   └── README.md
│
├── PRJ_DEMO/                    # Демо-проект (финмодели, слайды)
│   ├── micellar_water_model_v1.xlsx
│   └── slides/
│
├── backlog/                     # Бэклог задач
│   ├── README.md
│   └── Backlog.txt              # SSoT — все задачи (текстовый формат)
│
├── scripts/                     # Утилиты
│   ├── README.md
│   ├── backup_to_git.zsh        # Бэкап на GitHub
│   ├── convert_xlsx_to_md.py    # Excel → Markdown
│   └── md_to_html.py            # Markdown → HTML
│
└── .claude/                     # Настройки Claude Code
    ├── skills/                  # Скиллы + экспертные роли
    │   ├── ecom-manager/        # (references/role.md = Head of E-Commerce)
    │   ├── project-manager/     # (references/role.md = Project Manager)
    │   ├── excel-worker/
    │   └── skill-creator/
    └── rules/                   # Автоматически загружаемые правила
        └── error-learning.md
```

## Принципы организации

### Папки проектов (PRJ_*)
Каждый проект — отдельная папка с префиксом `PRJ_`. Внутри обязательно README.md и FACTS.md с ключевыми метриками.

### Бэклог
Единый файл `backlog/Backlog.txt` — Single Source of Truth для всех задач по всем проектам. Текстовый формат. Поля: ID, проект, название, описание, приоритет (1–100), дедлайн, спринт, статус, комментарий.

### Кросс-ссылки
Не дублировать информацию. Каждый факт описан в одном месте. Используются маркеры:
- `[CANONICAL]` — первоисточник
- `[REF: path]` — ссылка на первоисточник
- `[CONFIRMED: source]` — проверенная информация
- `[PLACEHOLDER: owner]` — нужно заполнить

### Версионирование файлов
- Excel-файлы сохраняются с суффиксом `_vX.Y.xlsx` (X — крупные изменения, Y — мелкие)
- Версия репозитория в файле `VERSION` (semver)
