# Brief: Установка внешних Claude Code agents/skills (Вариант C)

Last Updated: 2026-05-02
Owner: Vadim
Status: APPROVED → IN PROGRESS

## Цель

Подключить 4 внешних артефакта (3 субагента + 1 скилл) к рабочей среде так,
чтобы они были (1) переиспользуемы во всех проектах на этой машине и
(2) воспроизводимо устанавливались на новой машине после `git clone EMPTY_code`.

## Контекст

Пользователь форкает шаблон `EMPTY_code` под разные продукты и работает с
нескольких машин. Нужны качественные универсальные агенты (`python-pro`,
`security-auditor`, `multi-agent-coordinator`) и скилл (`webapp-testing`)
без дублирования кода между форками.

## Подход — Вариант C: глобальная установка + bootstrap-скрипт

**Файлы:** ставятся глобально в `~/.claude/agents/` и `~/.claude/skills/`.
**Воспроизводимость:** скрипт `scripts/install-claude-tools.sh` едет с шаблоном,
ставит файлы по pinned commit SHA через `curl raw.githubusercontent.com`.
**Документация:** `.claude/EXTERNAL-TOOLS.md` — список ожидаемых артефактов,
их источники, лицензии, инструкция установки.

Альтернативы и почему отвергнуты:
- Vendored в проектный `.claude/` — каждый форк тащит чужой код, лицензионная
  возня, дубли при обновлениях.
- Только глобально без скрипта — на новой машине забываешь, что нужно поставить;
  шаблон не самодокументируем.

## Источники (pinned)

| Артефакт | Источник | Имя файла | SHA |
|---|---|---|---|
| `python-pro` | [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) (MIT) | `categories/02-language-specialists/python-pro.md` | `6f804f0c` |
| `security-auditor` | VoltAgent (MIT) | `categories/04-quality-security/security-auditor.md` | `6f804f0c` |
| `multi-agent-coordinator` | VoltAgent (MIT) | `categories/09-meta-orchestration/multi-agent-coordinator.md` | `6f804f0c` |
| `webapp-testing` (skill) | [anthropics/skills](https://github.com/anthropics/skills) (Anthropic License) | `skills/webapp-testing/` (директория целиком) | `5128e186` |

**Почему `security-auditor`, не `security-reviewer`:** в VoltAgent файл
называется `security-auditor` — устанавливаем как есть, чтобы:
1. Не путать с `agent-teams:security-reviewer` (bug-level review кода)
2. Имя точнее отражает скоп — compliance audit (SOC2, ISO 27001, threat modeling)
Эти два агента **комплементарны**: один для review-on-PR, другой для
проектного аудита.

## Риски и митигации

| Риск | Митигация |
|---|---|
| Upstream может удалить/перенести файл | Pinning по commit SHA — сломается только обновление, не текущая установка |
| `webapp-testing` требует Python `playwright` | Скрипт проверяет наличие, подсказывает `pip install playwright && playwright install chromium` |
| Конфликт имени `security-reviewer` ↔ `agent-teams:security-reviewer` | Снят переименованием на `security-auditor` |
| Глобальные файлы видны в других проектах | Это и есть желаемое поведение (cross-project reuse) |

## Чек-лист реализации

- [ ] Загрузить 4 артефакта в `~/.claude/` по pinned SHA
- [ ] Создать `scripts/install-claude-tools.sh` (идемпотентный, с пинами)
- [ ] Сделать скрипт исполняемым
- [ ] Создать `.claude/EXTERNAL-TOOLS.md` (источники, лицензии, инструкция)
- [ ] Добавить таргет `install-claude-tools` в `Makefile`
- [ ] Сослаться на `.claude/EXTERNAL-TOOLS.md` из `CLAUDE.md` (раздел «Навигация»)
- [ ] Сослаться из `.claude/README.md` и `scripts/README.md`
- [ ] Прогнать скрипт повторно — убедиться в идемпотентности
- [ ] Проверить, что агенты видны: `ls ~/.claude/agents/`

## Метрика успеха

После завершения:
1. `ls ~/.claude/agents/` показывает 3 новых файла
2. `ls ~/.claude/skills/webapp-testing/` показывает SKILL.md + examples/ + scripts/
3. `make install-claude-tools` идемпотентен (повторный запуск не ломает)
4. Документация в `.claude/EXTERNAL-TOOLS.md` объясняет что/откуда/зачем/как
5. На новой машине: `git clone && make install-claude-tools` → все 4 артефакта стоят
