# Архитектура репозитория

Last Updated: 2026-05-29

## Назначение

Шаблонный стартер для селлеров на маркетплейсах и e-commerce. Форкается
студентами курса Вайб-Коммерс под свои проекты. В репо нет персональных
данных автора или клиентов (Принцип №0).

## Высокоуровневая структура

```
vibecommerce_test_code/
├── CLAUDE.md                # Канон для Claude Code
├── AGENTS.md                # Канон для OpenAI Codex
├── README.md                # Навигация для человека
├── AGENDA.md                # Текущий фокус сессии
├── FACTS.md                 # Стабильные факты (шаблон для форка)
├── ROADMAP.md               # Стратегия / фазы
├── HANDOFF.md               # Сдача сессии (skill /handoff)
├── VERSION                  # 0.3.0
├── Makefile                 # install / test / lint / sync-agents / verify-agents
├── pyproject.toml           # Python зависимости + ruff + pytest config
├── .env.example             # Шаблон переменных окружения
│
├── _modules/                # МЕТОДИЧЕСКИЕ МОДУЛИ (read-only для студента)
│   ├── 01-niche-selection/
│   ├── 02-unit-economics/
│   ├── 03-marketplace-analytics/
│   ├── 04-funnel-jtbd/
│   ├── 05-ads-optimization/
│   ├── 06-certification-legal/
│   └── 07-financial-reporting/
│
├── my-project/              # РАБОЧАЯ ЗОНА СТУДЕНТА (data/ gitignored)
│   ├── 00-niche/ … 06-finance/
│   ├── data/                # gitignored
│   └── reports/
│
├── _knowledge/              # СПРАВОЧНИКИ (общие для всех селлеров)
│   ├── marketplaces/        # WB / Ozon / ЯМ / Avito basics
│   ├── legal/               # 152-ФЗ, ЗоЗПП, маркировка, налоги, сертификация
│   └── suppliers/           # Alibaba, 1688, локальные
│
├── _prompts/                # БИБЛИОТЕКА ПРОМПТОВ
│   ├── roles/               # SMM Consultant, seller-assistant
│   ├── jtbd/                # jtbd-card-basic (полные 9 в VIP)
│   └── library/             # Тематические узкие промпты
│
├── _practices/              # 8-этапный workflow + Plan Before Act
├── _specs/                  # Templates (brief, plan, ADR, tech-spec) + codex-compat
├── backlog/                 # Lifecycle: ideas → briefs → plans → archive/{done,rejected}
├── _changelogs/CHANGELOG.md
├── _status/PROJECT_STATUS.md
├── _references/             # Ссылки на внешние ресурсы
├── _handoffs/               # История handoff-сессий
├── _reports/                # Отчёты по проекту
├── _private/                # gitignored: secrets/, docs/, meetings/, data/
├── documentation/           # Этот файл + onboarding/
│
├── .claude/                 # Claude Code-specific
│   ├── settings.json        # permissions + enabledPlugins + hooks
│   ├── skills/              # 19 slash-команд (FREE)
│   ├── agents/              # 6 sub-агентов (FREE)
│   ├── rules/               # 7 правил (plan-before-act, cost-control, etc.)
│   ├── hooks/               # memory-bank-check.sh
│   └── EXTERNAL-TOOLS.md
│
├── .codex/                  # OpenAI Codex-specific
│   ├── config.toml.template
│   ├── skills/              # симлинки на ../.agents/skills/ (после C12)
│   ├── agents/              # генерируются из ../.agents/subagents/ (после C14)
│   └── hooks/               # симлинки на ../_shared/hooks/
│
├── .agents/                 # Cross-agent shared (после полной C7+C12+C14)
│   ├── skills/<name>/SKILL.md
│   └── subagents/<name>.yaml
│
├── _shared/                 # Общие инструкции для обоих агентов
│   ├── INSTRUCTIONS.md      # импортируется через @ в CLAUDE.md и AGENTS.md
│   ├── MEMORY.md            # кросс-сессионная общая память
│   ├── memory-policy.md
│   ├── mcp.yaml             # источник истины для MCP-серверов
│   └── hooks/               # общие хуки
│
└── scripts/
    ├── sync-agents-config.sh    # симлинки + генераторы (stub, полная — C7)
    └── verify-cross-compat.sh   # smoke-проверка
```

## Информационная архитектура (lifecycle)

```
backlog/ideas/  →  backlog/briefs/  →  backlog/plans/  →  код  →  documentation/
   (что если?)      (стоит ли?)         (как?)
                          │                  │
                          ↓                  ↓
                  archive/rejected/   archive/done/

Крупные фичи (>3 дней): _specs/<feature>/ параллельно (tech-spec, ADR)
```

## Тиринг

| Тир | Репо | Содержимое |
|-----|------|------------|
| FREE | `vibecommerce_test_code` (этот) | workflow + базовая методика + onboarding |
| VIP | `vibecommerce_vip_code` (private) | премиум-IP, платные API, полные промпт-наборы |

Hook'и FREE → VIP помечены `📈 Углубление в vibecommerce_vip_code`.

## Cross-agent compatibility

Шаблон работает в обоих AI-агентах:
- **Claude Code** читает `CLAUDE.md` + `.claude/`
- **OpenAI Codex** читает `AGENTS.md` (agents.md spec) + `.codex/`
- Общая часть — `_shared/INSTRUCTIONS.md` (через `@`-import)
- Общие skills/subagents — `.agents/` (симлинки в `.claude/` и `.codex/`)

Подробности → [`../_specs/codex-compat/README.md`](../_specs/codex-compat/README.md).

## Git Workflow

```
local (рабочая) → push → main (GitHub)
```

Только две ветки. Без `dev`/`prod` — это шаблон без боевого деплоя.

## Связанные

- Главная инструкция AI: [`../CLAUDE.md`](../CLAUDE.md), [`../AGENTS.md`](../AGENTS.md)
- Workflow: [`../_practices/00-WORKFLOW.md`](../_practices/00-WORKFLOW.md)
- Onboarding: [`onboarding/README.md`](onboarding/README.md)
- Проекты: [`projects.md`](projects.md)
- Skills и роли: [`skills-and-roles.md`](skills-and-roles.md)
