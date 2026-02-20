"""Sync HTTP client for MPStats API (Ozon, Wildberries, Yandex Market).

Usage:
    from client import MPStatsClient
    client = MPStatsClient(api_key="...")
    item = client.get_item(123456, platform="oz")
"""

from __future__ import annotations

import logging
import os
import time

import httpx

logger = logging.getLogger(__name__)

PLATFORMS = ("oz", "wb", "ym")


class MPStatsClient:
    """Sync client for MPStats API with retry and rate-limit handling.

    Supports Ozon (/oz/), Wildberries (/wb/), Yandex Market (/ym/).
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://mpstats.io/api",
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.Client | None = None

    def _get_client(self) -> httpx.Client:
        if self._client is None or self._client.is_closed:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers={
                    "X-Mpstats-TOKEN": self.api_key,
                    "Content-Type": "application/json",
                },
                timeout=self.timeout,
            )
        return self._client

    def close(self) -> None:
        if self._client and not self._client.is_closed:
            self._client.close()

    def __enter__(self) -> MPStatsClient:
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict | None = None,
        json_body: dict | None = None,
        max_retries: int = 3,
    ) -> dict | list | None:
        """Make HTTP request with retry and rate-limit handling."""
        client = self._get_client()
        backoff = 1.0

        for attempt in range(1, max_retries + 1):
            try:
                logger.debug("MPStats %s /%s (attempt %d)", method, endpoint, attempt)

                if method == "GET":
                    resp = client.get(f"/{endpoint}", params=params or {})
                else:
                    resp = client.post(f"/{endpoint}", params=params or {}, json=json_body or {})

                if resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", backoff))
                    logger.warning("MPStats 429, retry after %ds", retry_after)
                    time.sleep(retry_after)
                    backoff *= 2
                    continue

                if resp.status_code == 404:
                    logger.info("MPStats 404 for /%s", endpoint)
                    return None

                if resp.status_code >= 500:
                    logger.warning("MPStats %d for /%s (attempt %d)", resp.status_code, endpoint, attempt)
                    if attempt < max_retries:
                        time.sleep(backoff)
                        backoff *= 2
                        continue
                    return None

                resp.raise_for_status()
                return resp.json()

            except httpx.TimeoutException:
                logger.warning("MPStats timeout for /%s (attempt %d)", endpoint, attempt)
                if attempt < max_retries:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                return None

            except httpx.HTTPError as exc:
                logger.warning("MPStats error for /%s: %s (attempt %d)", endpoint, exc, attempt)
                if attempt < max_retries:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                return None

        return None

    @staticmethod
    def _check_platform(platform: str) -> None:
        if platform not in PLATFORMS:
            raise ValueError(f"Unknown platform '{platform}', expected one of {PLATFORMS}")

    # ── Item endpoints ─────────────────────────────────────────────

    def get_item(self, item_id: int, platform: str = "oz") -> dict | None:
        """Get base item info.

        OZ: GET /oz/get/item/{id}
        WB: GET /wb/get/item/{id}/summary
        YM: GET /ym/get/item/{id} (unverified)
        """
        self._check_platform(platform)
        if platform == "wb":
            return self._request("GET", f"wb/get/item/{item_id}/summary")
        return self._request("GET", f"{platform}/get/item/{item_id}")

    def get_item_by_date(
        self, item_id: int, d1: str, d2: str, platform: str = "oz",
    ) -> list | None:
        """GET /{platform}/get/item/{id}/by_date"""
        self._check_platform(platform)
        return self._request(
            "GET", f"{platform}/get/item/{item_id}/by_date",
            params={"d1": d1, "d2": d2},
        )

    # WB-specific item endpoints

    def get_item_keywords(self, item_id: int) -> list | None:
        """GET /wb/get/item/{id}/keywords (WB only)."""
        return self._request("GET", f"wb/get/item/{item_id}/keywords")

    def get_item_seo(self, item_id: int) -> dict | None:
        """GET /wb/get/item/{id}/seo (WB only)."""
        return self._request("GET", f"wb/get/item/{item_id}/seo")

    def get_item_by_size(self, item_id: int) -> list | None:
        """GET /wb/get/item/{id}/by_size (WB only)."""
        return self._request("GET", f"wb/get/item/{item_id}/by_size")

    # ── Category endpoints ─────────────────────────────────────────

    def get_category_by_date(
        self, path: str, d1: str, d2: str, platform: str = "oz",
    ) -> list | None:
        """GET /{platform}/get/category/by_date"""
        self._check_platform(platform)
        return self._request(
            "GET", f"{platform}/get/category/by_date",
            params={"path": path, "d1": d1, "d2": d2},
        )

    def get_category_products(
        self,
        path: str,
        d1: str,
        d2: str,
        platform: str = "oz",
        *,
        start_row: int = 0,
        end_row: int = 5000,
    ) -> dict | None:
        """POST /{platform}/get/category — product listing sorted by revenue."""
        self._check_platform(platform)
        return self._request(
            "POST",
            f"{platform}/get/category",
            params={"path": path, "d1": d1, "d2": d2},
            json_body={
                "startRow": start_row,
                "endRow": end_row,
                "filterModel": {},
                "sortModel": [{"colId": "revenue", "sort": "desc"}],
            },
        )

    def get_category_sellers(
        self, path: str, d1: str, d2: str, platform: str = "oz",
    ) -> list | None:
        """GET /{platform}/get/category/sellers"""
        self._check_platform(platform)
        return self._request(
            "GET", f"{platform}/get/category/sellers",
            params={"path": path, "d1": d1, "d2": d2},
        )

    def get_category_brands(
        self, path: str, d1: str, d2: str, platform: str = "oz",
    ) -> list | None:
        """GET /{platform}/get/category/brands"""
        self._check_platform(platform)
        return self._request(
            "GET", f"{platform}/get/category/brands",
            params={"path": path, "d1": d1, "d2": d2},
        )

    def get_category_subcategories(
        self, path: str, d1: str, d2: str, platform: str = "oz",
    ) -> list | None:
        """GET /{platform}/get/category/subcategories"""
        self._check_platform(platform)
        return self._request(
            "GET", f"{platform}/get/category/subcategories",
            params={"path": path, "d1": d1, "d2": d2},
        )

    def get_categories_tree(self, platform: str = "oz") -> list | None:
        """GET /{platform}/get/categories — full rubricator."""
        self._check_platform(platform)
        return self._request("GET", f"{platform}/get/categories")

    # WB-specific category endpoints

    def get_category_price_segmentation(
        self, path: str, d1: str, d2: str,
    ) -> list | None:
        """GET /wb/get/category/price_segmentation (WB only)."""
        return self._request(
            "GET", "wb/get/category/price_segmentation",
            params={"path": path, "d1": d1, "d2": d2},
        )

    # ── Brand endpoints ────────────────────────────────────────────

    def get_brand_products(
        self,
        brand: str,
        d1: str,
        d2: str,
        platform: str = "oz",
        *,
        start_row: int = 0,
        end_row: int = 100,
    ) -> dict | None:
        """POST /{platform}/get/brand — brand products sorted by revenue."""
        self._check_platform(platform)
        return self._request(
            "POST",
            f"{platform}/get/brand",
            params={"path": brand, "d1": d1, "d2": d2},
            json_body={
                "startRow": start_row,
                "endRow": end_row,
                "filterModel": {},
                "sortModel": [{"colId": "revenue", "sort": "desc"}],
            },
        )

    def get_brand_by_date(
        self, brand: str, d1: str, d2: str, platform: str = "oz",
    ) -> list | None:
        """GET /{platform}/get/brand/by_date"""
        self._check_platform(platform)
        return self._request(
            "GET", f"{platform}/get/brand/by_date",
            params={"path": brand, "d1": d1, "d2": d2},
        )

    # ── Seller endpoints ───────────────────────────────────────────

    def get_seller_products(
        self,
        seller: str,
        d1: str,
        d2: str,
        platform: str = "wb",
        *,
        start_row: int = 0,
        end_row: int = 100,
    ) -> dict | None:
        """POST /{platform}/get/seller — seller products sorted by revenue."""
        self._check_platform(platform)
        return self._request(
            "POST",
            f"{platform}/get/seller",
            params={"path": seller, "d1": d1, "d2": d2},
            json_body={
                "startRow": start_row,
                "endRow": end_row,
                "filterModel": {},
                "sortModel": [{"colId": "revenue", "sort": "desc"}],
            },
        )

    # ── API Limit ──────────────────────────────────────────────────

    def get_api_limit(self) -> dict | None:
        """GET /user/report_api_limit"""
        return self._request("GET", "user/report_api_limit")


def create_client() -> MPStatsClient:
    """Create MPStatsClient from .env file. Raises ValueError if key missing."""
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("MPSTATS_API_KEY")
    if not api_key:
        raise ValueError(
            "MPSTATS_API_KEY not found in environment. "
            "Add it to .env file (see .env.example)."
        )
    return MPStatsClient(api_key=api_key)
