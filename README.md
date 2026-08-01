# ZE8ES

Nowoczesna, responsywna strona internetowa dla studia tworzącego strony, aplikacje, systemy, automatyzacje i rozwiązania AI dla firm.

- Repozytorium: `totalnybet-create/ZE8EZ`
- Nazwa marki na stronie: **ZE8ES**
- Gałąź produkcyjna: `main`
- Technologia: HTML, CSS i JavaScript bez ciężkich zależności

## Cel projektu

Zbudowanie od podstaw kompletnej strony firmowej inspirowanej przekazanym kierunkiem wizualnym: ciemny interfejs premium, akcenty fioletowo-niebieskie, mocna sekcja otwierająca, prezentacja usług, projektów, procesu współpracy, FAQ i formularza kontaktowego.

## Aktualna struktura

```text
ZE8EZ/
├── .github/
│   └── workflows/
│       ├── deploy-pages.yml
│       └── quality.yml
├── assets/
│   ├── logo-mark.svg
│   ├── script.js
│   └── styles.css
├── docs/
│   ├── IMPLEMENTATION_PLAN.md
│   └── STATUS.md
├── scripts/
│   └── quality_check.py
├── 404.html
├── index.html
├── robots.txt
├── sitemap.xml
└── README.md
```

## Uruchomienie lokalne

Projekt jest statyczny. Można otworzyć `index.html` bezpośrednio w przeglądarce albo uruchomić prosty serwer:

```bash
python -m http.server 8080
```

Następnie wejść na `http://localhost:8080`.

## Kontrola jakości

```bash
python scripts/quality_check.py
```

Skrypt sprawdza między innymi:

- wymagane metadane i pojedynczy nagłówek `h1`,
- unikalne identyfikatory,
- działające odnośniki wewnętrzne,
- obecność lokalnych plików CSS, JavaScript i SVG,
- podstawy dostępności obrazów,
- rozdzielenie HTML, CSS i JavaScript,
- obecność reguł responsywnych oraz obsługi ograniczenia animacji.

Kontrola uruchamia się automatycznie przez GitHub Actions po zmianach na `main`.

## Status funkcjonalny

- [x] Repozytorium i dokumentacja
- [x] Design system i pełny układ responsywny
- [x] Nagłówek oraz menu mobilne
- [x] Hero i autorska wizualizacja produktu
- [x] Sekcja usług
- [x] Wskaźniki i karuzela projektów
- [x] Proces współpracy
- [x] Sekcja O nas
- [x] Standard współpracy i FAQ
- [x] Formularz z walidacją przeglądarki
- [x] SEO techniczne, favicon, robots i sitemap
- [x] Automatyczne testy jakości
- [x] Workflow publikacji GitHub Pages
- [ ] Podłączenie bezpiecznej wysyłki formularza
- [ ] Zastąpienie demonstracyjnego portfolio prawdziwymi realizacjami
- [ ] Uzupełnienie prawdziwych danych firmy
- [ ] Testy wizualne na fizycznych urządzeniach
- [ ] Końcowa optymalizacja Lighthouse i publikacja domeny

## Zasady realizacji

- całość kodu, dokumentacji i historii zmian jest zapisywana na GitHubie,
- większe funkcje otrzymują osobne, opisane commity,
- projekt jest rozwijany mobile-first i bez poziomego przewijania,
- używany jest semantyczny HTML oraz obsługa klawiatury,
- treści demonstracyjne są oznaczone i nie udają potwierdzonych realizacji lub opinii,
- projekt pozostaje prosty do dalszej rozbudowy i migracji na wybrany hosting.

Szczegółowy plan znajduje się w `docs/IMPLEMENTATION_PLAN.md`, a aktualny stan w `docs/STATUS.md`.
