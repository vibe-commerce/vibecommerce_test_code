# 00-FORKING-GUIDE.md — как форкать шаблон под новый проект

Last Updated: 2026-05-02

Шаблон [EMPTY_code](https://github.com/VadimDSL/EMPTY_code) — готовая
скелетная структура проекта с Claude Code skills, агентами, правилами,
дизайн-системой и инфраструктурой деплоя. Этот гайд проведёт тебя через
форк до первого `make run`.

## Шаг 0. Создать форк

```bash
git clone https://github.com/VadimDSL/EMPTY_code.git my-project
cd my-project
rm -rf .git && git init
git remote add origin https://github.com/<user>/<repo>.git
```

или через GitHub UI: «Use this template» → создать репо.

## Шаг 1. Заменить placeholders в корневых файлах

В шаблоне placeholders заключены в `{фигурные скобки}`. Пройди файлы по
порядку и замени всё.

### CLAUDE.md (13 placeholders)

| Placeholder | Что вписать |
|-------------|-------------|
| `{Название проекта}` | имя проекта в заголовке |
| `{Одно-два предложения: что за проект…}` | описание |
| `{Python 3.11+ / TypeScript / ...}` | язык |
| `{aiogram 3.x / Astro / Next.js / ...}` | фреймворк |
| `{Supabase / PostgreSQL / SQLite / ...}` | БД |
| `{Redis / ...}` | кэш (или удали строку) |
| `{VPS / Vercel / ...}` | хостинг |
| `{Docker / GitHub Actions / ...}` | CI/CD |
| `{dev URL}`, `{dev DB}` | DEV окружение |
| `{prod URL}`, `{prod DB}` | PROD окружение |
| Секция **Key Files** (5 строк) | каноничные файлы проекта |
| Секция **File Editing Rules** | file-type-specific правила (Excel / Notebooks / SQL / dist) — или удали секцию, если для твоего стека таких правил нет |

### README.md (2 placeholders)

| Placeholder | Что вписать |
|-------------|-------------|
| `{repo}` (в Quick Start) | путь к git-репо |
| Заголовок «Claude Code Project Template v0.2.0» | замени на имя проекта |

### AGENDA.md (6 placeholders)

Текущий фокус сессии. Очисти содержимое и пиши новое.

### FACTS.md (19 placeholders)

Стабильные факты проекта (бренд, команда, продукты). Заполни один раз —
обновляй раз в квартал.

### ROADMAP.md (7 placeholders)

Стратегические фазы. Опиши свои.

### documentation/01-OVERVIEW.md (6 placeholders)

| Placeholder | Что вписать |
|-------------|-------------|
| `{date}` | сегодняшняя дата (`YYYY-MM-DD`) |
| `{Что за проект}`, `{Зачем}`, `{Целевая аудитория}` | описание |
| Стек | повтор из CLAUDE.md |

## Шаг 2. Скрипты деплоя (опционально, если деплоишь на VPS)

| Файл | Placeholders | Что вписать |
|------|--------------|-------------|
| `scripts/deploy-dev.sh` | 12 | домен, SSH-хост, проект, юзер |
| `scripts/deploy-prod.sh` | 12 | то же для PROD |
| `scripts/connect-vps.sh` | 37 | VPS-команды (postgres, redis, logs) |
| `scripts/smoke-test.sh` | 23 | URLs и эндпоинты для smoke-тестов |

В шапке каждого скрипта есть секция `CONFIGURATION`. Замени:

- `{YOUR_DOMAIN}` — домен
- `{your-vps-host}` — SSH-хост из `~/.ssh/config`
- `{project}` — имя проекта
- `{user}` — пользователь VPS

Если деплой не на VPS (например Vercel) — удали неактуальные скрипты и
замени `_practices/` ссылки соответственно.

## Шаг 3. Конфигурация Python-проекта (если Python)

| Файл | Что менять |
|------|-----------|
| `pyproject.toml` | имя проекта, описание, зависимости |
| `config/default.yaml` | базовые настройки |

Если стек **не** Python — удали `pyproject.toml`, `Makefile` (или адаптируй)
и каталог `tests/`.

## Шаг 4. Очистить пример кода

Шаблон содержит skeleton:

```
src/
├── main.py          # пример "hello world"
├── config.py
├── collectors/
├── processors/
├── storage/
└── utils/
```

Удали или замени `main.py`, `collectors/`, `processors/`, `storage/`
своим кодом. Структура папок — это рекомендация (Three-Layer Rule), не
обязаловка.

## Шаг 5. Удалить специфичное под автора

```bash
# Удалить подпапку, если в ней нет нужного для тебя
rm -rf _specs/jtbd-research/   # AJTBD-исследование Замесина
rm -rf design-system/AI-generated-mockups/  # макеты другого проекта

# Очистить changelog предыдущего автора (но оставить README)
rm _changelogs/0.1.0-*.md _changelogs/0.2.0-*.md
```

## Шаг 6. Skills и agents — что оставить

В `.claude/skills/` лежат универсальные skills (deploy, commit, test, ...).
Их можно оставить все — они дёшево живут в репо и могут пригодиться.

Если что-то не нужно — просто удали папку skill'а, он перестанет показываться
в slash-команде Claude Code.

## Шаг 7. Адаптировать skill `project-knowledge`

В `.claude/skills/project-knowledge/references/` 4 reference-файла описывают
**этот** шаблон. Под форк адаптируй:

- `architecture.md` — твоя структура папок (если меняется)
- `workflow.md` — твой Git-workflow (если ветки другие)
- `patterns.md` — твои конвенции имён
- `lifecycle.md` — обычно не трогай (универсальный)

## Шаг 8. Установка и первый запуск

```bash
make install          # uv sync или npm install
make run              # smoke-проверка
make test             # тесты должны проходить (или быть пустыми)
make lint             # lint должен быть чистым
```

## Шаг 9. Первый коммит

```bash
git add -A   # ВНИМАНИЕ: проверь git status, чтобы не закоммитить .env
git status
git commit -m "init: fork from EMPTY_code v0.2.0"
git push -u origin main
```

## Шаг 10. Настроить CLAUDE.local.md (опционально)

Если у тебя есть личные правила, которые не должны попасть в команду —
создай `CLAUDE.local.md` (он в `.gitignore`). Anthropic подгружает его как
3-й уровень CLAUDE.md.

```markdown
<!-- CLAUDE.local.md -->
# Личные правила Vadim

- Когда я говорю «деплой» без указания env — спрашивай, dev или prod
- ...
```

## Адаптация под тип проекта

Шаблон универсальный — Python / TypeScript / Web / контент. Под конкретный
тип — следующие подсказки.

### Python Backend (Telegram-бот, FastAPI, парсер)

- **CLAUDE.md → Стек:** Python 3.11+, aiogram / FastAPI, Supabase / PostgreSQL, Redis, Docker
- **Архитектура:** Handlers → Services → Repositories
- **Команды:** `make install`, `make run`, `make test`, `ruff check src/`
- **`.claude/settings.json` hook:** `ruff check --fix` после Write на `.py` (уже настроен)
- **Удалить:** `design-system/` (если без UI)
- **Полезные skills:** `/test`, `/deploy-dev`, `/deploy-prod`, `/logs`

### Web Frontend (Astro, Next.js, React)

- **CLAUDE.md → Стек:** TypeScript, Astro / Next.js, Tailwind CSS, Vercel
- **Архитектура:** Pages → Components → Data
- **Команды:** `npm run dev`, `npm run build`, `npm test`
- **`.claude/settings.json` hook:** `prettier --write` или `eslint --fix` (см. `deploy/hooks-examples.md`)
- **Оставить:** `design-system/` (полезный каталог токенов)
- **Удалить:** `pyproject.toml`, `Makefile` (или адаптировать), `tests/conftest.py`
- **Добавить в CLAUDE.md:** Component Naming Convention, Routing-таблицу, Analytics Events
- **Полезные skills:** `/design-system`, `/qa-tester` (Playwright)

### Контент / PM проект (без кода)

- **CLAUDE.md:** убрать секции «Стек», «Архитектура», «Окружения», «Деплой»
- **Добавить:** Команда проекта, Целевая аудитория, «Как со мной работать»
- **Удалить:** `src/`, `tests/`, `pyproject.toml`, `Makefile`, `scripts/deploy-*.sh`
- **Активно использовать:** `FACTS.md`, `ROADMAP.md`, README в каждой папке
- **Полезные skills:** `/project-manager`, `/web-research`, `/lawyer`, `/jtbd-research`

### Гибридный (бизнес + код)

- Оставить всё, удалить только явно ненужное
- В CLAUDE.md описать оба слоя: «Бизнес-контекст» + «Технический стек»
- Для domain-skills — копировать индивидуальные skill-папки из других репо

## Чек-лист после форка (TL;DR)

- [ ] CLAUDE.md — заполнены 13 placeholder'ов + Key Files + File Editing Rules
- [ ] README.md — заголовок и Quick Start
- [ ] AGENDA.md, FACTS.md, ROADMAP.md — наполнены
- [ ] documentation/01-OVERVIEW.md — заполнен
- [ ] pyproject.toml / package.json — имя проекта, зависимости
- [ ] scripts/*.sh — заполнены или удалены
- [ ] src/ — заменён скелет на свой код
- [ ] Удалено специфичное под автора (jtbd-research, AI-mockups, старые changelog)
- [ ] skill `project-knowledge` адаптирован под структуру форка
- [ ] `make install && make run` проходит
- [ ] Первый коммит и push на свой remote
- [ ] (опционально) `CLAUDE.local.md` для личных правил

## Миграция с 0.2.x на 0.3.0

В релизе 0.3.0 устранены 5 групп дубликатов skill↔agent и 4 «тяжёлых»
skill вынесены в саб-агенты для изоляции контекста. Если форк синхронизирует
шаблон — нужны точечные действия.

### Что удалено

| Файл | Замена | Действие в форке |
|------|--------|------------------|
| `.claude/agents/git-ops.md` | skills `/commit`, `/push`, `/cherry-pick`, `/merge-to-prod`, `/git-status`, `/backup` | Если в форке вызывался `Agent(subagent_type="git-ops")` — заменить на конкретный slash |
| `.claude/agents/deployer.md` | skills `/deploy-dev`, `/deploy-prod`, `/docs` | Если в форке вызывался `Agent(subagent_type="deployer")` — разнести по slash'ам |
| `.claude/skills/web-research/` | агент `web-researcher` | Если в форке вызывался `/web-research` — пользователь теперь триггерит фразой («исследуй», «research», «найди») или через делегацию |
| `.claude/skills/techdebt/` | агент `techdebt-scanner` | То же — фразой («tech debt», «техдолг») или из других агентов |

### Что изменилось

| Skill | Что было | Что стало |
|-------|----------|-----------|
| `/test` | Сам запускал lint/types/tests | Тонкий entry, делегирует `test-runner` через Agent tool. Поведение для пользователя идентично |
| `/docs` | Сам обновлял 5 файлов | Тонкий entry, делегирует `docs-generator`. Расширен: ERROR_REGISTRY, `_changelogs/{env}.md` |
| `/lawyer` | Сам отвечал | Тонкий entry, делегирует `lawyer` агент |
| `/seo-audit` | Сам аудитил | Тонкий entry, делегирует `seo-auditor` агент |
| `/deploy-prod` | Без sync-check | Добавлен шаг 3 «Sync check» (git fetch + status), нумерация шагов сдвинулась 3→4..7→8 |

### Что добавлено

4 новых субагента в `.claude/agents/`:

- `lawyer.md` — Юрист РФ (B2C/ЗоЗПП/152-ФЗ)
- `web-researcher.md` — структурированный интернет-ресёрч
- `techdebt-scanner.md` — сканер техдолга
- `seo-auditor.md` — SEO+AEO аудит

Все с `model: inherit` и минимальным набором tools (read-only там, где возможно).

### Чек-лист миграции форка

- [ ] Pull шаблона (или ручной merge `.claude/` директории)
- [ ] Убрать любые ссылки на удалённые subagents в кастомных скиллах форка
- [ ] Если в форке были свои дополнения к удалённым `web-research/SKILL.md`
      или `techdebt/SKILL.md` — перенести их в новые субагенты
- [ ] Smoke-проверка ключевых скиллов: `/test`, `/docs`, `/deploy-prod`
- [ ] Обновить кастомный CLAUDE.md форка, если он ссылается на удалённые
      пути

## Миграция с 0.3.x на 0.4.0

В 0.4.0 разделены два мета-skill: один для Claude Agent SDK (Python/TS),
другой — для Claude Code subagents (`.claude/agents/`).

### Что переименовано

| Было | Стало | Что делать в форке |
|------|-------|---------------------|
| `/agent-creator` (был про SDK) | `/agent-sdk-builder` | Если в форке использовался для Python/TS SDK — переключиться на `/agent-sdk-builder` |

### Что новое

- **`/agent-creator`** — теперь про создание Claude Code subagents в
  `.claude/agents/<name>.md`. 6 шагов: decision tree → frontmatter → prompt
  → tools → model → тестирование. 4 reference-файла.
- **`skill-creator/references/`** — добавлены 4 файла: `anti-patterns.md`,
  `evaluation-driven.md`, `claude-code-extensions.md`, `limits-and-budgets.md`.
  Это дополнения, `SKILL.md` upstream-совместим (Apache 2.0 копия Anthropic).

### Чек-лист миграции 0.3.x → 0.4.0

- [ ] Pull шаблона
- [ ] Если форк использовал `/agent-creator` для Python/TS SDK — заменить
      все ссылки на `/agent-sdk-builder`
- [ ] Если в форке свой `.claude/skills/agent-creator/` — решить, оставлять
      ли его как override (project scope > user/plugin) или удалить и
      использовать новый шаблонный
- [ ] Smoke: фраза «создай саб-агента» → должна триггерить `agent-creator`,
      «build SDK app on Python» → `agent-sdk-builder`
- [ ] Если у форка пишутся свои skills — посмотреть новые references в
      `skill-creator/references/` (anti-patterns, evaluation-driven)

## Связанные

- Родитель: [`README.md`](README.md)
- Шаблон: [VadimDSL/EMPTY_code](https://github.com/VadimDSL/EMPTY_code)
- Описание архитектуры: skill `project-knowledge` → `references/architecture.md`
- Workflow: skill `project-knowledge` → `references/workflow.md`
- Anti-patterns CLAUDE.md: [`90-AI-AGENT-BEST-PRACTICES.md`](90-AI-AGENT-BEST-PRACTICES.md)
