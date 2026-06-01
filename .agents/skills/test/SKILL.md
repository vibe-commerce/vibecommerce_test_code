---
name: test
description: Тестирование кода и функционала — lint, types, unit tests, build check. Используй при тестировании, проверке, test, lint, smoke test, проверке качества кода.
---

# /test — Testing & Validation (entry-point)

Тонкий entry-point. Полный workflow тестирования живёт в саб-агенте
`test-runner` — он изолирует контекст (десятки строк вывода lint/pytest
не загрязняют основной диалог) и переиспользуется другими агентами
(например, `code-reviewer` через Review Mode).

## Instructions

### 1. Распарсь аргумент

Возможные варианты от пользователя:
- (без аргумента) → режим `quick` (lint + unit tests, быстрый цикл разработки)
- `/test full` → все проверки + e2e + data pipeline
- `/test e2e` → только e2e
- `/test data-pipeline` → только проверка `data/processed/`
- `/test focus:<path>` → запускать тесты только для указанного пути

Если режим неоднозначен — спроси пользователя одной строкой.

### 2. Делегируй `test-runner` через Agent tool

```
Agent tool:
  subagent_type: test-runner
  description: Run tests in <mode> mode
  prompt: "<mode> + что именно тестировать (например, focus path)"
```

Агент вернёт структурированный отчёт (см. формат в его SKILL).

### 3. Передай отчёт пользователю

Перепиши кратко:
- Total / Passed / Failed
- Top-3 проблемы (если есть)
- Рекомендация: «Ready for deploy» / «Needs fixes»

При FAIL — сразу предложи следующий шаг (фикс конкретных файлов / запуск
`/test focus:...` после исправления).

## Правила

1. **НЕ исправляй ошибки сам** — задача skill только запустить и переслать отчёт
2. Не пересказывай весь вывод линтера — только summary + ключевые проблемы
3. Если `test-runner` вернул ошибку запуска — диагностируй (нет venv, нет деп) и предложи фикс
