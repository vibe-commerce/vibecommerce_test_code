# `.claude/skills/` — Claude Code slash-команды

Last Updated: 2026-05-29

## Что здесь

Skills — это slash-команды Claude Code. Каждая папка с `SKILL.md` =
одна команда.

## FREE skills (этот репо)

### Meta / devtools
| Skill | Назначение |
|-------|------------|
| `agent-creator` | Создание Claude Code subagent'ов |
| `skill-creator` | Создание новых skills |
| `project-knowledge` | База знаний структуры/конвенций/lifecycle |

### Utility
| Skill | Назначение |
|-------|------------|
| `backup` | Коммит + push с осмысленным сообщением |
| `project-manager` | Управление бэклогом, спринтами, приоритизацией |

### Git workflow
| Skill | Назначение |
|-------|------------|
| `/commit` | AI-генерация commit message |
| `/push` | Безопасный push с подтверждением |
| `/git-status` | Статус веток (только local + main) |
| `/handoff` | Сдача сессии → HANDOFF.md |

### Dev workflow
| Skill | Назначение |
|-------|------------|
| `/architect` | Архитектурный план → backlog/plans/ |
| `/docs` | Обновление документации |
| `/test` | lint + types + unit + build |
| `/qa-tester` | Ручное QA с Playwright |

### Legal
| Skill | Назначение |
|-------|------------|
| `/lawyer` | Юрист РФ (ЗоЗПП, 152-ФЗ, B2C, ИП) — **basic** |

### Marketplace hybrid (basic → VIP)
| Skill | Назначение |
|-------|------------|
| `mpstats-analyst` (basic) | 2 базовых метода: `get_category_summary`, `get_top_products` |
| `mpstats-research` (basic) | Single-niche analysis (top-10 конкурентов + базовая статистика) |
| `price-elasticity` (basic) | Arc elasticity, single product |
| `seo-audit` (basic) | Базовый технический аудит (robots, sitemap, meta) |
| `_seo-shared` | Утилиты для seo-audit basic |

## Hybrid skills (basic в FREE, PRO в VIP)

В FREE-репо остаются **базовые версии** с явным hook на VIP. В каждом
SKILL.md в конце есть секция «📈 Полная версия — в `vibecommerce_vip_code`».

Текущие гибриды: `mpstats-analyst`, `mpstats-research`, `price-elasticity`, `seo-audit`.

## VIP-only skills (НЕТ в этом репо)

Эти skills есть только в `vibecommerce_vip_code`:

- `jtbd-research` — глубокая методология AJTBD (Замесин)
- `ecom-manager` — Head of E-Commerce orchestrator
- `seo-content` — keyword research + content brief
- `seo-positions` — мониторинг позиций (Yandex XML + Ahrefs/Semrush)
- `seo-research` — конкурентский SEO-ресёрч

⚠️ Если ты видишь эти папки в FREE-репо — они здесь временно, до миграции
в VIP-репо (фаза V плана апгрейда). См. [план](../../backlog/plans/2026-05-28-upgrade-test-code-from-best-practices.md).

## DEPRECATED (удалены)

- ~~`excel-worker`~~ — удалён 2026-05-29 (использовать generic `openpyxl`/`pandas` без отдельного skill)

## Как добавить новый skill

```bash
# Используй skill-creator:
/skill-creator

Создай skill для {задачи}.
```

Или вручную: создай папку `.claude/skills/<name>/` с `SKILL.md`. Frontmatter
SKILL.md — см. `skill-creator/references/`.

## Связанные

- Родитель: [`../README.md`](../README.md)
- Cross-agent shared skills: [`../../.agents/skills/`](../../.agents/skills/) *(пусто, наполняется в C12)*
- Sub-агенты: [`../agents/`](../agents/)
- Rules: [`../rules/`](../rules/)
- Tiering matrix (полная): [`../../backlog/plans/2026-05-28-skills-agents-tiering-matrix.md`](../../backlog/plans/2026-05-28-skills-agents-tiering-matrix.md)
