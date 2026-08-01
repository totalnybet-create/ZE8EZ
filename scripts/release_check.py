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

    sample = '<head>\n  <meta property="og:description" content="Opis">\n</head>'
    configured = build_index(sample, expected)
    if f'<link rel="canonical" href="{expected}">' not in configured:
        fail("Konfigurator nie dodaje canonical")
    if f'<meta property="og:url" content="{expected}">' not in configured:
        fail("Konfigurator nie dodaje og:url")
    if expected not in build_robots(expected) or expected not in build_sitemap(expected):
        fail("Konfigurator nie używa jednego adresu w robots i sitemap")

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
        if "Allow: /" not in robots or f"Sitemap: {base_url}sitemap.xml" not in robots:
            fail("robots.txt nie jest zgodny z adresem produkcyjnym")
        if f"<loc>{base_url}</loc>" not in sitemap:
            fail("sitemap.xml nie jest zgodna z adresem produkcyjnym")
    else:
        if og_url_match:
            fail("Wersja rozwojowa zawiera og:url bez canonical")
        if "Disallow: /" not in robots:
            fail("Wersja rozwojowa powinna blokować indeksowanie")
        if "<loc>" in sitemap:
            fail("Wersja rozwojowa nie może zawierać niepotwierdzonego adresu sitemap")

    if 'content="noindex,nofollow"' not in privacy:
        fail("Robocza polityka prywatności musi pozostać poza indeksem")

    print("OK: stan wydania, robots, sitemap, canonical i dokument prywatności są spójne.")


if __name__ == "__main__":
    main()
