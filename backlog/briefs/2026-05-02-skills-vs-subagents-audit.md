# Аудит: skills vs sub-agents в `.claude/`

Дата: 2026-05-02
Источник: запрос пользователя в сессии 2026-05-02 («что в скиллах надо переделать в саб-агенты»)
Статус: бриф

## Проблема

В `.claude/` параллельно существуют **24 skills** и **6 sub-agents**, при этом
часть скиллов выполняет работу, которая лучше ложится на саб-агентскую модель
(изолированный контекст, делегирование, экспертная роль). Дополнительно есть
**5 групп прямых дубликатов** между skills и agents — без чёткого разделения
ролей. Это рассинхронизирует поведение Claude и захламляет контекст.

## Целевая аудитория

- AI-агент Claude Code, работающий в этом репозитории и в его форках.
- Разработчик-владелец репозитория (ясное соответствие «команда → исполнитель»).

## Цель / результат

Чёткая архитектура `.claude/`:
- skill = entry-point (slash-команда + диалог + лёгкая оркестрация);
- sub-agent = исполнитель тяжёлой/специализированной работы в изолированном
  контексте.

Финальное состояние:
1. Удалены или конвертированы дубликаты (см. таблицу ниже).
2. Создано 4 новых саб-агента из существующих скиллов.
3. 5 скиллов переведены на гибридную модель (skill вызывает агента).
4. Обновлены README в `.claude/skills/` и `.claude/agents/`.

## Принципы skill vs sub-agent

| Признак | Skill | Sub-agent |
|---------|-------|-----------|
| Триггер | `/команда` или фраза в диалоге | Делегация из основного контекста (Agent tool) |
| Контекст | Основной (виден пользователю) | Изолированный |
| Назначение | Workflow, диалог, подтверждения, оркестрация | Тяжёлая работа: чтение десятков файлов, research, аудит, экспертная роль |
| Выход | Действия + диалог | Структурированный отчёт |
| Размер процедуры | До ~100 строк | Без ограничения |
| Когда выбрать | Slash-команда с подтверждением; короткая операция | Читает >5 файлов; экспертная роль; параллельная работа |

**Эвристика:** если задача читает >5 файлов или делает много WebFetch — это
саб-агент. Иначе захламляет основной контекст.

---

## План A — Новые саб-агенты (4 шт)

Создать в `.claude/agents/`:

| Имя файла | Источник | Почему саб-агент |
|-----------|----------|------------------|
| `lawyer.md` | skill `lawyer` | Экспертная роль с большим узкоспециальным промптом — изолировать контекст |
| `web-researcher.md` | skill `web-research` | WebSearch + WebFetch top-10 источников — много мусора в основном контексте |
| `techdebt-scanner.md` | skill `techdebt` | Сканирует все файлы `src/` — десятки файлов читает |
| `seo-auditor.md` | skill `seo-audit` | 247 строк инструкций + читает config/HTML/robots/sitemap — read-only research |

После создания — удалить или превратить в тонкие entry-skills (если нужен
slash-триггер).

## План B — Гибриды (skill = entry, agent = executor)

| Skill | Что делегировать | Куда |
|-------|------------------|------|
| `qa-tester` | Playwright-тестирование, контент-анализ | новый `qa-runner` агент или существующий `test-runner` |
| `architect` | Разведку кода | существующий внешний `Explore` или `feature-dev:code-explorer` |
| `seo-content` | SERP-анализ конкурентов, кластеризацию | новый `web-researcher` (см. План A) |
| `seo-research` | 609 строк CLI + анализ | новый `seo-researcher` агент |
| `seo-positions` | Опционально — агрегацию данных из API | по необходимости |

Референс уже работающего гибрида: skill `design-system` → agent `design-critic`.

---

## План C — Дубликаты skill ↔ agent (детальная сводная таблица)

### Сводный обзор

