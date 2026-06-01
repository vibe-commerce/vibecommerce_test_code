"""Расчёт налогов и комиссий маркетплейсов для одной продажи.

Универсальный калькулятор: WB / Ozon / Я.Маркет.
Используется в модуле 02 для построения юнит-экономики SKU.

Без реальных клиентских данных — только формулы.
"""
from dataclasses import dataclass
from typing import Literal

Marketplace = Literal["wb", "ozon", "ym"]
TaxRegime = Literal["usn_6", "usn_15", "osno"]


@dataclass(frozen=True)
class MarketplaceFees:
    """Параметры комиссий маркетплейса (заполняй из _knowledge/marketplaces/)."""
    commission_pct: float
    """Комиссия МП в % от цены (например, 0.17 для WB электроники)."""
    logistics_per_unit: float
    """Логистика МП за 1 единицу, руб."""
    acquiring_pct: float = 0.015
    """Эквайринг ~1.5%."""
    storage_per_day: float = 0.5
    """Хранение FBO, руб/день/единица."""


@dataclass(frozen=True)
class SaleInputs:
    price: float
    cogs: float
    ads_share: float
    """Доля рекламы от выручки (ДРР), например 0.10 = 10%."""
    return_rate: float
    """Доля возвратов, например 0.10 = 10%."""
    return_cost: float
    """Стоимость одного возврата, руб (логистика обратно + переупаковка)."""
    storage_days: float
    """Сколько дней SKU в среднем лежит на складе МП до продажи."""


def calc_marketplace_costs(sale: SaleInputs, fees: MarketplaceFees) -> dict[str, float]:
    """Расчёт всех расходов МП на 1 продажу."""
    commission = sale.price * fees.commission_pct
    logistics = fees.logistics_per_unit
    acquiring = sale.price * fees.acquiring_pct
    ads_cost = sale.price * sale.ads_share
    return_cost = sale.return_cost * sale.return_rate
    storage_cost = fees.storage_per_day * sale.storage_days
    total = commission + logistics + acquiring + ads_cost + return_cost + storage_cost
    return {
        "commission": commission,
        "logistics": logistics,
        "acquiring": acquiring,
        "ads": ads_cost,
        "returns": return_cost,
        "storage": storage_cost,
        "total_mp_costs": total,
    }


def calc_tax(revenue: float, gross_profit: float, regime: TaxRegime) -> float:
    """Расчёт налога по выбранному режиму (для ИП).

    - usn_6: 6% от выручки (revenue)
    - usn_15: 15% от прибыли (gross_profit, мин. 1% от выручки)
    - osno: 13% НДФЛ от прибыли + НДС 20% (упрощённо: считаем только НДФЛ)
    """
    if regime == "usn_6":
        return revenue * 0.06
    if regime == "usn_15":
        min_tax = revenue * 0.01
        return max(gross_profit * 0.15, min_tax)
    if regime == "osno":
        return gross_profit * 0.13
    raise ValueError(f"unknown tax regime: {regime}")


def unit_economics(
    sale: SaleInputs,
    fees: MarketplaceFees,
    regime: TaxRegime = "usn_6",
) -> dict[str, float]:
    """Полная юнит-экономика одной продажи: маржа после всех вычетов."""
    mp = calc_marketplace_costs(sale, fees)
    gross_profit = sale.price - sale.cogs - mp["total_mp_costs"]
    tax = calc_tax(sale.price, gross_profit, regime)
    net_profit = gross_profit - tax
    return {
        **mp,
        "revenue": sale.price,
        "cogs": sale.cogs,
        "gross_profit": gross_profit,
        "tax": tax,
        "net_profit": net_profit,
        "net_margin_pct": (net_profit / sale.price) if sale.price else 0.0,
    }


if __name__ == "__main__":
    # Пример: синтетика, не реальные цифры
    demo_sale = SaleInputs(
        price=2000,
        cogs=800,
        ads_share=0.10,
        return_rate=0.10,
        return_cost=80,
        storage_days=15,
    )
    demo_wb = MarketplaceFees(
        commission_pct=0.17,
        logistics_per_unit=45,
    )
    result = unit_economics(demo_sale, demo_wb, regime="usn_6")
    for k, v in result.items():
        if k.endswith("_pct"):
            print(f"{k:24s} {v*100:7.2f}%")
        else:
            print(f"{k:24s} {v:10.2f}")
