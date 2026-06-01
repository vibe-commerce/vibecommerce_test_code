"""Data models for MPStats API responses (Ozon, Wildberries, Yandex Market).

Platform-independent models with from_api() parsing for each marketplace.
"""

from __future__ import annotations

from dataclasses import dataclass, field


def _fmt(n: float | int) -> str:
    """Format number with space thousands separator."""
    if isinstance(n, float):
        if n == int(n):
            n = int(n)
        else:
            return f"{n:,.2f}".replace(",", " ")
    return f"{n:,}".replace(",", " ")


PLATFORM_NAMES = {"oz": "Ozon", "wb": "Wildberries", "ym": "Яндекс Маркет"}


# ── Item Summary ───────────────────────────────────────────────────


@dataclass
class ItemSummary:
    """Key fields from item API response. Works for OZ and WB."""

    platform: str
    id: int
    name: str
    brand: str
    seller: str
    seller_id: int | None
    category: str
    final_price: float
    price: float
    rating: float
    reviews_count: int
    balance: int
    # OZ-specific
    delivery_scheme: str = ""
    discount: int = 0
    # WB-specific
    pics_count: int = 0

    @classmethod
    def from_api(cls, data: dict, platform: str = "oz") -> ItemSummary:
        """Parse from MPStats API response."""
        if platform == "oz":
            return cls._from_oz(data)
        if platform == "wb":
            return cls._from_wb(data)
        return cls._from_generic(data, platform)

    @classmethod
    def _from_oz(cls, data: dict) -> ItemSummary:
        item = data.get("item", data)
        raw_rating = item.get("rating", 0) or 0
        return cls(
            platform="oz",
            id=item.get("id", 0),
            name=item.get("name", ""),
            brand=item.get("brand", ""),
            seller=item.get("seller", ""),
            seller_id=item.get("seller_id") or item.get("supplier_id"),
            category=item.get("category", ""),
            final_price=item.get("final_price", 0),
            price=item.get("price", 0),
            rating=raw_rating / 100 if raw_rating > 10 else raw_rating,
            reviews_count=item.get("comments", 0),
            balance=item.get("balance", 0),
            delivery_scheme=item.get("delivery_scheme", "FBO"),
            discount=item.get("discount", 0),
        )

    @classmethod
    def _from_wb(cls, data: dict) -> ItemSummary:
        item = data.get("item", data)
        raw_rating = item.get("rating", 0) or 0
        return cls(
            platform="wb",
            id=item.get("id", 0),
            name=item.get("name", ""),
            brand=item.get("brand", ""),
            seller=item.get("seller", "") or item.get("supplier", ""),
            seller_id=item.get("supplier_id"),
            category=item.get("category", ""),
            final_price=item.get("final_price", 0),
            price=item.get("price", 0),
            rating=raw_rating / 100 if raw_rating > 10 else raw_rating,
            reviews_count=item.get("feedbacks", 0) or item.get("comments", 0),
            balance=item.get("balance", 0),
            pics_count=item.get("pics", 0),
        )

    @classmethod
    def _from_generic(cls, data: dict, platform: str) -> ItemSummary:
        """Fallback parser for unknown platforms (YM etc)."""
        item = data.get("item", data)
        raw_rating = item.get("rating", 0) or 0
        return cls(
            platform=platform,
            id=item.get("id", 0),
            name=item.get("name", ""),
            brand=item.get("brand", ""),
            seller=item.get("seller", ""),
            seller_id=item.get("seller_id") or item.get("supplier_id"),
            category=item.get("category", ""),
            final_price=item.get("final_price", 0),
            price=item.get("price", 0),
            rating=raw_rating / 100 if raw_rating > 10 else raw_rating,
            reviews_count=item.get("comments", 0) or item.get("feedbacks", 0),
            balance=item.get("balance", 0),
        )

    def format(self) -> str:
        """Format as human-readable text."""
        mp = PLATFORM_NAMES.get(self.platform, self.platform)
        lines = [
            f"{'=' * 50}",
            f"  {self.name}",
            f"{'=' * 50}",
            f"Маркетплейс: {mp}",
            f"ID: {self.id}",
            f"Продавец: {self.seller}",
            f"Бренд: {self.brand}",
            f"Категория: {self.category}",
            "",
            "--- Цена ---",
            f"Текущая цена:    {_fmt(self.final_price)} руб.",
            f"Цена без скидки: {_fmt(self.price)} руб.",
        ]
        if self.discount:
            lines.append(f"Скидка:          {self.discount}%")

        lines.extend([
            "",
            "--- Рейтинг и отзывы ---",
            f"Рейтинг:  {self.rating:.1f} / 5.0",
            f"Отзывов:  {_fmt(self.reviews_count)}",
        ])

        lines.extend([
            "",
            "--- Остатки ---",
            f"Баланс: {_fmt(self.balance)} шт.",
        ])
        if self.delivery_scheme:
            lines.append(f"Схема:  {self.delivery_scheme}")

        return "\n".join(lines)


# ── Category Product ───────────────────────────────────────────────


