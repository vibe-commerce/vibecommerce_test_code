# `.claude/hooks/` — Bash-хуки Claude Code

Last Updated: 2026-05-01

## Что здесь

Хуки — это shell-команды, которые Claude Code выполняет в ответ на события
(PreToolUse, PostToolUse, Stop и др.). Регистрируются в `.claude/settings.json`.

В отличие от правил (`../rules/`) хуки **детерминированы** — выполняются всегда,
не зависят от внимания LLM. Используй для действий, которые «должны произойти
без исключений».

## Содержимое

- `memory-bank-check.sh` — PostToolUse warning при изменении файла без обновления
  README в его папке (реализует правило MEMORY BANK из CLAUDE.md)

## Как пользоваться

1. Добавь скрипт в эту папку
2. `chmod +x скрипт.sh`
3. Зарегистрируй в [`../settings.json`](../settings.json) → `hooks.<EventName>`
4. Документируй здесь, в README

## Связанные

- Родитель: [`../README.md`](../README.md)
- Правила (advisory): [`../rules/`](../rules/)
- Регистрация: [`../settings.json`](../settings.json)
