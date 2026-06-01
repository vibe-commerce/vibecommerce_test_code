# Установка окружения на macOS

Last Updated: 2026-05-29

## Что нужно

| Инструмент | Зачем | Команда |
|------------|-------|---------|
| Homebrew | Менеджер пакетов | https://brew.sh |
| Git | Версионирование | `brew install git` |
| Python 3.11+ | Скрипты модулей | `brew install python@3.11` |
| uv | Быстрый Python deps | `brew install uv` |
| GitHub CLI | Работа с GitHub | `brew install gh` |
| Claude Code | AI-агент | https://claude.com/claude-code |

## Шаг 1 — Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Шаг 2 — Базовые инструменты

```bash
brew install git python@3.11 uv gh jq
```

## Шаг 3 — Claude Code (опционально)

Скачай и установи с https://claude.com/claude-code или VS Code Extension.

## Шаг 4 — Установка зависимостей репо

```bash
cd my-seller-project
make install
```

Это запустит `uv sync` (или `pip install -e .`), создаст `.venv`.

## Шаг 5 — GitHub Auth

```bash
gh auth login
# Выбери GitHub.com, HTTPS, login with browser
gh auth status  # проверка
```

Если работаешь с организацией `vibe-commerce`:
```bash
gh auth switch --user vibe-commerce
```

## Шаг 6 — Проверка

```bash
python --version    # 3.11+
uv --version
git --version
gh --version
```

Готово. Дальше → [`quickstart-fork.md`](quickstart-fork.md) шаг 3.

## Troubleshooting

### `command not found: brew`
Добавь brew в PATH:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

### `python` указывает на 2.7
```bash
echo 'export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
```

### Permission denied при `make install`
Проверь, что ты в правильной папке (`pwd`). Не `sudo make install`.

## Связанные

- Установка на Windows: [`install-windows.md`](install-windows.md)
- Quickstart форка: [`quickstart-fork.md`](quickstart-fork.md)
