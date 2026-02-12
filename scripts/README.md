# Скрипты и утилиты

Last Updated: 2026-02-12

## Доступные скрипты

### backup_to_git.zsh
**Назначение:** Бэкап всех изменений на GitHub одной командой.
**Запуск:** `./scripts/backup_to_git.zsh "комментарий"` или алиас `backup "комментарий"`
**Зависимости:** git

### convert_xlsx_to_md.py
**Назначение:** Конвертация Excel-файла в Markdown-таблицу (для читаемости в Git).
**Запуск:** `uv run --with openpyxl scripts/convert_xlsx_to_md.py файл.xlsx`
**Флаги:** `-o output.md` (файл), `--sheet "Лист1"` (конкретный лист)
**Зависимости:** openpyxl

### md_to_html.py
**Назначение:** Конвертация Markdown в HTML (для отчётов и презентаций).
**Запуск:** `uv run --with markdown scripts/md_to_html.py отчёт.md -o отчёт.html`
**Зависимости:** markdown

## Алиасы для .zshrc
```bash
alias backup="./scripts/backup_to_git.zsh"
alias xlsx2md="uv run --with openpyxl scripts/convert_xlsx_to_md.py"
alias md2html="uv run --with markdown scripts/md_to_html.py"
```
