#!/usr/bin/env python3
"""Jednorazowo upraszcza kontakt ZE8ES do potwierdzonego kanału e-mail."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
SCRIPT = ROOT / "assets" / "script.js"
VISUAL_CSS = ROOT / "assets" / "visual-upgrades.css"
SITE_CONFIG = ROOT / "assets" / "site-config.json"
VISUAL_TEST = ROOT / "scripts" / "visual_check.mjs"
QUALITY = ROOT / "scripts" / "quality_check.py"
PRIVACY = ROOT / "privacy.html"


def replace_regex(path: Path, pattern: str, replacement: str, label: str, *, flags: int = 0) -> None:
    source = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, source, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f"{label}: oczekiwano jednego dopasowania, znaleziono {count}")
    path.write_text(updated, encoding="utf-8")


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    source = path.read_text(encoding="utf-8")
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: oczekiwano jednego wystąpienia, znaleziono {count}")
    path.write_text(source.replace(old, new, 1), encoding="utf-8")


contact_section = '''    <section class="section" id="kontakt" aria-labelledby="contact-title">
      <div class="container contact-card">
        <div class="contact-grid">
          <div class="contact-copy reveal">
            <p class="kicker">Zacznijmy współpracę</p>
            <h2 id="contact-title">Masz pomysł?<br><span class="gradient-text">Napisz do ZE8ES.</span></h2>
            <p>Obsługujemy klientów z całej Polski i pracujemy zdalnie. Obecnie przyjmujemy zapytania wyłącznie przez e-mail.</p>
            <div class="contact-list">
              <span data-business-detail><i aria-hidden="true">✓</i> Cała Polska — współpraca zdalna</span>
              <span data-business-detail><i aria-hidden="true">✓</i> Kontakt wyłącznie przez e-mail</span>
              <span><i aria-hidden="true">✓</i> Jasny zakres i kolejność prac</span>
            </div>
          </div>

          <aside class="contact-direct reveal" aria-label="Bezpośredni kontakt e-mail">
            <p class="kicker">Kontakt e-mail</p>
            <a class="contact-email" href="mailto:totalnybet@gmail.com">totalnybet@gmail.com</a>
            <p>W wiadomości opisz cel projektu, potrzebne funkcje i orientacyjny termin. Odpowiedź otrzymasz drogą e-mailową.</p>
            <a class="btn btn-primary" href="mailto:totalnybet@gmail.com?subject=Zapytanie%20o%20projekt%20ZE8ES">Napisz e-mail <span aria-hidden="true">→</span></a>
            <small>ZE8ES nie publikuje obecnie numeru telefonu ani formularza kontaktowego.</small>
          </aside>
        </div>
      </div>
    </section>
  </main>'''

replace_regex(
    INDEX,
    r'    <section class="section" id="kontakt".*?    </section>\n  </main>',
    contact_section,
    "sekcja kontaktowa",
    flags=re.DOTALL,
)

replace_regex(
    SCRIPT,
    r"\n  const form = document\.querySelector\('#contact-form'\);.*?\n  const year =",
    "\n  const year =",
    "usunięcie obsługi formularza",
    flags=re.DOTALL,
)

css_marker = "/* Kontakt wyłącznie e-mailowy. */"
css = VISUAL_CSS.read_text(encoding="utf-8")
if css_marker not in css:
    css += f'''\n\n{css_marker}\n.contact-direct {{\n  align-self: stretch;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  gap: 18px;\n  min-width: 0;\n  padding: clamp(24px, 4vw, 42px);\n  border: 1px solid rgba(255,255,255,.1);\n  border-radius: 18px;\n  background: rgba(4,8,15,.64);\n  box-shadow: inset 0 1px rgba(255,255,255,.035), 0 24px 54px rgba(0,0,0,.2);\n}}\n.contact-direct p {{ margin: 0; color: var(--muted); line-height: 1.7; }}\n.contact-direct .kicker {{ color: #a995ff; }}\n.contact-email {{\n  overflow-wrap: anywhere;\n  color: #fff;\n  font-size: clamp(23px, 3vw, 36px);\n  font-weight: 800;\n  letter-spacing: -.035em;\n  text-decoration: none;\n}}\n.contact-email:hover {{ color: #bdafff; }}\n.contact-direct .btn {{ align-self: flex-start; }}\n.contact-direct small {{ color: #7f899a; line-height: 1.55; }}\n@media (max-width: 820px) {{\n  .contact-direct {{ padding: 24px; }}\n  .contact-direct .btn {{ width: 100%; justify-content: center; }}\n}}\n'''
    VISUAL_CSS.write_text(css, encoding="utf-8")

SITE_CONFIG.write_text(
    json.dumps(
        {
            "brandName": "ZE8ES",
            "brandType": "marka",
            "publicEmail": "totalnybet@gmail.com",
            "serviceArea": "Cała Polska",
            "workModel": "zdalnie",
            "contactMethod": "e-mail",
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n",
    encoding="utf-8",
)

visual = VISUAL_TEST.read_text(encoding="utf-8")
visual = visual.replace("  const postRequests = [];\n", "", 1)
visual = re.sub(
    r"  page\.on\('request', \(request\) => \{\n    if \(request\.method\(\) === 'POST'\) postRequests\.push\(request\.url\(\)\);\n  \}\);\n",
    "",
    visual,
    count=1,
)
visual, count = re.subn(
    r"      const form = page\.locator\('#contact-form'\);.*?\n\n      const privacyResponse =",
    '''      if (await page.locator('#contact-form').count()) {
        failures.push('mobile-390: strona nadal zawiera nieaktywny formularz kontaktowy');
      }
      const emailLinks = page.locator('a[href^="mailto:totalnybet@gmail.com"]');
      if ((await emailLinks.count()) < 2) {
        failures.push('mobile-390: brak bezpośrednich linków do publicznego e-maila');
      }
      const emailCard = page.locator('.contact-direct');
      if (!(await emailCard.isVisible())) {
        failures.push('mobile-390: karta kontaktu e-mail nie jest widoczna');
      }

      const privacyResponse =''',
    visual,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise RuntimeError(f"test formularza: oczekiwano jednego dopasowania, znaleziono {count}")
visual = visual.replace(
    "console.log(`OK: zapisano ${viewports.length} zrzutów strony, zrzut polityki prywatności i zweryfikowano potwierdzone dane kontaktowe.`);",
    "console.log(`OK: zapisano ${viewports.length} zrzutów strony, zrzut polityki prywatności i zweryfikowano kontakt wyłącznie e-mailowy.`);",
    1,
)
VISUAL_TEST.write_text(visual, encoding="utf-8")

quality = QUALITY.read_text(encoding="utf-8")
quality, count = re.subn(
    r'''    for required_fragment, label in \(\n        \('name="website"'.*?            fail\(f"Brak elementu formularza: \{label\}"\)\n''',
    '''    for required_fragment, label in (
        ('href="mailto:totalnybet@gmail.com', "bezpośredni kontakt e-mail"),
        ('data-business-detail', "potwierdzone dane kontaktowe"),
        ('href="privacy.html"', "odnośnik do polityki prywatności"),
    ):
        if required_fragment not in source:
            fail(f"Brak elementu kontaktowego: {label}")
''',
    quality,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise RuntimeError(f"kontrola elementów kontaktowych: oczekiwano jednego dopasowania, znaleziono {count}")

quality, count = re.subn(
    r'''    try:\n        form_config = json\.loads\(\(ROOT / "assets/site-config\.json"\).*?            fail\(f"Niepoprawna wartość \{key\} w konfiguracji formularza"\)\n''',
    '''    try:
        site_config = json.loads((ROOT / "assets/site-config.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(f"Niepoprawny JSON konfiguracji strony: {error}")
    expected_contact = {
        "brandName": "ZE8ES",
        "brandType": "marka",
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
''',
    quality,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise RuntimeError(f"kontrola konfiguracji: oczekiwano jednego dopasowania, znaleziono {count}")

quality, count = re.subn(
    r'''    for form_security_fragment in \("AbortController", "assets/site-config\.json", "sessionStorage", "formEndpoint"\):\n        if form_security_fragment not in javascript:\n            fail\(f"Brak zabezpieczenia formularza: \{form_security_fragment\}"\)\n''',
    '''    if "#contact-form" in javascript or "formEndpoint" in javascript:
        fail("JavaScript nadal zawiera nieużywaną obsługę formularza")
    if 'mailto:totalnybet@gmail.com' not in source:
        fail("Strona nie zawiera potwierdzonego kanału e-mail")
''',
    quality,
    count=1,
)
if count != 1:
    raise RuntimeError(f"kontrola martwego kodu formularza: oczekiwano jednego dopasowania, znaleziono {count}")
quality = quality.replace(
    'print("OK: HTML, SEO, grafiki, responsywność, formularz, prywatność i infrastruktura testów przeszły kontrolę.")',
    'print("OK: HTML, SEO, grafiki, responsywność, kontakt e-mail, prywatność i infrastruktura testów przeszły kontrolę.")',
    1,
)
QUALITY.write_text(quality, encoding="utf-8")

privacy = PRIVACY.read_text(encoding="utf-8")
privacy, count = re.subn(
    r'''      <section aria-labelledby="scope">.*?      </section>''',
    '''      <section aria-labelledby="scope">
        <h2 id="scope">2. Zakres przetwarzanych danych</h2>
        <p>Serwis nie posiada obecnie formularza kontaktowego. Kliknięcie adresu e-mail otwiera program pocztowy użytkownika, a zakres przekazanych danych zależy od treści wysłanej wiadomości. Nie należy przesyłać informacji, które nie są potrzebne do odpowiedzi na zapytanie.</p>
      </section>''',
    privacy,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise RuntimeError("Nie udało się zaktualizować zakresu danych w polityce prywatności")
privacy, count = re.subn(
    r'''      <section aria-labelledby="recipients">.*?      </section>''',
    '''      <section aria-labelledby="recipients">
        <h2 id="recipients">4. Odbiorcy i dostawcy usług</h2>
        <p>Strona jest publikowana przez GitHub Pages, a korespondencja trafia na skrzynkę Gmail wskazaną jako publiczny adres kontaktowy. Przed finalizacją dokumentu należy potwierdzić dane operatora marki, faktycznych dostawców oraz zasady przechowywania korespondencji.</p>
      </section>''',
    privacy,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise RuntimeError("Nie udało się zaktualizować odbiorców danych w polityce prywatności")
privacy, count = re.subn(
    r'''      <section aria-labelledby="security">.*?      </section>''',
    '''      <section aria-labelledby="security">
        <h2 id="security">8. Bezpieczeństwo kontaktu e-mail</h2>
        <p>Strona nie przesyła treści wiadomości przez własny formularz ani własny serwer. Wiadomość jest tworzona i wysyłana przez program pocztowy użytkownika. Nie należy umieszczać w niej haseł, danych szczególnych kategorii ani innych informacji zbędnych do przygotowania odpowiedzi.</p>
      </section>''',
    privacy,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise RuntimeError("Nie udało się zaktualizować bezpieczeństwa kontaktu w polityce prywatności")
PRIVACY.write_text(privacy, encoding="utf-8")

# Końcowa weryfikacja przed commitem.
index = INDEX.read_text(encoding="utf-8")
script = SCRIPT.read_text(encoding="utf-8")
visual_test = VISUAL_TEST.read_text(encoding="utf-8")
for required in (
    "totalnybet@gmail.com",
    "Kontakt wyłącznie przez e-mail",
    "Cała Polska — współpraca zdalna",
    "contact-direct",
):
    if required not in index:
        raise RuntimeError(f"Brak wymaganej treści kontaktowej: {required}")
if "contact-form" in index or "formEndpoint" in script:
    raise RuntimeError("Pozostał nieaktywny formularz lub jego obsługa")
if "contact-form" not in visual_test:
    raise RuntimeError("Test nie sprawdza usunięcia formularza")

print("OK: ZE8ES korzysta teraz wyłącznie z potwierdzonego kontaktu e-mail.")
