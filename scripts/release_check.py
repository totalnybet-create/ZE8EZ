#!/usr/bin/env python3
"""Sprawdza spójność konfiguracji rozwojowej lub produkcyjnej ZE8ES."""

from __future__ import annotations

import re
from pathlib import Path

from configure_release import build_index, build_robots, build_sitemap, normalize_base_url

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> None:
    expected = "https://example.com/project/"
    if normalize_base_url("https://example.com/project") != expected:
        fail("Normalizacja adresu produkcyjnego działa niepoprawnie")

    sample = (
        '<head>\n'
        '  <meta name="robots" content="index,follow">\n'
        '  <meta property="og:description" content="Opis">\n'
        '</head>'
    )
    blocked = build_index(sample, expected)
    enabled = build_index(sample, expected, enable_indexing=True)

    for configured in (blocked, enabled):
        if f'<link rel="canonical" href="{expected}">' not in configured:
            fail("Konfigurator nie dodaje canonical")
        if f'<meta property="og:url" content="{expected}">' not in configured:
            fail("Konfigurator nie dodaje og:url")

    if 'content="noindex,nofollow"' not in blocked:
        fail("Konfigurator powinien domyślnie blokować indeksowanie")
    if 'content="index,follow"' not in enabled:
        fail("Jawna flaga nie włącza indeksowania")

    blocked_robots = build_robots(expected)
    blocked_sitemap = build_sitemap(expected)
    if "Disallow: /" not in blocked_robots or "Sitemap:" in blocked_robots:
        fail("Domyślna konfiguracja robots.txt nie blokuje indeksowania")
    if "<loc>" in blocked_sitemap:
        fail("Domyślna mapa witryny nie powinna publikować adresów")

    enabled_robots = build_robots(expected, enable_indexing=True)
    enabled_sitemap = build_sitemap(expected, enable_indexing=True)
    if "Allow: /" not in enabled_robots or f"Sitemap: {expected}sitemap.xml" not in enabled_robots:
        fail("Jawna flaga nie konfiguruje robots.txt")
    if f"<loc>{expected}</loc>" not in enabled_sitemap:
        fail("Jawna flaga nie konfiguruje sitemap.xml")

    index = (ROOT / "index.html").read_text(encoding="utf-8")
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    privacy = (ROOT / "privacy.html").read_text(encoding="utf-8")

    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', index)
    og_url_match = re.search(r'<meta\s+property="og:url"\s+content="([^"]+)"', index)

    if canonical_match:
        base_url = canonical_match.group(1)
        if not base_url.startswith("https://"):
            fail("Canonical produkcyjny nie używa HTTPS")
        if not og_url_match or og_url_match.group(1) != base_url:
            fail("og:url nie jest zgodny z canonical")
    elif og_url_match:
        fail("Wersja bez canonical zawiera og:url")

    indexing_enabled = "Allow: /" in robots
    if indexing_enabled:
        if not canonical_match:
            fail("Indeksowanie wymaga canonical")
        base_url = canonical_match.group(1)
        if f"Sitemap: {base_url}sitemap.xml" not in robots:
            fail("robots.txt nie jest zgodny z adresem produkcyjnym")
        if f"<loc>{base_url}</loc>" not in sitemap:
            fail("sitemap.xml nie jest zgodna z adresem produkcyjnym")
    else:
        if "Disallow: /" not in robots:
            fail("Przy wyłączonym indeksowaniu robots.txt powinien zawierać Disallow: /")
        if "<loc>" in sitemap:
            fail("Przy wyłączonym indeksowaniu sitemap.xml nie może publikować adresów")

    if 'content="noindex,nofollow"' not in privacy:
        fail("Robocza polityka prywatności musi pozostać poza indeksem")

    print("OK: stan wydania, robots, sitemap, canonical i dokument prywatności są spójne.")


if __name__ == "__main__":
    main()
