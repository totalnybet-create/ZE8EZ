#!/usr/bin/env python3
"""Lekka kontrola jakości statycznej strony ZE8ES bez zewnętrznych zależności."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.tags: Counter[str] = Counter()
        self.title_found = False
        self.description_found = False
        self.lang_found = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags[tag] += 1
        values = dict(attrs)
        if tag == "html" and values.get("lang"):
            self.lang_found = True
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"] or "")
        if tag == "meta" and values.get("name") == "description" and values.get("content"):
            self.description_found = True

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_data(self, data: str) -> None:
        if self.get_starttag_text() and data.strip():
            return


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data.strip()


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> None:
    if not INDEX.exists():
        fail("Brak index.html")

    source = INDEX.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(source)
    title_parser = TitleParser()
    title_parser.feed(source)

    if not parser.lang_found:
        fail("Brak atrybutu lang w elemencie html")
    if not title_parser.title:
        fail("Brak tytułu strony")
    if not parser.description_found:
        fail("Brak meta description")
    if parser.tags["h1"] != 1:
        fail(f"Strona powinna zawierać dokładnie jeden h1, znaleziono: {parser.tags['h1']}")

    duplicates = [item for item, count in Counter(parser.ids).items() if count > 1]
    if duplicates:
        fail(f"Powtarzające się identyfikatory: {', '.join(duplicates)}")

    known_ids = set(parser.ids)
    broken_anchors = sorted(
        href for href in parser.hrefs
        if href.startswith("#") and href != "#" and href[1:] not in known_ids
    )
    if broken_anchors:
        fail(f"Odnośniki do nieistniejących sekcji: {', '.join(broken_anchors)}")

    unsafe_links = []
    for href in parser.hrefs:
        parsed = urlparse(href)
        if parsed.scheme and parsed.scheme not in {"http", "https", "mailto", "tel"}:
            unsafe_links.append(href)
    if unsafe_links:
        fail(f"Niedozwolone schematy odnośników: {', '.join(unsafe_links)}")

    required = [ROOT / "README.md", ROOT / "404.html", ROOT / "robots.txt", ROOT / "sitemap.xml"]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        fail(f"Brak wymaganych plików: {', '.join(missing)}")

    print("OK: podstawowa kontrola HTML, SEO, identyfikatorów i odnośników zakończona powodzeniem.")


if __name__ == "__main__":
    main()
