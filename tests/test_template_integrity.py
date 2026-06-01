"""Регрессионный контур целостности шаблона.

Ловит дефекты, найденные QA-прогоном 2026-06-01 (план:
backlog/plans/2026-06-01-fix-template-integrity.md), чтобы они не вернулись:
валидность install-конфига, синхрон версий, отсутствие личных путей,
парсимость всех конфигов, резолв локальных Markdown-ссылок.
"""

import ast
import json
import re
import subprocess
import tomllib
import urllib.parse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# Бинарные/не-текстовые расширения — пропускаем при сканах содержимого.
BINARY_SUFFIXES = {".xlsx", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip"}

PEP508_NAME = re.compile(r"^[A-Za-z0-9]([A-Za-z0-9._-]*[A-Za-z0-9])?$")


def _tracked_files() -> list[Path]:
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    return [ROOT / line for line in out.stdout.splitlines() if line]


def _text_files() -> list[Path]:
    files = []
    for f in _tracked_files():
        if f.suffix.lower() in BINARY_SUFFIXES or not f.is_file():
            continue
        try:
            f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        files.append(f)
    return files


def test_pyproject_name_is_valid_pep508():
    """name = "{project}" ломал uv/pip install — не должно повториться."""
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    name = data["project"]["name"]
    assert "{" not in name and "}" not in name, f"placeholder в name: {name!r}"
    assert PEP508_NAME.match(name), f"невалидное PEP 508 имя: {name!r}"


def test_version_in_sync():
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    version_file = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert data["project"]["version"] == version_file, (
        f"pyproject={data['project']['version']} != VERSION={version_file}"
    )


def test_no_personal_absolute_paths():
    """Принцип №0 — ни одного личного абсолютного пути в tracked-файлах."""
    offenders = [
        str(f.relative_to(ROOT))
        for f in _text_files()
        if "/Users/vadimbakanov" in f.read_text(encoding="utf-8") and f.name != "test_template_integrity.py"
    ]
    assert not offenders, f"личные пути найдены в: {offenders}"


def test_all_python_parses_under_311():
    bad = []
    for f in _tracked_files():
        if f.suffix != ".py":
            continue
        try:
            ast.parse(f.read_text(encoding="utf-8"), filename=str(f), feature_version=(3, 11))
        except SyntaxError as e:
            bad.append(f"{f.relative_to(ROOT)}: {e}")
    assert not bad, bad


def test_all_configs_parse():
    """JSON/YAML/TOML конфиги валидны (ловит дефект generated TOML из cross-agent)."""
    errors = []
    for f in _tracked_files():
        if not f.is_file():
            continue
        try:
            if f.suffix == ".json":
                json.loads(f.read_text(encoding="utf-8"))
            elif f.suffix in {".yaml", ".yml"}:
                yaml.safe_load(f.read_text(encoding="utf-8"))
            elif f.suffix == ".toml" or f.name.endswith(".toml.template"):
                tomllib.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, yaml.YAMLError, tomllib.TOMLDecodeError) as e:
            errors.append(f"{f.relative_to(ROOT)}: {e}")
    assert not errors, errors


def test_tests_directory_is_nonempty():
    """make test не должен давать ложноположительный «0 тестов»."""
    test_files = list((ROOT / "tests").glob("test_*.py"))
    assert len(test_files) >= 1


# --- Локальный link-check для навигационных Markdown-документов ---------------

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _is_checkable_link(target: str) -> bool:
    if target.startswith(("http://", "https://", "mailto:", "#", "file://", "<")):
        return False
    if "{" in target or "}" in target or "*" in target:
        return False  # шаблонные placeholders
    return True


def test_local_markdown_links_resolve():
    """Относительные ссылки в навигационных доках указывают на существующие пути."""
    nav_docs = [
        ROOT / "README.md",
        ROOT / "CLAUDE.md",
        ROOT / "ROADMAP.md",
        ROOT / "AGENDA.md",
        ROOT / "FACTS.md",
        *(ROOT.glob("*/README.md")),
        *(ROOT.glob("_modules/*/README.md")),
    ]
    broken = []
    for doc in nav_docs:
        if not doc.exists():
            continue
        for m in LINK_RE.finditer(doc.read_text(encoding="utf-8")):
            target = m.group(1).split("#")[0].strip()
            if not target or not _is_checkable_link(target):
                continue
            # %20 и прочая URL-кодировка путей (пробелы в именах файлов)
            target = urllib.parse.unquote(target)
            resolved = (doc.parent / target).resolve()
            if not resolved.exists():
                broken.append(f"{doc.relative_to(ROOT)} -> {target}")
    assert not broken, "битые локальные ссылки:\n" + "\n".join(broken)
