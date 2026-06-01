# Настройка VIP-доступа

Last Updated: 2026-05-29

> Этот гайд нужен только если у тебя есть **VIP-тариф** курса Вайб-Коммерс
> и доступ к private репо `vibecommerce_vip_code`.

## Что даёт VIP

Расширения поверх FREE-шаблона:

- **VIP skills:** `/jtbd-research`, `/ecom-manager`, `/seo-content`,
  `/seo-positions`, `/seo-research`, `/counterparty-check`,
  `/product-deep-research`, `/yandex-wordstat`
- **PRO-версии гибридов:** `mpstats-analyst` PRO, `mpstats-research` PRO,
  `price-elasticity` PRO, `seo-audit` PRO
- **VIP agents:** `niche-researcher`, `shopping-researcher`, `seo-auditor`
- **Полные knowledge-наборы:** `marketplace-discounts-guide.md`,
  полные `marketplaces/`, `suppliers/`
- **9 промптов AJTBD** + полная методология Замесина
- **Премиум роли:** `Head_of_E-Commerce`, `AJTBD_Copilot`, `CFO`, `Product_Hero`
- **Cashflow advanced**, расширенный P&L дашборд

## Шаг 1 — Получить доступ

Доступ выдаётся через GitHub team `vibe-commerce-vip-students`. Если ты
уже оплатил VIP, но invite не пришёл — напиши в TG `@vadim_bakanov_ai`.

```bash
gh auth login  # авторизуйся с GitHub аккаунтом, привязанным к VIP
gh auth status  # проверь
```

## Шаг 2 — Клонировать VIP-репо рядом

```bash
# Рядом с твоим FREE-репо
cd ..
git clone https://github.com/vibe-commerce/vibecommerce_vip_code
ls
# my-seller-project/    vibecommerce_vip_code/
```

## Шаг 3 — Подключение VIP к FREE

**Рекомендуемый способ — git pull (плоское использование):**

Просто держи `vibecommerce_vip_code` рядом и используй файлы оттуда напрямую:

```bash
# В Claude Code чате при работе с FREE-репо:
"Открой и прочитай vibecommerce_vip_code/_modules/01-niche-selection/README.md
 — расскажи различия с FREE-версией"
```

Обновления:
```bash
cd ../vibecommerce_vip_code
git pull origin main
```

## Шаг 4 — Альтернатива: copy-on-demand

Если нужны VIP-skills постоянно в FREE workflow, можно скопировать
конкретный skill:

```bash
cp -r ../vibecommerce_vip_code/.claude/skills/jtbd-research .claude/skills/
# Только не коммитить это в свой публичный репо (если он публичный)!
```

⚠️ **Не коммить VIP-контент в публичный FREE-репо** — BSL 1.1 лицензия VIP
запрещает перераспределение.

## Шаг 5 — Дополнительные .env для VIP

VIP-skills используют платные API:
```bash
# .env (gitignored)
AHREFS_API_KEY=
SEMRUSH_API_KEY=
DATAFORSEO_LOGIN=
DATAFORSEO_PASSWORD=
DADATA_API_KEY=
DADATA_SECRET_KEY=
```

См. `.env.example` — там уже есть все placeholder'ы.

## Шаг 6 — Проверка

В Claude Code чате (при работающем VIP):
```
/jtbd-research

Помоги с глубокой AJTBD-сегментацией для моей ниши.
```

Если skill не найден — проверь, что VIP-skills скопированы или что
Claude Code видит обе папки.

## Связанные

- Базовые skills (FREE): см. `.claude/skills/README.md`
- VIP-репо: `https://github.com/vibe-commerce/vibecommerce_vip_code`
- TG для вопросов VIP: `@vadim_bakanov_ai`
