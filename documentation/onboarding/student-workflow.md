# Workflow студента: день-в-день

Last Updated: 2026-05-29

> Как студент работает с шаблоном после форка и установки.

## Общая схема

```
Утро (10 мин):
  1. cat AGENDA.md        ← что было вчера, текущий фокус
  2. /git-status          ← состояние ветки
  3. Выбираешь задачу из плана текущего модуля

День (4-8 часов):
  4. Открываешь _modules/<номер>/README.md
  5. Копируешь шаблоны/скрипты в my-project/<номер>/
  6. Работаешь над задачей (Claude помогает через slash-команды)
  7. Сохраняешь результат в my-project/reports/

Вечер (15 мин):
  8. /handoff             ← обновляет HANDOFF.md
  9. /commit              ← AI-генерация commit message
  10. (опц.) /push        ← если готов запушить
```

## Подробно

### Шаг 1 — Старт сессии

```bash
# Открой AGENDA.md
cat AGENDA.md

# Или в Claude Code:
"Прочитай AGENDA.md, расскажи где мы остановились"

# Проверь git
/git-status
```

### Шаг 2 — Выбор модуля и задачи

См. `_modules/README.md` — порядок прохождения.

Внутри модуля (`_modules/01-niche-selection/README.md`) есть **чек-лист
«модуль закрыт»** — это твои задачи.

### Шаг 3 — Plan Before Act

Если задача нетривиальная — Claude **должен** сначала создать план в
`backlog/plans/{date}-{slug}.md` (правило `plan-before-act.md`).

```
/architect

Задача: выбрать нишу из top-30 категорий MPStats по 5 критериям.
```

→ Claude создаст план в `backlog/plans/`. Прочитай. Скажи «делай» / «ок»
→ Claude начнёт исполнять.

### Шаг 4 — Работа с модулем

```bash
# Создаёшь свою рабочую папку
mkdir -p my-project/00-niche/data
mkdir -p my-project/00-niche/reports

# Копируешь шаблон
cp _modules/01-niche-selection/templates/niche-scoring-template.xlsx \
   my-project/00-niche/

# Кладёшь свои выгрузки в data/ (gitignored!)
cp ~/Downloads/mpstats-export.csv my-project/00-niche/data/

# Запускаешь скрипты
python _modules/01-niche-selection/add_buyback_rate.py \
   my-project/00-niche/data/mpstats-export.csv
```

### Шаг 5 — Feedback Loop

После генерации/изменения кода:
```
/test          # lint + unit tests
```

Если падает → исправь → повтори (max 3 попытки). Если не сходится за 3 → пауза.

### Шаг 6 — Сохранение результата

```bash
# Финальный отчёт в reports/
echo "# Отчёт по выбору ниши $(date +%Y-%m-%d)" > \
  my-project/reports/01-niche-selection-$(date +%Y-%m-%d).md

# Подробности
```

### Шаг 7 — Завершение сессии

```bash
# 1. Обнови AGENDA.md (что сделано сегодня, что осталось)
/handoff

# 2. Закоммить
/commit
# Claude сгенерирует осмысленный commit message

# 3. (Опционально) Push на свой GitHub
/push
```

## Принципы работы

### KISS
Не плоди абстракции на будущее. Если задача — посчитать ABCDX по 30 SKU
один раз — не делай pipeline на 1000 SKU.

### YAGNI
Не пиши код «на будущее». Если не нужно прямо сейчас — не делай.

### Plan Before Act
Перед нетривиальной правкой — план в файл, согласование, потом исполнение.
Без явного сигнала AI **ждёт**.

### Memory Bank
README в каждой папке — карта памяти. Меняешь файл — обновляешь README.

### Принцип №0
В test_code НЕТ персональных данных. Свои данные → `my-project/data/`
(gitignored). Боевые токены → `_private/secrets/` (gitignored).

## Полезные skills для повседневной работы

| Когда | Skill |
|-------|-------|
| Начало задачи | `/architect` (план) |
| Поиск в коде | `/project-knowledge` |
| Что-то сломалось | `/test` (lint/types/tests) |
| Конец дня | `/handoff` + `/commit` + `/push` |
| Юридический вопрос | `/lawyer` |
| QA своего лендинга | `/qa-tester` |

## Связанные

- Полный workflow (8 этапов): [`../../_practices/00-WORKFLOW.md`](../../_practices/00-WORKFLOW.md)
- Plan Before Act: [`../../_practices/01-plan-then-act.md`](../../_practices/01-plan-then-act.md)
- Feedback Loop: [`../../_practices/04-feedback-loop.md`](../../_practices/04-feedback-loop.md)
- Модули: [`../../_modules/README.md`](../../_modules/README.md)