| # | Группа | Дубликат? | Решение | Действие |
|---|--------|-----------|---------|----------|
| 1 | `git-ops` agent ↔ 6 git skills | **Да, 90%** | Удалить агента | `git-ops.md` → удалить. Создать опц. skill `/pr` для GitHub PR. |
| 2 | `deployer` agent ↔ `deploy-dev`/`deploy-prod` skills | **Да, 90%** | Удалить агента | `deployer.md` → удалить. `rollback` оставить (не дубликат). |
| 3 | `test-runner` agent ↔ `test` skill | **Частично** | Гибрид | Skill `/test` = тонкий entry, делегирует `test-runner`. Агент остаётся для вызова из других агентов. |
| 4 | `docs-generator` agent ↔ `docs` skill | **Частично** (skill шире) | Гибрид + расширение агента | Skill `/docs` = тонкий entry, делегирует `docs-generator`. Расширить агент: ERROR_REGISTRY, `_changelogs/`. |
| 5 | `design-critic` agent ↔ `design-system` skill | **Нет** | Уже правильно | Skill вызывает агента — это эталон. |

---

### Группа 1 — `git-ops` vs git skills

**Файлы:**
- Agent: `.claude/agents/git-ops.md` (192 строки, 8 операций)
- Skills: `commit` (80), `push` (40), `cherry-pick` (52), `merge-to-prod` (58), `git-status` (58), `backup` (84)

**Покрытие операций:**

| Операция | git-ops agent | Skills | Покрытие | Уникальность |
|----------|---------------|--------|----------|--------------|
| Status | ✅ (5 строк) | ✅ `git-status` (58 строк, детальнее: unpushed, pending release) | Skill полнее | — |
| Commit | ✅ (30 строк) | ✅ `commit` (80 строк, preview + diff stat) | Skill полнее | — |
| Push | ✅ (20 строк) | ✅ `push` (40 строк) | Идентично | — |
| Pull | ✅ (5 строк) | ❌ нет skill | Только agent | Pull-only skill не нужен (вызывается внутри `/push`, `/deploy-dev`) |
| Merge | ✅ (10 строк) | ✅ `merge-to-prod` (58 строк, double confirm) | Skill безопаснее | — |
| Cherry-pick | ✅ (8 строк) | ✅ `cherry-pick` (52 строки, local→dev specific) | Skill специфичнее | — |
| GitHub PR | ✅ (10 строк) | ❌ нет skill | **Только agent** | Создать `/pr` skill (опционально) |
| GitHub view | ✅ (5 строк) | ❌ нет skill | Только agent | Можно через bash `gh pr list` |
| Backup | ❌ | ✅ `backup` (84) | Только skill | — |

**Вердикт:** контент дублируется на 90%, skills полнее и безопаснее. Уникальные
операции agent (pull, gh pr) либо инлайнены в skills, либо требуют отдельного
skill.

**Решение:** **удалить `git-ops.md`**. Опционально создать skill `/pr` для
GitHub PR-операций.

**Аргументы за удаление агента:**
1. Git-операции короткие (1-3 команды), не загрязняют контекст.
2. Все требуют диалога с пользователем (подтверждения) — это профиль skill.
3. Skills актуальнее (с safety-чеками для prod, конкретными примерами).
4. Slash-триггеры — более явный UX (`/commit` понятнее чем «git-ops, сделай commit»).

---

### Группа 2 — `deployer` vs deploy skills

**Файлы:**
- Agent: `.claude/agents/deployer.md` (132 строки, DEV+PROD)
- Skills: `deploy-dev` (60), `deploy-prod` (75), `rollback` (155)

**Покрытие:**

