# Quickstart: форк шаблона

Last Updated: 2026-05-29

> Цель: за 30 минут получить рабочий fork шаблона `vibecommerce_test_code`,
> заполненный твоими данными, готовый к первому модулю.

## Шаг 1 — Клонирование

```bash
# 1.1. Клонируешь шаблон в свою папку
git clone https://github.com/vibe-commerce/vibecommerce_test_code my-seller-project
cd my-seller-project

# 1.2. Создаёшь свой репо на GitHub (приватный — Settings → New repository)
# 1.3. Меняешь remote на свой репо
git remote set-url origin https://github.com/{your-username}/my-seller-project
git push -u origin main
```

## Шаг 2 — Установка окружения

См. для своей OS:
- [`install-macos.md`](install-macos.md)
- [`install-windows.md`](install-windows.md)

Кратко:
```bash
# macOS / Linux
make install
# глобальные skills/agents (~/.claude/) — вручную, см. .claude/EXTERNAL-TOOLS.md

# Windows (через WSL2 или Git Bash)
# см. install-windows.md
```

## Шаг 3 — Заполнение FACTS.md

Открой `FACTS.md` и замени `{placeholder}` на свои данные:

```markdown
- Название: My Seller Project
- Репозиторий: https://github.com/{username}/my-seller-project
- Лендинг: (если есть)
- Юрлицо: ИП {фамилия} (ИНН в _private/secrets/)
- Стек: Python 3.11+, pandas, openpyxl
- Окружения: local (только) — нет dev/prod
```

⚠️ **Боевые токены/реквизиты** — НЕ в FACTS.md! Только в `_private/secrets/`
(этот каталог в `.gitignore`).

## Шаг 4 — Настройка AI-агентов

См.:
- [`claude-code-setup.md`](claude-code-setup.md) — для Claude Code
- [`codex-setup.md`](codex-setup.md) — для OpenAI Codex (опционально)

## Шаг 5 — Запуск первого модуля

```bash
# 1. Прочитай карту модулей
cat _modules/README.md

# 2. Выбери первый модуль (рекомендуется 01-niche-selection)
cat _modules/01-niche-selection/README.md

# 3. Создай рабочую папку в my-project/00-niche
# 4. Запусти модуль
```

## Шаг 6 — Первый коммит

```bash
git checkout -b local                  # рабочая ветка
git add FACTS.md AGENDA.md
git commit -m "feat: initial fork setup, FACTS заполнен"
# main можно держать как mirror local (без push'а если приватный)
```

## Чек-лист «форк готов»

- [ ] Клонирован и привязан к своему GitHub-репо
- [ ] `make install` отработал без ошибок
- [ ] `FACTS.md` заполнен своими данными
- [ ] `.env` создан из `.env.example` с твоими API-ключами (если есть)
- [ ] Claude Code Setup пройден (см. `claude-code-setup.md`)
- [ ] `_modules/README.md` прочитан, выбран первый модуль

## Что НЕ делать

- ❌ Коммитить `.env` (gitignore защищает, но проверь)
- ❌ Складывать боевые токены в `FACTS.md` или README'ах
- ❌ Редактировать файлы в `_modules/` (read-only) — копируй в `my-project/`
- ❌ Игнорировать `_practices/00-WORKFLOW.md` — это твой workflow

## Связанные

- Полный workflow: [`../../_practices/00-WORKFLOW.md`](../../_practices/00-WORKFLOW.md)
- Структура проекта: [`../../README.md`](../../README.md)
- Принципы CLAUDE.md: [`../../CLAUDE.md`](../../CLAUDE.md)
