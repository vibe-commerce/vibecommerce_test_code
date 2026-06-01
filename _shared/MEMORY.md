# MEMORY — общая память репо для AI-агентов

Last Updated: 2026-05-29

> Эта память видна и Claude Code, и OpenAI Codex (читается через `_shared/`).
> Личная память отдельного агента (Claude `~/.claude/memory/`) — отдельно.

## Стабильные факты

- Шаблон форкается студентами курса Вайб-Коммерс
- Workflow упрощён: только `local` + `main`, без dev/prod
- В репо НЕТ персональных/клиентских данных (Принцип №0)
- Тиринг: FREE (этот репо) + VIP (`vibecommerce_vip_code`)
- Cross-agent совместимость через `AGENTS.md` + `CLAUDE.md` + `_shared/INSTRUCTIONS.md`

## Активные правила

- `plan-before-act` — перед нетривиальной правкой план в файл + согласование
- `cost-control` — лимиты на платные API (Apify, scrape.do)
- `marketplace-data-freshness` — rate limits + обновление кеша
- `legal-data-freshness` — мониторинг 152-ФЗ, ЗоЗПП, ТР ТС, ПП РФ № 2425
- `auto-backup` — предлагать бэкап после значимой работы
- `error-learning` — записывать ошибки в `.claude/data/error-log.md`
- `session-retrospective` — маркеры в коде/коммитах

## Decisions log (важные решения апгрейда)

- 2026-05-28 — Workflow упрощён до `local` + `main` (выкинут DEV/PROD деплой)
- 2026-05-28 — Реальные данные мигрированы в `real-commerce_code`:
  - АВТОЗАПЧАСТИ → `clients/avtozapchasti/`
  - ФИНОТЧЕТ → `_private/finance/`
  - Anton-Masha → `clients/anton-masha/`
  - electronics-returned-stock → `clients/electronics-returned-stock/`
- 2026-05-28 — Тиринг FREE/VIP — детально в [`backlog/plans/2026-05-28-skills-agents-tiering-matrix.md`](../backlog/plans/2026-05-28-skills-agents-tiering-matrix.md)
- 2026-05-28 — VIP-лицензия BSL 1.1 (как `vibecommerce_ai_analyst_code`)
- 2026-05-28 — Cross-agent compat реализуется через `AGENTS.md` (Codex) + `CLAUDE.md` (Claude) + `_shared/INSTRUCTIONS.md` (общее)

## Что в работе

- Апгрейд test_code 0.2.0 → 0.3.0 (см. [`backlog/plans/2026-05-28-upgrade-test-code-from-best-practices.md`](../backlog/plans/2026-05-28-upgrade-test-code-from-best-practices.md))
- Создание VIP-репо `vibecommerce_vip_code` (фаза V — открытая задача)
- Split гибридов (mpstats-analyst basic/PRO, etc.) — после VIP-репо

## Открытые вопросы

- Архивация donor-репо (`vibecommerce_demo_code`, `vadim-bakanov-ai-dev`) — гигиена, не блокер
- Полная реализация sync-agents-config.sh (генератор Claude .md ↔ Codex .toml)

## Связанные

- Полная история: [`../_changelogs/CHANGELOG.md`](../_changelogs/CHANGELOG.md)
- Текущий статус: [`../_status/PROJECT_STATUS.md`](../_status/PROJECT_STATUS.md)
- Политика памяти: [`memory-policy.md`](memory-policy.md)
