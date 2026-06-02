# `_shared/hooks/` — общие хуки

Last Updated: 2026-06-02

## Что здесь

Зарезервировано под **платформо-агностичные** хуки-хелперы (общие для Claude
Code и OpenAI Codex). Сейчас таких нет.

⚠️ Хуки `memory-bank-check` и `auto-ruff` — это **платформо-специфичные
адаптеры** с разным I/O-контрактом, поэтому НЕ шарятся через симлинки:
- Claude-версии — реальные файлы в `.claude/hooks/` (конфиг — `settings.json`)
- Codex-версии — реальные файлы в `.codex/hooks/` (apply_patch-aware;
  монтируются через `.codex/hooks.json` + `[features] hooks = true` в `.codex/config.toml`)

## Текущие хуки (платформо-специфичные — лежат НЕ здесь)

- `memory-bank-check.sh` — PostToolUse: при изменении файла напоминает обновить
  `README.md` его папки. Claude → `.claude/hooks/`, Codex → `.codex/hooks/`.
- `auto-ruff.sh` — PostToolUse: `ruff --fix` изменённых `.py`. Codex → `.codex/hooks/`.

`_shared/hooks/` остаётся пустой до появления реально платформо-агностичного хука.

## Связанные

- Родитель: [`../README.md`](../README.md)
- Claude hooks: [`../../.claude/hooks/`](../../.claude/hooks/)
- Codex hooks: [`../../.codex/hooks/`](../../.codex/hooks/)
