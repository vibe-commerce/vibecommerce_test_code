---
name: {skill-name}
description: {1-2 предложения — когда Claude должен активировать этот скилл}
---

# {Skill Name}

## Input
- {что получает скилл от пользователя}
- {опциональные параметры}

## Output
- {что возвращает: формат, файлы, структура}

## Steps
1. {Шаг 1 — конкретное действие}
2. IF {условие} → {действие A}
   ELSE → {действие B}
3. FOR EACH {элемент}:
   - {проверка}
   - {действие}
4. Run `make test` → if fails → fix → retry (max 3)
5. {Финальный шаг — формирование результата}

## Constraints
- {Ограничение 1 — что НЕ делать}
- {Ограничение 2}

## Quality Gates
- [ ] {Проверка 1}
- [ ] {Проверка 2}

## Memory
Path: `.claude/data/{skill-name}-memory.md`
- Read at start of each run
- Write lessons learned, edge cases, anti-patterns at end

## References
- @{reference-file-1.md}
- @{reference-file-2.md}
