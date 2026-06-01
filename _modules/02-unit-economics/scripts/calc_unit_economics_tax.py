"""Расчёт юнит-экономики SKU с учётом разных налоговых режимов.

Сравнение УСН 6% / УСН 15% / ОСНО для одной модельной продажи.
Без реальных клиентских данных.
"""
from calc_marketplace_tax import MarketplaceFees, SaleInputs, unit_economics


def compare_tax_regimes(sale: SaleInputs, fees: MarketplaceFees) -> dict[str, dict[str, float]]:
    """Сравнить чистую маржу при УСН 6% / УСН 15% / ОСНО."""
    return {
        "usn_6": unit_economics(sale, fees, "usn_6"),
        "usn_15": unit_economics(sale, fees, "usn_15"),
        "osno": unit_economics(sale, fees, "osno"),
    }


def print_comparison(comparison: dict[str, dict[str, float]]) -> None:
    print(f"{'Метрика':24s} {'УСН 6%':>10s} {'УСН 15%':>10s} {'ОСНО':>10s}")
    print("-" * 60)
    for metric in ("gross_profit", "tax", "net_profit"):
        row = [comparison[r][metric] for r in ("usn_6", "usn_15", "osno")]
        print(f"{metric:24s} {row[0]:10.2f} {row[1]:10.2f} {row[2]:10.2f}")
    print(f"{'net_margin_pct':24s} "
          f"{comparison['usn_6']['net_margin_pct']*100:9.2f}% "
          f"{comparison['usn_15']['net_margin_pct']*100:9.2f}% "
          f"{comparison['osno']['net_margin_pct']*100:9.2f}%")


if __name__ == "__main__":
    demo_sale = SaleInputs(
        price=2000, cogs=800, ads_share=0.10,
        return_rate=0.10, return_cost=80, storage_days=15,
    )
    demo_fees = MarketplaceFees(commission_pct=0.17, logistics_per_unit=45)
    comparison = compare_tax_regimes(demo_sale, demo_fees)
    print_comparison(comparison)
