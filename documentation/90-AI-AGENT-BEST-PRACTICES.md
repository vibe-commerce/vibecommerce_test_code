# Best Practices работы с AI-агентами (Claude Code)

Last Updated: 2026-05-02

Практические инсайты по повышению качества работы с Claude Code и AI-агентами в разработке.

---

## 1. Plan & Act — сначала планируй, потом делай

**Суть:** Смещение фокуса с кодирования на планирование. ~80% времени — планирование, ~20% — отладка и доработка.

**Как применять:**
- Перед любой доработкой говори агенту: «Спланируй, как ты это будешь делать, и напиши мне план»
- Агент пишет план — ты его ревьюишь
- Скорее всего первый план не понравится — итерируй
- Только после утверждения плана — переходи к реализации

**Почему это важно:**
- Планирование стало суперкритичным шагом
- Дешевле поправить план, чем переделывать код
- Агент лучше работает, когда у него есть чёткий утверждённый план

---

## 2. Документация — пиши для агентов, не только для людей

**Суть:** Документация теперь нужна не столько людям, сколько AI-агентам. Агент опирается на документацию как на «память» между сессиями.

**Как применять:**
- После каждой значимой доработки говори агенту: «Запиши всё в документацию»
- Документируй: архитектуру, handlers, деплой, тестирование, troubleshooting, webhooks, мониторинг, работу с БД
- Создавай детальные гайды по каждому аспекту системы (getting started, architecture, database, deploy, testing, error handling и т.д.)
- Автоматизируй через скилл `/docs` — чтобы агент сам понимал, когда нужно документировать

**Структура документации (пример):**
```
documentation/
├── overview.md          # Общее описание проекта
├── getting-started.md   # Как начать работу
├── architecture.md      # Архитектура системы
├── database.md          # Схема и работа с БД
├── deploy.md            # Процесс деплоя
├── testing.md           # Как тестировать
├── troubleshooting.md   # Решение проблем
├── webhooks.md          # Работа с вебхуками
├── monitoring.md        # Мониторинг
├── handlers.md          # Описание хендлеров
└── ERROR_REGISTRY.md    # Реестр багов
```

**Важно:** Это гигантский файл (или набор файлов), где всё детально расписано. Чем лучше документация — тем качественнее работает агент.

---

## 3. Реестр багов (Error Registry)

**Суть:** Отдельная документация, куда агент записывает каждый найденный и исправленный баг.

**Как применять:**
- Агент при нахождении бага документирует:
  - **Что за баг** (симптом)
  - **Как исправил** (root cause + fix)
  - **Как не повторить** (prevention)
- Это не просто часть документации — это отдельный реестр
- Помогает агенту не повторять одни и те же ошибки в будущих сессиях

**Реализация:** Правило в `.claude/rules/error-learning.md` + файл `.claude/data/error-log.md`

---

## 4. Техдолг и постоянное улучшение

**Суть:** Периодически проси агента провести аудит всей системы инструкций, документации и скиллов.

**Как применять:**
- Говори агенту: «Посмотри свои инструкции, все скиллы, всю документацию. Ещё посмотри в другие проекты и в интернете лучшие практики. Скажи, что можно улучшить»
- Области аудита:
  - **CLAUDE.md** — базовые инструкции проекта
  - **Скиллы** — что можно добавить/улучшить
  - **Документация** — что неполное или устаревшее
  - **Правила** (`.claude/rules/`) — что нужно обновить
- Используй скилл `/techdebt` для автоматизации

**Цикл улучшения:**
```
Кодирование → Документирование → Аудит (техдолг) → Улучшение инструкций → Повтор
```

---

## 5. Субагенты и команды агентов (Swarm of Agents)

**Суть:** Использование нескольких агентов с разными ролями для повышения качества кода.

### 5a. Субагенты (Task tool)
- Делегирование подзадач отдельным агентам
- Не тратят контекстное окно основного агента
- Подходят для исследования, параллельных задач, ревью

### 5b. Команды агентов (Agent Teams)
- Создаёшь **агента-кодера** и **агента-ревьюера**
- Из основного диалога запускаешь задачу
- Кодер разрабатывает фичу
- Ревьюер проверяет и не пропускает, пока не будет ОК
- Они итерируют между собой, не тратя контекст основного агента
- Готовый результат отдают обратно

**Преимущества:**
- Качество кода выше за счёт встроенного ревью
- Основной контекст не забивается деталями реализации
- Имитация реального процесса разработки (developer + reviewer)

**Как включить:** Скилл `agent-teams:team-feature` — запускает команду с кодерами, ревьюерами и тех-лидом.

---

---

## 6. Playbook vs Narrative Skills

