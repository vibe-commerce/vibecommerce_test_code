# `.agents/` — cross-agent shared skills и subagents

Last Updated: 2026-05-29

## Что здесь

Общая папка для skills и subagents, которые работают одинаково в Claude Code
и OpenAI Codex.

```
.agents/
├── skills/<name>/SKILL.md       ← один SKILL.md → используется обоими через симлинки
├── subagents/<name>.yaml        ← один YAML → генерируются .md (Claude) и .toml (Codex)
└── README.md
```

## Архитектура (вариант C из ресёрча)

```
┌─────────────────┐     ┌─────────────────┐
│ .claude/skills/ │     │ .codex/skills/  │
│  <name>         │     │  <name>         │
│  (симлинк)      │     │  (симлинк)      │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └──────────┬────────────┘
                    ▼
         ┌─────────────────┐
         │ .agents/skills/ │
         │  <name>/SKILL.md│  ← Источник истины
         └─────────────────┘
```

Для subagents — генератор из `.agents/subagents/<name>.yaml`:
- → `.claude/agents/<name>.md` (Claude формат)
- → `.codex/agents/<name>.toml` (Codex формат)

## Текущее состояние

После реализации `scripts/sync-agents-config.sh` (пункт C7 плана) сюда
переедут все FREE-skills из `.claude/skills/`:
- `commit`, `push`, `git-status`
- `architect`, `docs`, `handoff`
- `test`, `qa-tester`
- `lawyer`, `project-knowledge`
- `agent-creator`, `skill-creator`
- `backup`, `project-manager`
- `mpstats-analyst` (basic), `mpstats-research` (basic), `price-elasticity` (basic), `seo-audit` (basic)
- `_seo-shared`

Skills с Claude-only зависимостями (плагины) — помечены `claude-only: true`
в frontmatter и не симлинкуются в `.codex/`.

## SKILL.md frontmatter (совместимый с agentskills.io)

```yaml
---
name: commit
description: AI-генерация commit message из git diff
version: 1.0.0
agents:
  - claude-code
  - codex
tools:
  - bash
  - git
trigger: "/commit"
---
```

## Связанные

- Родитель: [`../README.md`](../README.md)
- Claude skills: [`../.claude/skills/`](../.claude/skills/)
- Codex skills: [`../.codex/skills/`](../.codex/skills/)
- Sync script: [`../scripts/sync-agents-config.sh`](../scripts/sync-agents-config.sh) *(в работе)*
- Полная архитектура: [`../_specs/codex-compat/`](../_specs/codex-compat/) *(в работе)*
