#!/usr/bin/env python3
"""Sprawdza rzeczywiście opublikowaną stronę ZE8ES po wdrożeniu GitHub Pages."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
import json
import os
import re
import time

SITE_URL = os.environ.get(
    "ZE8ES_PUBLIC_URL",
    "https://totalnybet-create.github.io/ZE8EZ/",
).rstrip("/") + "/"
REPORT_PATH = Path(os.environ.get("ZE8ES_PUBLIC_REPORT", "public-smoke-report.json"))
SUMMARY_PATH = Path(os.environ.get("ZE8ES_PUBLIC_SUMMARY", "public-smoke-summary.md"))
USER_AGENT = "ZE8ES-public-smoke-check/1.0"


@dataclass
class CheckResult:
    name: str
    url: str
    expected_status: int
    actual_status: int | None
    passed: bool
    details: str = ""


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in {"script", "img"} and values.get("src"):
            self.references.add(values["src"] or "")
        if tag == "link" and values.get("href"):
            self.references.add(values["href"] or "")


def fetch(url: str, *, retries: int = 4, delay: int = 8) -> tuple[int, bytes, str]:
    last_error = ""
    for attempt in range(retries):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT, "Cache-Control": "no-cache"})
            with urlopen(request, timeout=25) as response:
                return response.status, response.read(), response.headers.get("Content-Type", "")
        except HTTPError as error:
            body = error.read()
            if error.code < 500 or attempt == retries - 1:
                return error.code, body, error.headers.get("Content-Type", "")
            last_error = f"HTTP {error.code}"
        except (URLError, TimeoutError) as error:
            last_error = str(error)
        if attempt < retries - 1:
            time.sleep(delay)
    raise RuntimeError(last_error or "Nieznany błąd pobierania")


def check_url(name: str, path: str, expected_status: int = 200) -> tuple[CheckResult, bytes, str]:
    url = urljoin(SITE_URL, path)
    try:
        status, body, content_type = fetch(url)
        passed = status == expected_status
        details = content_type or "brak Content-Type"
        return CheckResult(name, url, expected_status, status, passed, details), body, content_type
    except RuntimeError as error:
        return CheckResult(name, url, expected_status, None, False, str(error)), b"", ""


def main() -> None:
    parsed_site = urlparse(SITE_URL)
    if parsed_site.scheme != "https" or not parsed_site.netloc:
        raise SystemExit("ZE8ES_PUBLIC_URL musi być poprawnym adresem HTTPS")

    results: list[CheckResult] = []

    home_result, home_body, home_type = check_url("Strona główna", "")
    results.append(home_result)
    home_html = home_body.decode("utf-8", errors="replace")

    if home_result.passed:
        semantic_checks = {
            "Marka ZE8ES": "ZE8ES" in home_html,
            "Język polski": bool(re.search(r'<html[^>]+lang=["\']pl["\']', home_html, re.I)),
            "Element main": bool(re.search(r"<main(?:\s|>)", home_html, re.I)),
            "Brak mieszanej zawartości": not bool(re.search(r'(?:src|href)=["\']http://', home_html, re.I)),
            "HTML Content-Type": "text/html" in home_type.lower(),
        }
        for name, passed in semantic_checks.items():
            results.append(CheckResult(name, SITE_URL, 200, 200 if passed else None, passed))

        parser = AssetParser()
        parser.feed(home_html)
        required_references = {
            "assets/styles.css",
            "assets/visual-upgrades.css",
            "assets/responsive-fixes.css",
            "assets/script.js",
            "assets/logo-mark.svg",
            "assets/hero-visual.svg",
        }
        for reference in sorted(required_references):
            results.append(
                CheckResult(
                    f"Referencja HTML: {reference}",
                    SITE_URL,
                    200,
                    200 if reference in parser.references else None,
                    reference in parser.references,
                )
            )

    public_files = [
        ("Podstawowy CSS", "assets/styles.css", "text/css"),
        ("Warstwa wizualna CSS", "assets/visual-upgrades.css", "text/css"),
        ("Poprawki responsywne CSS", "assets/responsive-fixes.css", "text/css"),
        ("JavaScript", "assets/script.js", "javascript"),
        ("Logo SVG", "assets/logo-mark.svg", "image/svg+xml"),
        ("Hero SVG", "assets/hero-visual.svg", "image/svg+xml"),
        ("Polityka prywatności", "privacy.html", "text/html"),
    ]
    for name, path, expected_type in public_files:
        result, body, content_type = check_url(name, path)
        if result.passed and expected_type not in content_type.lower():
            result.passed = False
            result.details = f"Nieoczekiwany Content-Type: {content_type or 'brak'}"
        if result.passed and not body:
            result.passed = False
            result.details = "Pusty plik"
        results.append(result)

    missing_path = f"__smoke-missing-{int(time.time())}.html"
    not_found_result, not_found_body, _ = check_url("Własna strona 404", missing_path, 404)
    if not_found_result.passed and b"ZE8ES" not in not_found_body:
        not_found_result.passed = False
        not_found_result.details = "Odpowiedź 404 nie zawiera marki ZE8ES"
    results.append(not_found_result)

    failures = [result for result in results if not result.passed]
    payload = {
        "site": SITE_URL,
        "checkedAtUnix": int(time.time()),
        "passed": not failures,
        "checks": [asdict(result) for result in results],
    }
    REPORT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary_lines = [
        "# Publiczny test ZE8ES",
        "",
        f"Adres: {SITE_URL}",
        "",
        "| Kontrola | Wynik | Status HTTP |",
        "|---|---:|---:|",
    ]
    for result in results:
        marker = "✅" if result.passed else "❌"
        status = str(result.actual_status) if result.actual_status is not None else "—"
        summary_lines.append(f"| {result.name} | {marker} | {status} |")
    summary_lines.extend(["", f"Łącznie: {len(results) - len(failures)}/{len(results)} kontroli zaliczonych."])
    SUMMARY_PATH.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    if failures:
        print("Wykryto problemy na publicznej stronie:")
        for result in failures:
            print(f"- {result.name}: {result.details or 'kontrola nieudana'} ({result.url})")
        raise SystemExit(1)

    print(f"OK: publiczna strona przeszła {len(results)} kontroli.")


if __name__ == "__main__":
    main()
