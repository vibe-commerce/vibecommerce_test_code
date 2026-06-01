"""Smoke-тесты CLI-утилит из scripts/.

convert_xlsx_to_md.py — проверяем round-trip xlsx → markdown-таблица.
md_to_html.py требует пакет `markdown` (не в core-deps) — отдельной командой:
    uv run --with markdown scripts/md_to_html.py <file.md>
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

openpyxl = pytest.importorskip("openpyxl")


def test_convert_xlsx_to_md(tmp_path):
    src = tmp_path / "sample.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["SKU", "Маржа"])
    ws.append(["A-1", 1500])
    wb.save(src)

    out = tmp_path / "out.md"
    res = subprocess.run(
        [sys.executable, str(SCRIPTS / "convert_xlsx_to_md.py"), str(src), "-o", str(out)],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, res.stderr
    md = out.read_text(encoding="utf-8")
    assert "| SKU | Маржа |" in md
    assert "| A-1 | 1500 |" in md
    assert "| --- | --- |" in md
