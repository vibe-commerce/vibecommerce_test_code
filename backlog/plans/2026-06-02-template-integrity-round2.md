# План: Ремонт внутренней целостности — раунд 2 (0.3.1 → 0.3.2)

Дата: 2026-06-02
Источник: аудит репозиториев 2026-06-02 (read-only, 4 агента + проверки git/grep)
Статус: СОГЛАСОВАН 2026-06-02 → в работе (итерация 1: только FREE P0–P3)

> **Решения (2026-06-02):** №2 Codex-хуки = **Вариант A** (реализовать, порт из
> EMPTY_code). №5 объём итерации 1 = **только FREE целиком** (P0–P3); VIP P0–P1 —
> следующей итерацией.

<!--
Plan = «КАК ДЕЛАТЬ». НЕ исполняется до явного сигнала-согласования
(.claude/rules/plan-before-act.md). При отклонении в процессе — обнови файл.
-->

## Контекст

Аудит 2026-06-02 проверял FREE-шаблон (`vibecommerce_test_code`, v0.3.1) и
парный VIP-репо (`vibecommerce_vip_code`, v0.3.0) по 5 критериям: корректность,
**внутренняя** связность, адекватность, актуальность, соответствие исходной
задаче (скелет EMPTY_code + тиринг FREE/VIP + Codex compat).

**Scope (уточнение пользователя 2026-06-02):** «связность» = только **внутри
репозитория** (битые ссылки, README↔структура, @import, файлы-сироты). Связи
**между** репозиториями (осиротевший `skills_pack`, тройное дублирование
SEO-скиллов, клоны `123`/`vibecommerce_test_kojo`, отставание от upstream
EMPTY_code) — **вне scope** этого плана (вынесены в раздел «Вне scope»).

Что уже знаем (проверено):
- Прежний план [`2026-06-01-fix-template-integrity.md`](2026-06-01-fix-template-integrity.md)
  **исполнен частично** коммитом `1db2101`: pyproject (`name`/`version=0.3.1`),
  `verify-cross-compat.sh` (убран stub), `.codex/agents/*.toml` (валидный TOML),
  ~25 README, Makefile, bump VERSION+CHANGELOG. Но чек-лист не отмечен, план не
  заархивирован, и **часть пунктов не выполнена**.
- Принцип №0 в FREE соблюдён полностью (0 секретов/PII, `.env.example` пустой) —
  **не трогаем, не регрессируем**.
- Скелет, тиринг (FREE-сторона), Codex-структура — на месте. Исходная задача
  достигнута; этот план закрывает остаточные дефекты целостности.