**Narrative** — скилл как текст: "ты эксперт, проанализируй". Агент сам выбирает путь. Результат непредсказуем.

**Playbook** — скилл как алгоритм: Input → Steps (IF/FOR/constraints) → Output. Шаги "приколочены". Результат стабильный.

| | Narrative | Playbook |
|---|-----------|---------|
| Повторяемость | Низкая | Высокая |
| Контекст | Много | Мало |
| Отладка | "Он как-то не так подумал" | "Сломалось на шаге 4" |
| Самоэволюция | Нет | Да (агент правит шаги) |

**Когда Narrative:** творческие задачи, brainstorm, свободная консультация.
**Когда Playbook:** повторяемые процессы, аудиты, генерация артефактов.

Шаблон: `_specs/templates/skill-playbook.md`

---

## 7. Multi-Agent Patterns

### Dev + Tester Loop

```
User → Orchestrator
         ├── Developer → пишет код
         └── Tester → тестирует
              ↓
         Developer фиксит → Tester проверяет → max 3 итерации → эскалация
```

Реализация: `code-reviewer.md` + `test-runner.md` агенты.

### Board of Advisors

Несколько экспертных агентов анализируют проект с разных углов. Оркестратор собирает вердикты → взвешенный план.

Готовая реализация: github.com/wild-defi/claude-code-skills/tree/main/board-of-advisors

---

## 8. Skill Memory Pattern

Каждый важный скилл хранит память в `.claude/data/{skill-name}-memory.md`:
- **Читает** при старте — учитывает прошлый опыт
- **Записывает** при завершении — lessons learned, edge cases, anti-patterns

---

## 9. Skill Testing & Evolution

После создания скилла через `/skill-creator`:
1. Anthropic Skill Creator включает evaluation и benchmarks
2. Прогони тестовые задания на субагентах
3. Найди слабости → улучши скилл → повтори

---

## 10. Visual Monitoring

Автоматический визуальный мониторинг:

| Инструмент | Что делает |
|------------|-----------|
| agent-browser (skills.sh/vercel-labs) | Скриншоты + visual diff |
| markdown-to-html (skills.sh/jimliu) | HTML-отчёты из markdown |
| Claude Cron (code.claude.com/docs/en/scheduled-tasks) | Запуск по расписанию |

Use-cases: QA после деплоя, конкурентный мониторинг, design compliance.

---

## 11. UI Development Tools

**Agentation** (agentation.dev) — React-компонент для визуальных аннотаций:
- `npm install agentation`
- Кликаешь на элемент → комментарий → Markdown с CSS-селектором → Claude Code
- MCP-интеграция в v2.0

---

## 12. Code Review Tools

**CodeRabbit** (coderabbit.ai) — AI-ревьюер для GitHub PR. Подключается как GitHub App.

---

## 13. Session Retrospective

1. В процессе работы оставляй маркеры: `TODO: это плохо, надо поменять`
2. Раз в неделю запускай `/insights` — анализ за 30 дней
3. Обнови скиллы и правила по результатам

Правило: `.claude/rules/session-retrospective.md`

---

## 14. External Skill Sources

| Источник | Особенность |
|----------|-------------|
| skills.sh | Security-аудит от 3 компаний. `npx skills update` |
| VoltAgent/awesome-agent-skills | 200+ community скиллов |

---

## 15. Remote Agent Control

Официальные плагины Anthropic:
- **Telegram**: github.com/anthropics/claude-plugins-official/.../telegram/
- **Discord**: github.com/anthropics/claude-plugins-official/.../discord/

---

## 16. Anti-patterns CLAUDE.md

