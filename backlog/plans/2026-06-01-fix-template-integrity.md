# План: Починка целостности шаблона (integrity-fix)

Дата: 2026-06-01
Источник: — (бриф не писался, фича-фикс по результатам QA-прогона)
Статус: РЕАЛИЗОВАН — 0.3.1 (функционал, коммит 1db2101) + 0.3.2 (остаток doc-гигиены,
шапки версий, битые ссылки). Codex-хуки и sync в VIP — в плане
[`2026-06-02-template-integrity-round2.md`](2026-06-02-template-integrity-round2.md).

<!--
Plan = «КАК ДЕЛАТЬ». План НЕ исполняется до явного сигнала-согласования
(.claude/rules/plan-before-act.md). При отклонении — обновить файл.
-->

## Контекст

QA-прогон шаблона `vibecommerce_test_code` v0.3.0 (2026-06-01) показал: Python
синтаксис валиден, `ruff check` чист, часть smoke-проверок проходит. Но найдены
**блокеры**, из-за которых свежий форк не устанавливается, cross-agent слой
частично не загружается, `make test` даёт ложноположительный результат и
нарушается Принцип №0 (pure template, без личных данных).

Что уже знаем (проверено эмпирически):
- `uv pip install -e ".[dev]"` в чистом venv падает: `name = "{project}"` —
  невалидное PEP 508 имя пакета. По той же причине падают документированные
  `uv run --with ...` команды из `scripts/README.md`.
- `pytest -v` собирает `0` тестов и завершается с exit code `5`, но `make test`
  скрывает ошибку через `|| echo`; `make lint` скрывает ошибки аналогично.
