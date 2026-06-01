# architecture.md — структура репозитория EMPTY_code

Last Updated: 2026-05-01

## Дерево проекта

```
{project}/
├── .claude/                   # AI Brain
│   ├── skills/                # Skills (slash commands)
│   ├── agents/                # Sub-agents
│   ├── rules/                 # Поведенческие правила (auto-backup, error-learning, retrospective)
│   ├── hooks/                 # Bash-хуки (memory-bank-check.sh и др.)
│   ├── data/                  # Skill memory (error-log.md и др.)
│   └── settings.json          # Permissions, hooks, enabled plugins
├── _practices/                # Workflow разработки (00-WORKFLOW.md + 5 правил)
├── src/                       # Исходный код
│   ├── main.py
│   ├── config.py
│   ├── collectors/
│   ├── processors/
│   ├── storage/
│   └── utils/
├── config/                    # YAML конфигурация (default.yaml, local.yaml — gitignored)
├── data/                      # Данные (raw/processed/cache — gitignored)
├── notebooks/                 # Jupyter ноутбуки
├── tests/                     # pytest (unit, e2e, slow markers)
├── scripts/                   # smoke-test, deploy-dev, deploy-prod, connect-vps
├── deploy/                    # Шаблоны Docker, Nginx, hooks
├── design-system/             # Vite + React + Tailwind каталог токенов
├── backlog/                   # ideas/ → briefs/ → tasks
├── _specs/                    # Спецификации + templates/ + design/THEMES.md
├── _status/                   # Состояние окружений (DEV/PROD)
├── _changelogs/               # История релизов
├── _reports/                  # Периодические отчёты (weekly/monthly/postmortem)
├── _references/               # Справочники, бенчмарки, исследовательские заметки
├── _evals/                    # Golden-датасеты для оценки AI-фич
├── _private/                  # Приватная зона (gitignored): secrets/, docs/, meetings/, data/
├── documentation/             # Пронумерованные факты (01-OVERVIEW … 90-AI-AGENT-BEST-PRACTICES)
├── README.md                  # Точка входа для человека
├── CLAUDE.md                  # Инструкции для AI
├── AGENDA.md                  # Текущий фокус сессии
├── HANDOFF.md                 # Сдача сессии (через /handoff)
├── FACTS.md                   # Стабильные факты проекта
├── ROADMAP.md                 # Стратегический план (фазы)
├── VERSION                    # Версия шаблона
└── Makefile                   # install/run/test/lint
```

## Архитектурный паттерн (Three-Layer Rule)

```
{Handlers/Pages} → {Services/API} → {Repositories/Models}
```

Каждый слой имеет одну ответственность (SRP). Запрещено вызывать модели из handlers
напрямую — только через services.

## Информационные слои

| Слой | Папка | Горизонт | Что хранится |
|------|-------|----------|--------------|
| Идеи | `backlog/ideas/` | дни-недели | Сырые заметки, после оформления удаляются |
| Брифы | `backlog/briefs/` | недели | Оформленные брифы, после переноса в _specs/ удаляются |
| Спеки | `_specs/` | недели-месяцы | Спецификации фич + шаблоны (templates/) |
| Реализация | `src/`, `tests/` | месяцы-годы | Код |
| Факты | `documentation/` | месяцы-годы | Только реализованное (пронумерованные `01-…` … `90-…`) |
| Релизы | `_changelogs/` | годами | История изменений шаблона |
| Состояние | `_status/` | актуально | Снапшоты DEV/PROD |

## Корневые файлы

| Файл | Назначение |
|------|-----------|
| `CLAUDE.md` | Critical rules + навигация для AI |
| `README.md` | Описание шаблона + точки входа для человека |
| `AGENDA.md` | Текущий фокус сессии |
| `HANDOFF.md` | Сдача сессии (генерируется skill `/handoff`) |
| `FACTS.md` | Стабильные факты проекта |
| `ROADMAP.md` | Стратегические фазы |
| `VERSION` | Версия шаблона (semver) |
| `.gitignore` | Игнорируемые пути |
| `Makefile` | install/run/test/lint |
| `pyproject.toml` | Python-зависимости и lint-конфиг |

## Соглашения по именованию папок

В этом шаблоне используются префиксы для визуальной иерархии:

| Префикс | Значение | Примеры |
|---------|----------|---------|
| `_name` | операционный слой / системная папка | `_practices`, `_specs`, `_status`, `_changelogs`, `_private` |
| `name` (без префикса) | стандартная папка кода / данных | `src`, `tests`, `config`, `data`, `notebooks` |
| `.claude` | AI-инфраструктура (Claude Code) | `.claude/skills`, `.claude/agents`, `.claude/rules` |

В форках шаблона можно вводить `__name` для основных бизнес-папок и `___name` для
индивидуальных проектов — как в проекте `vibecommerce_code` (внутренний репо автора).
