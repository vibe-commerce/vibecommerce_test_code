# Vibe-Commerce — Рабочее пространство E-Commerce менеджера

Last Updated: 2026-02-12

## Описание
Структурированный репозиторий для работы с Claude Code: проекты, аналитика, бэклог задач, автоматизация.

## Структура

### Проекты
- [PRJ_MARKETPLACE/](PRJ_MARKETPLACE/) — работа с маркетплейсами (WB, OZON, и др.)
- [PRJ_DTC/](PRJ_DTC/) — собственный e-commerce (D2C)
- [PRJ_ANALYTICS/](PRJ_ANALYTICS/) — аналитика и отчёты
- [PRJ_DEMO/](PRJ_DEMO/) — демо-проект (финансовые модели, слайды)

### Управление
- [backlog/](backlog/) — бэклог задач (`Backlog.txt` — Single Source of Truth)
- [scripts/](scripts/) — утилиты (бэкап, конвертация, отчёты)
- [documentation/](documentation/) — документация по архитектуре и проектам

### Настройки Claude Code
- [CLAUDE.md](CLAUDE.md) — главная инструкция
- `.claude/skills/` — скиллы + экспертные роли (ecom-manager, project-manager, excel-worker, backup)
- `.claude/rules/` — автоматически загружаемые правила (error-learning, auto-backup)

## Быстрый старт
1. Открой Claude Code в этой папке
2. Он прочитает `CLAUDE.md` и сразу знает контекст
3. Используй скиллы: `/ecom-manager`, `/project-manager`, `/excel-worker`, `/backup`

## Связанные ресурсы
- [REF: backlog/Backlog.txt] — все задачи
- [REF: .claude/skills/] — скиллы и экспертные роли
