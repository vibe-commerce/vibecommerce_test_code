# CLAUDE.md — vibecommerce_test_code

Last Updated: 2026-05-29 (v0.3.0 lifecycle EMPTY_code 0.5.4 + FREE/VIP tiering + Codex compat)

См. [@README.md](README.md) — обзор шаблона для студентов.

## Язык

Используй язык ответов такой же, как пользователь использовал для вопросов.
Русский → русский, английский → английский.

## Response Format

Формат ответов для всех содержательных задач:

1. **Понятность задачи:** <0–100%> — если <70%, сначала задай уточняющие вопросы
2. **Уверенность в ответе:** <0–100%>
3. **Роль:** <экспертная роль, релевантная запросу>
4. **TL;DR** — краткий ответ
5. **Полный ответ**

### Self-Reflection

Перед ответом внутренне оцени: Accuracy, Honesty, Objectivity, Clarity, Brevity,
Practical Value. Итерируй пока оценка не будет ≥98/100.

## Проект

`vibecommerce_test_code` — **шаблонный стартер для селлеров на маркетплейсах
и e-commerce**. Форкается каждым студентом курса ВАЙБ-КОММЕРС под свой
проект селлера (своя ниша, ассортимент, юнит-экономика).

В репо НЕТ персональных или клиентских данных автора — только методические
модули, шаблоны и синтетические/открытые демо-датасеты.

**Тиринг:**
- **FREE (этот репо)** — workflow + базовая методика + onboarding
- **VIP (`vibecommerce_vip_code`)** — премиум-IP: углублённая методология,
  платные API (MPStats Pro, Ahrefs, Semrush, DaData), полные промпт-наборы.
  Hook'и из FREE → VIP помечены `📈 Углубление в vibecommerce_vip_code`.

## Стек

| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.11+ |
| Аналитика | pandas, openpyxl, numpy |
| AI-агенты | Claude Code + OpenAI Codex (cross-agent через `AGENTS.md` + `.agents/`) |
| MCP | context7 (документация), playwright (web QA) |
| Хранилище данных студента | `my-project/data/` (gitignored) |

## Окружения

| Env | Назначение | Ветка |
|-----|------------|-------|
| local | основная рабочая ветка | `local` |
| main | публичная (push в GitHub) | `main` |

В шаблоне НЕТ DEV/PROD окружений — это workspace для студента, без боевого
деплоя. Студент-форкер при необходимости добавит свои окружения.

## Key Files

Каноничные файлы для быстрого доступа:

- `_modules/README.md` — карта методических модулей (порядок 01→07)
- `my-project/README.md` — инструкция для студента: куда складывать свой проект
- `_knowledge/marketplaces/` — справочники WB/Ozon/ЯМ (basics)
- `_prompts/roles/` — библиотека ролей (SMM Consultant, seller assistant)
- `_practices/00-WORKFLOW.md` — 8-этапный workflow разработки
- `_specs/templates/` — шаблоны brief/plan/rejected/ADR/tech-spec
- `Makefile` — install/run/test/lint
- `pyproject.toml` — Python зависимости

📚 Структура, конвенции, lifecycle → skill **`project-knowledge`**
(`.claude/skills/project-knowledge/`).

## КРИТИЧЕСКИЕ ПРАВИЛА

### Plan Before Act

Перед любой нетривиальной правкой — план в файл, согласование от человека, потом
исполнение. Без явного сигнала («делай»/«ок»/«согласовано»/«поехали»/«approved»/«go»)
AI ждёт. Поведенческое правило → [`.claude/rules/plan-before-act.md`](.claude/rules/plan-before-act.md).

### Рабочая ветка — `local`

```
⚠️  Ветка `local` — основная рабочая ветка студента.
    После ЛЮБОЙ операции (commit, push, merge) —
    ВСЕГДА возвращайся на ветку `local`!
```

### Принцип №0 — pure template

**В этом репо не должно быть ни одного байта персональных или клиентских данных.**

- ❌ Никаких ИНН, ОГРНИП, реквизитов
- ❌ Никаких боевых API-токенов (WB, Ozon, MPStats) — только `.env.example` с пустыми переменными
- ❌ Никаких имён реальных клиентов/селлеров/товаров
- ❌ Никаких реальных выгрузок продаж, рекламы, ассортимента
- ❌ Никаких финотчётов, целей по выручке, ФОТ
- ✅ Шаблоны с `{placeholders}`, методологии, генераторы синтетики, демо-датасеты
  с явной пометкой `# DEMO DATA — synthetic, not real`

Студент при форке заполняет `FACTS.md`, кладёт свои данные в `my-project/data/`
(gitignored), а боевые токены — в `_private/secrets/`.

