#!/usr/bin/env python3
"""Lekka kontrola jakości statycznej strony ZE8ES bez zewnętrznych zależności."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree
import json
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
    for stylesheet in ("assets/visual-upgrades.css", "assets/responsive-fixes.css"):
        if stylesheet not in parser.stylesheets:
            fail(f"Arkusz {stylesheet} nie jest ładowany bezpośrednio w HTML")
    if not any(item.endswith(".js") for item in parser.sources):
        fail("Brak zewnętrznego pliku JavaScript")
    if parser.inline_style_blocks:
        fail("Style powinny znajdować się w osobnym pliku CSS")
    if parser.inline_script_blocks:
        fail("Skrypty powinny znajdować się w osobnym pliku JavaScript")
    if parser.images_without_alt:
        fail(f"Obrazy bez atrybutu alt: {', '.join(parser.images_without_alt)}")

    for required_fragment, label in (
        ('href="mailto:totalnybet@gmail.com', "bezpośredni kontakt e-mail"),
        ('data-business-detail', "potwierdzone dane kontaktowe"),
        ('href="privacy.html"', "odnośnik do polityki prywatności"),
    ):
        if required_fragment not in source:
            fail(f"Brak elementu kontaktowego: {label}")

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
        ROOT / "privacy.html",
        ROOT / "robots.txt",
        ROOT / "sitemap.xml",
        ROOT / "lighthouserc.cjs",
        ROOT / ".nojekyll",
        ROOT / "assets/styles.css",
        ROOT / "assets/visual-upgrades.css",
        ROOT / "assets/responsive-fixes.css",
        ROOT / "assets/script.js",
        ROOT / "assets/site-config.json",
        ROOT / "assets/logo-mark.svg",
        ROOT / "assets/hero-visual.svg",
        ROOT / "assets/project-local.svg",
        ROOT / "assets/project-antiques.svg",
        ROOT / "assets/project-store.svg",
        ROOT / "docs/IMPLEMENTATION_PLAN.md",
        ROOT / "docs/STATUS.md",
        ROOT / "docs/QA_MATRIX.md",
        ROOT / "docs/LEGAL_INPUTS.md",
        ROOT / "scripts/visual_check.mjs",
        ROOT / ".github/workflows/quality.yml",
        ROOT / ".github/workflows/lighthouse.yml",
        ROOT / ".github/workflows/visual-regression.yml",
        ROOT / ".github/workflows/deploy-pages.yml",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        fail(f"Brak wymaganych plików: {', '.join(missing)}")

    css_files = [
        ROOT / "assets/styles.css",
        ROOT / "assets/visual-upgrades.css",
        ROOT / "assets/responsive-fixes.css",
    ]
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

    try:
        site_config = json.loads((ROOT / "assets/site-config.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(f"Niepoprawny JSON konfiguracji strony: {error}")
    expected_contact = {
        "brandName": "ZE8ES",
        "brandType": "marka",
        "operatorName": "Marcin Siedlarek",
        "operatorType": "osoba prywatna",
        "publicEmail": "totalnybet@gmail.com",
        "serviceArea": "Cała Polska",
        "workModel": "zdalnie",
        "contactMethod": "e-mail",
    }
    for key, expected in expected_contact.items():
        if site_config.get(key) != expected:
            fail(f"Niepoprawna wartość {key} w konfiguracji strony")
    if "formEndpoint" in site_config:
        fail("Konfiguracja strony nadal zawiera nieużywany endpoint formularza")

    privacy = (ROOT / "privacy.html").read_text(encoding="utf-8")
    if 'content="noindex,nofollow"' not in privacy:
        fail("Robocza polityka prywatności musi pozostać poza indeksem")
    required_privacy_fragments = (
        "Dokument roboczy",
        "Marcin Siedlarek",
        "osoba prywatna",
        "[adres lub miejscowość do uzupełnienia]",
        "totalnybet@gmail.com",
    )
    missing_privacy = [fragment for fragment in required_privacy_fragments if fragment not in privacy]
    if missing_privacy:
        fail(f"Polityka prywatności nie zawiera wymaganych danych lub oznaczeń: {', '.join(missing_privacy)}")

    css = (ROOT / "assets/styles.css").read_text(encoding="utf-8")
    visual_css = (ROOT / "assets/visual-upgrades.css").read_text(encoding="utf-8")
    responsive_css = (ROOT / "assets/responsive-fixes.css").read_text(encoding="utf-8")
    javascript = (ROOT / "assets/script.js").read_text(encoding="utf-8")
    visual_test = (ROOT / "scripts/visual_check.mjs").read_text(encoding="utf-8")
    visual_workflow = (ROOT / ".github/workflows/visual-regression.yml").read_text(encoding="utf-8")
    lighthouse_workflow = (ROOT / ".github/workflows/lighthouse.yml").read_text(encoding="utf-8")

    if "@media (max-width:" not in css or "@media (max-width:" not in visual_css or "@media (max-width:" not in responsive_css:
        fail("Brak reguł responsywnych w arkuszach CSS")
    if "prefers-reduced-motion" not in css or "prefers-reduced-motion" not in visual_css or "prefers-reduced-motion" not in responsive_css:
        fail("Brak obsługi ograniczenia animacji")
    for breakpoint in (1280, 1090, 820, 430, 350):
        if str(breakpoint) not in responsive_css:
            fail(f"Brak oczekiwanego breakpointu {breakpoint}px w poprawkach responsywnych")
    if "IntersectionObserver" not in javascript:
        fail("Brak obserwatora sekcji i elementów interfejsu")
    if "pointerdown" not in javascript or "ArrowRight" not in javascript:
        fail("Karuzela nie ma pełnej obsługi dotyku i klawiatury")
    if "#contact-form" in javascript or "formEndpoint" in javascript:
        fail("JavaScript nadal zawiera nieużywaną obsługę formularza")
    if 'mailto:totalnybet@gmail.com' not in source:
        fail("Strona nie zawiera potwierdzonego kanału e-mail")

    for width in (1440, 1024, 768, 390, 320):
        if f"width: {width}" not in visual_test:
            fail(f"Test wizualny nie obejmuje szerokości {width}px")
    if "documentElement.scrollWidth" not in visual_test or "pageerror" not in visual_test:
        fail("Test wizualny nie sprawdza poziomego przewijania lub błędów JavaScript")
    if "scripts/visual_check.mjs" not in visual_workflow or "upload-artifact" not in visual_workflow:
        fail("Workflow testów wizualnych nie uruchamia skryptu lub nie zapisuje artefaktów")
    if "@lhci/cli" not in lighthouse_workflow or "upload-artifact" not in lighthouse_workflow:
        fail("Workflow Lighthouse jest niekompletny")

    print("OK: HTML, SEO, grafiki, responsywność, kontakt e-mail, operator, prywatność i infrastruktura testów przeszły kontrolę.")


if __name__ == "__main__":
    main()
