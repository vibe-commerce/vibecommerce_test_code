# `_prompts/` — библиотека промптов и ролей

Last Updated: 2026-05-29

## Структура

- [`roles/`](roles/) — промпты-роли для разных задач (SMM Consultant, seller assistant)
- [`jtbd/`](jtbd/) — JTBD-промпты (FREE: 1 базовая карточка; полные 9 — в VIP)
- [`library/`](library/) — каталог промптов по тематикам

## Как использовать

Промпты — это **готовые системные сообщения** для AI-агента (Claude/Codex),
которые задают экспертную роль и контекст. Используются для повторяющихся
задач:

- «Сделай SEO-анализ карточки» → `roles/SMM_Consultant.md`
- «Опиши сегмент по JTBD» → `jtbd/jtbd-card-basic.md`
- «Как мне помочь как селлеру?» → `roles/seller-assistant-basic.md`

### Способ 1: Slash-команда (Claude Code)

```
/SMM_Consultant
{твой запрос}
```

### Способ 2: Копипаст в новый чат

```
Открой нужный промпт → скопируй содержимое → вставь как первое сообщение
в новом чате с AI-агентом → дальше задавай задачи.
```

## Принципы

- **Роли в `roles/`** — стабильные «персоны» (1 файл = 1 роль = 1 SKILL).
  Заголовок: «Ты — {роль}. Твоя экспертиза: ... Ты помогаешь {ЦА} с {задачами}»
- **JTBD-промпты в `jtbd/`** — для исследований сегментов и работ
- **Тематические в `library/`** — узкие задачи (тренд-анализ, лендинг, etc.)

## 📈 Углубление в `vibecommerce_vip_code`

Полная библиотека:

### Роли (VIP)
- `Head_of_E-Commerce.md` — полная роль директора по e-commerce
- `AJTBD_Copilot.md` — компаньон по AJTBD-методологии Замесина
- `Product_Hero.md` — мини-продакт для микросегментов
- `CFO.md` — финансовый директор селлера

### JTBD-промпты (VIP, 9 штук)
1. trend-analysis
2. ajtbd-interview-analysis
3. ajtbd-recruit-respondents
4. ajtbd-rat-risks
5. ajtbd-segments-b2b
6. ajtbd-segments-b2c
7. ajtbd-jobs-graph
8. ajtbd-landing-text
9. ajtbd-card-extended

## Связанные

- Knowledge: [`../_knowledge/`](../_knowledge/) (для подсказок промптов)
- Skills: [`../.claude/skills/`](../.claude/skills/)
- Модули: [`../_modules/`](../_modules/) (промпты применяются к задачам модулей)
