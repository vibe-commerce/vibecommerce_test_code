---
name: seo-audit
description: |
  BASIC. Базовый технический SEO-аудит сайта или одной страницы:
  robots.txt, sitemap.xml, meta-tags, HTTP-коды, основные Core Web Vitals.
  Без AEO, без Schema.org генерации, без платных API (Ahrefs/Semrush).

  Use when: (1) basic technical SEO check, (2) check robots/sitemap/meta,
  (3) проверка базовых HTTP-кодов и редиректов, (4) "проверь seo basic",
  "технический seo", "basic seo audit", "robots txt", "sitemap check".

  For full audit with AEO + Schema.org + competitors + Ahrefs/Semrush — see VIP repo.
---

# SEO Audit (BASIC)

Базовый технический SEO-аудит. Что есть в FREE — что в VIP.

## Что доступно в FREE (basic)

1. **`robots.txt`** — наличие, корректность, AI-crawler access (basic check)
2. **`sitemap.xml`** — наличие, валидность, кол-во URL
3. **Meta-tags** — `<title>`, `<meta description>`, `<meta robots>`, `<link rel="canonical">`
4. **HTTP-коды** — нет ли 404/500 на ключевых страницах, корректность редиректов 301
5. **Core Web Vitals (basic)** — LCP, FID, CLS через open-source инструменты (Lighthouse CLI)
6. **Mobile-friendly** — viewport meta-tag

## Step 1: Detect Project Context

Detect the framework by checking config files in the project root.

```
Glob: astro.config.* → Astro (SSG)
Glob: next.config.* → Next.js (SSR/SSG)
Glob: nuxt.config.* → Nuxt (SSR)
Glob: hugo.toml → Hugo (SSG)
Glob: index.html in root → Plain HTML
```

## Step 2: Basic checks

### Manual checks (без API)

```bash
# robots.txt
curl -s https://example.com/robots.txt

# sitemap
curl -sI https://example.com/sitemap.xml | head

# meta tags
curl -s https://example.com/ | grep -E "<title|<meta name=\"description|canonical"

# Lighthouse (если установлен)
npx lighthouse https://example.com --only-categories=performance,seo --output=json
```

### Report

Простой Markdown-отчёт:

```markdown
## Basic SEO Audit — {domain}

| Check | Status | Issue |
|-------|--------|-------|
| robots.txt | ✅ / ❌ | ... |
| sitemap.xml | ✅ / ❌ | ... |
| Title tags | ✅ / ❌ | ... |
| Meta descriptions | ✅ / ❌ | ... |
| Canonical | ✅ / ❌ | ... |
| HTTPS | ✅ / ❌ | ... |
| Mobile viewport | ✅ / ❌ | ... |
| Core Web Vitals (LCP/FID/CLS) | ✅ / 🟡 / ❌ | ... |
```

## Связанные

- `_seo-shared` — утилиты framework detection
- `_modules/03-marketplace-analytics/` — для SEO маркетплейса

## 📈 Полная версия — в VIP-репо `vibecommerce_vip_code`

**PRO-версия (`seo-audit` PRO + полный SEO Suite):**

- **AEO (AI Engine Optimization):** проверка autonomous fragments, FAQ-маркап, AI-crawler access deep
- **Schema.org JSON-LD генерация** — Organization, Product, BreadcrumbList, FAQPage, Article, и т.д.
- **Ahrefs MCP** — backlinks, domain rating, anchor texts, competitor analysis
- **Semrush MCP** — keywords positions, traffic share, content gap
- **DataForSEO** — SERP-результаты, keyword difficulty, кластеризация
- **Конкурентский SEO** — детальный анализ топ-3 конкурентов с recommendations
- **Sub-agent `seo-auditor`** — полный технический+on-page+AEO аудит за один прогон

Плюс полный SEO Suite (отдельные skills):
- `/seo-content` — keyword research + content brief
- `/seo-positions` — мониторинг позиций (Yandex XML + Google SC + Ahrefs/Semrush)
- `/seo-research` — конкурентский SEO-ресёрч с keyword clustering

Подключение → `documentation/onboarding/vip-setup.md`.
