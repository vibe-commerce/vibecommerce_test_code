# `.codex/hooks/` — хуки для OpenAI Codex

Last Updated: 2026-06-02

## Что здесь

Реальные **Codex-специфичные** PostToolUse-адаптеры (apply_patch-aware):

- `auto-ruff.sh` — `ruff check --fix` по изменённым `.py`. Codex правит файлы
  через `apply_patch`, поэтому пути берутся из `tool_input.command`
  (маркеры `*** Add/Update/Delete File:`) с fallback на `git status`.
- `memory-bank-check.sh` — при изменении файла напоминает обновить `README.md`
  его папки (правило MEMORY BANK). Предупреждение — через `{"systemMessage": …}`.
  НЕ блокирует действие.

Это **не симлинки**: Claude- и Codex-адаптеры имеют разный I/O-контракт
(Claude-версии — в `.claude/hooks/`). См. [`../../_shared/hooks/README.md`](../../_shared/hooks/README.md).

## Как монтируются

1. `.codex/hooks.json` — PostToolUse matcher + self-locating команды
   (`git rev-parse --show-toplevel` → работает из любого подкаталога).
2. `.codex/config.toml` → `[features] hooks = true` (грузит `hooks.json`
   для trusted repo).

Тихо выходят (`exit 0`), если `jq`/`ruff`/`git` недоступны.

## Связанные

- Родитель: [`../README.md`](../README.md)
- Механизм монтирования: [`../hooks.json`](../hooks.json), [`../config.toml`](../config.toml)
- Общая политика хуков: [`../../_shared/hooks/README.md`](../../_shared/hooks/README.md)
