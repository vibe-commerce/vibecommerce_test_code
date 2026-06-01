# Changelog

История изменений шаблона `vibecommerce_test_code`. Newest first.

Semver правило шаблона (template) — в [CLAUDE.md](../CLAUDE.md) раздел
«Semver для шаблона vibecommerce_test_code».

## 0.3.0 — 2026-05-29

MAJOR-апгрейд скелета: миграция к структуре EMPTY_code v0.5.4 + тиринг
FREE/VIP + Codex-совместимость.

Детальный план, статус и отчёт апгрейда — в `EMPTY_code/_reports/`:
- `2026-05-29-audit-and-free-vs-vip-comparison.md`
- `2026-05-29-test-code-upgrade-status.md`
- `2026-05-29-test-code-upgrade-agenda.md`

### Added
- Канонический скелет EMPTY_code v0.5.4 (Makefile, pyproject.toml, _specs/, _practices/, backlog/lifecycle, etc.)
- 7 методических модулей в `_modules/` (01-niche → 07-financial)
- Рабочая зона студента `my-project/` с 7 подпапками
- Базовая knowledge база `_knowledge/{marketplaces,legal,suppliers}/`
- Промпт-библиотека `_prompts/{roles,jtbd,library}/`
- Cross-agent compatibility: `AGENTS.md` (Codex канон), `_shared/INSTRUCTIONS.md`, `.agents/`, `.codex/`, `scripts/sync-agents-config.sh`, `verify-cross-compat.sh`
- 19 FREE skills + 6 sub-agents + 7 rules + memory-bank-check hook
- Onboarding для студента (`documentation/onboarding/`)
- git tag `pre-upgrade-2026-05-28` (точка отката)

### Removed
- Реальные клиентские данные и токены → в `real-commerce_code/`
- DEV/PROD артефакты (workflow упрощён до `local` + `main`)
- DEPRECATED skill `excel-worker`
- Мусор: CLAUDE copy.md, CLAUDE_secure.md, test.txt, image.png (файлы удалены).
  Пустые husk-папки `PRJ_*`/`_DATA`/`ФИНОТЧЕТ` — удаление ожидает подтверждения (F8)

### Security
- ⚠️ Требуется ротация `WB_API_TOKEN` (лежал в plain-text)

### Fixed (2026-05-31 — по сплошной верификации)
- Принцип №0: убраны имя/email из примера промпта `04-supplier-outreach-1688.md` (F1)
- `.gitignore`: защита `my-project/data/*` + `**/personal-*` + `.gitkeep` (F2, #86)
- `make lint` 66 → 0 ошибок (ruff `--fix` + `target py312` + per-file-ignores `_modules/**`) (F3)
- #74 `slice_buyback_top.py` (генератор FREE-среза) + #83/#72 `balance-template.xlsx` + генератор (F4/F5)
- Убраны stale-маркеры `*(TBD)*` / «(создаётся в фазе)» в README (F6/F7)

> ⏳ **Не закоммичено:** весь апгрейд 0.3.0 + F-серия держатся в working tree
> (209 изменений). Точка отката — tag `pre-upgrade-2026-05-28`. Достоверный
> статус → `EMPTY_code/_reports/2026-05-29-test-code-upgrade-status.md`
> (актуализирован 2026-05-31) и раздел 13 плана апгрейда.

### Migration (для форков 0.2.x)
1. Сделать `git tag pre-upgrade` перед мерджем
2. Применить диффы по структуре
3. Обновить `CLAUDE.md` по эталону
4. Запустить чек-лист «реальные данные унесены»

## 0.2.0 — 2026-02 (legacy)

Стартовая версия. Структура PRJ_*, без backlog lifecycle, без `_practices`/`_specs` каркаса.
