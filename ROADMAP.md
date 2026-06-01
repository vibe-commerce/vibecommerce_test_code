# Roadmap — vibecommerce_test_code

Last Updated: 2026-05-29

> Стратегический план развития **шаблона** (template). Не путать с roadmap'ом
> студента, который форкает шаблон под свой проект селлера.
>
> Детальные спеки → [_specs/](_specs/), оперативные задачи → [backlog/](backlog/).

## Завершено

### Phase 0 (template) — Стартовая версия 0.2.0
- [x] Создание test_code как тестового workspace курса
- [x] PRJ_* проекты (MARKETPLACE, PRICING, ANALYTICS, ВОРОНКА, ВЫБОР_НИШИ)
- [x] Первые skills (mpstats-analyst, ecom-manager, project-manager, etc.)

## В работе

### Phase 1 (template) — Апгрейд 0.3.0 (текущая)

**Цель:** превратить test_code в шаблонный стартер для студентов-селлеров
курса Вайб-Коммерс с тирингом FREE/VIP и cross-agent совместимостью.

План: [`backlog/plans/2026-05-28-upgrade-test-code-from-best-practices.md`](backlog/plans/2026-05-28-upgrade-test-code-from-best-practices.md).

- [x] ШАГ 0 — защита реальных данных (миграция в real-commerce_code)
- [x] Фаза 0 — чистка мусора и старых планов
- [ ] Фаза 1 — канонический скелет EMPTY_code v0.5.4 (70% выполнено)
- [ ] Фаза 2 — AI-инфраструктура (.claude/{settings,rules,hooks})
- [ ] Фаза 2.5/2.6 — миграция и добавление skills + agents
- [ ] Фаза 3 — knowledge + prompts (marketplaces, legal, suppliers, roles, JTBD)
- [ ] Фаза 4 — юнит-экономика (шаблоны без реальных цифр)
- [ ] Фаза 5 — реорганизация PRJ_* → _modules/ + my-project/
- [ ] Фаза 7 — onboarding студента (quickstart-fork, install-{macos,windows}, claude-code-setup, vip-setup)
- [ ] Фаза C — Cross-agent compatibility (Claude Code + OpenAI Codex)

## Следующие фазы

### Phase 2 (template) — VIP-репо

Параллельная задача в [`vibecommerce_vip_code`](https://github.com/vibe-commerce/vibecommerce_vip_code) (private):

- [ ] V1-V3 — форк скелета из test_code v0.3.0, BSL 1.1 лицензия
- [ ] V4-V8 — миграция VIP skills (jtbd-research, ecom-manager, seo-content, seo-positions, seo-research), agents (niche-researcher, shopping-researcher, seo-auditor), knowledge (marketplace-discounts, 6-фазная методика выбора ниши, supplier deep-dive), prompts (Head_of_E-Commerce, AJTBD Copilot, CFO, Product Hero)
- [ ] V10-V14 — onboarding для VIP-студентов + git pull workflow

### Phase 3 (template) — Архивация donor-репо

После завершения миграции — пометить `vibecommerce_demo_code` и
`vadim-bakanov-ai-dev` как архивные (вариант A/B/C/D — открытый вопрос плана).

## Бэклог стратегий (low priority)

- Возможный design-system модуль для DTC-стора (Phase 6 плана — пока skip)
- Расширение knowledge до marketplace-specific guides (TG-каналы, Avito)
- Интеграция с FinOlog/Финтабло (если будет запрос от студентов)

---

> Правила обновления:
> - Перенос из «В работе» в «Завершено» — на момент мержа в `main`
> - Новые фазы добавляются после ревью бэклога (раз в квартал)
> - Если пункт стоит в «Ближайшем» >2 месяцев — пересмотри приоритет