- `make test-e2e` объявлен в `.PHONY`, но не имеет recipe и ничего не делает.
- `.codex/agents/test-runner.toml` и `.codex/agents/techdebt-scanner.toml`
  не парсятся: генератор вставляет prompt в TOML без экранирования `\`.
- `make verify-agents` зелёный, хотя два generated TOML невалидны: проверка
  cross-agent слоя неполная.
- Каноничные демо-данные модуля 05 закоммичены в
  `_modules/05-ads-optimization/data-demo/` (ads_data_v1.0/v2.0, sales_data_v1.0).
- «Золотой стандарт» путей в репо — `__file__`-относительные пути
  ([generate_unit_economy_template.py:139](../../_modules/02-unit-economics/templates/generate_unit_economy_template.py#L139),
  [funnel_analysis.py:27](../../_modules/05-ads-optimization/scripts/funnel_analysis.py#L27)).
- `backlog/plans/2026-05-02-repos-upgrade/` — пустая директория.
- `ruff format --check _modules/ scripts/` показывает 25 неформатированных
  учебных файлов. Это не блокер работоспособности; исправлять отдельным
  механическим коммитом, не смешивать с функциональными правками.

Ограничения:
- Принцип №0 — ни одного байта личных/клиентских данных и личных абсолютных путей.
- KISS/YAGNI — чиним по существующему образцу, без новых абстракций.
- Git-правила — без `git add .`, коммит только по сигналу пользователя.
- `_specs/<feature>/` не создаём: это ремонт текущего шаблона, отдельная
  архитектурная спецификация не нужна.

## Подход

Четыре приоритета. **P0 = честная установка и тестовый контур**,
**P1 = cross-agent слой**, **P2 = pure-template и pipeline модуля 05**,
**P3 = документационная гигиена и отдельная механическая чистка**.

### P0 — Честная установка и тестовый контур

- **Шаг 1. `pyproject.toml`.**
  - `name = "{project}"` → валидный дефолт `name = "vibecommerce-seller-project"`
    + комментарий «# переименуй при форке под свой проект».
  - `version = "0.0.2"` → `version = "0.3.1"`; синхронно bump `VERSION` и
    `_changelogs/CHANGELOG.md`. Версия `0.3.0` уже выпущена, ремонт — PATCH.
  - Сохранить контракт Python `>=3.11`; `ruff target-version = "py311"`.
    Проверка `ast.parse(..., feature_version=(3, 11))` уже прошла на 32 файлах.
  - Smoke: `uv venv /tmp/t && VIRTUAL_ENV=/tmp/t uv pip install -e ".[dev]"` → success.

- **Шаг 2. Зависимости включённых модулей.**
  - Добавить в runtime dependencies используемые скриптами `openpyxl`,
    `pandas`, `numpy`, `matplotlib`, `requests`.
  - Оставить `markdown` одноразовой зависимостью утилиты:
    `uv run --with markdown scripts/md_to_html.py ...`.
  - Не вводить optional-extra `analytics`: `make install` из quick start должен
    готовить окружение для запуска включённых FREE-модулей без второго шага.

- **Шаг 3. Сделать Makefile честным.**
  - `install`: выбирать `uv`/`pip` по наличию команды, не маскировать реальную
    ошибку установки fallback-вызовом.
  - `lint`: убрать `2>/dev/null || echo`; ненулевой exit code должен доходить
    до пользователя и CI.
  - `test`: запускать `pytest tests/ -v` без маскировки exit code.
  - `test-e2e`: убрать из `.PHONY` и текущей документации до появления e2e;
    workflow уже корректно говорит «если есть e2e».

- **Шаг 4. Добавить минимальный регрессионный контур.**
  - Создать `tests/test_template_integrity.py`: PEP 508 install-конфиг,
    отсутствие личных абсолютных путей, валидность YAML/JSON/TOML и непустой
    набор тестов.
  - Создать `tests/test_module_05_pipeline.py`: копировать модуль 05 в `tmp_path`
    и запускать pipeline там, чтобы тест не изменял tracked `.xlsx`.
  - Создать `tests/test_cli_tools.py`: smoke `convert_xlsx_to_md.py`; для
    `md_to_html.py` smoke оставить отдельной командой через `uv --with markdown`.

### P1 — Cross-agent слой

- **Шаг 5. Починить TOML-сериализацию в `scripts/sync-agents-config.sh`.**
  - Все TOML-строки (`name`, `description`, `model`, `tools`, `prompt`, MCP
    string/list values) сериализовать через единый helper на основе
    `json.dumps(value, ensure_ascii=False)`: JSON quoting совместим с TOML basic
    strings и экранирует `\`, `"`, переводы строк.
  - Перегенерировать `.codex/agents/*.toml`, `.claude/agents/*.md`,
    `.codex/.mcp.toml`, `.claude/.mcp.json`.
  - Проверить идемпотентность: второй `make sync-agents` не создаёт diff.

- **Шаг 6. Усилить `scripts/verify-cross-compat.sh`.**
  - Парсить `_shared/mcp.yaml` и все `.agents/subagents/*.yaml`.
  - Парсить `.claude/.mcp.json`, `.codex/.mcp.toml`,
    `.codex/config.toml.template`, все `.codex/agents/*.toml`.
  - Проверять не только наличие symlink, но и ожидаемый target.
  - Убрать пометку `STATUS: stub`; после правки `make verify-agents` обязан
    ловить исходный TOML-дефект.

### P2 — Pure template и pipeline модуля 05

- **Шаг 7. Унификация путей всех 4 скриптов модуля 05 → `../data-demo/`.**
  Образец (как в funnel, но с правильной целевой папкой):
  ```python
  import os
  SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
  DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data-demo")
  os.makedirs(DATA_DIR, exist_ok=True)
  ```
  - `generate_sales_data.py:403` → `os.path.join(DATA_DIR, "sales_data_v1.0.xlsx")`
  - `generate_ads_data.py:652` → `os.path.join(DATA_DIR, "ads_data_v1.0.xlsx")`
  - `abcdx_analysis.py:383-384` → INPUT `ads_data_v1.0.xlsx`, OUTPUT `ads_data_v2.0.xlsx` в DATA_DIR
  - `funnel_analysis.py:28-29` → читать из DATA_DIR (а не SCRIPT_DIR);
    графики/отчёт — в `DATA_DIR/analysis_output/` (поведение сохранить).
  - Это одновременно убирает личные пути `/Users/<user>/...PRJ_MARKETPLACE/`
    и чинит pipeline (generate → abcdx → funnel сходятся на одной папке).
  - Обновить `_modules/05-ads-optimization/README.md`: добавить пропущенный
    запуск `generate_ads_data.py` между генерацией продаж и ABCDX.

