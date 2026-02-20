#!/usr/bin/env python3
"""Check MPStats API limits and verify that the API key works.

Usage:
    uv run --with httpx,python-dotenv PRJ_ANALYTICS/mpstats/check_limit.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add parent dir so we can import client
sys.path.insert(0, str(Path(__file__).parent))

from client import create_client


def main() -> None:
    try:
        client = create_client()
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    print("Проверка подключения к MPStats API...")
    print()

    with client:
        data = client.get_api_limit()

    if data is None:
        print("ERROR: Не удалось получить ответ от API.")
        print("Проверьте:")
        print("  1. Правильность MPSTATS_API_KEY в .env")
        print("  2. Доступность https://mpstats.io/api")
        sys.exit(1)

    print("API подключение: OK")
    print()
    print("--- Лимиты API ---")
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