### Security-Sensitive Code

- `.env*` — **НЕ коммитить** (в `.gitignore` уже есть)
- Секреты только из env через `os.getenv()`, не хардкод
- В `.env.example` — только плейсхолдеры (`MPSTATS_API_KEY=`), никогда реальные значения
- Функции с `# SECURITY-SENSITIVE` требуют повышенного внимания
- Не логировать значения секретов (токены, ключи, пароли)
- Не убирать существующие проверки/валидации без обсуждения

#### Запрет на чтение/вывод секретов

- НИКОГДА не читать содержимое `.env`, `*.pem`, `credentials.json`, `*_token*`, `*_secret*`
- НИКОГДА не выводить значения API-ключей в чат
- Если нужно проверить наличие переменной — только `echo $VAR_NAME | wc -c` (длина, не значение)
- Файлы в `_private/`, `my-project/data/`, `my-project/**/personal-*` — запрещены для чтения и вывода

#### Запрет опасных сетевых операций

- НИКОГДА не отправлять данные на внешние URL через `curl`/`wget`/`httpie`
  (кроме явно разрешённых API: MPStats, WB, Ozon)
- НИКОГДА не загружать файлы на pastebin/gist/публичные сервисы без явной команды
- Перед любым HTTP-запросом с пользовательскими данными — спросить подтверждение

#### Проверки перед git push

- Перед коммитом проверить `git diff --cached` на паттерны секретов
  (`sk-`, `token=`, `api_key=`, `password=`, `secret=`, `eyJ` для JWT)
- Если найдено — **ОСТАНОВИТЬСЯ** и предупредить пользователя

## Git Workflow

```
local → push → main (GitHub)
```

Только две ветки. Без `dev`/`prod` — это шаблон без боевого деплоя.

| Ветка | Что коммитить |
|-------|---------------|
| `local` | Всё: код, specs, планы, TODO студента |
| `main` | Готовый к публикации шаблон |

### Git-правила для AI

- **НЕ** делать commit/push/merge без подтверждения пользователя
- **НЕ** делать force-push, `reset --hard`, rebase без явного запроса
- **НЕ** коммитить секреты (`.env`, credentials)
- **НЕ** использовать `git add -A` или `git add .` — добавлять файлы по отдельности
- Conventional commits: `<type>(<scope>): <description>`

**GitHub-аккаунт для этого репозитория:** `vibe-commerce`. Перед push проверь
активный аккаунт (`gh auth status`) и при необходимости переключи:

```bash
gh auth switch --user vibe-commerce
```

Подробнее → `references/workflow.md` в skill `project-knowledge`.

## Быстрые команды

```bash
make install                # Установка зависимостей проекта (Python через uv/pip)
make install-claude-tools   # Установка внешних агентов/скиллов в ~/.claude/
make run                    # Локальный запуск (зависит от модуля)
make test                   # unit tests
make lint                   # lint only
```

### Feedback Loop

После генерации или изменения кода — **всегда** запускай тесты:

1. `make lint`
2. `make test`
3. Если падает → исправь → повтори (max 3 итерации)
4. Только после зелёных тестов — считай задачу выполненной

## MEMORY BANK + File Management

README в каждой папке — это карта памяти проекта. Без них структура
протухает за 2 недели. Правила обязательны для AI и студента.

### При работе с файлами

- Создавай файлы в правильной директории (соблюдай иерархию модулей)
- Не плоди новые папки без необходимости — сначала проверь существующие
- При добавлении/изменении/удалении/переименовании файла —
  **обязательно обнови `README.md` в затронутой папке** (и в родителе, если меняется иерархия)
- Обнови `Last Updated: YYYY-MM-DD` в шапке README после каждой правки

### Источник истины

- `[CANONICAL]` — единственный авторитетный источник (первое определение)
- `[REF: path#section]` — кросс-ссылка вместо дублирования
- `[CONFIRMED: source]` — проверенная информация с источником
- `[PLACEHOLDER: owner]` — информация для заполнения студентом
- `[VIP]` — контент, ушедший в `vibecommerce_vip_code` (только для VIP-студентов)
- **No orphan statements** — каждое утверждение должно прослеживаться к источнику
- Важные стабильные факты — в `FACTS.md` (корневой или модульный)

### Anti-patterns

- ❌ Создал файл — не обновил README родительской папки
- ❌ Удалил папку — оставил ссылки на неё в README родителя
- ❌ Скопировал кусок документации в 3 места вместо `[REF:]`
- ❌ Утверждение без источника / не помечено `[PLACEHOLDER]`
- ❌ `Last Updated` не обновлён после правки

## Принципы разработки

