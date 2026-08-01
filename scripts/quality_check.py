#!/usr/bin/env python3
"""Lekka kontrola jakości statycznej strony ZE8ES bez zewnętrznych zależności."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.sources: list[str] = []
        self.stylesheets: list[str] = []
        self.tags: Counter[str] = Counter()
        self.description_found = False
        self.lang_found = False
        self.inline_style_blocks = 0
        self.inline_script_blocks = 0
        self.images_without_alt: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags[tag] += 1
        values = dict(attrs)

        if tag == "html" and values.get("lang"):
            self.lang_found = True
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"] or "")
        if tag == "script":
            if values.get("src"):
                self.sources.append(values["src"] or "")
            else:
                self.inline_script_blocks += 1
        if tag == "link" and values.get("href"):
            href = values["href"] or ""
            self.sources.append(href)
            if values.get("rel") == "stylesheet":
                self.stylesheets.append(href)
        if tag == "img":
            src = values.get("src") or "<brak src>"
            self.sources.append(src)
            if "alt" not in values:
                self.images_without_alt.append(src)
        if tag == "style":
            self.inline_style_blocks += 1
        if tag == "meta" and values.get("name") == "description" and values.get("content"):
            self.description_found = True

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


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


def is_local_reference(value: str) -> bool:
    parsed = urlparse(value)
    return not parsed.scheme and not value.startswith(("#", "//", "data:"))


def css_file_references(path: Path) -> list[Path]:
    source = path.read_text(encoding="utf-8")
    references: list[Path] = []
    for raw_value in re.findall(r"url\(([^)]+)\)", source):
        value = raw_value.strip().strip("\"'")
        if not is_local_reference(value):
            continue
        clean_value = value.split("?", 1)[0].split("#", 1)[0]
        if clean_value:
            references.append((path.parent / clean_value).resolve())
    return references


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
    if parser.tags["main"] != 1:
        fail(f"Strona powinna zawierać dokładnie jeden element main, znaleziono: {parser.tags['main']}")
    if not parser.stylesheets:
        fail("Brak zewnętrznego arkusza stylów")
    if not any(item.endswith(".js") for item in parser.sources):
        fail("Brak zewnętrznego pliku JavaScript")
    if parser.inline_style_blocks:
        fail("Style powinny znajdować się w osobnym pliku CSS")
    if parser.inline_script_blocks:
        fail("Skrypty powinny znajdować się w osobnym pliku JavaScript")
    if parser.images_without_alt:
        fail(f"Obrazy bez atrybutu alt: {', '.join(parser.images_without_alt)}")

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

    local_references = [value.split("?", 1)[0].split("#", 1)[0] for value in parser.hrefs + parser.sources if is_local_reference(value)]
    missing_references = sorted({value for value in local_references if value and not (ROOT / value).exists()})
    if missing_references:
        fail(f"Odnośniki do brakujących plików: {', '.join(missing_references)}")

    required = [
        ROOT / "README.md",
        ROOT / "404.html",
        ROOT / "robots.txt",
        ROOT / "sitemap.xml",
        ROOT / "assets/styles.css",
        ROOT / "assets/visual-upgrades.css",
        ROOT / "assets/script.js",
        ROOT / "assets/logo-mark.svg",
        ROOT / "assets/hero-visual.svg",
        ROOT / "assets/project-local.svg",
        ROOT / "assets/project-service.svg",
        ROOT / "assets/project-store.svg",
        ROOT / "docs/IMPLEMENTATION_PLAN.md",
        ROOT / "docs/STATUS.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        fail(f"Brak wymaganych plików: {', '.join(missing)}")

    css_files = [ROOT / "assets/styles.css", ROOT / "assets/visual-upgrades.css"]
    missing_css_references = []
    for css_file in css_files:
        missing_css_references.extend(
            str(reference.relative_to(ROOT))
            for reference in css_file_references(css_file)
            if ROOT in reference.parents and not reference.exists()
        )
    if missing_css_references:
        fail(f"CSS odwołuje się do brakujących plików: {', '.join(sorted(set(missing_css_references)))}")

    svg_files = [path for path in required if path.suffix == ".svg"]
    for svg_file in svg_files:
        try:
            ElementTree.parse(svg_file)
        except ElementTree.ParseError as error:
            fail(f"Niepoprawny plik SVG {svg_file.relative_to(ROOT)}: {error}")

    css = (ROOT / "assets/styles.css").read_text(encoding="utf-8")
    visual_css = (ROOT / "assets/visual-upgrades.css").read_text(encoding="utf-8")
    javascript = (ROOT / "assets/script.js").read_text(encoding="utf-8")
    if "@media (max-width:" not in css or "@media (max-width:" not in visual_css:
        fail("Brak reguł responsywnych w arkuszach CSS")
    if "prefers-reduced-motion" not in css or "prefers-reduced-motion" not in visual_css:
        fail("Brak obsługi ograniczenia animacji")
    if "IntersectionObserver" not in javascript:
        fail("Brak obserwatora sekcji i elementów interfejsu")
    if "visual-upgrades.css" not in javascript:
        fail("Dodatkowa warstwa stylów nie jest ładowana przez skrypt")
    if "pointerdown" not in javascript or "ArrowRight" not in javascript:
        fail("Karuzela nie ma pełnej obsługi dotyku i klawiatury")

    print("OK: HTML, SEO, odnośniki, grafiki SVG, CSS, responsywność i dostępność przeszły kontrolę.")


if __name__ == "__main__":
    main()