- **Шаг 8. Зачистка личных путей `/Users/<user>/` в не-.py файлах.**
  - `_specs/codex-compat/README.md:12,14,19` — ссылки на приватные репо
    (EMPTY_code, vadim-bakanov-ai-dev) → текст без абсолютной ссылки
    («внутренний репо автора, в форке недоступен»).
  - `_specs/design/themes/01-*.css:4-5`, `02-*.css:4-5` — комментарий `Source:`
    → оставить только имя репо-источника без `/Users/...`.
  - `.agents/skills/project-knowledge/references/architecture.md:97` → дать
    обобщённую формулировку без абсолютного пути.
  - `backlog/briefs/2026-05-02-mcp-setup-recommendations.md:77,161,173` →
    заменить `/Users/<user>/Documents/_CODE` на плейсхолдер `<путь-к-коду>`.
  - `_handoffs/2026-05-08_18-01.md:85` → исторический артефакт; заменить путь
    на `<repo-root>`: pure-template правило действует и для истории.
  - Контроль: `grep -rI "/Users/<user>" . | grep -v /.git/` → пусто.

- **Шаг 9. Обезвредить похожий на реальный Ozon API key пример.**
  - `_knowledge/marketplaces/ozon-basics.md:43`: UUID-подобное значение заменить
    на явный placeholder `{ozon-api-key}`.
  - Повторить секрет-скан по tracked-файлам; `.env.example` оставить с пустыми
    значениями.

### P3 — Документационная гигиена

- **Шаг 10. Убрать заявленный, но отсутствующий `install-claude-tools`.**
  - Удалить таргет из `Makefile`, упоминания из quick start/onboarding и мёртвую
    ссылку из `.claude/EXTERNAL-TOOLS.md`.
  - Сохранить `backlog/briefs/2026-05-02-install-claude-tools.md` как будущую
    идею. Не создавать фиктивный скрипт без согласованного поведения.

