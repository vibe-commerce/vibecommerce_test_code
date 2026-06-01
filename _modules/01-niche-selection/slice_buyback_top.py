"""slice_buyback_top.py — генерация FREE-справочника % выкупа по нишам (top-N).

FREE-версия = срез top-N ниш из полной обогащённой MPStats-выгрузки.
Полный справочник (100+ ниш) + методика расчёта — в `vibecommerce_vip_code`.

Источник по умолчанию: `OZON - выбор ниши - с выкупом.csv` (полная выгрузка,
~4400 ниш, разделитель `;`, десятичная запятая, BOM). На выходе — компактный
CSV top-N ниш, отсортированных по выбранной метрике.

Запуск:
    python3 slice_buyback_top.py                  # top-30 по выручке
    python3 slice_buyback_top.py --top 20 --by buyback
    python3 slice_buyback_top.py --input <file.csv> --output <out.csv>

# DEMO DATA — открытые MPStats данные по категориям. Не привязано к селлеру.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

HERE = Path(__file__).parent
DEFAULT_INPUT = HERE / "OZON - выбор ниши - с выкупом.csv"
DEFAULT_OUTPUT = HERE / "Сводка - выкуп top (FREE, generated).csv"

# Имена колонок источника ищутся по подстроке — формат MPStats может меняться.
COL_NICHE = "Название предмета"
COL_REVENUE = "Выручка, ₽"
COL_SALES = "Продажи, шт."
COL_BUYBACK = "Процент выкупа, %"


def _num(value: str | None) -> float:
    """Парсит русское число: '37 020 979' / '929,66' / '' → float."""
    if not value:
        return 0.0
    s = value.strip().replace("\xa0", "").replace(" ", "").replace(",", ".")
    if not s or s in {"-", "—"}:
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


def _find_col(fieldnames: list[str], needle: str) -> str | None:
    """Находит имя колонки по подстроке (устойчиво к BOM/кавычкам)."""
    for name in fieldnames:
        if needle in name:
            # для 'Выручка, ₽' исключаем 'Упущенная выручка' / 'Потенциал'
            if needle == COL_REVENUE and ("Упущен" in name or "Потенциал" in name):
                continue
            return name
    return None


def slice_top(input_path: Path, output_path: Path, top: int, by: str) -> None:
    with input_path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh, delimiter=";")
        fieldnames = reader.fieldnames or []
        c_niche = _find_col(fieldnames, COL_NICHE) or (fieldnames[0] if fieldnames else "")
        c_rev = _find_col(fieldnames, COL_REVENUE)
        c_sales = _find_col(fieldnames, COL_SALES)
        c_buy = _find_col(fieldnames, COL_BUYBACK)
        rows: list[dict[str, object]] = []
        for r in reader:
            niche = (r.get(c_niche) or "").strip().strip('"')
            if not niche:
                continue
            rows.append({
                "niche": niche,
                "revenue": _num(r.get(c_rev)) if c_rev else 0.0,
                "sales": _num(r.get(c_sales)) if c_sales else 0.0,
                "buyback": _num(r.get(c_buy)) if c_buy else 0.0,
            })

    key = by if by in {"revenue", "buyback", "sales"} else "revenue"
    # для выкупа берём только ниши с продажами (иначе % — шум)
    if key == "buyback":
        rows = [r for r in rows if float(r["sales"]) > 0]
    rows.sort(key=lambda r: float(r[key]), reverse=True)
    sliced = rows[:top]

    with output_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh, delimiter=";")
        writer.writerow(["№", "Ниша", "Выручка, ₽", "Продажи, шт.", "Процент выкупа, %"])
        for i, r in enumerate(sliced, start=1):
            writer.writerow([
                i, r["niche"],
                f"{float(r['revenue']):.0f}", f"{float(r['sales']):.0f}",
                f"{float(r['buyback']):.1f}".replace(".", ","),
            ])

    print(f"✅ FREE-срез: top-{top} ниш по '{by}' → {output_path.name}")
    print(f"   источник: {input_path.name} ({len(rows)} ниш всего)")
    print("   📈 Полный справочник (100+ ниш) + методика — в vibecommerce_vip_code")


def main() -> None:
    p = argparse.ArgumentParser(description="FREE-срез справочника % выкупа по нишам (top-N)")
    p.add_argument("--top", type=int, default=30, help="сколько ниш в срезе (по умолчанию 30)")
    p.add_argument("--by", choices=["revenue", "buyback", "sales"], default="revenue",
                   help="метрика сортировки (по умолчанию revenue)")
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = p.parse_args()
    if not args.input.exists():
        raise SystemExit(f"❌ Источник не найден: {args.input}")
    slice_top(args.input, args.output, args.top, args.by)


if __name__ == "__main__":
    main()
