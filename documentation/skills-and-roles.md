# Скиллы и роли

Last Updated: 2026-02-12

## Скиллы Claude Code (.claude/skills/)
Скиллы — переиспользуемые команды, вызываемые через `/имя-скилла`.

### /ecom-manager
Анализ e-commerce метрик, ревью карточек, юнит-экономика, конкурентный анализ.

### /project-manager
Управление бэклогом, планирование спринтов, статус-отчёты, приоритизация задач.

### /excel-worker
Чтение, анализ и модификация Excel-файлов. Работа с выгрузками, моделями, отчётами.

### /skill-creator
Создание новых скиллов для Claude Code.

## Экспертные роли (внутри скиллов)
Роли встроены в скиллы как `references/role.md` и загружаются автоматически при вызове скилла.

- **ecom-manager** → `.claude/skills/ecom-manager/references/role.md` (Head of E-Commerce)
- **project-manager** → `.claude/skills/project-manager/references/role.md` (Project Manager)

## Автоматические правила (.claude/rules/)
Правила загружаются автоматически при каждом запуске.

### error-learning.md
После бага или 2+ неудачных попыток — логировать ошибку, причину, исправление и меры предотвращения.