CLAUDE.md загружается в системный промпт **каждой сессии**. Anthropic явно
предупреждает: *«Bloated CLAUDE.md files cause Claude to ignore your actual
instructions!»* ([best practices](https://code.claude.com/docs/en/best-practices)).

### Тест каждой строки

Перед добавлением строки в CLAUDE.md спроси: **«Если убрать эту строку —
Claude начнёт ошибаться?»** Если ответ «нет» — выкидывай.

### Antipatterns

#### ❌ Дерево файлов в CLAUDE.md

```markdown
<!-- ПЛОХО -->
## Структура проекта
{project}/
├── src/
│   ├── main.py
│   ├── ...
└── tests/
```

Claude видит структуру через `ls`/Read. Дерево в CLAUDE.md — дубликат, который
быстро рассинхронизируется с реальностью.

**Решение:** перенеси дерево в skill (`.claude/skills/project-knowledge/references/architecture.md`)
и подгружай по триггеру, или вообще не пиши — Claude сам разберётся.

#### ❌ Дублирование навигационных таблиц

Когда у тебя 4 таблицы навигации — «Документация», «Инфраструктура»,
«Навигация по проекту», «Рабочая память сессии» — это **один и тот же
список** с разной нарезкой. Каждый файл придётся обновлять в 4 местах.

**Решение:** оставь **одну** таблицу «Навигация по задачам» и используй
`@import` для деталей.

#### ❌ Файл-by-файл описание кодовой базы

```markdown
<!-- ПЛОХО -->
- src/utils/format.py — содержит функции форматирования дат
- src/utils/parse.py — парсинг JSON
- src/utils/api.py — HTTP-клиент
```

Claude умеет читать файлы. Описывать каждый — bloat.

**Решение:** опиши **архитектурный паттерн** (Three-Layer Rule), а не файлы.

#### ❌ Список всех skill'ов в CLAUDE.md

Skills уже видны Claude через системный промпт (см. список в начале каждой
сессии). Дублировать в CLAUDE.md — bloat.

**Решение:** ссылка одной строкой на `.claude/skills/README.md`.

#### ❌ CLAUDE.md без `@import`

Anthropic поддерживает синтаксис `@path/to/file.md` для модульной
загрузки — официальный способ держать CLAUDE.md тонким.

**Решение:** для каждого крупного блока (workflow, principles, conventions) —
один `@import` вместо инлайн-копии.

#### ❌ README в подпапках без обновления

Создал файл — забыл обновить README родителя. Через 2 недели структура
протухла, README врёт, Claude путается.

**Решение:** правило MEMORY BANK + хук `.claude/hooks/memory-bank-check.sh`.
Хук warn'ит при изменении файла без обновления README в его папке.

#### ❌ Утверждения без источника

```markdown
<!-- ПЛОХО -->
- Деплой занимает 3 минуты
- API возвращает 200 в 99.9% случаев
```

Откуда эти цифры? Если выдумано — `[PLACEHOLDER: replace with measured value]`.
Если измерено — `[CONFIRMED: source]`.

**Решение:** правило **No orphan statements** — каждое утверждение должно
прослеживаться к источнику.

### Целевой размер

- CLAUDE.md ≤ **260 строк** (Anthropic best practice)
- Превышаешь? — выноси в skill `project-knowledge`, в `_practices/`,
  в `documentation/`, в reference-файлы
- Используй `@import` для крупных блоков

### Чем CLAUDE.md отличается от skill

| Аспект | CLAUDE.md | Skill |
|--------|-----------|-------|
| Загрузка | Каждую сессию (всегда) | По триггеру (когда нужен) |
| Размер | ≤ 260 строк | Несколько файлов, ≤ 300 строк каждый |
| Содержит | Critical rules, policy, навигация | Domain knowledge, references |
| Пример | «не коммитить .env», «всегда возвращайся на local» | «как работает наш Git-workflow в деталях» |

См. также: [`00-FORKING-GUIDE.md`](00-FORKING-GUIDE.md) — чек-лист
заполнения шаблона для нового проекта.

---

## 17. Anti-patterns при создании skills и subagents (официально от Anthropic)

Источники: [skill best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices),
[engineering blog 2025-10-16](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills),
[skills docs](https://code.claude.com/docs/en/skills),
[sub-agents docs](https://code.claude.com/docs/en/sub-agents).

### 17a. Anti-patterns в YAML frontmatter и описаниях

| ❌ Плохо | ✅ Как надо | Почему |
|---------|-------------|--------|
| `name: helper` / `utils` / `tools` | `name: processing-pdfs` (gerund) | Vague names не триггерятся, gerund-форма точнее |
| `name: claude-helper` или `anthropic-tools` | без слов `claude`, `anthropic` | Reserved words, могут конфликтовать |
| `description: I can help you with PDFs...` | `description: Comprehensive PDF processing for...` | Description пишется в **третьем лице** (это инструкция Claude, а не Claude users) |
| `description: Use this when you want to...` | `description: Use when (1)..., (2)..., (3)...` | Конкретные триггеры с примерами фраз пользователя |
| Description без явных «когда использовать» | Description содержит и «что делает», и «когда триггерить» | Body загружается ПОСЛЕ триггера — секция «When to Use» в body не помогает |
| Description > 1024 символов | Description ≤ 1024 (description + when_to_use ≤ 1536) | Лимит обрезается в skill listing |

### 17b. Anti-patterns в теле SKILL.md / агента

| ❌ Плохо | ✅ Как надо | Почему |
|---------|-------------|--------|
| «PDF (Portable Document Format) is a file format developed by Adobe...» | Сразу к делу: «To rotate a PDF use pypdf:» | Claude знает что такое PDF — verbose explanations засоряют контекст |
| «Use pypdf, or pdfplumber, or PyMuPDF, or...» | Один default + escape hatch для редких случаев | Too many options = fragile triggering |
| «If you're doing this before August 2025...» | Time-agnostic + опционально `<details>` для legacy | Time-sensitive info протухает |
| Mix terms: «API endpoint» / «URL» / «route» | Один термин на всю SKILL.md | Inconsistent terminology путает |
| `scripts\helper.py` | `scripts/helper.py` | Только forward slashes (Windows pathing — anti-pattern) |
| `TIMEOUT = 47` без комментария | `TIMEOUT = 47  # API rate limit, see issue #234` | Voodoo constants — должны быть документированы |
| `return open(path).read()` без обработки | `try: ... except FileNotFoundError: ...` | «Punt to Claude» в скриптах = silent failures |
| Reference > 100 строк без TOC | TOC в начале reference-файла | Claude может читать частично через `head -100` — нужен обзор |
| SKILL.md → adv.md → details.md (двух уровней вложенности) | SKILL.md → ref.md (один уровень) | Nested references глубже одного уровня плохо обнаруживаются |
| SKILL.md > 500 строк | Разбить на reference-файлы по доменам | Bloat SKILL.md ≠ progressive disclosure |
| README.md / CHANGELOG.md / INSTALLATION.md внутри skill | Только SKILL.md + scripts/ + references/ + assets/ | Auxiliary docs — clutter, скиллы только для AI |

### 17c. Anti-patterns при работе со скиллами

- **Создавать skills без evaluations.** Anthropic требует evaluation-driven подход:
  3+ конкретных сценария → baseline (без skill) → minimal instructions →
  iterate. Без этого скилл превращается в «вроде работает».

- **Не тестировать на разных моделях.** Haiku может требовать больше деталей,
  Opus меньше. Один и тот же SKILL.md может работать на Sonnet и проваливаться
  на Haiku.

- **Untrusted skills.** Скиллы исполняют код. Перед использованием стороннего
  скилла — проверить SKILL.md + scripts/ + внешние URL.

- **Дублировать содержимое в SKILL.md и references/.** Информация должна жить
  в **одном** месте. SKILL.md = procedural, references/ = detailed reference.

### 17d. Anti-patterns специфичные для subagents

| ❌ Плохо | ✅ Как надо | Почему |
|---------|-------------|--------|
| Все агенты `model: opus` | `inherit` для общих, `sonnet` для workers, `haiku` для тривиального, `opus` только для сложного reasoning | Дорого + медленно без выигрыша |
| Subagent с `Task` в tools | Никогда не давать `Task` субагенту | Subagents не могут спавнить субагентов |
| Без `tools:` whitelist | Принцип least privilege: только нужные tools | Security risk + waste tokens |
| Гигантские system prompts (>500 строк) | Фокусированный prompt + references/ через skills field | Wastes context |
| Слишком много субагентов одного типа | Начинай с 2-3, добавляй когда обоснованно | Coordination overhead > benefit |
| Skip hooks для sensitive ops | PreToolUse hooks для Write/Edit на sensitive paths | Security |

### 17e. Лимиты и budgets (полезно знать)

- `description` + `when_to_use` обрезается на **1,536 символов** в skill listing
- При большом количестве skills общий budget ≈ **1% от context window** (fallback 8,000 символов).
  Регулируется `SLASH_COMMAND_TOOL_CHAR_BUDGET`
- При auto-compaction оставляются первые **5,000 токенов** каждого invoked skill,
  total budget **25,000 токенов** на все skills
- SKILL.md body — рекомендация **≤ 500 строк**
- name — **≤ 64 символов**, lowercase + hyphens, без `claude`/`anthropic`

---

## Резюме

| # | Практика | Эффект |
|---|----------|--------|
| 1 | **Plan & Act** | Меньше переделок, точнее результат |
| 2 | **Документация для агентов** | Агент «помнит» между сессиями |
| 3 | **Реестр багов** | Не повторяет ошибки |
| 4 | **Техдолг и аудит** | Система постоянно улучшается |
| 5 | **Команды агентов** | Выше качество, встроенное ревью |
| 6 | **Playbook-скиллы** | Стабильный, повторяемый результат |
| 7 | **Dev+Tester loop** | Автоматическое ревью кода |
| 8 | **Skill Memory** | Скиллы учатся на опыте |
| 9 | **Visual Monitoring** | Автоматическое QA |
| 10 | **Session Retrospective** | Непрерывное улучшение |
| 11 | **Anti-patterns CLAUDE.md** | Тонкая CLAUDE.md → Claude слушается инструкций |
| 17 | **Anti-patterns skills/subagents** | Триггеры срабатывают, контекст не засоряется |