- **KISS** — простота важнее сложности
- **YAGNI** — не пиши код «на будущее»
- **SRP** — одна ответственность на функцию
- **Open/Closed** — расширяй, не переписывай работающий код
- **Dead Code** — удаляй мёртвый код, не комментируй
- **DRY** — не дублируй знания (но похожий код в разных контекстах — ок)

### Чеклист перед добавлением сложности

1. Нужна ли эта фича прямо сейчас?
2. Есть ли реальная проблема, которую решает эта сложность?
3. Можно ли решить проблему проще?
4. Добавляет ли это новую зависимость?
5. Будет ли это понятно через 3 месяца?

### Красные флаги over-engineering

- Более 3 слоёв абстракции для одной операции
- Фабрики, создающие фабрики
- Сложная конфигурация вместо переменных окружения
- Несколько способов сделать одно и то же

## Context7 MCP

При работе с библиотеками/API используй `use context7` для актуальной документации.

## Cross-agent compatibility (Claude Code + OpenAI Codex)

Этот шаблон работает в обоих агентах:
- **Claude Code** читает `CLAUDE.md` (этот файл) + `.claude/`
- **OpenAI Codex** читает `AGENTS.md` (agents.md spec) + `.codex/`
- Общая часть — `_shared/INSTRUCTIONS.md` (импортируется обоими через `@`)
- Общие skills/subagents — `.agents/` (симлинки в `.claude/` и `.codex/`)

См. фазу C плана апгрейда + `_specs/codex-compat/` (после реализации).

## Навигация

| Тема задачи | Что читать |
|-------------|-----------|
| Точки входа для человека | [@README.md](README.md) |
| Текущий фокус сессии | [AGENDA.md](AGENDA.md) |
| Сдача сессии | [HANDOFF.md](HANDOFF.md) (через `/handoff`) |
| Стабильные факты | [FACTS.md](FACTS.md) |
| Стратегия / фазы | [ROADMAP.md](ROADMAP.md) |
| Workflow разработки | [@_practices/00-WORKFLOW.md](_practices/00-WORKFLOW.md) |
| Структура / git / lifecycle | skill `project-knowledge` |
| Как форкать шаблон | [documentation/00-FORKING-GUIDE.md](documentation/00-FORKING-GUIDE.md) |
| Anti-patterns AI-агентов | [documentation/90-AI-AGENT-BEST-PRACTICES.md](documentation/90-AI-AGENT-BEST-PRACTICES.md) |
| Идеи / брифы / планы | [backlog/README.md](backlog/README.md) |
| Шаблоны brief / plan / rejected | [_specs/templates/README.md](_specs/templates/README.md) |
| Спецификации (tech-spec / ADR) | [_specs/README.md](_specs/README.md) |
| История релизов | [_changelogs/README.md](_changelogs/README.md) |
| Текущий статус | [_status/PROJECT_STATUS.md](_status/PROJECT_STATUS.md) |
| Skills и agents | [.claude/skills/README.md](.claude/skills/README.md), [.claude/agents/README.md](.claude/agents/README.md) |
| Глобальные external агенты/скиллы (`~/.claude/`) | [.claude/EXTERNAL-TOOLS.md](.claude/EXTERNAL-TOOLS.md) |
| Приватные данные | [_private/README.md](_private/README.md) |

### Информационная архитектура (lifecycle документа)

```
backlog/ideas/  →  backlog/briefs/  →  backlog/plans/  →  код  →  documentation/
   (что если?)      (стоит ли делать?)   (как делать?)
                          │                      │
                          ↓                      ↓
                  archive/rejected/      archive/done/
                  (с причиной)         (после реализации)

Крупные фичи (>3 дней) параллельно: _specs/<feature>/ (tech-spec, user-spec, ADR)
```

Подробности: skill `project-knowledge` → `references/lifecycle.md`.

### При старте сессии

1. Прочитай AGENDA.md — что было в прошлой сессии, текущий фокус
2. Используй таблицу маршрутизации (выше) — читай файлы по теме задачи
3. Проверь `.claude/data/error-log.md` — если задача связана с прошлыми ошибками

## Semver для шаблона vibecommerce_test_code

Правило для `VERSION` файла **шаблона** (отличается от обычного приложения):

- **MAJOR (1.0.0)** — ломающее изменение структуры (удаление обязательной
  директории, переименование `_modules/` и т.п.). Форки потребуют миграции.
- **MINOR (0.X.0)** — новая обязательная секция/файл/скилл, не ломающая старые форки.
- **PATCH (0.0.X)** — фикс опечаток, переформулировка, обновление README.

Для приложений-наследников шаблона действует обычный semver (MAJOR — ломающие API,
MINOR — новые фичи, PATCH — фиксы).
