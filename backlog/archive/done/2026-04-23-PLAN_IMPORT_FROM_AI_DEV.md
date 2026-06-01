# PLAN: Импорт полезного из `vibe-commerce/vadim-bakanov-ai-dev`

> **🗄️ ARCHIVED 2026-05-29 — DONE (partially)**
>
> Закрыт. То, что не выполнено, теперь часть актуального плана:
> `backlog/plans/2026-05-28-upgrade-test-code-from-best-practices.md`
>
> Конкретно поглощены:
> - Фаза 2.5/2.6 — миграция skills и agents из ai-dev (включая `agent-creator`, `skill-creator`)
> - Фаза 7 — документация и onboarding
> - Фаза C — Cross-agent compatibility (использует ai-dev `.agents/skills/` как пример)

---

> Дата: 2026-04-23
> Источник: https://github.com/vibe-commerce/vadim-bakanov-ai-dev (ветка `local`)
> Цель: перенести в текущий workspace (`vibecommerce_test_code`) те части шаблона AI Dev, которые применимы к e-com менеджеру (не к код-проекту)

---

## Контекст и фильтр

Внешний репо — **dev-шаблон** для AI-разработки кода (Python/TS + Docker + deploys). Текущий репо — **workspace e-com менеджера** (аналитика, бэклог, проекты, автоматизация рутины). Часть контента (Docker, nginx, deploy-dev, test-runner, CI hooks) **НЕ применима** и будет пропущена. Импортируется только то, что полезно для непрограммистского workspace'а.

---

## ✅ TIER 1 — HIGH PRIORITY (импортировать обязательно)

Универсальная инфраструктура знаний и планирования, работает в любом workspace'е.

### 1.1. Документация о лучших практиках AI-агентов

| Источник | Цель | Действие |
|---|---|---|
| `documentation/AI_AGENT_BEST_PRACTICES.md` | Методика: Plan&Act, док для агентов, Error Registry, техдолг, суб-агенты, ревью | **Копировать в `documentation/`** |
| `documentation/SYSTEM_ARCHITECTURE.md` | Мета-схема как устроен `.claude/` (skills/agents/rules/data) | **Копировать в `documentation/`** |
| `documentation/ERROR_REGISTRY.md` | Шаблон реестра багов/ошибок (human-readable, комплемент к `.claude/data/error-log.md`) | **Копировать в `documentation/`** |

**Обоснование:** это знание о том, **как работать с Claude Code**. Оно универсально и прямо дополняет существующее правило `.claude/rules/error-learning.md`.

### 1.2. Шаблоны спецификаций (_specs/)

| Источник | Цель | Действие |
|---|---|---|
| `_specs/README.md` | Индекс спецификаций | **Создать в `_specs/`** |
| `_specs/templates/user-spec.md` | Шаблон бизнес-спеки | **Копировать в `_specs/templates/`** |
| `_specs/templates/tech-spec.md` | Шаблон тех-спеки (адаптировать под "analysis-spec") | **Копировать, опционально переименовать** |
| `_specs/templates/task.md` | Шаблон декомпозированной задачи | **Копировать в `_specs/templates/`** |
| `_specs/RECOMMENDED_SYSTEM.md` | Blueprint настройки Claude Code для новых проектов | **Копировать (для справки)** |

**Обоснование:** у тебя уже есть `PLAN_REORGANIZATION*.md` в корне — шаблоны дадут структуру на будущее (например, `PRJ_MARKETPLACE/strategy/` можно оформить через `user-spec`).

### 1.3. Working session memory + project status

| Источник | Цель | Действие |
|---|---|---|
| `AGENDA.md` | "Working memory" между сессиями — current focus, last session, next steps | **Копировать в корень** (адаптировать под e-com контекст) |
| `_status/DEVELOPMENT_STATUS.md` | Статус проектов для быстрого возврата после паузы | **Копировать как `_status/PROJECT_STATUS.md`** (переименовать — у тебя нет "development") |
| `_changelogs/` (сам паттерн) | Опционально — журнал значимых апдейтов workspace'а | **Создать пустой `_changelogs/workspace.md`** |

