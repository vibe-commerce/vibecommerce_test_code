# _shared/INSTRUCTIONS.md — общие инструкции для AI-агентов

> Этот файл импортируется обоими каноническими файлами:
> - [`../CLAUDE.md`](../CLAUDE.md) → читает Claude Code
> - [`../AGENTS.md`](../AGENTS.md) → читает OpenAI Codex
>
> Здесь — то, что одинаково для обоих агентов. Специфика — в каждом из них.

Last Updated: 2026-05-29

## Проект

`vibecommerce_test_code` — шаблонный стартер для селлеров на маркетплейсах
и e-commerce. Форкается каждым студентом курса Вайб-Коммерс под свой проект.

В репо НЕТ персональных или клиентских данных автора — только методические
модули, шаблоны и синтетические/открытые демо-датасеты.

## Принцип №0 — pure template

**В репо не должно быть ни одного байта персональных или клиентских данных.**

- ❌ Никаких ИНН, ОГРНИП, реквизитов
- ❌ Никаких боевых API-токенов (только `.env.example` с пустыми значениями)
- ❌ Никаких имён реальных клиентов/селлеров/товаров
- ❌ Никаких реальных выгрузок продаж, рекламы, ассортимента
- ❌ Никаких финотчётов с цифрами автора
- ✅ Шаблоны с `{placeholders}`, методологии, генераторы синтетики, демо-датасеты с пометкой `# DEMO DATA — synthetic, not real`

## Lifecycle документа

```
backlog/ideas/ → backlog/briefs/ → backlog/plans/ → код → documentation/
  (что если?)     (стоит ли?)        (как?)
                       │                  │
                       ↓                  ↓
              archive/rejected/   archive/done/

Крупные фичи параллельно: _specs/<feature>/ (tech-spec, user-spec, ADR)
```

## Git Workflow

```
local (рабочая ветка) → push → main (GitHub)
```

Только две ветки. Без `dev`/`prod` — это шаблон без боевого деплоя.

### Git-правила для AI

- **НЕ** делать commit/push/merge без подтверждения пользователя
- **НЕ** делать force-push, `reset --hard`, rebase без явного запроса
- **НЕ** коммитить секреты (`.env`, credentials)
- **НЕ** использовать `git add -A` или `git add .` — добавлять файлы по отдельности
- Conventional commits: `<type>(<scope>): <description>`

## Plan Before Act

Перед любой нетривиальной правкой — план в файл, согласование от человека,
потом исполнение. Без явного сигнала («делай»/«ок»/«поехали»/«approved»/«go»)
AI ждёт. См. [`.claude/rules/plan-before-act.md`](../.claude/rules/plan-before-act.md).

## Security

- `.env*` — НЕ коммитить (в `.gitignore`)
- Секреты только из env через `os.getenv()` — НЕ хардкод
- Не логировать значения секретов (токены, ключи, пароли)
- НИКОГДА не выводить значения API-ключей в чат
- Перед коммитом — проверять `git diff --cached` на паттерны секретов
  (`sk-`, `token=`, `api_key=`, `password=`, `secret=`, `eyJ` для JWT)
- Файлы в `_private/`, `my-project/data/`, `my-project/**/personal-*` — запрещены для чтения и вывода

## Принципы разработки

- **KISS** — простота важнее сложности
- **YAGNI** — не пиши код «на будущее»
- **SRP** — одна ответственность на функцию
- **Open/Closed** — расширяй, не переписывай работающий код
- **Dead Code** — удаляй мёртвый код, не комментируй
- **DRY** — не дублируй знания (но похожий код в разных контекстах — ок)

## MEMORY BANK + File Management

README в каждой папке — карта памяти проекта. Без них структура протухает за 2 недели.

- Создавай файлы в правильной директории (соблюдай иерархию модулей)
- При добавлении/изменении/удалении/переименовании файла — обязательно обнови
  `README.md` в затронутой папке (и в родителе, если меняется иерархия)
- Обнови `Last Updated: YYYY-MM-DD` после правки

### Tagging convention

- `[CANONICAL]` — первое определение факта (один на факт)
- `[REF: path#section]` — кросс-ссылка вместо дублирования
- `[CONFIRMED: source-url-or-date]` — проверенная информация
- `[PLACEHOLDER: owner]` — для заполнения студентом
- `[VIP]` — углублённая версия в `vibecommerce_vip_code`

## Структура шаблона

```
vibecommerce_test_code/
├── CLAUDE.md / AGENTS.md / _shared/INSTRUCTIONS.md   ← AI инструкции
├── README.md / FACTS.md / ROADMAP.md / AGENDA.md / HANDOFF.md
├── _modules/<NN>-<name>/         ← методические модули (read-only)
├── my-project/                   ← рабочая зона студента (data/ gitignored)
├── _knowledge/{marketplaces,legal,suppliers}/
├── _prompts/{roles,jtbd,library}/
├── _practices/                   ← 8-этапный workflow
├── _specs/                       ← templates: brief, plan, ADR, tech-spec
├── backlog/{ideas,briefs,plans,archive/{done,rejected}}/
├── _changelogs/CHANGELOG.md
├── _status/PROJECT_STATUS.md
├── _private/                     ← gitignored: secrets, docs, data
├── _references/ / _handoffs/ / _reports/
├── documentation/                ← FORKING-GUIDE, onboarding/
├── .claude/{settings.json, skills/, agents/, rules/, hooks/}   ← Claude-only
├── .codex/{config.toml, skills/, agents/, prompts/, hooks/}    ← Codex-only
├── .agents/{skills/, subagents/}                                ← общая папка
└── scripts/{sync-agents-config.sh, verify-cross-compat.sh}
```

## Тиринг FREE/VIP

- **FREE** (этот репо) — workflow + базовая методика + onboarding
- **VIP** (`vibecommerce_vip_code`, private) — премиум-IP: углублённые методологии,
  платные API, полные промпт-наборы

Hook'и FREE→VIP помечены `📈 Углубление в vibecommerce_vip_code`.

## Связанные

- Claude-specific: [`../CLAUDE.md`](../CLAUDE.md)
- Codex-specific: [`../AGENTS.md`](../AGENTS.md)
- Память: [`MEMORY.md`](MEMORY.md)
- Политика памяти: [`memory-policy.md`](memory-policy.md)
- MCP конфиг: [`mcp.yaml`](mcp.yaml)
