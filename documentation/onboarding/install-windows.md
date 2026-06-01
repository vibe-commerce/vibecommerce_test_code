# Установка окружения на Windows

Last Updated: 2026-05-29

> **Рекомендация:** работать через **WSL2** (Ubuntu 22.04+). Это даст
> Linux-окружение поверх Windows и снимет 90% проблем с путями/правами.
> Альтернатива — Git Bash + native Python, но больше нюансов.

## Вариант A — WSL2 (рекомендуется)

### Шаг 1 — Установка WSL2

```powershell
# В PowerShell от админа
wsl --install -d Ubuntu-22.04
# Перезагрузка, создание пользователя
```

### Шаг 2 — Внутри WSL Ubuntu

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3.11 python3.11-venv python3-pip jq

# uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh -y
```

### Шаг 3 — VS Code + WSL extension

Установи VS Code на Windows, добавь extension `WSL` (Microsoft). Открой
свой репо через `Open Folder in WSL`.

## Вариант B — Native Windows (без WSL)

### Шаг 1 — Git Bash + Python

1. Git for Windows: https://git-scm.com/download/win (включает Git Bash)
2. Python 3.11+: https://python.org/downloads/windows/ (галочка «Add to PATH»)
3. uv: `pip install uv`

### Шаг 2 — Зависимости в Git Bash

```bash
cd my-seller-project
make install  # или uv sync
```

⚠️ Проблемы native Windows:
- Кодировки путей с кириллицей (`PRJ_ВЫБОР_НИШИ/` мигрировано в `_modules/01-niche-selection/`, новых таких путей нет, но осторожно)
- Конец строк: настрой `git config core.autocrlf true`
- Permissions: запускай Git Bash от обычного пользователя, не админа

### Шаг 3 — GitHub CLI

Скачай с https://cli.github.com/

```bash
gh auth login
```

## Шаг 4 — Claude Code

VS Code Extension работает в обоих вариантах (WSL и native).
Установи `Claude Code` extension из Marketplace.

## Шаг 5 — Проверка

```bash
python --version    # 3.11+
uv --version
git --version
gh --version
```

## Troubleshooting (Windows)

### `make: not found`
```bash
# WSL: sudo apt install make
# Native: установи Make for Windows или используй Git Bash + ручные команды:
uv sync
```

### Long paths error
```powershell
# В PowerShell от админа:
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

### Кодировка cmd / PowerShell ломает кириллицу
Используй Git Bash или WSL terminal вместо cmd.

## Связанные

- Установка на macOS: [`install-macos.md`](install-macos.md)
- Quickstart форка: [`quickstart-fork.md`](quickstart-fork.md)