| Шаг | deployer agent | deploy-dev skill | deploy-prod skill | Совпадение |
|-----|----------------|------------------|-------------------|------------|
| Проверка ветки | ✅ | ✅ | ✅ | Идентично |
| Sync check | ✅ | ✅ | ❌ (отсутствует в skill — это **минус skill**) | Agent чуть лучше |
| Safety checklist (PROD) | ✅ | — | ✅ | Идентично |
| Запуск deploy скрипта | ✅ | ✅ | ✅ | Идентично |
| Проверка логов | ✅ | ✅ | ✅ | Идентично |
| **Обновление `_status/{ENV}.md`** | ✅ (этап 7) | ❌ | ❌ | **Только agent** |
| Возврат на `local` | ✅ | ✅ | ✅ | Идентично |
| Rollback | ❌ | — | — | Только skill `rollback` |

**Уникальность agent:** интегрированное обновление `_status/{ENV}.md` в
workflow деплоя. У skills это вынесено в отдельный `/docs`.

**Вердикт:** 90% дублирование. Skills декомпозированы лучше (отдельные команды
для DEV и PROD), но потеряли «sync check» (deploy-prod) и «обновление статуса».

**Решение:** **удалить `deployer.md`**, дополнить skills:
1. В `deploy-prod` SKILL.md добавить шаг «Sync check» (уже есть в `deploy-dev`).
2. После `/deploy-{dev,prod}` явно вызывать `/docs` (документация = отдельная
   ответственность, отдельный slash).
3. `rollback` оставить (уникален).

**Альтернатива:** оставить `deployer` как fallback для голосового
«разверни на dev» без конкретного слэша. Но это даёт два пути для одного
действия — путаница. Я бы не оставлял.

---

### Группа 3 — `test-runner` vs `test`

**Файлы:**
- Agent: `.claude/agents/test-runner.md` (117 строк)
- Skill: `.claude/skills/test/SKILL.md` (100 строк)

**Сравнение фаз:**

| Фаза | test-runner | test | Различия |
|------|-------------|------|----------|
| Lint | ✅ | ✅ | Идентично |
| Type Check | ✅ | ✅ | Идентично |
| Syntax Check | ✅ | ❌ | Только agent (но дублирует Type Check для Python) |
| Unit Tests | ✅ | ✅ | Идентично |
| Build Check | ✅ | ✅ | Идентично |
| Pytest markers | ❌ | ✅ | Только skill |
| Data Pipeline check | ❌ | ✅ | Только skill |
| Quick / Full / Review modes | ✅ | ❌ | **Только agent** — Review Mode принимает список файлов от других агентов |

**Уникальность agent — критична:** Review Mode позволяет `code-reviewer`,
`deployer` (любому агенту) делегировать тестирование. Skill этого не умеет.

**Уникальность skill:** Pytest markers, Data Pipeline check. Это можно
перенести в агент.

**Вердикт:** не полный дубликат. Агент нужен для **вызова из других
агентов**. Skill дублирует базовую функциональность.

**Решение C — гибрид:**
1. Расширить `test-runner` — добавить Pytest markers и Data Pipeline check.
2. Превратить skill `test/SKILL.md` в тонкий entry: получает аргументы
   пользователя, делегирует `test-runner` через Agent tool.
3. Skill сохраняет slash-триггер `/test` для UX.

**Псевдокод нового `test/SKILL.md`:**
```
1. Парсинг аргумента (quick / full / e2e / data-pipeline)
2. Вызвать sub-agent test-runner с режимом и path
3. Передать отчёт пользователю
```

---

### Группа 4 — `docs-generator` vs `docs`

**Файлы:**
- Agent: `.claude/agents/docs-generator.md` (90 строк)
- Skill: `.claude/skills/docs/SKILL.md` (75 строк)

**Покрытие:**

| Файл для обновления | docs-generator | docs skill | Где описано |
|---------------------|----------------|------------|-------------|
| `_status/{ENV}.md` | ✅ | ✅ | Оба |
| `_status/PENDING_RELEASE.md` | ✅ | ✅ | Оба |
| `_status/DEVELOPMENT_STATUS.md` | ✅ | ✅ | Оба |
| `documentation/ERROR_REGISTRY.md` | ❌ | ✅ | **Только skill** |
| `_changelogs/{env}.md` | ❌ | ✅ | **Только skill** |

