# MCP Setup — аудит и рекомендации для EMPTY_code

Last Updated: 2026-05-02
Owner: Vadim Bakanov
Status: brief (черновик рекомендаций)

## TL;DR

- **Подключено:** Context7 (✓), Playwright (через plugin, ✓), Google Drive/Gmail/Calendar (требуют OAuth, не активированы).
- **Дубль:** Context7 подключён дважды — напрямую через npx (`~/.claude/mcp.json`) и через плагин `context7@claude-plugins-official`. Один источник нужно отключить, иначе модель видит дублированные инструменты в промпте.
- **Несовпадение настроек:** в `~/.claude/settings.json` Playwright из `claude-plugins-official`, в `EMPTY_code/.claude/settings.json` — `playwright@anthropic-official`. Привести к одному источнику.
- **Топ-3 рекомендуемых** (must-add по приоритету): **GitHub MCP** → **Filesystem MCP** → **Sequential Thinking MCP**.
- **По стеку проекта:** добавить **Supabase MCP** (PostgreSQL), **Vercel MCP** (Astro/Next.js), **Sentry MCP** (errors), **Exa MCP** (мощный web search для код-примеров).

## 1. Что уже подключено (факт)

| MCP | Откуда | Статус | Назначение |
|-----|--------|--------|-----------|
| context7 | `~/.claude/mcp.json` (npx) + plugin `context7@claude-plugins-official` | ✓ Connected (дубль) | Актуальная документация библиотек |
| playwright | plugin `playwright@claude-plugins-official` (user) / `playwright@anthropic-official` (project) | ✓ Connected | Browser automation, e2e, визуальное QA |
| Google Drive | Anthropic-managed (`drivemcp.googleapis.com`) | ⚠️ Needs auth | Доступ к файлам Google Drive |
| Google Calendar | Anthropic-managed | ⚠️ Needs auth | Календарь, события |
| Gmail | Anthropic-managed | ⚠️ Needs auth | Поиск/отправка писем |

**Действия:**
1. Решить дубль `context7`: оставить **plugin-версию** (она единая для всех проектов через `enabledPlugins`), удалить `npx`-версию из `~/.claude/mcp.json`.
2. Привести Playwright к единому источнику: `playwright@claude-plugins-official` в обоих файлах.
3. Решить, нужна ли Google-триада. Для текущего workflow (skills, бэклог в `backlog/`, спеки в `_specs/`) — **не нужна**. Если будет интеграция с Google Docs / расписанием встреч — авторизовать.

## 2. Лучшие практики (источники)

Источники, на которых построены рекомендации:

- [Anthropic MCP Registry API](https://api.anthropic.com/mcp-registry/v0/servers) — официальный реестр серверов с метаданными `worksWith: [claude-code, claude-api, claude-desktop]`. Из 100 серверов 84 совместимы с Claude Code.
- [modelcontextprotocol/servers (GitHub)](https://github.com/modelcontextprotocol/servers) — 7 эталонных серверов от MCP steering group: Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking, Time.
- [Claude Code MCP docs](https://code.claude.com/docs/en/mcp) — официальная инструкция по подключению.
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) — plugin-каталог Anthropic (там Context7, Playwright, Linear, GitHub и т.д.).
- Сводки 2026: [Bannerbear](https://www.bannerbear.com/blog/8-best-mcp-servers-for-claude-code-developers-in-2026/), [Toolradar](https://toolradar.com/blog/best-mcp-servers-claude-code), [MCPcat](https://mcpcat.io/guides/best-mcp-servers-for-claude-code/), [Builder.io](https://www.builder.io/blog/best-mcp-servers-2026), [Apidog](https://apidog.com/blog/top-10-mcp-servers-for-claude-code/), [DeployHQ](https://www.deployhq.com/blog/best-mcp-servers-for-web-developers).

Сходимость источников: **GitHub, Sequential Thinking, Playwright, Context7, Filesystem** — упоминаются почти во всех топах как ядро для Claude Code.

## 3. Семь эталонных reference-серверов Anthropic

Из [официального репозитория MCP steering group](https://github.com/modelcontextprotocol/servers):

| Сервер | Что делает | Нужен ли тебе |
|--------|-----------|--------------|
| **Filesystem** | Безопасные файловые операции с конфигом доступа | ✅ ДА — у тебя 12+ репо в `_CODE/`, сейчас `additionalDirectories` хардкодишь руками в `settings.local.json` |
| **Memory** | Граф-знаний для долговременной памяти между сессиями | ⚠️ Скорее НЕТ — у тебя уже работает auto-memory в `~/.claude/projects/.../memory/` + `MEMORY.md`. Дубль |
| **Sequential Thinking** | Структурированное reflective-мышление | ✅ ДА — твой `think-through` plugin делает похожее, но Sequential Thinking даёт нативные thinking-блоки для архитектурных решений |
| **Git** | Чтение/поиск в git-репозиториях | ⚠️ Не критично — `git` через Bash покрывает 95% сценариев |
| **Fetch** | HTTP-запросы и конвертация HTML→Markdown | ⚠️ НЕТ — встроенный `WebFetch` уже есть |
| **Time** | Конвертация timezone, текущее время | ✅ Можно — лёгкий, бесплатный, помогает в session-retrospective и при планировании |
| **Everything** | Test-server для разработки своих MCP | ❌ НЕТ — только для авторов MCP |

## 4. Рекомендуемые MCP по приоритету

### Tier 1 — поставить в первую очередь

#### 1. GitHub MCP

**Зачем:** у тебя есть `/commit`, `/push`, `/backup`, `/cherry-pick`, `/merge-to-prod` — все они используют `gh` CLI через Bash. GitHub MCP даёт прямой нативный доступ к PR, issues, code search, branches без context-switch и без парсинга текста.

**Использование в твоих скиллах:**
- `/backup` сможет создать PR с описанием на основе git diff
- `/git-status` сможет читать остальные ветки и непрозрачное состояние remote
- Для других репо (`vibecommerce_code`, `CRM_code` и т.д.) — единая навигация по issues

**Установка:** `claude mcp add --transport http github https://api.githubcopilot.com/mcp/` (требует GitHub PAT с правами `repo`).

#### 2. Filesystem MCP (reference)

**Зачем:** у тебя в `additionalDirectories` сейчас руками вписано 17 путей в `~/.claude/settings.json` и в project-level `settings.local.json`. Filesystem MCP заменяет это конфигом, плюс добавляет `read_file`, `write_file`, `move_file`, `search_files`, `list_directory` через структурированный интерфейс.

**Особенно полезно** для cross-repo работы (анализ скиллов в 12 репо одновременно — то, чем ты регулярно занимаешься, см. задачи в `backlog/`).

**Установка:** `claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem <путь-к-вашему-коду>`.

#### 3. Sequential Thinking MCP (reference)

**Зачем:** твой workflow требует Plan-then-Act (см. `_practices/01-plan-then-act.md`). Sequential Thinking добавляет нативный инструмент `think` со step-by-step reflection, ревизией предыдущих шагов и ветвлением гипотез — это делает планирование архитектуры более прозрачным.

**Дополняет, а не заменяет** твой plugin `think-through`: skill вызывает экспертов, а Sequential Thinking — структурирует одиночный размышляющий проход внутри одного запроса.

**Установка:** `claude mcp add sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking`.

### Tier 2 — добавить под конкретные проекты твоего стека

#### 4. Supabase MCP

**Зачем:** в `CLAUDE.md` Supabase упомянут как один из вариантов БД. Если хотя бы один из активных репо использует Supabase (а судя по `vibecommerce_*`, `vadim_v*`, скорее всего да) — этот MCP позволяет писать/применять SQL миграции, инспектировать схемы и логи прямо из Claude.

**Установка:** [Supabase MCP](https://github.com/supabase/mcp-server-supabase) — официальный, есть в реестре Anthropic как `com.supabase/mcp`.

#### 5. Vercel MCP

**Зачем:** Astro / Next.js (упомянуты в `CLAUDE.md` как варианты) часто деплоятся на Vercel. Прямой доступ к деплоям, логам, переменным окружения, превью.

**Установка:** [Vercel MCP](https://vercel.com/docs/mcp/vercel-mcp) — официальный, в реестре как `com.vercel/vercel-mcp`.

#### 6. Sentry MCP

**Зачем:** error monitoring. У тебя есть `_status/` с состоянием окружений и `.claude/data/error-log.md` с правилом `error-learning`. Sentry MCP позволяет ассистенту вытащить актуальный stack trace при дебаге, не переключаясь на Sentry UI.

**Установка:** `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp` ([sentry-mcp](https://github.com/getsentry/sentry-mcp)).

**Подключай только если** реально используешь Sentry в активных проектах. Если нет — пропусти.

### Tier 3 — опционально, под нишевые сценарии

#### 7. Exa MCP — поиск документации/кода

**Зачем:** Exa делает семантический поиск по GitHub, документации, StackOverflow. В реестре как `ai.exa/exa`. Полезно когда `WebSearch` и Context7 не находят актуальный пример.

#### 8. Linear MCP — если перейдёшь на Linear

Сейчас бэклог ведёшь в `backlog/ideas/`, `backlog/briefs/`, `_specs/` — **не нужно**. Если соберёшься переехать — `app.linear/linear` есть в реестре Anthropic.

#### 9. Notion MCP — если объединить knowledge base

Тоже не нужно сейчас (skills + memory bank покрывают), но если внешним людям понадобится доступ к идеям — Notion MCP (`com.notion/mcp`) — путь.

#### 10. Figma MCP — для design-system

У тебя в репо есть `design-system/` (Vite + React + Tailwind) и `_specs/design/THEMES.md` с 4 темами. Если будешь работать с Figma-макетами — Figma MCP даёт точный доступ к токенам, переменным, структуре компонентов вместо скриншотов. Сейчас не критично.

#### 11. Time MCP (reference)

Лёгкий, бесплатный. Используется в `session-retrospective` и `Last Updated` метках. Можно поставить, но без него тоже живётся.

## 5. Что НЕ ставить

- **AWS MCP** — у тебя VPS/Docker, нет AWS в стеке.
- **Stripe** — нет платёжного бэкенда в активной разработке.
- **Jira / ClickUp / Asana** — у тебя свой workflow в `backlog/`.
- **Cloudflare** — пока не используешь Workers (если поедешь — добавь).
- **Fetch MCP** — встроенный `WebFetch` покрывает.
- **Memory MCP (reference)** — дублирует существующую auto-memory систему.
- **Git MCP (reference)** — Bash + `git` покрывает.

## 6. Финальный рекомендованный набор

```
✓ context7 (уже есть, убрать дубль)
✓ playwright (уже есть, привести к одному источнику)
+ github                      # Tier 1
+ filesystem                  # Tier 1
+ sequential-thinking         # Tier 1
+ supabase                    # Tier 2 (если активно используешь)
+ vercel                      # Tier 2 (если деплоишь Astro/Next.js на Vercel)
+ sentry                      # Tier 2 (если используешь Sentry)
```

7 серверов вместо текущих 2 — это минимально достаточный набор для twelve-repo polyglot setup без шума в промпте.

## 7. Чек-лист действий

- [ ] Удалить дубль context7: убрать запись из `~/.claude/mcp.json`, оставить plugin
- [ ] Привести `playwright` к одному ID в `~/.claude/settings.json` и `EMPTY_code/.claude/settings.json`
- [ ] Установить **github** MCP (`claude mcp add github`), создать PAT с `repo` scope
- [ ] Установить **filesystem** MCP с корнем `<путь-к-вашему-коду>`
- [ ] Установить **sequential-thinking** MCP
- [ ] Решить по **supabase** — какие репо реально его используют
- [ ] Решить по **vercel** — какие репо там деплоятся
- [ ] Решить по **sentry** — нужно ли error tracking прямо сейчас
- [ ] После установки: обновить `CLAUDE.md` в EMPTY_code, добавить раздел «MCP Setup» со списком и назначением каждого
- [ ] Прогнать `/handoff` или обновить `AGENDA.md` с новой инфраструктурой

## 8. Связанные документы

- [CLAUDE.md](../../CLAUDE.md) — раздел «Context7 MCP» (расширить)
- [`.claude/settings.json`](../../.claude/settings.json) — `enabledPlugins` и `permissions`
- `~/.claude/mcp.json` — глобальные MCP-конфиги
- [`backlog/briefs/2026-05-02-skills-vs-subagents-audit.md`](2026-05-02-skills-vs-subagents-audit.md) — параллельный аудит инструментов
- [`_practices/00-WORKFLOW.md`](../../_practices/00-WORKFLOW.md) — этап 4 (разработка) и 5 (feedback loop) — где MCP вписываются

## 9. Источники (проверено 2026-05-02)

- [Anthropic MCP Registry](https://api.anthropic.com/mcp-registry/v0/servers) — официальный API
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) — 7 reference servers
- [code.claude.com/docs/en/mcp](https://code.claude.com/docs/en/mcp) — Claude Code MCP docs
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) — официальный plugin marketplace
- [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp)
- Сводные обзоры 2026: [Bannerbear top-8](https://www.bannerbear.com/blog/8-best-mcp-servers-for-claude-code-developers-in-2026/), [Toolradar](https://toolradar.com/blog/best-mcp-servers-claude-code), [MCPcat](https://mcpcat.io/guides/best-mcp-servers-for-claude-code/), [Apidog top-10](https://apidog.com/blog/top-10-mcp-servers-for-claude-code/), [DeployHQ](https://www.deployhq.com/blog/best-mcp-servers-for-web-developers)