- **Шаг 11. Мёртвые ссылки на 2 несуществующих плана** (10 файлов:
  ROADMAP.md, .claude/skills/README.md, _changelogs/README.md, _shared/MEMORY.md,
  _specs/codex-compat/README.md, documentation/onboarding/codex-setup.md,
  backlog/plans/README.md, 3× archive/*).
  - Git-история подтверждает: планы никогда не были закоммичены.
  - Не перенаправлять на пустой `backlog/plans/2026-05-02-repos-upgrade/`.
  - В актуальных документах заменить ссылки на `_changelogs/CHANGELOG.md`
    и текущий integrity-план, где это соответствует смыслу.
  - В архивных документах убрать hyperlink, сохранить текстовое историческое
    упоминание.

- **Шаг 12. Прочие битые md-ссылки.**
  - Исправить реальные битые ссылки: `../deploy/`,
    `../../design-system/`, `.agents/skills/architect` → plan-before-act,
    `backlog/archive/README.md` → отсутствующий lifecycle plan.
  - Для примеров и шаблонов (`<url>`, `FORMS.md`, `user-spec.md`, `tech-spec.md`)
    заменить ложные Markdown-ссылки на code literals либо корректные ссылки,
    чтобы link-check различал документацию и placeholders.
  - Добавить проверку локальных Markdown-ссылок в
    `tests/test_template_integrity.py`.

- **Шаг 13. README во ВСЕХ важных папках проекта** (решение пользователя от
  2026-06-02: «README — очень важная инструкция, должна быть во всех важных
  папочках»; override исходного приоритезированного варианта).
  Добавить memory-bank README во все собственные папки проекта без него:
  `_handoffs/`, все подпапки `_modules/*` (scripts/templates/data-demo/cashflow),
  `_prompts/roles/`, `_prompts/jtbd/`, `_specs/archive/`, `_specs/design/`,
  `_specs/design/themes/`, `_specs/jtbd-research/`,
  `backlog/ideas/prompt-library/`, `backlog/ideas/repo-library/`,
  `my-project/00-niche/…06-finance/`, `my-project/data/`, `my-project/reports/`,
  `.claude/data/`, `.codex/agents/`, `.codex/hooks/`, `.codex/prompts/`,
  `.codex/skills/`, `.agents/skills/`, `.agents/subagents/`.
  - **Исключения (обоснованные):** внутренние подпапки вендоренных скиллов
    (`.agents/skills/<skill>/{references,scripts,assets}`) — у них конвенция
    `SKILL.md`, README дублировал бы её; `_private/{data,docs,meetings,secrets}` —
    gitignored, секреты, уже описаны в `_private/README.md`; пустая
    `backlog/plans/2026-05-02-repos-upgrade/`.

- **Шаг 14. Механическое форматирование отдельным коммитом.**
  - Выполнить `ruff format _modules/ scripts/ tests/`.
  - Не смешивать форматирование 25 учебных файлов с функциональными diff.
  - После форматирования повторить `ruff check` и тесты.

## Альтернативы (отвергнутые)

- **Оставить `|| echo` в Makefile как дружелюбный fallback** — нет: команда
  сообщает успех при отсутствии тестов и при реальном lint-дефекте.
- **Добавить TOML dependency только для генератора** — нет: достаточно
  стандартного `json.dumps` для корректного TOML quoting и `tomllib` для проверки.
- **Поднять Python requirement до 3.12** — нет: синтаксический scan с
  `feature_version=(3, 11)` прошёл; сохраняем заявленную совместимость 3.11+.
- **Сделать `install-claude-tools.sh` заглушкой** — нет: публичная команда должна
  выполнять заявленную функцию, а не симулировать успех.
- **Удалить скрипты модуля 05 вместо починки** — нет, это методический контент
  курса, демо-данные закоммичены, скрипты нужны.
- **Чинить пути на `PRJ_MARKETPLACE/` + создать эту папку** — нет, каноничная
  папка уже есть (`data-demo/`), плодить вторую = нарушение DRY/структуры.
- **Сделать `name` валидным, но оставить `{project}`-семантику через env** —
  over-engineering; простой валидный дефолт + комментарий решает.
- **Массово создать README во все 17 папок сразу в P0** — раздувает блокер-фазу;
  пользовательские точки входа включены в P3, остаток — отдельный follow-up.

## Риски и митигации

| Риск | Вероятность | Митигация |
|------|-------------|-----------|
| Правка путей funnel сломает генерацию PNG | низкая | smoke-прогон pipeline после правки, OUTPUT_DIR-поведение сохранить 1:1 |
| `..`-относительный путь ломается при запуске из чужого cwd | низкая | используем `os.path.abspath(__file__)`, не cwd |
| Зачистка .md убирает нужную автору ссылку на приватный репо | средняя | заменяем на текст, не удаляем смысл; решение явно зафиксировано ниже |
| TOML quoting чинит один prompt, но ломает другой | средняя | парсить все generated TOML + дважды запускать sync |
| Pipeline-тест меняет tracked xlsx | средняя | запускать копию модуля из `tmp_path`, после теста проверять `git status` |
| Link-check ловит ссылки-примеры как реальные | средняя | code literals для placeholders + точечные исключения с комментарием |
| Bump version затронет форки | низкая | PATCH `0.3.1`, синхронно обновить VERSION/pyproject/changelog |

## Чек-лист реализации

**P0 — установка и тестовый контур:**
- [ ] `pyproject.toml`: name → `vibecommerce-seller-project`, version → `0.3.1`, ruff target → `py311`
- [ ] `pyproject.toml`: добавить runtime dependencies включённых FREE-модулей
- [ ] `Makefile`: убрать ложноположительные fallback из install/lint/test, убрать пустой `test-e2e`
- [ ] Создать `tests/test_template_integrity.py`, `tests/test_module_05_pipeline.py`, `tests/test_cli_tools.py`
- [ ] Smoke: editable-install в чистом venv проходит

**P1 — cross-agent:**
- [ ] `sync-agents-config.sh`: безопасная TOML-сериализация всех строк
- [ ] Перегенерировать cross-agent артефакты; второй sync не создаёт diff
- [ ] `verify-cross-compat.sh`: YAML/JSON/TOML parse + проверка target симлинков
- [ ] Regression: исходные невалидные generated TOML теперь парсятся

**P2 — pure template и модуль 05:**
- [ ] `generate_sales_data.py` → DATA_DIR/sales_data_v1.0.xlsx
- [ ] `generate_ads_data.py` → DATA_DIR/ads_data_v1.0.xlsx
- [ ] `abcdx_analysis.py` → DATA_DIR in/out
- [ ] `funnel_analysis.py` → DATA_DIR (вместо SCRIPT_DIR)
- [ ] README модуля 05 → полный порядок generate-sales → generate-ads → abcdx → funnel
- [ ] Smoke: pipeline generate→abcdx→funnel отрабатывает на data-demo/
- [ ] Зачистка личных путей в .py/.md/.css/handoff
- [ ] `grep /Users/<user>` → пусто (кроме .git)
- [ ] Ozon UUID-пример → явный placeholder; secret scan tracked-файлов чист

**P3 — документация и механическая чистка:**
- [ ] Убрать публичные упоминания отсутствующего `install-claude-tools`
- [ ] Мёртвые ссылки на 2 отсутствующих плана — убрать/заменить без фиктивного target
- [ ] Остальные битые md-ссылки — исправить; link-check зелёный
- [ ] README в пользовательских точках входа; остаток вынести в follow-up backlog item
- [ ] Форматирование отдельным механическим коммитом
- [ ] Обновить README затронутых папок + `Last Updated`
- [ ] Запись о `0.3.1` в `_changelogs/CHANGELOG.md`, bump `VERSION`

## Метрика «успех»

1. `uv venv /tmp/t && VIRTUAL_ENV=/tmp/t uv pip install -e ".[dev]"` → success (P0.1).
2. `make test` выполняет ненулевой набор тестов и завершается `0`; намеренно
   сломанный TOML в temp fixture делает regression-тест красным.
3. `make lint` и `make verify-agents` завершаются `0`; повторный
   `make sync-agents` не создаёт diff.
4. `grep -rI "/Users/<user>" . | grep -v /.git/` → пусто.
5. Secret scan tracked-файлов не находит live-key/JWT сигнатуры; `.env.example`
   содержит только пустые значения.
6. Pipeline модуля 05 (generate-sales → generate-ads → abcdx → funnel)
   проходит в temp-копии без правок путей и без изменения tracked `.xlsx`.
7. Проверка локальных Markdown-ссылок проходит; placeholders не маскируются под
   реальные hyperlinks.
8. `git status --short` после тестов содержит только ожидаемые правки ремонта.

## Решения для согласования

1. **Версия:** выпустить ремонт как `0.3.1`, а не переписывать уже выпущенную `0.3.0`.
2. **Python:** оставить `>=3.11`, привести ruff к `py311`.
3. **Зависимости:** включить зависимости FREE-модулей в обычный `make install`,
   без optional-extra.
4. **`install-claude-tools`:** убрать незавершённую публичную команду; идею
   оставить в brief до отдельного проектирования.
5. **Мёртвые планы:** не восстанавливать выдуманное содержимое и не ссылаться
   на пустую директорию; заменить ссылки на существующие источники.
6. **README:** ~~закрыть только точки входа~~ → **override пользователя
   (2026-06-02):** README во ВСЕХ важных папках проекта в рамках этого ремонта.
   Исключения — вендоренные подпапки скиллов, gitignored `_private/*`, пустые dir.

## Связанные

- QA-прогон 2026-06-01 (источник находок) — этот план
- Индекс активных планов: [`README.md`](README.md)
- Архив после реализации: `../archive/done/2026-06-01-fix-template-integrity.md`
- Правило: `.claude/rules/plan-before-act.md`, workflow: `_practices/00-WORKFLOW.md`
