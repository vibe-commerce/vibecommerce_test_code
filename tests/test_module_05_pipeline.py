"""Smoke-тест pipeline модуля 05 (ads-optimization).

Запускает generate-sales → generate-ads → ABCDX в КОПИИ модуля (tmp_path),
чтобы не менять tracked .xlsx в data-demo/. Проверяет, что цепочка сходится
на одной папке и tracked-данные остаются нетронутыми.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "_modules" / "05-ads-optimization"

pytest.importorskip("pandas")
pytest.importorskip("numpy")
pytest.importorskip("openpyxl")


def _run(script: Path) -> None:
    res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert res.returncode == 0, f"{script.name} упал:\n{res.stderr}"


def test_pipeline_generates_into_data_demo(tmp_path):
    dst = tmp_path / "05-ads-optimization"
    shutil.copytree(MODULE, dst)
    data_demo = dst / "data-demo"
    for x in data_demo.glob("*.xlsx"):
        x.unlink()  # докажем, что генераторы воссоздают данные с нуля

    scripts = dst / "scripts"
    _run(scripts / "generate_sales_data.py")
    _run(scripts / "generate_ads_data.py")
    _run(scripts / "abcdx_analysis.py")

    assert (data_demo / "sales_data_v1.0.xlsx").exists()
    assert (data_demo / "ads_data_v1.0.xlsx").exists()
    assert (data_demo / "ads_data_v2.0.xlsx").exists()  # выход ABCDX


def test_tracked_demo_data_untouched():
    """После любого прогона tracked data-demo не должна иметь git-diff."""
    res = subprocess.run(
        ["git", "status", "--porcelain", "_modules/05-ads-optimization/data-demo"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    # Игнорируем untracked-файлы (??) — они не являются модификацией tracked
    # данных (напр. новый README). Ловим только изменения/удаления .xlsx.
    dirty = [ln for ln in res.stdout.splitlines() if ln and not ln.startswith("??")]
    assert not dirty, "tracked data-demo изменена:\n" + "\n".join(dirty)


@pytest.mark.slow
def test_funnel_runs(tmp_path, monkeypatch):
    pytest.importorskip("matplotlib")
    monkeypatch.setenv("MPLBACKEND", "Agg")
    dst = tmp_path / "05-ads-optimization"
    shutil.copytree(MODULE, dst)
    scripts = dst / "scripts"
    # funnel читает ads_data_v2.0 (выход ABCDX) + sales_data_v1.0 — нужна вся цепочка
    for x in (dst / "data-demo").glob("*.xlsx"):
        x.unlink()
    _run(scripts / "generate_sales_data.py")
    _run(scripts / "generate_ads_data.py")
    _run(scripts / "abcdx_analysis.py")
    _run(scripts / "funnel_analysis.py")
    out = dst / "data-demo" / "analysis_output"
    assert (out / "funnel_report.xlsx").exists()
    assert list(out.glob("*.png")), "funnel не сгенерировал графики"
