# Цветовые темы шаблона — каталог

Last Updated: 2026-05-01

Шаблонный репозиторий идёт с **4 готовыми цветовыми темами**.
Каждая тема имеет светлый и тёмный режим с переключением через
`data-theme` атрибут на `<html>`.

При создании нового проекта из шаблона **выбирается одна тема**.
Остальные можно удалить или оставить как референс.

## Таблица тем

| # | Имя | Источник | Стиль | Файл |
|---|-----|----------|-------|------|
| 1 | **vibecommerce-cyan** | `vibecommerce_code` (Midnight Blue + Cyan) | Tech / Dark-first / Premium | [themes/01-vibecommerce-cyan.css](themes/01-vibecommerce-cyan.css) |
| 2 | **slovo-editorial** | `SLOVO_code` (Editorial Brutalism) | Editorial / Cream + Sage | [themes/02-slovo-editorial.css](themes/02-slovo-editorial.css) |
| 3 | **geist-neutral** | Geist / Vercel-style baseline | Neutral B2B / SaaS-friendly | [themes/03-geist-neutral.css](themes/03-geist-neutral.css) |
| 4 | **monochrome** | Pure black & white | Минимализм / Текстовые проекты | [themes/04-monochrome.css](themes/04-monochrome.css) |

## Как выбрать тему

| Тип проекта | Рекомендация |
|---|---|
| AI/tech-продукт, презентации, B2C-курс | **vibecommerce-cyan** |
| Editorial / контент / медиа / журнал / блог | **slovo-editorial** |
| B2B SaaS, dashboards, нейтральный стиль | **geist-neutral** |
| Текстовая утилита, документация, MVP | **monochrome** |

При создании проекта из шаблона диалог:
> «Какую тему берём? 1) vibecommerce-cyan, 2) slovo-editorial,
> 3) geist-neutral, 4) monochrome. Default = 3.»

После выбора — оставить только нужный CSS, удалить остальные,
обновить `design-system/src/index.css` с импортом выбранной темы.

---

## Шрифты — лицензии и пригодность для коммерческих проектов

Все шрифты, используемые в темах — **Open Source**, **коммерческое
использование разрешено**.

