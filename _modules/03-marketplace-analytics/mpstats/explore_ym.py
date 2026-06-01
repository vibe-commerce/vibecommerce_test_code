#!/usr/bin/env python3
"""Explore Yandex Market endpoints on MPStats API.

MPStats YM endpoints are not publicly documented. This script tests
common endpoint patterns to discover what's available.

Usage:
    uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/explore_ym.py
    uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/explore_ym.py --item 12345
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from client import create_client, MPStatsClient


# Candidate endpoints to probe (based on OZ/WB patterns)
PROBE_ENDPOINTS = [
    ("GET", "ym/get/categories", {}, "Дерево категорий"),
    ("GET", "ym/get/category/by_date", {"path": "Электроника", "d1": "2026-01-19", "d2": "2026-02-19"}, "Категория за период"),
    ("GET", "ym/get/category/sellers", {"path": "Электроника", "d1": "2026-01-19", "d2": "2026-02-19"}, "Продавцы категории"),
    ("GET", "ym/get/category/brands", {"path": "Электроника", "d1": "2026-01-19", "d2": "2026-02-19"}, "Бренды категории"),
]


def probe_endpoint(
    client: MPStatsClient, method: str, endpoint: str, params: dict, desc: str,
) -> dict:
    """Test a single endpoint and return result info."""
    print(f"  [{method}] /{endpoint} — {desc}...", end=" ", flush=True)
    try:
        result = client._request(method, endpoint, params=params, max_retries=1)
        if result is not None:
            rtype = type(result).__name__
            size = len(result) if isinstance(result, (list, dict)) else 0
            print(f"OK ({rtype}, {size} items)")
            return {"endpoint": endpoint, "status": "OK", "type": rtype, "size": size}
        else:
            print("NULL (404 or error)")
            return {"endpoint": endpoint, "status": "NULL"}
    except Exception as e:
        print(f"ERROR: {e}")
        return {"endpoint": endpoint, "status": "ERROR", "error": str(e)}


def probe_item(client: MPStatsClient, item_id: int) -> None:
    """Test item-level endpoints for a specific ID."""
    item_endpoints = [
        ("GET", f"ym/get/item/{item_id}", {}, "Base info"),
        ("GET", f"ym/get/item/{item_id}/summary", {}, "Summary"),
        ("GET", f"ym/get/item/{item_id}/by_date", {"d1": "2026-01-19", "d2": "2026-02-19"}, "By date"),
    ]
    print(f"\n--- Item endpoints (ID: {item_id}) ---")
    for method, endpoint, params, desc in item_endpoints:
        result = probe_endpoint(client, method, endpoint, params, desc)
        if result["status"] == "OK":
            data = client._request(method, endpoint, params=params, max_retries=1)
            print(f"    Preview: {json.dumps(data, ensure_ascii=False)[:200]}...")


def main() -> None:
    parser = argparse.ArgumentParser(description="Explore MPStats YM endpoints")
    parser.add_argument("--item", type=int, help="Test item endpoints with this ID")
    args = parser.parse_args()

    try:
        client = create_client()
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    print("=" * 50)
    print("  MPStats Yandex Market — Endpoint Explorer")
    print("=" * 50)
    print()

    with client:
        # General endpoints
        print("--- Category endpoints ---")
        results = []
        for method, endpoint, params, desc in PROBE_ENDPOINTS:
            r = probe_endpoint(client, method, endpoint, params, desc)
            results.append(r)

        # Item endpoints
        if args.item:
            probe_item(client, args.item)

        # Summary
        ok = [r for r in results if r["status"] == "OK"]
        print(f"\n{'=' * 50}")
        print(f"  Результат: {len(ok)}/{len(results)} эндпоинтов доступны")
        print(f"{'=' * 50}")

        if ok:
            print("\nРабочие эндпоинты:")
            for r in ok:
                print(f"  - /{r['endpoint']} ({r['type']}, {r['size']} items)")
        else:
            print("\nНи один YM-эндпоинт не ответил.")
            print("Возможные причины:")
            print("  1. MPStats ещё не поддерживает YM через API")
            print("  2. Нужен другой prefix (не /ym/)")
            print("  3. Нужен отдельный тариф для YM")


if __name__ == "__main__":
    main()