**НЕ импортировать:** `_status/DEV.md`, `_status/PROD.md`, `_status/PENDING_RELEASE.md` — это про окружения deploy'а, неприменимо.

### 1.4. Улучшения в `CLAUDE.md`

Не полная замена — **точечные вставки**:

| Блок | Где в источнике | Зачем |
|---|---|---|
| **Language rule** ("Используй язык пользователя") | `CLAUDE.md` начало | У тебя этого явно нет |
| **Self-Reflection** (Accuracy/Honesty/Objectivity/…) | `CLAUDE.md` Response Format | Улучшает качество ответов |
| **Рабочая ветка** (если будешь использовать local/dev/prod) | — | **Пропустить** — у тебя `main`, не нужно |

**Действие:** вручную добавить 2 секции в существующий `CLAUDE.md` без пересоздания.

### 1.5. Плагины из `.claude/settings.json`

В источнике включены полезные плагины, которые у тебя отсутствуют (проверить `.claude/settings.local.json`):

- `context7@claude-plugins-official` — актуальная документация библиотек
- `agent-teams@ilia-izmailov-plugins` — команды агентов с ревью
- `frontend-design@claude-plugins-official`
- `claude-md-management@claude-plugins-official`
- `think-through@ilia-izmailov-plugins`
- `pr-review-toolkit@claude-plugins-official`
- `playground@claude-plugins-official`
- `vibe-audit@ilia-izmailov-plugins`
- `feature-dev@claude-plugins-official`
- `code-simplifier@claude-plugins-official`

**Действие:** проверить какие уже есть, добавить недостающие в `settings.local.json`. *(Судя по системному контексту сессии — большинство уже активны, но нужна сверка.)*

---

## 🟡 TIER 2 — MEDIUM PRIORITY (полезно, но опционально)

Скиллы, которые дополняют существующие. **Импорт только если ты подтвердишь**, что нужны.

### 2.1. Git-скиллы

| Источник | Что даёт | Стоит ли |
|---|---|---|
| `.claude/skills/commit/SKILL.md` | `/commit` — AI-генерация commit message (conventional commits) | **Да** — у тебя есть `/backup` (commit+push одной командой), но `/commit` даёт контроль над сообщением без пуша |
| `.claude/skills/git-status/SKILL.md` | `/git-status` — multi-branch обзор | **Опционально** — у тебя одна ветка `main`, но скилл универсален |
| `.claude/skills/push/SKILL.md` | `/push` — безопасный push с preview | **Опционально** — overlapping с `/backup` |

**НЕ импортировать:** `cherry-pick`, `merge-to-prod`, `rollback` — у тебя нет `local→dev→prod` workflow.

### 2.2. Планирование и качество

| Источник | Что даёт | Стоит ли |
|---|---|---|
| `.claude/skills/architect/SKILL.md` | `/architect` — архитектурный анализ и план реализации фичи | **Да** — можно адаптировать под "стратегический анализ" для e-com кейсов |
| `.claude/skills/techdebt/SKILL.md` | `/techdebt` — скан TODO/FIXME/больших файлов | **Адаптировать** — у тебя нет кода, но можно переделать в "workspace-audit" (проверка битых ссылок, устаревших файлов, TODO в .md) |
| `.claude/skills/docs/SKILL.md` | `/docs` — обновление документации после значимых изменений | **Да** — универсально полезен |

### 2.3. OpenAI Codex совместимость

| Источник | Что даёт | Стоит ли |
|---|---|---|
| `AGENTS.md` | Зеркало `CLAUDE.md` для Codex CLI | **Только если планируешь использовать Codex.** Иначе пропустить. |
| `.agents/` | Скиллы для Codex (mirror `.claude/skills/`) | **Пропустить** без явной потребности |

---

## 🔴 TIER 3 — SKIP (не импортировать)

Чисто dev-артефакты, для e-com workspace'а бесполезны:

- ❌ `deploy/` — Dockerfile.node/python, docker-compose, nginx configs, pyproject.toml
- ❌ `scripts/connect-vps.sh`, `deploy-dev.sh`, `deploy-prod.sh`, `smoke-test.sh`
- ❌ Скиллы: `deploy-dev`, `deploy-prod`, `rollback`, `cherry-pick`, `merge-to-prod`, `test`, `qa-tester`
- ❌ Агенты: `deployer.md`, `test-runner.md` (нет кода для деплоя/тестов)
- ❌ PostToolUse ruff hook в `.claude/settings.json` (нет Python src/)
- ❌ `VERSION` файл (workspace не версионируется по semver)
- ❌ SEO-скиллы (`seo-audit`, `seo-content`, `seo-positions`, `seo-research`, `_seo-shared`) — **уже есть локально**, более свежие
- ❌ `skill-creator`, `agent-creator`, `project-manager`, `lawyer`, `backup` — **уже есть локально**
- ❌ `.claude/agents/docs-generator.md` — привязан к DEV/PROD окружениям, не твой случай

---

## 📋 Финальный чек-лист импорта (при подтверждении)

Файлы, которые будут созданы (абсолютные пути):

```
vibecommerce_test_code/
├── AGENDA.md                                            # новый — working memory
├── _specs/
│   ├── README.md                                        # новый
│   ├── RECOMMENDED_SYSTEM.md                            # новый (blueprint)
│   └── templates/
│       ├── user-spec.md                                 # новый
│       ├── tech-spec.md                                 # новый
│       └── task.md                                      # новый
├── _status/
│   └── PROJECT_STATUS.md                                # новый (переименован из DEVELOPMENT_STATUS)
├── _changelogs/
│   └── workspace.md                                     # новый (пустой шаблон)
├── documentation/
│   ├── AI_AGENT_BEST_PRACTICES.md                       # новый
│   ├── SYSTEM_ARCHITECTURE.md                           # новый
│   └── ERROR_REGISTRY.md                                # новый
├── .claude/
│   └── skills/
│       ├── commit/SKILL.md                              # новый [TIER 2 — подтвердить]
│       ├── git-status/SKILL.md                          # новый [TIER 2 — подтвердить]
│       ├── architect/SKILL.md                           # новый [TIER 2 — подтвердить]
│       ├── docs/SKILL.md                                # новый [TIER 2 — подтвердить]
│       └── workspace-audit/SKILL.md                     # новый [TIER 2 — адаптация techdebt]
└── CLAUDE.md                                            # редактирование (+ Language + Self-Reflection)
```

**Итого новых файлов:** ~10 (TIER 1) + до 5 скиллов (TIER 2)
**Итого правок:** 1 (`CLAUDE.md`)

---

## ❓ Вопросы к тебе перед стартом

1. **TIER 2 скиллы** (`commit`, `git-status`, `architect`, `docs`, `workspace-audit`) — импортируем все или выборочно?
2. **`AGENTS.md` для Codex CLI** — пропускаем (по умолчанию) или нужен?
3. **Скилл `techdebt` → `workspace-audit`** — делаем адаптацию под e-com workspace (проверка битых ссылок в .md, пустые папки, устаревшие TODO в backlog/README), или копируем as-is?
4. **Плагины в `settings.local.json`** — добавить недостающие или сделаешь сам через `/config`?
5. **Переименование `DEVELOPMENT_STATUS.md → PROJECT_STATUS.md`** — ок, или оставить исходное имя?

---

## Ожидаемая последовательность выполнения

1. Создать директории `_specs/`, `_specs/templates/`, `_status/`, `_changelogs/`
2. Скачать TIER 1 файлы из GitHub API (curl/gh) → сохранить локально
3. Адаптировать тексты (убрать упоминания `dev`/`prod`/`VERSION`/`Docker` там, где неуместно)
4. Вставить в `CLAUDE.md` блок Language + Self-Reflection
5. (При подтверждении TIER 2) скачать и адаптировать скиллы
6. Обновить `README.md` в корне — отразить новую структуру папок
7. Обновить `MEMORY.md` (auto-memory) — запись о новых конвенциях `_specs/`, `_status/`, `AGENDA.md`
8. Предложить `/backup`

---

**Статус плана:** DRAFT — ждёт подтверждения пользователя.
