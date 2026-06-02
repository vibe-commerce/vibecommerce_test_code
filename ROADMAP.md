# Roadmap — vibecommerce_test_code

Last Updated: 2026-06-02

> Стратегический план развития **шаблона** (template). Не путать с roadmap'ом
> студента, который форкает шаблон под свой проект селлера.
>
> Детальные спеки → [_specs/](_specs/), оперативные задачи → [backlog/](backlog/).

## Завершено

### Phase 0 (template) — Стартовая версия 0.2.0
- [x] Создание test_code как тестового workspace курса
- [x] PRJ_* проекты (MARKETPLACE, PRICING, ANALYTICS, ВОРОНКА, ВЫБОР_НИШИ)
- [x] Первые skills (mpstats-analyst, ecom-manager, project-manager, etc.)

### Phase 1 (template) — Апгрейд 0.3.0 → 0.3.2

**Цель:** превратить test_code в шаблонный стартер для студентов-селлеров
курса Вайб-Коммерс с тирингом FREE/VIP и cross-agent совместимостью. **Достигнута.**

История релизов — в [`_changelogs/CHANGELOG.md`](_changelogs/CHANGELOG.md):
0.3.0 — апгрейд скелета; 0.3.1 / 0.3.2 — ремонт целостности.

- [x] ШАГ 0 — защита реальных данных (миграция в real-commerce_code)
- [x] Фаза 0 — чистка мусора и старых планов
- [x] Фаза 1 — канонический скелет EMPTY_code v0.5.4
- [x] Фаза 2 — AI-инфраструктура (.claude/{settings,rules,hooks})
- [x] Фаза 2.5/2.6 — миграция и добавление skills + agents
- [x] Фаза 3 — knowledge + prompts (marketplaces, legal, suppliers, roles, JTBD)
- [x] Фаза 4 — юнит-экономика (шаблоны без реальных цифр)
- [x] Фаза 5 — реорганизация PRJ_* → _modules/ + my-project/
- [x] Фаза 7 — onboarding студента (quickstart-fork, install-{macos,windows}, claude-code-setup, vip-setup)
- [x] Фаза C — Cross-agent compatibility (Claude Code + OpenAI Codex)
- [x] 0.3.1 — ремонт целостности (install / тесты / cross-agent / pure-template)
- [x] 0.3.2 — ремонт целостности раунд 2 + рабочие Codex-хуки (apply_patch-aware, self-locating)

## В работе

### Sync целостности FREE → VIP (итерация 2 плана integrity-round2)

Портировать фиксы целостности 0.3.1 / 0.3.2 в `vibecommerce_vip_code`
(verify-скрипт, pyproject, валидный TOML агентов, битые ссылки, Принцип №0),
bump VIP → 0.3.1. План:
[`backlog/plans/2026-06-02-template-integrity-round2.md`](backlog/plans/2026-06-02-template-integrity-round2.md).

## Следующие фазы

### Phase 2 (template) — VIP-репо (развёрнут: v0.3.0, BSL 1.1)

В [`vibecommerce_vip_code`](https://github.com/vibe-commerce/vibecommerce_vip_code) (private):

- [x] V1-V3 — форк скелета из test_code, BSL 1.1 лицензия
- [~] V4-V8 — миграция VIP skills / agents / knowledge / prompts (~80%; остаток:
  6-фазная методика ниши, supplier deep-dive, Ahrefs/Semrush-интеграции)
- [~] V10-V14 — onboarding для VIP-студентов + git pull workflow
- [ ] Sync целостности 0.3.1 / 0.3.2 + bump VIP → 0.3.1 (см. «В работе»)

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
