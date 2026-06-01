# Handoff — 2026-05-08

> Загрузи этот файл в новую сессию: «прочти HANDOFF.md и продолжи».

## Состояние репозитория

- Branch: `local`
- Last commit: `97cb179 release(template): v0.5.4 — фиксы по верификации репозитория`
- Uncommitted: 4 новых файла (ресёрч + план кросс-совместимости), не коммичено по запросу пользователя:
  - `_specs/codex-compat/research.md` (мастер-сводка)
  - `_specs/codex-compat/research-claude-code.md`
  - `_specs/codex-compat/research-codex.md`
  - `_specs/codex-compat/research-cross-agent.md`
  - `backlog/plans/2026-05-08-codex-compatibility.md`
- Прочие unstaged изменения (не относятся к этой задаче): см. `git status` — наследие предыдущих сессий, в этой сессии не трогали.

## Что сделано в этой сессии

- **Уточнили задачу через вопросы**: пользователь выбрал конфигурацию C+C+C — Codex VS Code extension, максимальный паритет, оба файла канон с общим `_shared/INSTRUCTIONS.md`, max-порт скиллов и субагентов.
- **Запустили 3 параллельных web-research агентов** (web-researcher), каждый сохранил отдельный markdown-отчёт в `_specs/codex-compat/`:
  - Anthropic Claude Code 2026 — все фичи (`research-claude-code.md`, 266 строк, ~19KB).
  - OpenAI Codex 2026 (CLI + VS Code + Cloud) — все фичи (`research-codex.md`, 326 строк, ~24KB).
  - agents.md spec + cross-agent best practices 2026 (`research-cross-agent.md`, 211 строк, ~18KB).
- **Создали мастер-сводку** `_specs/codex-compat/research.md` — TL;DR, cross-mapping таблица Claude↔Codex, архитектурный выбор, риски, директорная схема, полный список источников.
- **Создали детальный план** `backlog/plans/2026-05-08-codex-compatibility.md` (~150 строк) по шаблону `_specs/templates/plan.md`: 7 фаз, чек-лист, риски, метрика успеха, оценка 12-18 часов.
- **План показан пользователю**, ждали явное «делай» по правилу `plan-before-act`.

## На чём остановились

План полностью написан, ресёрч сохранён, **пользователь решил отложить исполнение** — переключаемся на handoff. К правке репозитория НЕ приступали. Файлы плана и ресёрча — единственные изменения этой сессии (новые файлы, не коммичены).

## Что не доделано

- [ ] **Получить явный сигнал-согласование** по плану `backlog/plans/2026-05-08-codex-compatibility.md` (правило `plan-before-act` — без «делай» / «ок» / «поехали» к работе не приступать).
- [ ] **Phase 0** — каркас: `AGENTS.md`, `_shared/INSTRUCTIONS.md`, `.codex/`, `.agents/`.
- [ ] **Phase 1** — генератор-скрипт `scripts/sync-agents-config.sh` + `scripts/verify-cross-compat.sh`.
- [ ] **Phase 2** — общий MCP YAML + общие hooks в `_shared/hooks/`.
- [ ] **Phase 3** — миграция 27 skills в `.agents/skills/` через симлинки.
- [ ] **Phase 4** — конвертер subagents (md ↔ toml) для 9 субагентов.
- [ ] **Phase 5** — адаптация Claude-only фич (`agent-teams`, plugin-marketplace) под Codex.
- [ ] **Phase 6** — документация + bump 0.6.0 + smoke-test в VS Code (Claude Code + Codex одновременно).
- [ ] Открытые предположения, требующие подтверждения пользователя:
  - Симлинки vs копии для Windows-форков.
  - MCP context7 транспорт (stdio?) — проверить, что Codex его потянет.
  - VERSION bump → 0.6.0 (правильный уровень?).
  - `_shared/MEMORY.md` как репо-локальное дополнение к auto-memory Claude — устраивает ли компромисс.