Остаток в FREE (не закрыт `1db2101`):
- Шапки версий рассинхронизированы: [README.md:16](../../README.md#L16) = «0.3.0»
  (файл вообще не в диффе 0.3.1), [CLAUDE.md:3](../../CLAUDE.md#L3) и
  [AGENTS.md:7-8](../../AGENTS.md#L7-L8) = «0.3.0 / 2026-05-29», против
  VERSION/CHANGELOG = 0.3.1.
- [ROADMAP.md:28](../../ROADMAP.md#L28): «Фаза 1 — 70%» + Фазы 2/2.5/3/4/5/7/C
  все `[ ]`, хотя фактически выполнены (0.3.1 тронул в ROADMAP только 1 строку —
  битую ссылку, не статус фаз).
- **Codex-хуки — молчаливый отказ:** [.codex/config.toml.template:21-23](../../.codex/config.toml.template#L21-L23)
  объявляет `[hooks] path=".codex/hooks"`, но [.codex/hooks/](../../.codex/hooks/)
  содержит только README-заглушку; `_shared/hooks/` — тоже только README. При
  запуске Codex в форке `memory-bank-check`/`auto-ruff` не сработают вообще.
- `_practices/{00-WORKFLOW,03-development-checklist,05-document-and-backup}.md`
  велят писать в несуществующий `_changelogs/local.md` (есть только `CHANGELOG.md`).
- Ссылки на `_status/{DEV,PROD,PENDING_RELEASE}.md` и deploy-инфру в
  `.claude/agents/docs-generator.md`, `.agents/subagents/docs-generator.yaml`,
  `.agents/skills/docs/SKILL.md`, `documentation/{10-ARCHITECTURE,40-DEPLOY}.md` —
  противоречат «в шаблоне нет DEV/PROD».
- Битая symlink-относительная ссылка: [.agents/skills/architect/SKILL.md:10](../../.agents/skills/architect/SKILL.md#L10)
  `](../../rules/plan-before-act.md)` резолвится в `.claude/` контексте, но ломается
  в `.agents/`/`.codex/` (там `../../rules/` = несуществующая `.agents/rules/`).
- Шапки `Last Updated: 2026-05-29` в ~11 навигационных файлах.
- Формулировки отстали: CLAUDE.md «Codex compat … фаза C (после реализации)»,
  AGENTS.md `codex-setup.md` «в работе» — хотя реализовано.
- Корневой `HANDOFF.md` протух (2026-05-08, чужой контекст v0.5.4) — как и AGENDA,
  это student-fill артефакт, должен быть шаблонной заглушкой.
- Вендоренные скиллы: `skill-creator/SKILL.md` — 6 ссылок на не-вендоренные
  upstream-файлы; `agent-creator` — смешаны references двух разных скиллов
  (agent-creator + agent-sdk-builder), нет 4 references skill-creator.

Остаток в VIP (фиксы 0.3.1 туда **не доехали** — те же баги живы):
- `pyproject.toml:3` version=`0.0.2` (vs VERSION 0.3.0).
- `scripts/verify-cross-compat.sh` помечен `STATUS: stub`, всегда «PASSED».
- 9 невалидных `.codex/agents/*.toml`; нет рабочего `.codex/config.toml`.
- 2 битые внутренние ссылки: `_shared/MEMORY.md:33`,
  `_specs/codex-compat/README.md:97`.
- Личные пути `/Users/vadimbakanov/...` в 6 tracked-файлах.
- Masked Ozon-токены в `_knowledge/marketplaces-pro/ozon/API/api-performans-docs.txt`.
- DRY: `marketplace-discounts-guide.md` идентичен в 2 местах.
- README отсутствуют в `.codex/{agents,hooks,prompts,skills}`, `_prompts/{roles,jtbd}`,
  `_handoffs/`, `_specs/{archive,design,jtbd-research}/`, `marketplaces-pro/{ozon,wb}/`.
- `documentation/00-FORKING-GUIDE.md` велит студенту `git clone EMPTY_code` вместо VIP.
- Тег `[VIP]` объявлен в конвенциях, применён 0 раз.
- Codex-хуки/конфиг — **уже спланированы** в незакоммиченном VIP-плане
  `2026-06-02-codex-infrastructure-hardening.md` → этот пласт делегируем туда,
  не дублируем.

Ограничения:
- Принцип №0 — не вносить личных данных/абсолютных путей; не регрессировать чистоту FREE.
- KISS/YAGNI — чиним по существующему образцу (golden standard 0.3.1), без новых абстракций.
- Git — без `git add .`, коммит только по сигналу пользователя; FREE и VIP — отдельные репо/коммиты.
- `_specs/<feature>/` не создаём — это ремонт, не новая фича.

## Подход

Два репо, приоритеты внутри каждого. **FREE — первичен** (публикуемый, рабочая
директория). VIP — параллельный ремонт; Codex-пласт VIP делегирован его
собственному плану.

### FREE · P0 — Правда о версии и статусе (быстро, безопасно)

- **Шаг 1.** Bump до `0.3.2` синхронно: `VERSION`, `pyproject.toml` (`version`),
  `_changelogs/CHANGELOG.md` (новая запись 0.3.2 — что чинили). PATCH: ремонт
  целостности, структура не меняется.
- **Шаг 2.** Шапки версий → 0.3.2 + дата 2026-06-02: `README.md:16`, `CLAUDE.md:3`,
  `AGENTS.md:7-8`. Согласовать формулировку (убрать «0.3.0», обновить дату).
- **Шаг 3.** `ROADMAP.md`: перенести Фазы 1/2/2.5/3/4/5/7/C из «В работе» в
  «Завершено» с `[x]` по факту; в «В работе» оставить только реально открытое
  (Codex-хуки из P1, и VIP-фазы как параллельная задача). Снять «70% выполнено».
- **Шаг 4.** `Last Updated: 2026-05-29 → 2026-06-02` в навигации, где контент
  актуализируется этим ремонтом (≈11 файлов: CLAUDE/README/AGENTS/ROADMAP +
  затронутые README).

### FREE · P1 — Codex-хуки: устранить молчаливый отказ

Решение «реализовать или честно убрать декларацию» (см. «Решения для согласования» №2):
- **Вариант A (рекомендуется):** портировать из `EMPTY_code` (0.6.2) логику
  `auto-ruff.sh` + `memory-bank-check.sh` (apply_patch-aware + self-locating через
  `git rev-parse --show-toplevel`) в `_shared/hooks/*.sh`, прокинуть симлинки в
  `.codex/hooks/` через `scripts/sync-agents-config.sh`, добавить минимальный
  механизм монтирования хуков в Codex-runtime под симлинк-модель FREE.
  - **Шаг 5A.** Создать `_shared/hooks/{auto-ruff,memory-bank-check}.sh`.
  - **Шаг 6A.** Симлинки `.codex/hooks/` + согласовать с `config.toml.template`.
  - **Шаг 7A.** Smoke: запустить Codex-хук из подкаталога и на `apply_patch` —
    срабатывает (ruff форматирует, memory-bank-check ловит README).
- **Вариант B (интерим, если A окажется тяжёлым):** убрать декларацию хуков из
  `config.toml.template:21-23` и `AGENTS.md:76`, в README `.codex/hooks/` честно
  пометить «не реализовано, планируется» — чтобы конфиг не врал.

### FREE · P2 — Внутренние ссылки и ref-гигиена

- **Шаг 8.** `_changelogs/local.md` (3 файла в `_practices/`) → заменить на
  `_changelogs/CHANGELOG.md` (файла `local.md` в шаблоне нет).
- **Шаг 9.** `_status/{DEV,PROD,PENDING_RELEASE}.md` и deploy-инфра
  (`docs-generator.md/.yaml`, `docs/SKILL.md`, `documentation/{10-ARCHITECTURE,40-DEPLOY}.md`):
  привести в соответствие с «нет DEV/PROD» — пометить блоки «не применимо в
  шаблоне без деплоя» либо вынести deploy-специфику; не оставлять ссылок на
  несуществующие файлы статуса.
- **Шаг 10.** `architect/SKILL.md:10` — путь к `plan-before-act.md`, корректный во
  всех трёх контекстах (`.claude`/`.agents`/`.codex`) или явный комментарий о
  symlink-резолве.
- **Шаг 11.** Корневой `HANDOFF.md` → сбросить в шаблонную заглушку (как AGENDA:
  `{placeholder}` + футер «заполни при форке»), убрав чужой контекст v0.5.4.
- **Шаг 12.** Формулировки «фаза C (после реализации)» (CLAUDE.md) и «в работе»
  (AGENTS.md про `codex-setup.md`) → «реализовано».

### FREE · P3 — Вендоренные скиллы (низкий приоритет)

- **Шаг 13.** `skill-creator/SKILL.md`: 6 ссылок на не-вендоренные upstream-файлы
  (FORMS/OOXML/REDLINING/…) → довендорить или заменить на code-literals (не
  hyperlink), чтобы link-check не считал их битыми.
- **Шаг 14.** `agent-creator`: развести с `agent-sdk-builder` — оставить корректный
  набор references, доездить 4 references `skill-creator` из upstream (если нужны).

### VIP · P0 — Портировать фиксы целостности 0.3.1 (которые VIP не получил)

- **Шаг 15.** `pyproject.toml:3` version `0.0.2 → 0.3.1`.
- **Шаг 16.** `verify-cross-compat.sh`: снять `STATUS: stub`, перенести реальные
  проверки из FREE (YAML/JSON/TOML parse + target симлинков).
- **Шаг 17.** Починить TOML-сериализацию `sync-agents-config.sh` (как в FREE,
  через `json.dumps`), перегенерировать `.codex/agents/*.toml`; проверить
  идемпотентность (второй sync без diff). При необходимости создать рабочий
  `.codex/config.toml`.
- **Шаг 18.** README в `.codex/{agents,hooks,prompts,skills}`, `_prompts/{roles,jtbd}`,
  `_handoffs/`, `_specs/{archive,design,jtbd-research}/`, `marketplaces-pro/{ozon,wb}/`.

### VIP · P1 — Внутренняя связность и Принцип №0

- **Шаг 19.** Битые ссылки: `_shared/MEMORY.md:33`, `_specs/codex-compat/README.md:97`
  → убрать/перенаправить на существующие источники.
- **Шаг 20.** Зачистить личные пути `/Users/vadimbakanov/...` в 6 файлах →
  плейсхолдер/обобщённая формулировка (как в FREE 0.3.1).
- **Шаг 21.** Masked Ozon-токены в `api-performans-docs.txt` → явные плейсхолдеры.
- **Шаг 22.** DRY: `marketplace-discounts-guide.md` — оставить один CANONICAL,
  второй заменить на `[REF:]`.
- **Шаг 23.** `00-FORKING-GUIDE.md`: `git clone EMPTY_code` → `…/vibecommerce_vip_code`.
- **Шаг 24.** Тег `[VIP]`: либо применить к premium-блокам, либо убрать обещание из
  конвенций (решить — см. №4).
- **Шаг 25.** После фиксов — bump VIP до `0.3.1` (VERSION + .md шапки + CHANGELOG),
  выровнять с FREE по «получил интеграционные фиксы».

### VIP · делегировано

- **Codex-хуки/конфиг/rules** — исполнять отдельным планом
  `backlog/plans/2026-06-02-codex-infrastructure-hardening.md` (уже составлен,
  12 дефектов, 8 фаз). Здесь не дублируем; синхронизировать только version-bump.

## Альтернативы (отвергнутые)

- **Один общий коммит на FREE+VIP** — нет: разные репо, разная история, Принцип №0
  по-разному применяется; отдельные коммиты.
- **Codex-хуки FREE: просто `cp` из EMPTY_code** — нет: у EMPTY_code другая модель
  (`hooks.json` + rsync-зеркало), у FREE — симлинки; нужен перенос логики, не файлов.
- **Переписать выпущенную 0.3.1 вместо новой 0.3.2** — нет, 0.3.1 уже в истории;
  ремонт — следующий PATCH.
- **Включить в этот план cross-repo (skills_pack, клоны, upstream-дрейф)** — нет,
  пользователь явно сузил scope до внутренней связности.
- **Включить content-добор VIP (6-фазная ниша, supplier deep-dive, Ahrefs/Semrush)** —
  нет: это feature/content-работа, не целостность; отдельный бриф (см. «Вне scope»).
- **Codex-хуки FREE Вариант B (просто убрать декларацию)** как основной — нет:
  теряем заявленную возможность; B только как интерим, если A дорог.

## Риски и митигации

| Риск | Вероятность | Митигация |
|------|-------------|-----------|
| Codex-хуки (Вар. A) ломаются из подкаталога / на apply_patch | средняя | портировать self-locating + apply_patch-парсинг из EMPTY_code 0.6.2 1:1, smoke из подкаталога |
| Перенос symlink-модели хуков сложнее ожидаемого | средняя | таймбокс; при превышении — откат на Вариант B (честная де-декларация) |
| Правка `_status`/deploy-ссылок сотрёт нужный методический контент | низкая | не удалять, а помечать «не применимо в шаблоне», смысл сохранять |
| Version-bump затронет форки студентов | низкая | PATCH 0.3.2; синхронно VERSION/pyproject/CHANGELOG/шапки |
| Порт фиксов в VIP регрессирует его специфику | средняя | переносить по образцу FREE точечно, прогнать `make verify-agents` в VIP |
| ROADMAP-перенос разойдётся с фактом | низкая | сверять каждую фазу с реальным наличием файлов перед `[x]` |
| Зачистка `/Users/` в VIP убьёт нужную автору ссылку | низкая | заменять текстом, не удалять смысл |

## Чек-лист реализации

**FREE · P0 — версия и статус:**
- [ ] Bump 0.3.2: VERSION + pyproject.version + запись в CHANGELOG
- [ ] Шапки версий: README.md:16, CLAUDE.md:3, AGENTS.md:7-8 → 0.3.2 / 2026-06-02
- [ ] ROADMAP: фазы 1/2/2.5/3/4/5/7/C → «Завершено» `[x]`; снять «70%»
- [ ] Last Updated → 2026-06-02 в затронутой навигации (~11 файлов)

**FREE · P1 — Codex-хуки:**
- [ ] Решение Вариант A или B (согласовать)
- [ ] (A) `_shared/hooks/{auto-ruff,memory-bank-check}.sh` + симлинки `.codex/hooks/`
- [ ] (A) smoke: хук срабатывает из подкаталога и на apply_patch
- [ ] (B-альт) убрать декларацию хуков из config.toml.template + AGENTS.md:76

**FREE · P2 — ссылки/ref:**
- [ ] `_changelogs/local.md` (3× `_practices/`) → `CHANGELOG.md`
- [ ] `_status/{DEV,PROD,PENDING_RELEASE}` + deploy-ссылки → «не применимо в шаблоне»
- [ ] `architect/SKILL.md:10` — путь, валидный во всех контекстах
- [ ] корневой `HANDOFF.md` → шаблонная заглушка
- [ ] «фаза C (после реализации)» / «в работе» → «реализовано»

**FREE · P3 — вендоренные скиллы:**
- [ ] `skill-creator/SKILL.md`: 6 битых ссылок → вендор/code-literals
- [ ] `agent-creator`: развести с agent-sdk-builder, починить references

**VIP · P0 — порт фиксов 0.3.1:**
- [ ] pyproject version 0.0.2 → 0.3.1
- [ ] verify-cross-compat.sh: stub → реальные проверки
- [ ] sync-agents-config.sh TOML-fix + перегенерация `.codex/agents/*.toml` (идемпотентно)
- [ ] README в 6 группах папок

**VIP · P1 — связность и Принцип №0:**
- [ ] 2 битые ссылки (MEMORY.md:33, codex-compat/README.md:97)
- [ ] зачистка `/Users/vadimbakanov` в 6 файлах → пусто (кроме .git)
- [ ] masked Ozon-токены → плейсхолдеры
- [ ] DRY: marketplace-discounts-guide.md (CANONICAL + REF)
- [ ] FORKING-GUIDE: clone EMPTY_code → vibecommerce_vip_code
- [ ] `[VIP]`-тег: применить или убрать из конвенций
- [ ] bump VIP → 0.3.1 (VERSION + шапки + CHANGELOG)

**Housekeeping:**
- [ ] Прежний план 2026-06-01: отметить выполненные пункты, заархивировать в `archive/done/`
- [ ] Обновить `backlog/plans/README.md` (индекс) + Last Updated

## Метрика «успех»

1. FREE: `grep -rn "0\.3\.0" README.md CLAUDE.md AGENTS.md` не находит версию-шапку;
   VERSION/pyproject/CHANGELOG согласованы на 0.3.2.
2. FREE: ROADMAP не содержит «70% выполнено» и `[ ]` на фактически готовых фазах.
3. FREE: Codex-хук реально срабатывает (Вар. A) ИЛИ конфиг не объявляет
   несуществующих хуков (Вар. B) — нет молчаливого отказа.
4. FREE: link-check локальных md-ссылок зелёный (нет `_changelogs/local.md`,
   `_status/DEV…`, architect-ссылки, skill-creator-битых).
5. FREE: `make lint && make test && make verify-agents` → 0; Принцип №0 secret-scan чист.
6. VIP: `uv pip install -e .` в чистом venv проходит (pyproject 0.3.1 валиден);
   `make verify-agents` ловит исходный TOML-дефект (не «PASSED»-заглушка).
7. VIP: `grep -rI "/Users/vadimbakanov" . | grep -v /.git/` → пусто; 2 битые
   ссылки устранены; VIP на 0.3.1.
8. Оба: `git status` после прогона — только ожидаемые правки ремонта.

## Решения для согласования

1. **Версия:** FREE → 0.3.2 (PATCH), VIP → 0.3.1 (догоняет интеграционные фиксы). ОК?
2. **Codex-хуки FREE:** Вариант A (реализовать, портом из EMPTY_code) или
   Вариант B (честно убрать декларацию до реализации)? *Рекомендую A.*
3. **deploy-инфра в FREE** (`documentation/40-DEPLOY.md`, `_status/DEV/PROD`-ссылки):
   пометить «не применимо» или удалить из шаблона без деплоя?
4. **Тег `[VIP]` в VIP:** применять к premium-блокам или убрать из конвенций
   (весь репо = VIP, тег избыточен)?
5. **Порядок:** делать FREE целиком, потом VIP? Или только FREE P0+P1 сейчас,
   остальное — следующей итерацией?

## Вне scope (по уточнению пользователя — связь между репо НЕ нужна)

Зафиксировано, чтобы не потерять, но в этот план не входит:
- `vibecommerce_skills_pack` — осиротел (0 ссылок, 1 коммит фев-2026), его 4
  SEO-скилла идентичны VIP 1:1 → решить: архив или назначить SSoT+submodule.
- Клон `123` — чистый старый слепок, безопасен к удалению.
- Клон `vibecommerce_test_kojo` — 11 незакоммиченных уникальных файлов
  (8-март MPStats-ресёрч + TODO), среди них данные, нарушающие Принцип №0 →
  извлечь ценное в личный workspace, потом архивировать.
- Дрейф от upstream `EMPTY_code` 0.5.4 → **0.6.3** (Codex-инфра 0.6.x; архитектурная
  развилка симлинки vs rsync-зеркало) → отдельное решение «какой дизайн канон».
- Content-добор тиринга VIP: «6-фазная методика ниши» (по факту 3 фазы),
  supplier deep-dive (по факту базовая шпаргалка), Ahrefs/Semrush (нет кода) →
  отдельный бриф, это feature-работа, не целостность.

## Связанные

- Аудит-источник: сессия 2026-06-02 (4 агента, read-only)
- Предыдущий раунд: [`2026-06-01-fix-template-integrity.md`](2026-06-01-fix-template-integrity.md)
- VIP Codex-пласт: `vibecommerce_vip_code/backlog/plans/2026-06-02-codex-infrastructure-hardening.md`
- Правило: [`.claude/rules/plan-before-act.md`](../../.claude/rules/plan-before-act.md)
- Workflow: [`_practices/00-WORKFLOW.md`](../../_practices/00-WORKFLOW.md)
- Архив после реализации: `../archive/done/2026-06-02-template-integrity-round2.md`
