# `_shared/hooks/` — общие хуки

Last Updated: 2026-05-29

## Что здесь

Общие хуки, которые должны срабатывать одинаково в Claude Code и OpenAI Codex.

Симлинки на эти хуки лежат в:
- `.claude/hooks/` (для Claude Code — конфигурируется в `settings.json`)
- `.codex/hooks/` (для Codex — конфигурируется в `config.toml`)

## Текущие хуки

(Скрипты лежат в `.claude/hooks/` пока. После реализации `scripts/sync-agents-config.sh`
они переедут сюда, а в `.claude/hooks/` и `.codex/hooks/` останутся симлинки.)

- `memory-bank-check.sh` — PostToolUse hook. При изменении файла предупреждает,
  если в его папке не обновлён `README.md`. (live в `.claude/hooks/`)

## Связанные

- Родитель: [`../README.md`](../README.md)
- Claude hooks: [`../../.claude/hooks/`](../../.claude/hooks/)
- Codex hooks: [`../../.codex/hooks/`](../../.codex/hooks/)
