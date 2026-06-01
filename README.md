<div align="center">
  <a href="https://vibecommerce.ru/course?r=gh">
    <img src="https://vibecommerce.ru/vibe-commerce-logo.png" alt="Вайб-Коммерс" width="80">
  </a>
  <h3>Шаблонный стартер для селлеров на маркетплейсах и e-commerce</h3>
  <a href="https://vibecommerce.ru/course?r=gh">
    <img src="https://img.shields.io/badge/Курс_Вайб--Коммерс_→-00BCD4?style=for-the-badge&logoColor=white" alt="Курс">
  </a>
</div>

---

# vibecommerce_test_code

Last Updated: 2026-05-29
Версия шаблона: **0.3.0**

## Что это

Шаблонный стартер для студентов курса «Вайб-Коммерс» и любого селлера на
маркетплейсах / e-commerce. Форкается под каждый проект селлера — даёт
готовые методические модули, AI-агентов и workflow для работы с Claude Code
и OpenAI Codex.

**Принцип №0:** в репо нет ни одного байта персональных или клиентских
данных. Только методики, синтетические демо-датасеты, открытые отраслевые
выгрузки (MPStats research).

## Тиринг

- **FREE (этот репо)** — базовая методика + workflow + onboarding
- **VIP** (`vibecommerce_vip_code`, private) — углублённые методологии,
  платные API (MPStats Pro, Ahrefs, Semrush, DaData), полные промпт-наборы

Hook'и FREE→VIP помечены `📈 Углубление в vibecommerce_vip_code`.

## Точки входа

| Что нужно | Куда смотреть |
|-----------|---------------|
| Инструкции для AI (Claude Code) | [CLAUDE.md](CLAUDE.md) |
| Инструкции для AI (OpenAI Codex) | [AGENTS.md](AGENTS.md) |
| Текущий фокус сессии | [AGENDA.md](AGENDA.md) |
| Сдача сессии | [HANDOFF.md](HANDOFF.md) (через `/handoff`) |
| Стабильные факты | [FACTS.md](FACTS.md) |
| Стратегия / фазы | [ROADMAP.md](ROADMAP.md) |
| Текущий статус | [_status/PROJECT_STATUS.md](_status/PROJECT_STATUS.md) |
| Версия | [VERSION](VERSION) |

## Навигация по задачам

| Тема задачи | Что читать |
|-------------|-----------|
| Как работать (workflow) | [_practices/00-WORKFLOW.md](_practices/00-WORKFLOW.md) |
| Методические модули (порядок 01→07) | [_modules/README.md](_modules/README.md) |
| Рабочая зона студента | [my-project/README.md](my-project/README.md) |
| Knowledge base (marketplaces / legal / suppliers) | [_knowledge/README.md](_knowledge/README.md) |
| Промпты (роли + JTBD) | [_prompts/README.md](_prompts/README.md) |
| Спецификации (templates) | [_specs/README.md](_specs/README.md) |
| История релизов | [_changelogs/CHANGELOG.md](_changelogs/CHANGELOG.md) |
| Идеи / брифы / планы | [backlog/README.md](backlog/README.md) |
| Skills (slash-команды) | [.claude/skills/README.md](.claude/skills/README.md) |
| Sub-агенты | [.claude/agents/README.md](.claude/agents/README.md) |
| Глобальные external агенты/скиллы | [.claude/EXTERNAL-TOOLS.md](.claude/EXTERNAL-TOOLS.md) |
| Приватные данные (gitignored) | [_private/README.md](_private/README.md) |

## AI-инфраструктура

```
.claude/                        # Claude Code-specific
├── skills/                     # Slash-команды
├── agents/                     # Sub-агенты
├── rules/                      # Поведенческие правила
├── hooks/                      # Bash-хуки
└── settings.json               # Permissions, hooks, plugins

.codex/                         # OpenAI Codex-specific (фаза C)
.agents/                        # Cross-agent shared skills/subagents (фаза C)
_shared/                        # Общие инструкции + MCP + hooks (фаза C)
```

## Информационная архитектура

```
backlog/ideas/ → backlog/briefs/ → backlog/plans/ → код → documentation/
  (что если?)     (стоит ли?)        (как?)
                       │                  │
                       ↓                  ↓
              archive/rejected/   archive/done/

Крупные фичи параллельно: _specs/<feature>/ (tech-spec, user-spec, ADR)
```

| Слой | Папка | Главный вопрос | Горизонт |
|------|-------|----------------|----------|
| Идеи | `backlog/ideas/` | «А что если?» | дни-недели |
| Брифы | `backlog/briefs/` | «Стоит ли делать?» | недели |
| Планы | `backlog/plans/` | «Как делать?» | дни-недели |
| Архив реализованного | `backlog/archive/done/` | история | годы |
| Архив отказов | `backlog/archive/rejected/` | почему не пошло | годы |
| Реализация | `_modules/`, `my-project/` | методика + sandbox студента | месяцы-годы |
| Факты | `documentation/` | реализованное | месяцы-годы |
| Релизы | `_changelogs/` | — | годами |
| Состояние | `_status/` | — | актуально |
| Приватное | `_private/` (gitignored) | — | бессрочно |

📌 **При добавлении / изменении / удалении файлов в любой папке —
обязательно обнови `README.md` в этой папке.** README — это карта памяти
проекта. Подробнее → CLAUDE.md, раздел «MEMORY BANK + File Management».

## Git Workflow

```
local (рабочая) → push → main (GitHub)
```

Только две ветки. Без `dev`/`prod` — это шаблон без боевого деплоя.

## Quick Start (форк-сценарий)

```bash
git clone <repo> my-seller-project && cd my-seller-project
# Заполни {placeholders} в CLAUDE.md, AGENTS.md, FACTS.md, README.md
make install
# Открой _modules/README.md — порядок прохождения 01→07
# Открой my-project/README.md — куда складывать свои данные
```

📖 Полный гайд по форку → [documentation/00-FORKING-GUIDE.md](documentation/00-FORKING-GUIDE.md)

## Cross-agent compatibility

Шаблон работает в **обоих** AI-агентах:
- **Claude Code** — читает `CLAUDE.md` + `.claude/`
- **OpenAI Codex** — читает `AGENTS.md` (agents.md spec) + `.codex/`
- Общая часть — `_shared/INSTRUCTIONS.md` (импортируется через `@`)

См. фазу C плана апгрейда + `_specs/codex-compat/` (после реализации).

## Автор

Vadim Bakanov, создатель [Vibe-Commerce](https://vibecommerce.ru)

## Лицензия

MIT (этот FREE-репо). `vibecommerce_vip_code` — BSL 1.1.
