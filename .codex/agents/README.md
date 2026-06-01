# `.codex/agents/` — конфиги суб-агентов для OpenAI Codex

Last Updated: 2026-06-02

## Что здесь

Сгенерированные `.toml`-конфиги суб-агентов для OpenAI Codex.
Создаются автоматически из `.agents/subagents/*.yaml` командой
`make sync-agents`.

## Как пользоваться

- НЕ редактировать вручную — файлы перезаписываются генерацией
- Источник правды — `.agents/subagents/*.yaml`
- После правки YAML — перегенерируй: `make sync-agents`

## Связанные

- Родитель: [`../README.md`](../README.md)
