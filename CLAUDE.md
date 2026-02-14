# CLAUDE.md

## Repository Overview
Рабочее пространство e-commerce менеджера (тестовое для курса ВАЙБ-КОММЕРС от Баканова Вадима). Проекты, аналитика, бэклог задач, автоматизация рутины.

## Response Format
Каждый ответ начинается с:
1. Понятность задачи: <0–100%> — если <70%, сначала задать уточняющие вопросы
2. Уверенность в ответе: <0–100%>
3. Роль: <экспертная роль>
4. TL;DR
5. Полный ответ

## Architecture
```
vibecommerce_test_code/
├── CLAUDE.md                    # Этот файл
├── README.md                    # Навигация и обзор
├── .claude/skills/              # Скиллы (команды + экспертные роли)
├── .claude/rules/               # Автоматически загружаемые правила
├── scripts/                     # Утилиты (бэкап, конвертация)
├── backlog/                     # Бэклог задач (Backlog.txt — SSoT)
├── documentation/               # Документация по архитектуре и проектам
├── PRJ_MARKETPLACE/             # Проект: маркетплейсы
├── PRJ_DTC/                     # Проект: собственный e-com
├── PRJ_PRICING/                 # Проект: управление ценами и репрайсинг
├── PRJ_ANALYTICS/               # Проект: аналитика и отчёты
└── PRJ_DEMO/                    # Проект: демо
```

## Common Commands
- `backup "комментарий"` — бэкап на GitHub (`./scripts/backup_to_git.zsh`)
- `xlsx2md файл.xlsx` — Excel → Markdown (`uv run --with openpyxl scripts/convert_xlsx_to_md.py`)
- `md2html отчёт.md` — Markdown → HTML (`uv run --with markdown scripts/md_to_html.py`)

## Role Selection
- E-commerce вопросы → `/ecom-manager` (роль: `.claude/skills/ecom-manager/references/role.md`)
- Планирование и задачи → `/project-manager` (роль: `.claude/skills/project-manager/references/role.md`)

## Project Naming
Папки проектов именуются `PRJ_<NAME>/` (префикс PRJ_, затем название).

## File Editing Rules
- **Markdown:** обновлять README.md при изменении структуры папки
- Каждая папка должна иметь README.md

## Backlog Rules
- Единый файл `backlog/Backlog.txt` — Single Source of Truth
- Не менять структуру колонок без явной команды
- Новые задачи — только добавлением строк (не перенумеровывать ID)
- Статусы: `TO DO`, `WIP`, `ON PRIORITY`, `DONE`, `ON HOLD`
- Приоритеты 1–100, без дубликатов, абсолютные

## Cross-References
- `[CANONICAL]` — первоисточник
- `[REF: path#section]` — ссылка на первоисточник
- `[CONFIRMED: source]` — проверенная информация
Не дублируй — ссылайся. Каждый факт описан в одном месте.

## Git Rules
БЕЗ явной команды пользователя НЕ делать:
- `git push`
- `git commit`
- `git rebase`
- `git reset`
- `git branch -D`

**GitHub-аккаунт для этого репозитория:** `vibe-commerce`
Перед push всегда проверяй активный аккаунт (`gh auth status`) и при необходимости переключай:
```bash
gh auth switch --user vibe-commerce
```