| Шрифт | Лицензия | Темы | Где брать |
|-------|----------|------|-----------|
| **Inter** | SIL Open Font License 1.1 | 1 (vibecommerce-cyan), 3 (geist-neutral), 4 (monochrome) | [Google Fonts](https://fonts.google.com/specimen/Inter), [rsms.me/inter](https://rsms.me/inter/) |
| **Space Grotesk** | SIL Open Font License 1.1 | 2 (slovo-editorial) | [Google Fonts](https://fonts.google.com/specimen/Space+Grotesk) |
| **JetBrains Mono** | SIL Open Font License 1.1 | все темы (моно) | [jetbrains.com/mono](https://www.jetbrains.com/mono/) |
| **Material Symbols Outlined** | Apache License 2.0 | все темы (иконки) | [Google Fonts Icons](https://fonts.google.com/icons) |

### Что НЕ использовать (даже если попадётся в чужом коде)

- ❌ **SF Mono / SF Pro** (Apple) — только в Apple-приложениях,
  для веба нелегально.
- ❌ **Helvetica / Helvetica Neue** — платная (Linotype/Monotype).
- ❌ **Proxima Nova** — платная.
- ❌ **Любые шрифты «бесплатно для личного использования»** —
  читать лицензию, обычно нельзя на сайт продукта.

### Замена для fallback monospace

В `vibecommerce_code/.claude/skills/md-to-presentation/` указан
`SF Mono` как fallback. Это **юридическая ошибка** для веба.
В шаблонных темах заменено на:

```css
font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code',
             ui-monospace, 'Consolas', monospace;
```

Все три первых fallback'а — Open Source.

---

## Структура CSS-токенов (общая для всех тем)

Каждая тема использует одинаковые имена CSS Custom Properties
для совместимости. Это позволяет переключать темы без правки
компонентов.

```css
:root {
  /* Поверхности */
  --bg              /* основной фон страницы */
  --surface         /* фон карточек, панелей */
  --surface-2       /* вторичный фон (приглушённые блоки) */
  --surface-3       /* акцентированная поверхность */

  /* Границы */
  --border          /* основная граница */
  --border-dim      /* приглушённая граница */

  /* Текст */
  --text            /* основной текст */
  --text-dim        /* вторичный текст */
  --text-muted      /* очень приглушённый текст */

  /* Бренд / акцент */
  --accent          /* основной акцент / CTA */
  --accent-hover    /* hover-состояние акцента */
  --accent-soft     /* фон бейджа / мягкая подсветка */
  --on-accent       /* текст поверх акцента */

  /* Семантика */
  --success         /* успех / подтверждение */
  --warning         /* предупреждение */
  --danger          /* ошибка / опасность */
  --info            /* информационное состояние */

  /* Эффекты */
  --shadow-sm       /* малая тень */
  --shadow-md       /* средняя тень */
  --shadow-lg       /* крупная тень */
  --radius-sm       /* малый радиус */
  --radius-md       /* средний радиус */
  --radius-lg       /* крупный радиус */
  --radius-pill     /* pill-форма */
}
```

---

## Механизм переключения темы

### HTML
```html
<html data-theme="light">
  <head>
    <link rel="stylesheet" href="themes/03-geist-neutral.css">
  </head>
  <body>
    ...
    <button id="theme-toggle">🌓</button>
  </body>
</html>
```

### JS (минимальный)
```js
// theme-toggle.js
const root = document.documentElement;
const stored = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const initial = stored || (prefersDark ? 'dark' : 'light');
root.setAttribute('data-theme', initial);

document.getElementById('theme-toggle')?.addEventListener('click', () => {
  const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});
```

### CSS-структура каждой темы

```css
/* 03-geist-neutral.css */
:root,
[data-theme="light"] { /* light tokens */ }

[data-theme="dark"] { /* dark tokens (только переопределения) */ }
```

Это работает **без JS** (через `prefers-color-scheme`):

```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { /* dark tokens */ }
}
```

Темы поддерживают оба механизма — JS-переключение через
`data-theme` имеет приоритет, по умолчанию следует системе.

---

## Использование в Tailwind

Все темы спроектированы так, чтобы CSS Custom Properties
подключались как Tailwind-токены через `tailwind.config.js`:

```js
// tailwind.config.js
export default {
  theme: {
    extend: {
      colors: {
        bg:        'var(--bg)',
        surface:   'var(--surface)',
        'surface-2': 'var(--surface-2)',
        text:      'var(--text)',
        'text-dim':'var(--text-dim)',
        accent:    'var(--accent)',
        'accent-hover': 'var(--accent-hover)',
        border:    'var(--border)',
        // ...
      },
      borderRadius: {
        sm:   'var(--radius-sm)',
        DEFAULT: 'var(--radius-md)',
        lg:   'var(--radius-lg)',
        pill: 'var(--radius-pill)',
      },
    },
  },
}
```

Затем в JSX/HTML:
```html
<div class="bg-surface text-text border border-border rounded">
  <button class="bg-accent text-on-accent hover:bg-accent-hover">CTA</button>
</div>
```

При смене темы (`data-theme="dark"`) все классы автоматически
работают с новыми значениями токенов.

---

## Связанные документы

- [_specs/design/themes/01-vibecommerce-cyan.css](themes/01-vibecommerce-cyan.css)
- [_specs/design/themes/02-slovo-editorial.css](themes/02-slovo-editorial.css)
- [_specs/design/themes/03-geist-neutral.css](themes/03-geist-neutral.css)
- [_specs/design/themes/04-monochrome.css](themes/04-monochrome.css)
- `design-system/` — каталог UI-компонентов с переключателем темы
  (папка появляется только после применения плана из
  `backlog/ideas/2026-05-01-template-upgrade-from-active-repos.md`; в базовом
  шаблоне её нет)
- Скилл `/design-system` — генерирует токены из референса для нового
  проекта (если 4 темы не подходят)
