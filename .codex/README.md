# `.codex/` — OpenAI Codex-specific конфиг

Last Updated: 2026-05-29

## Что здесь

Конфигурация, skills и hooks специфичные для OpenAI Codex.

```
.codex/
├── config.toml.template   ← шаблон конфига (копируется в ~/.codex/config.toml)
├── skills/<name>          ← симлинки на ../.agents/skills/<name>
├── agents/<name>.toml     ← генерируются из ../.agents/subagents/<name>.yaml
├── prompts/               ← legacy slash-commands (если нужны)
├── hooks/                 ← симлинки на ../_shared/hooks/
└── README.md
```

## Quick start

1. Скопируй конфиг:
   ```bash
   cp .codex/config.toml.template ~/.codex/config.toml
   # Подкорректируй под свои нужды
   ```

2. Запусти sync для проверки симлинков:
   ```bash
   bash scripts/sync-agents-config.sh   # после реализации (C7)
   ```

3. Проверь, что Codex видит:
   - `.codex/skills/` — slash-команды
   - `.codex/agents/` — sub-агенты
   - MCP-серверы из `_shared/mcp.yaml`

## Связанные

- Codex канон: [`../AGENTS.md`](../AGENTS.md)
- Общие инструкции: [`../_shared/INSTRUCTIONS.md`](../_shared/INSTRUCTIONS.md)
- Общие skills: [`../.agents/`](../.agents/)
- Claude эквивалент: [`../.claude/`](../.claude/)
- Onboarding: [`../documentation/onboarding/codex-setup.md`](../documentation/onboarding/codex-setup.md) *(в работе)*
