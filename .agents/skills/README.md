# `.agents/skills/` — cross-agent shared skills (источник правды)

Last Updated: 2026-06-02

## Что здесь

Единый источник правды для общих скиллов, видимых обоими агентами
(Claude Code и OpenAI Codex). Симлинкуются в `.claude/skills/` и
`.codex/skills/` командой `make sync-agents`.

## Как пользоваться

- Все правки общих скиллов вноси здесь
- После изменений — `make sync-agents` для обновления симлинков

## Связанные

- Родитель: [`../README.md`](../README.md)