@dataclass
class CategoryProduct:
    """Product from POST /{platform}/get/category response."""

    platform: str
    id: int
    name: str
    brand: str
    seller: str
    seller_id: int
    category: str
    final_price: float = 0.0
    sales: int = 0
    revenue: float = 0.0
    reviews_count: int = 0
    rating: float = 0.0
    position: int = 0
    balance: int = 0

    @classmethod
    def from_api(cls, data: dict, platform: str = "oz") -> CategoryProduct:
        return cls(
            platform=platform,
            id=data.get("id", 0),
            name=data.get("name", ""),
            brand=data.get("brand", ""),
            seller=data.get("seller", ""),
            seller_id=data.get("supplier_id", 0),
            category=data.get("category", ""),
            final_price=data.get("final_price", 0.0),
            sales=data.get("sales", 0),
            revenue=data.get("revenue", 0.0),
            reviews_count=data.get("comments", 0) or data.get("feedbacks", 0),
            rating=data.get("rating", 0.0),
            position=data.get("category_position", 0),
            balance=data.get("balance", 0),
        )


# ── Niche Context ──────────────────────────────────────────────────


@dataclass
class NicheContext:
    """Category-level market context built from by_date + sellers + brands."""

    platform: str
    category_name: str
    total_revenue: float
    total_sales: int
    avg_check: float
    sellers_count: int
    brands_count: int
    trend_pct: float
    trend_label: str  # "up", "down", "stable"

    def format(self) -> str:
        mp = PLATFORM_NAMES.get(self.platform, self.platform)
        trend_arrows = {"up": "+", "down": "-", "stable": "="}
        arrow = trend_arrows.get(self.trend_label, "?")
        return (
            f"\n--- Ниша: {self.category_name} ({mp}) ---\n"
            f"Выручка:    {_fmt(self.total_revenue)} руб.\n"
            f"Продажи:    {_fmt(self.total_sales)} шт.\n"
            f"Ср. чек:    {_fmt(self.avg_check)} руб.\n"
            f"Продавцов:  {self.sellers_count}\n"
            f"Брендов:    {self.brands_count}\n"
            f"Тренд:      [{arrow}] {self.trend_pct:+.1f}% ({self.trend_label})"
        )


# ── Category Metrics ───────────────────────────────────────────────


@dataclass
class CategoryMetrics:
    """Aggregated category metrics for analyze_category.py."""

    total_revenue: float = 0.0
    total_sales: int = 0
    avg_check: float = 0.0
    products_count: int = 0
    sellers_count: int = 0
    brands_count: int = 0
    revenue_trend_pct: float = 0.0
    revenue_trend: str = "stable"
    top5_sellers_revenue_pct: float = 0.0
    top5_brands_revenue_pct: float = 0.0
    top_sellers: list[dict] = field(default_factory=list)
    top_brands: list[dict] = field(default_factory=list)
    top_products: list[dict] = field(default_factory=list)

    def format(self, category_name: str, platform: str) -> str:
        mp = PLATFORM_NAMES.get(platform, platform)
        trend_arrows = {"up": "+", "down": "-", "stable": "="}
        arrow = trend_arrows.get(self.revenue_trend, "?")

        lines = [
            f"{'=' * 50}",
            f"  Категория: {category_name}",
            f"  Маркетплейс: {mp}",
            f"{'=' * 50}",
            "",
            "--- Объём рынка ---",
            f"Выручка:   {_fmt(self.total_revenue)} руб.",
            f"Продажи:   {_fmt(self.total_sales)} шт.",
            f"Ср. чек:   {_fmt(self.avg_check)} руб.",
            f"Тренд:     [{arrow}] {self.revenue_trend_pct:+.1f}%",
            "",
            "--- Участники ---",
            f"Товаров:    {_fmt(self.products_count)}",
            f"Продавцов:  {_fmt(self.sellers_count)}",
            f"Брендов:    {_fmt(self.brands_count)}",
            "",
            "--- Концентрация ---",
            f"Топ-5 продавцов: {self.top5_sellers_revenue_pct:.1f}% выручки",
            f"Топ-5 брендов:   {self.top5_brands_revenue_pct:.1f}% выручки",
        ]

        if self.top_sellers:
            lines.extend(["", "--- Топ-10 продавцов ---"])
            for i, s in enumerate(self.top_sellers[:10], 1):
                lines.append(
                    f"  {i:2d}. {s.get('name', '')[:35]:35s} "
                    f"{_fmt(s.get('revenue', 0)):>12s} руб. "
                    f"({_fmt(s.get('sales', 0))} шт.)"
                )

        if self.top_brands:
            lines.extend(["", "--- Топ-10 брендов ---"])
            for i, b in enumerate(self.top_brands[:10], 1):
                lines.append(
                    f"  {i:2d}. {b.get('name', '')[:35]:35s} "
                    f"{_fmt(b.get('revenue', 0)):>12s} руб."
                )

        if self.top_products:
            lines.extend(["", "--- Топ-10 товаров ---"])
            for i, p in enumerate(self.top_products[:10], 1):
                lines.append(
                    f"  {i:2d}. {p.get('name', '')[:45]:45s}\n"
                    f"      {_fmt(p.get('revenue', 0))} руб. | "
                    f"{_fmt(p.get('sales', 0))} шт. | "
                    f"{_fmt(p.get('final_price', 0))} руб."
                )

        return "\n".join(lines)
