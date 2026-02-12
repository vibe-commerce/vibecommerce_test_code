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
- [_PROMPTS/_ROLES/](_PROMPTS/_ROLES/) — экспертные роли
- `.claude/skills/` — скиллы (ecom-manager, project-manager, excel-worker)
- `.claude/rules/` — автоматически загружаемые правила

## Быстрый старт
1. Открой Claude Code в этой папке
2. Он прочитает `CLAUDE.md` и сразу знает контекст
3. Используй скиллы: `/ecom-manager`, `/project-manager`, `/excel-worker`

## Связанные ресурсы
- [REF: backlog/Backlog.txt] — все задачи
- [REF: _PROMPTS/_ROLES/] — экспертные роли
