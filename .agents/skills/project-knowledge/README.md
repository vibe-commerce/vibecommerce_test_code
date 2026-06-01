# `.claude/skills/project-knowledge/` — база знаний шаблона

Last Updated: 2026-05-01

## Что здесь

Skill, который содержит расширенный контекст шаблона EMPTY_code:
структуру, конвенции, Git-workflow, lifecycle документа.

CLAUDE.md держит только critical rules. Подробности — здесь.

## Содержимое

- `SKILL.md` — frontmatter + точки входа (когда что читать)
- `references/architecture.md` — структура папок, корневые файлы, three-layer rule
- `references/workflow.md` — Git-workflow, ветки, коммиты, deploy
- `references/patterns.md` — конвенции именования, теги, README в каждой папке
- `references/lifecycle.md` — жизненный цикл `ideas/ → briefs/ → _specs/ → код → documentation/`

## Как пользоваться

При работе с темой структуры / git / lifecycle — Claude автоматически подгружает
соответствующий reference-файл. Также подгружай вручную при создании нового
документа (чтобы выбрать правильное место и формат).

## Связанные

- Родитель: [`../README.md`](../README.md)
- CLAUDE.md ссылается на этот skill в разделе «MEMORY BANK + File Management»
