# Внешние Claude Code инструменты (глобальные)

Last Updated: 2026-05-02

## Что это

Шаблон `EMPTY_code` ожидает, что часть **универсальных** Claude Code агентов
и скиллов установлены **глобально** в `~/.claude/`, а не лежат в проектном
`.claude/` каждого форка. Это позволяет:

- Переиспользовать одну установку во всех проектах на машине
- Не дублировать чужой код в каждом форке
- Получать обновления централизованно (одной правкой `install-claude-tools.sh`)

Чтобы шаблон оставался самодостаточным, в репозитории есть **bootstrap-скрипт**:
он ставит всё нужное по pinned commit SHA из upstream-репозиториев.

## Установка / переустановка

```bash
make install-claude-tools
# или напрямую:
./scripts/install-claude-tools.sh
```

Скрипт **идемпотентен** — можно гонять повторно. После установки
**перезапусти Claude Code**, чтобы он подхватил новых агентов и скиллов.

## Что установлено

### Субагенты — `~/.claude/agents/`

Источник: [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) (MIT license)
Pinned SHA: `6f804f0cfab22fb62668855aa3d62ee3a1453077`

| Агент | Модель | Назначение |
|---|---|---|
| `python-pro` | sonnet | Production-grade Python: type-safe, async, FastAPI/Django/Pandas, тесты с pytest |
| `security-auditor` | opus | Security/compliance аудит: SOC2, ISO 27001, HIPAA, PCI DSS, threat modeling |
| `multi-agent-coordinator` | opus | Оркестрация распределённых workflow с несколькими агентами, dependency graph, fault tolerance |

**Не путать `security-auditor` с `agent-teams:security-reviewer`:**
- `agent-teams:security-reviewer` — bug-level review кода (XSS, SQLi, auth bypass)
  внутри `/team-feature` пайплайна
- `security-auditor` (этот) — проектный compliance audit, не привязан к диффу

Они комплементарны.

### Скиллы — `~/.claude/skills/`

Источник: [anthropics/skills](https://github.com/anthropics/skills) (Anthropic License — см. `LICENSE.txt` в директории скилла)
Pinned SHA: `5128e1865d670f5d6c9cef000e6dfc4e951fb5b9`

| Скилл | Зависимости | Назначение |
|---|---|---|
| `webapp-testing` | Python `playwright` | Browser automation для локальных веб-приложений: скриншоты, проверка UI, console logs |

**Зависимость:**
```bash
python3 -m pip install --user playwright
python3 -m playwright install chromium
```
На Homebrew Python (PEP 668) добавить `--break-system-packages`:
```bash
python3 -m pip install --user --break-system-packages playwright
```

## Почему глобально, а не в проектный `.claude/`

Сравнивались три подхода:

1. **Vendored в проектный `.claude/`** — каждый форк EMPTY_code тащит копию;
   обновления ломают workflow; лицензионные `LICENSE.txt` плодятся.
2. **Только глобально без скрипта** — на новой машине забываешь, что нужно,
   шаблон не самодокументируем.
3. **Глобально + bootstrap-скрипт** ⭐ — выбран. Репо чистый, новая машина
   бутстрапится одной командой, источник истины — upstream + pinned SHA.

Подробное обоснование: [`backlog/briefs/2026-05-02-install-claude-tools.md`](../backlog/briefs/2026-05-02-install-claude-tools.md)

## Обновление до новой версии upstream

1. Открыть `scripts/install-claude-tools.sh`
2. Заменить `SHA_VOLT` или `SHA_ANTHRO` на новый коммит
3. `make install-claude-tools` — переставит файлы из новой версии
4. Закоммитить изменение скрипта (история обновлений видна в git log)

## На новой машине после `git clone`

```bash
git clone <repo-url> && cd <repo>
make install-claude-tools
# Перезапустить Claude Code
```

Готово — все 4 артефакта стоят, идентичные другим машинам (по SHA).

## Что НЕ ставится глобально

В проектном `.claude/agents/` и `.claude/skills/` остаются **специфичные
для шаблона EMPTY_code** агенты и скиллы (commit, deploy-dev, lawyer,
project-knowledge, и т.д.) — они едут с репо, потому что заточены под
конкретный workflow этого шаблона.

## Связанные документы

- Бриф плана установки: [`backlog/briefs/2026-05-02-install-claude-tools.md`](../backlog/briefs/2026-05-02-install-claude-tools.md)
- Скрипт установки: [`scripts/install-claude-tools.sh`](../scripts/install-claude-tools.sh)
- Глобальные skills/agents в Claude Code docs: <https://code.claude.com/docs/en/sub-agents>
