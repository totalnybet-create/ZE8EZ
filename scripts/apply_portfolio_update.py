#!/usr/bin/env python3
"""Jednorazowo publikuje w portfolio dwie potwierdzone realizacje ZE8ES."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
VISUAL_CSS = ROOT / "assets" / "visual-upgrades.css"
README = ROOT / "README.md"
STATUS = ROOT / "docs" / "STATUS.md"


def replace_once(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    if count == 0 and new in source:
        return source
    if count != 1:
        raise RuntimeError(f"{label}: oczekiwano jednego wystąpienia, znaleziono {count}")
    return source.replace(old, new, 1)


def update_index() -> None:
    source = INDEX.read_text(encoding="utf-8")

    source = replace_once(
        source,
        '<div class="portfolio-heading"><div><p class="kicker">Wybrane koncepcje</p><h2>Zobacz nasze projekty.</h2></div>',
        '<div class="portfolio-heading"><div><p class="kicker">Wybrane realizacje</p><h2>Zobacz nasze projekty.</h2></div>',
        "nagłówek portfolio",
    )
    source = replace_once(
        source,
        'aria-label="Projekty demonstracyjne — użyj strzałek lewo i prawo"',
        'aria-label="Realizacje i koncepcje ZE8ES — użyj strzałek lewo i prawo"',
        "etykieta karuzeli",
    )

    old_legnicki = (
        '<article class="project-card" tabindex="-1" aria-label="Legnicki Rynek — koncepcja portalu lokalnego">'
        '<div class="project-copy"><small>Portal lokalny</small><h3>Legnicki Rynek</h3>'
        '<p>Koncepcja portalu ogłoszeniowego, aktualności i wydarzeń dla mieszkańców.</p>'
        '<a href="#kontakt">Zobacz zakres</a></div></article>'
    )
    new_legnicki = (
        '<article class="project-card project-card-real" tabindex="-1" aria-label="Legnicki Rynek — zrealizowany portal lokalny">'
        '<div class="project-copy"><small>Realizacja • portal lokalny</small><h3>Legnicki Rynek</h3>'
        '<p>Responsywny portal lokalnych ogłoszeń, wydarzeń i usług dla Legnicy oraz okolic.</p>'
        '<div class="project-links"><a href="https://github.com/totalnybet-create/Legnicki-Rynek-" target="_blank" rel="noopener noreferrer">Repozytorium ↗</a></div>'
        '</div></article>'
    )
    source = replace_once(source, old_legnicki, new_legnicki, "realizacja Legnicki Rynek")

    old_service = (
        '<article class="project-card" tabindex="-1" aria-label="Service Flow — koncepcja panelu usługowego">'
        '<div class="project-copy"><small>Panel usługowy</small><h3>Service Flow</h3>'
        '<p>Demonstracyjny panel zarządzania zleceniami, klientami oraz harmonogramem.</p>'
        '<a href="#kontakt">Zobacz zakres</a></div></article>'
    )
    new_antiques = (
        '<article class="project-card project-card-real" tabindex="-1" aria-label="Giełda Staroci — zrealizowany serwis o antykach">'
        '<div class="project-copy"><small>Realizacja • serwis tematyczny</small><h3>Giełda Staroci</h3>'
        '<p>Serwis treściowy poświęcony antykom, kolekcjonerstwu, historii przedmiotów i renowacji.</p>'
        '<div class="project-links">'
        '<a href="https://www.gielda-staroci.com/" target="_blank" rel="noopener noreferrer">Otwórz stronę ↗</a>'
        '<a class="project-link-secondary" href="https://github.com/totalnybet-create/GIELDA-STAROCI" target="_blank" rel="noopener noreferrer">Repozytorium</a>'
        '</div></div></article>'
    )
    source = replace_once(source, old_service, new_antiques, "realizacja Giełda Staroci")

    old_store = (
        '<article class="project-card" tabindex="-1" aria-label="North Store — koncepcja sklepu internetowego">'
        '<div class="project-copy"><small>E-commerce</small><h3>North Store</h3>'
        '<p>Koncepcja szybkiego sklepu internetowego z prostym procesem zakupowym.</p>'
        '<a href="#kontakt">Zobacz zakres</a></div></article>'
    )
    new_store = (
        '<article class="project-card project-card-concept" tabindex="-1" aria-label="North Store — demonstracyjna koncepcja sklepu internetowego">'
        '<div class="project-copy"><small>Koncepcja • e-commerce</small><h3>North Store</h3>'
        '<p>Demonstracyjna koncepcja szybkiego sklepu internetowego z prostym procesem zakupowym.</p>'
        '<div class="project-links"><a href="#kontakt">Zobacz zakres</a></div></div></article>'
    )
    source = replace_once(source, old_store, new_store, "koncepcja North Store")

    INDEX.write_text(source, encoding="utf-8")


def update_css() -> None:
    source = VISUAL_CSS.read_text(encoding="utf-8")
    source = replace_once(
        source,
        'url("project-service.svg")',
        'url("project-antiques.svg")',
        "grafika Giełdy Staroci",
    )

    marker = "/* Portfolio realizacji — linki i status projektu. */"
    if marker not in source:
        source += f'''\n\n{marker}\n.project-card-real {{\n  border-color: rgba(118, 87, 255, .28);\n}}\n.project-card-real .project-copy > small {{\n  color: #bcaeff;\n}}\n.project-card-concept .project-copy > small {{\n  color: #d0a9ff;\n}}\n.project-links {{\n  display: flex;\n  flex-wrap: wrap;\n  gap: 8px;\n  margin-top: 14px;\n}}\n.project-links a {{\n  display: inline-flex;\n  align-items: center;\n  min-height: 34px;\n  padding: 0 11px;\n  border: 1px solid rgba(255,255,255,.16);\n  border-radius: 8px;\n  background: rgba(108,76,255,.16);\n  font-size: 10px;\n  font-weight: 800;\n  letter-spacing: .02em;\n}}\n.project-links .project-link-secondary {{\n  color: #c4cad6;\n  background: rgba(255,255,255,.035);\n}}\n@media (max-width: 430px) {{\n  .project-copy {{ padding: 16px; }}\n  .project-links a {{ min-height: 32px; }}\n}}\n'''

    VISUAL_CSS.write_text(source, encoding="utf-8")


def update_docs() -> None:
    readme = README.read_text(encoding="utf-8")
    readme = readme.replace(
        "- [x] Usługi, portfolio demonstracyjne i proces współpracy",
        "- [x] Usługi, dwie potwierdzone realizacje, jedna koncepcja i proces współpracy",
    )
    README.write_text(readme, encoding="utf-8")

    status = STATUS.read_text(encoding="utf-8")
    status = status.replace(
        "- dostępna karuzela trzech koncepcji demonstracyjnych,",
        "- dostępna karuzela dwóch potwierdzonych realizacji i jednej koncepcji demonstracyjnej,",
    )
    status = status.replace(
        "4. Uzupełnić dane firmy i prawdziwe portfolio.",
        "4. Uzupełnić pozostałe dane firmy i dodać trzecią zatwierdzoną realizację.",
    )
    STATUS.write_text(status, encoding="utf-8")


def verify() -> None:
    index = INDEX.read_text(encoding="utf-8")
    css = VISUAL_CSS.read_text(encoding="utf-8")
    required = (
        "Legnicki Rynek",
        "Giełda Staroci",
        "https://www.gielda-staroci.com/",
        "https://github.com/totalnybet-create/Legnicki-Rynek-",
        "https://github.com/totalnybet-create/GIELDA-STAROCI",
    )
    missing = [value for value in required if value not in index]
    if missing:
        raise RuntimeError(f"Brak wymaganych danych portfolio: {missing}")
    if 'url("project-antiques.svg")' not in css:
        raise RuntimeError("Brak grafiki Giełdy Staroci w arkuszu CSS")
    if "Service Flow" in index:
        raise RuntimeError("Pozostała demonstracyjna karta Service Flow")


def main() -> None:
    update_index()
    update_css()
    update_docs()
    verify()
    print("OK: opublikowano Legnicki Rynek i Giełdę Staroci w portfolio ZE8ES.")


if __name__ == "__main__":
    main()
