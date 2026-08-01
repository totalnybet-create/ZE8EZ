# ZE8ES

Nowoczesna, responsywna strona internetowa dla studia tworzącego strony, aplikacje, systemy, automatyzacje i rozwiązania AI dla firm.

- Repozytorium: `totalnybet-create/ZE8EZ`
- Nazwa marki na stronie: **ZE8ES**
- Główna gałąź: `main`
- Technologia produkcyjna: statyczny HTML, CSS i JavaScript
- Publiczna wersja demonstracyjna: https://totalnybet-create.github.io/ZE8EZ/
- Stan publikacji: GitHub Pages działa przez workflow `Deploy ZE8ES to GitHub Pages`
- Stan indeksowania: zablokowane do czasu zatwierdzenia danych firmy, realizacji i dokumentów prawnych

## Cel projektu

Zbudowanie od podstaw kompletnej strony firmowej inspirowanej przekazanym kierunkiem wizualnym: ciemny interfejs premium, akcenty fioletowo-niebieskie, rozbudowana sekcja otwierająca, prezentacja usług, projektów, procesu współpracy, FAQ i formularza kontaktowego.

## Najważniejsze funkcje

- responsywny nagłówek i menu mobilne,
- autorska grafika hero SVG,
- pięć obszarów usług,
- dostępna karuzela projektów obsługiwana klawiaturą i dotykiem,
- proces współpracy, sekcja O nas i FAQ,
- formularz z walidacją, zgodą, honeypotem i konfigurowalnym endpointem HTTPS,
- robocza polityka prywatności oznaczona `noindex,nofollow`,
- automatyczne testy statyczne, Lighthouse i testy Playwright na pięciu szerokościach,
- bezpieczny skrypt konfigurujący canonical, Open Graph, robots i sitemapę po zatwierdzeniu wydania produkcyjnego.

## Struktura

```text
ZE8EZ/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── company-data.yml
│   │   ├── form-backend.yml
│   │   └── portfolio-item.yml
│   └── workflows/
│       ├── deploy-pages.yml
│       ├── lighthouse.yml
│       ├── quality.yml
│       └── visual-regression.yml
├── assets/
│   ├── hero-visual.svg
│   ├── logo-mark.svg
│   ├── project-local.svg
│   ├── project-service.svg
│   ├── project-store.svg
│   ├── responsive-fixes.css
│   ├── script.js
│   ├── site-config.json
│   ├── styles.css
│   └── visual-upgrades.css
├── docs/
│   ├── IMPLEMENTATION_PLAN.md
│   ├── LEGAL_INPUTS.md
│   ├── QA_MATRIX.md
│   ├── SEO_RELEASE.md
│   └── STATUS.md
├── scripts/
│   ├── configure_release.py
│   ├── quality_check.py
│   ├── release_check.py
│   └── visual_check.mjs
├── 404.html
├── index.html
├── lighthouserc.cjs
├── privacy.html
├── robots.txt
├── sitemap.xml
└── README.md
```

## Uruchomienie lokalne

```bash
python -m http.server 8080
```

Następnie otwórz `http://127.0.0.1:8080`.

## Kontrole lokalne

```bash
python scripts/quality_check.py
python scripts/release_check.py
```

Kontrole sprawdzają między innymi:

- strukturę HTML, metadane i pojedynczy nagłówek `h1`,
- unikalne identyfikatory i działające odnośniki,
- obecność i poprawność lokalnych CSS, JavaScript, JSON i SVG,
- breakpointy 1440, 1024, 768, 390 i 320 px,
- obsługę ograniczenia animacji,
- zabezpieczenia formularza i spójność polityki prywatności,
- dwa dozwolone stany SEO: bezpieczny rozwój albo kompletna publikacja HTTPS.

## Testy automatyczne

GitHub Actions uruchamia:

- `Quality checks` — kontrola statyczna oraz spójność wydania,
- `Visual regression checks` — zrzuty pięciu szerokości, błędy konsoli, poziome przewijanie, menu, FAQ, formularz i polityka prywatności,
- `Lighthouse audit` — trzy mobilne przebiegi Performance, Accessibility, Best Practices i SEO,
- `Deploy ZE8ES to GitHub Pages` — publikacja dopiero po przejściu bramki jakości.

## Formularz

Publiczna konfiguracja znajduje się w `assets/site-config.json`. Pole `formEndpoint` pozostaje puste do czasu zatwierdzenia backendu. Bez endpointu formularz nie wykonuje żadnego żądania POST.

Nie wolno zapisywać kluczy API, haseł ani tokenów w pliku konfiguracyjnym, kodzie frontendu lub treści Issue.

## Konfiguracja wydania produkcyjnego

Publiczny adres demonstracyjny jest potwierdzony, ale indeksowanie pozostaje wyłączone do czasu zatwierdzenia treści i dokumentów. Gdy projekt będzie gotowy produkcyjnie:

```bash
python scripts/configure_release.py https://totalnybet-create.github.io/ZE8EZ/ --dry-run
python scripts/configure_release.py https://totalnybet-create.github.io/ZE8EZ/
python scripts/release_check.py
```

Skrypt ustawia spójne `canonical`, `og:url`, `robots.txt` i `sitemap.xml`.

## Status funkcjonalny

- [x] Design system i pełny układ responsywny
- [x] Hero i autorska grafika produktu
- [x] Usługi, dwie potwierdzone realizacje, jedna koncepcja i proces współpracy
- [x] O nas, standard współpracy i FAQ
- [x] Bezpieczna architektura formularza oczekująca na endpoint
- [x] Robocza polityka prywatności i checklisty prawne
- [x] Automatyczne testy statyczne, wizualne i Lighthouse
- [x] Workflow publikacji z bramką jakości
- [x] GitHub Pages ustawione na `GitHub Actions`
- [x] Potwierdzony publiczny adres HTTPS
- [x] Pierwszy test na fizycznym telefonie i korekta mobilna
- [ ] Uzupełnienie prawdziwych danych firmy
- [ ] Podłączenie zatwierdzonego backendu formularza
- [ ] Zastąpienie koncepcji prawdziwymi realizacjami
- [ ] Finalizacja dokumentów prawnych
- [ ] Pełne testy na wymaganych urządzeniach i przeglądarkach
- [ ] Podłączenie domeny, Search Console i ewentualnej analityki

Szczegółowy stan znajduje się w `docs/STATUS.md`.
