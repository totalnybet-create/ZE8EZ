#!/usr/bin/env python3
"""Konfiguruje potwierdzony publiczny adres ZE8ES w plikach SEO."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
ROBOTS = ROOT / "robots.txt"
SITEMAP = ROOT / "sitemap.xml"


def normalize_base_url(value: str) -> str:
    parsed = urlparse(value.strip())
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("Adres produkcyjny musi być pełnym adresem HTTPS.")
    if parsed.query or parsed.fragment:
        raise ValueError("Adres bazowy nie może zawierać parametrów ani fragmentu.")
    path = parsed.path.rstrip("/")
    return f"https://{parsed.netloc}{path}/"


def remove_existing_seo_urls(source: str) -> str:
    patterns = (
        r"\n\s*<link\s+rel=[\"']canonical[\"'][^>]*>",
        r"\n\s*<meta\s+property=[\"']og:url[\"'][^>]*>",
    )
    for pattern in patterns:
        source = re.sub(pattern, "", source, flags=re.IGNORECASE)
    return source


def build_index(source: str, base_url: str) -> str:
    source = remove_existing_seo_urls(source)
    tags = (
        f'  <link rel="canonical" href="{base_url}">\n'
        f'  <meta property="og:url" content="{base_url}">\n'
    )
    marker = '  <meta property="og:description"'
    position = source.find(marker)
    if position == -1:
        raise ValueError("Nie znaleziono miejsca na metadane SEO w index.html.")
    line_end = source.find("\n", position)
    return source[: line_end + 1] + tags + source[line_end + 1 :]


def build_robots(base_url: str) -> str:
    return (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {base_url}sitemap.xml\n"
    )


def build_sitemap(base_url: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "  <url>\n"
        f"    <loc>{base_url}</loc>\n"
        "    <changefreq>weekly</changefreq>\n"
        "    <priority>1.0</priority>\n"
        "  </url>\n"
        "</urlset>\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url", help="Potwierdzony publiczny adres HTTPS, np. https://example.com/")
    parser.add_argument("--dry-run", action="store_true", help="Sprawdź wynik bez zapisywania plików.")
    args = parser.parse_args()

    base_url = normalize_base_url(args.base_url)
    index_content = build_index(INDEX.read_text(encoding="utf-8"), base_url)
    robots_content = build_robots(base_url)
    sitemap_content = build_sitemap(base_url)

    if args.dry_run:
        print(f"OK: konfiguracja dla {base_url} jest poprawna. Pliki nie zostały zmienione.")
        return

    INDEX.write_text(index_content, encoding="utf-8")
    ROBOTS.write_text(robots_content, encoding="utf-8")
    SITEMAP.write_text(sitemap_content, encoding="utf-8")
    print(f"OK: skonfigurowano publiczny adres {base_url}")


if __name__ == "__main__":
    main()