**Контекст-нагрузка:** обновление документации требует чтения коммитов,
кода, нескольких status-файлов → классическая работа для саб-агента.

**Вердикт:** skill умеет больше, но agent изолирует контекст. Нужно объединить.

**Решение C — гибрид:**
1. Расширить `docs-generator` — добавить обновление `ERROR_REGISTRY.md` и
   `_changelogs/{env}.md`.
2. Превратить skill `docs/SKILL.md` в тонкий entry: спросить env (DEV/PROD),
   делегировать `docs-generator` через Agent tool.
3. Skill сохраняет slash-триггер `/docs`.

---

### Группа 5 — `design-critic` vs `design-system` (эталон)

**Файлы:**
- Agent: `.claude/agents/design-critic.md`
- Skill: `.claude/skills/design-system/SKILL.md`

**Структура:** skill `design-system` создаёт дизайн-систему и явно вызывает
`design-critic` агента для аудита (10 dimensions, maturity matrix).

**Вердикт:** **корректное разделение, не трогать.** Использовать как
референс для гибридизации остальных пар.

---

## Сравнение стратегий по дубликатам

Три возможных глобальных подхода (выбрана смешанная):

| Подход | Плюсы | Минусы |
|--------|-------|--------|
| A. Skills only (удалить всех агентов-дубликатов) | Минимум файлов, явный UX | Нет изоляции контекста для тяжёлых задач |
| B. Agents only (удалить дублирующие skills) | Изоляция, переиспользование агентов | Теряются slash-триггеры, хуже UX |
| **C. Гибрид (skill=entry, agent=executor)** | Slash UX + изоляция + переиспользование | Больше файлов, два места правок |

**Применённое решение:** A для git и deploy (короткие операции), C для
test и docs (длительные, читают много файлов).

---

## Acceptance criteria

- [ ] Создано 4 новых саб-агента (План A): `lawyer`, `web-researcher`,
      `techdebt-scanner`, `seo-auditor`.
- [ ] 5 скиллов переведены на гибрид (План B).
- [ ] Удалены `git-ops.md` и `deployer.md` (дубликаты).
- [ ] `test/SKILL.md` и `docs/SKILL.md` стали тонкими entry-skills,
      вызывающими свои агенты.
- [ ] Расширены агенты: `test-runner` (+ pytest markers, data pipeline);
      `docs-generator` (+ ERROR_REGISTRY, `_changelogs/`).
- [ ] Опционально: создан `/pr` skill для GitHub PR-операций.
- [ ] Обновлены `.claude/skills/README.md` и `.claude/agents/README.md`.
- [ ] Изменения проверены на одном из форков (CRM_code или vibecommerce_code).

## Риски / открытые вопросы

1. **Поломка форков.** Форки используют существующую структуру. Нужно
   обновить `documentation/00-FORKING-GUIDE.md` с миграционным гайдом.
2. **Гибрид усложняет skill.** Тонкие entry-skills могут быть прозрачнее
   единого агента. Альтернатива — удалять skill полностью (вариант B).
3. **`/pr` skill — стоит ли?** Если редко используется — не создавать.
4. **Слэш-триггеры в саб-агентах.** Sub-agent может срабатывать по фразе из
   `description`, но не по слэшу. Нужно ли пользователю вызывать саб-агента
   слэшем (требует skill-обёртки)?
5. **`agent-creator` skill ↔ внешний `plugin-dev:agent-development` skill.**
   Возможно, тоже дублирование — изучить отдельно.

## Связанные документы

- Источник: ответ ассистента в сессии 2026-05-02
- Структура skills: [.claude/skills/README.md](../../.claude/skills/README.md)
- Структура agents: [.claude/agents/README.md](../../.claude/agents/README.md)
- Гайд по форку: [documentation/00-FORKING-GUIDE.md](../../documentation/00-FORKING-GUIDE.md)
- Эталон гибрида: skill `design-system` ↔ agent `design-critic`