## Следующие шаги (что делать в новой сессии)

1. **Прочитать** `backlog/plans/2026-05-08-codex-compatibility.md` (заодно `_specs/codex-compat/research.md` для контекста).
2. **Спросить пользователя**: «План остался в силе? Поехали с Phase 0?» — дождаться явного сигнала.
3. Если да → начать с **Phase 0 шаг 1** — извлечь общие секции из `CLAUDE.md` в `_shared/INSTRUCTIONS.md` (lifecycle, git workflow, принципы разработки, README-конвенции, security-sensitive).
4. Параллельно → создать `AGENTS.md` со структурой по [agents.md spec](https://agents.md) и @-import на `_shared/INSTRUCTIONS.md`.
5. Перед физическими move'ами скиллов (Phase 3) — обязательно гонять `make sync-agents` идемпотентно на dry-run; не делать массовые move'ы пока генератор не отлажен.

## Открытые вопросы / решения которые нужно принять

- Бэкап коммит для текущих 5 новых файлов (research × 4 + plan) — пользователь не подтвердил `/backup`. Решение отложено.
- Порядок исполнения относительно других планов — есть `backlog/plans/2026-05-02-repos-upgrade/` и `2026-05-06-md-export-toolkit.md`, не проверяли конфликты по файлам.
- Нужна ли отдельная фича-ветка для этой работы (`feature/codex-compat`) или работаем в `local` как обычно — пользователь не решил.

## Важный контекст (то, что легко забыть)

- **Архитектурный выбор пользователя жёстко зафиксирован**: вариант **C** по всем трём развилкам (Codex VS Code + max compat + оба файла канон со shared). НЕ переспрашивай эти решения в новой сессии.
- **Целевой Codex-продукт** — VS Code extension (Marketplace ID `openai.chatgpt`, общий пакет с CLI/Cloud). Фокус на нём, но решения должны работать и для Codex CLI.
- **Claude Code НЕ читает `AGENTS.md` нативно** (issue #6235 без ETA от Anthropic) — обходим через @-import внутри `CLAUDE.md`. Это критично, легко забыть.
- **agents.md** — спека минимальная, по сути не диктует структуру; индустриальный стандарт от AAIF (Linux Foundation).
- **Skills совместимы по [agentskills.io](https://agentskills.io)** — один SKILL.md работает в обоих, симлинки в `.claude/skills` и `.codex/skills` указывают на один источник в `.agents/skills/<name>/`.
- **Codex VS Code limit для AGENTS.md** — `project_doc_max_bytes` default 32768 байт (32KB). Тяжёлое выносить в `_shared/INSTRUCTIONS.md`.
- **Web-researcher агенты остались живы** — можно продолжить через SendMessage если нужны уточнения:
  - Anthropic-исследователь: `aee26feccc2b94fde`
  - Codex-исследователь: `a3ce1ecb863cbe04a`
  - Cross-agent-исследователь: `aeebbf5ad97a93e7e`

## Файлы которые надо открыть первыми

- `backlog/plans/2026-05-08-codex-compatibility.md` — план целиком (главное)
- `_specs/codex-compat/research.md` — мастер-сводка ресёрча с cross-mapping таблицей
- `_specs/codex-compat/research-claude-code.md` — детали Claude Code 2026 (если нужен глубокий контекст)
- `_specs/codex-compat/research-codex.md` — детали Codex 2026 (особенно §5 VS Code extension и §2 AGENTS.md)
- `_specs/codex-compat/research-cross-agent.md` — паттерны мульти-агентских репо 2026
- `CLAUDE.md` — отсюда будем извлекать общие секции в `_shared/INSTRUCTIONS.md`
- `.claude/settings.json` — список 11 плагинов, которые нужно аудитить в Phase 5
- `.claude/skills/` — 27 скиллов для миграции в `.agents/skills/`
- `.claude/agents/` — 9 субагентов для конвертации в YAML SSOT
