# Vibecommerce — Рабочее пространство E-Commerce менеджера

Last Updated: 2026-02-12

## Описание
Структурированный репозиторий для работы с Claude Code: проекты, аналитика, бэклог задач, автоматизация.

## Структура

### Проекты
- [MARKETPLACE_PRJ/](MARKETPLACE_PRJ/) — работа с маркетплейсами (WB, OZON, и др.)
- [DTC_PRJ/](DTC_PRJ/) — собственный e-commerce (D2C)
- [ANALYTICS_PRJ/](ANALYTICS_PRJ/) — аналитика и отчёты
- [DEMO_PRJ/](DEMO_PRJ/) — демо-проект (финансовые модели, слайды)

### Управление
- [backlog/](backlog/) — бэклог задач (`backlog.xlsx` — Single Source of Truth)
- [scripts/](scripts/) — утилиты (бэкап, конвертация, отчёты)

### Настройки Claude Code
- [CLAUDE.md](CLAUDE.md) — главная инструкция
- [_PROMPTS/_ROLES/](_PROMPTS/_ROLES/) — экспертные роли
- `.claude/skills/` — скиллы (ecom-manager, project-manager, excel-worker)
- `.claude/rules/` — автоматически загружаемые правила

## Быстрый старт
1. Открой Claude Code в этой папке
2. Он прочитает `CLAUDE.md` и сразу знает контекст
3. Используй скиллы: `/ecom-manager`, `/project-manager`, `/excel-worker`

## Связанные ресурсы
- [REF: backlog/backlog.xlsx] — все задачи
- [REF: _PROMPTS/_ROLES/] — экспертные роли
