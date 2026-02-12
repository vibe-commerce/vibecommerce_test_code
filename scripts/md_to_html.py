#!/usr/bin/env python3
"""Конвертация Markdown → HTML.

Использование:
    uv run --with markdown scripts/md_to_html.py отчёт.md
    uv run --with markdown scripts/md_to_html.py отчёт.md -o отчёт.html
"""

import argparse
import sys
from pathlib import Path

import markdown


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 800px; margin: 2em auto; padding: 0 1em; line-height: 1.6; color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
        th {{ background: #f5f5f5; font-weight: 600; }}
        tr:nth-child(even) {{ background: #fafafa; }}
        code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
        pre {{ background: #f0f0f0; padding: 1em; border-radius: 6px; overflow-x: auto; }}
        h1, h2, h3 {{ color: #1a1a1a; }}
    </style>
</head>
<body>
{content}
</body>
</html>"""


def md_to_html(filepath: str) -> str:
    text = Path(filepath).read_text(encoding="utf-8")
    title = Path(filepath).stem
    html_content = markdown.markdown(text, extensions=["tables", "fenced_code"])
    return HTML_TEMPLATE.format(title=title, content=html_content)


def main():
    parser = argparse.ArgumentParser(description="Markdown → HTML")
    parser.add_argument("file", help="Путь к .md файлу")
    parser.add_argument("-o", "--output", help="Выходной .html файл (по умолчанию — <имя>.html)")
    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"Файл не найден: {args.file}", file=sys.stderr)
        sys.exit(1)

    result = md_to_html(args.file)
    output = args.output or Path(args.file).with_suffix(".html").name

    Path(output).write_text(result, encoding="utf-8")
    print(f"Сохранено: {output}")


if __name__ == "__main__":
    main()
