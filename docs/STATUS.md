# Status projektu ZE8ES

Aktualizacja: 2026-08-01

## Stan bieżący

Wersja demonstracyjna ZE8ES działa publicznie pod adresem:

https://totalnybet-create.github.io/ZE8EZ/

GitHub Pages korzysta ze źródła `GitHub Actions`, a workflow `Deploy ZE8ES to GitHub Pages` został potwierdzony jako zakończony sukcesem. Strona została otwarta i sprawdzona na fizycznym telefonie. Po tym teście wykonano pierwszą korektę mobilną obejmującą zapis marki, skalę hero oraz odstępy przejścia do usług.

Projekt nadal nie jest wersją produkcyjną: brakuje zatwierdzonych danych firmy, prawdziwych realizacji, backendu formularza i finalnych dokumentów prawnych. Indeksowanie pozostaje celowo wyłączone.

## Wykonane

### Interfejs i treść

- marka ZE8ES oraz własny znak SVG,
- ciemny interfejs premium z akcentami fioletowo-niebieskimi,
- responsywny nagłówek i dostępne menu mobilne,
- autorska grafika hero SVG z laptopem, telefonem, panelami i orbitami,
- osobna warstwa precyzyjnych poprawek dla 1440, 1024, 768, 390 i 320 px,
- korekta mobilna po teście na rzeczywistym telefonie,
- pięć obszarów usług,
- animowane wskaźniki standardów realizacji,
- dostępna karuzela dwóch potwierdzonych realizacji i jednej koncepcji demonstracyjnej,
- czterostopniowy proces współpracy,
- sekcja O nas, standard współpracy i FAQ,
- sekcja kontaktowa i stopka,
- oznaczenie treści demonstracyjnych bez udawania potwierdzonych realizacji lub opinii.

### Interakcje i dostępność

- sterowanie menu klawiaturą i klawiszem Escape,
- wskazywanie aktywnej sekcji nawigacji,
- ograniczenie animacji przez `prefers-reduced-motion`,
- karuzela obsługiwana przyciskami, strzałkami i gestem dotykowym,
- zatrzymywanie automatycznej karuzeli podczas interakcji i po ukryciu karty,
- FAQ aktualizujące `aria-expanded`,
- widoczny fokus klawiatury,
- formularz z walidacją, wymaganymi etykietami i komunikatem `aria-live`.

### Formularz i prywatność

- publiczna konfiguracja formularza w `assets/site-config.json`,
- blokada endpointów bez HTTPS,
- timeout żądania i obsługa błędów,
- podstawowe ograniczenie częstotliwości wysyłki,
- honeypot i minimalny czas wypełnienia,
- wymagana zgoda na kontakt,
- bezpieczny tryb bez endpointu — brak żądania POST,
- robocza polityka prywatności `privacy.html` oznaczona `noindex,nofollow`,
- checklista danych prawnych `docs/LEGAL_INPUTS.md`,
- formularz Issue do przekazania konfiguracji backendu bez sekretów.

### Testy i jakość

- statyczny skrypt `scripts/quality_check.py`,
- test spójności wydania `scripts/release_check.py`,
- skrypt konfiguracji publicznego adresu `scripts/configure_release.py`,
- test Playwright dla pięciu szerokości,
- kontrola błędów konsoli, nieudanych zasobów i poziomego przewijania,
- automatyczny test menu, FAQ, formularza i polityki prywatności,
- zrzuty ekranu zapisywane jako artefakty GitHub Actions,
- trzy mobilne przebiegi Lighthouse,
- progi dla Accessibility, Best Practices, SEO, CLS, LCP i TBT,
- workflow Pages zatrzymujący publikację po błędzie kontroli statycznej lub konfiguracji wydania,
- pierwszy test na fizycznym telefonie zakończony poprawnym wyświetleniem strony.

### SEO i publikacja

- działający publiczny adres GitHub Pages przez HTTPS,
- źródło publikacji ustawione na `GitHub Actions`,
- udany przebieg workflow wdrożeniowego,
- favicon SVG i strona błędu 404,
- metadane podstawowe i Open Graph bez włączania indeksowania wersji demonstracyjnej,
- indeksowanie wersji rozwojowej zablokowane w `robots.txt`,
- pusta, poprawna składniowo sitemap do czasu zatwierdzenia wydania produkcyjnego,
- procedura wydania SEO w `docs/SEO_RELEASE.md`,
- konfigurator, który po zatwierdzeniu produkcji ustawi canonical, `og:url`, robots i sitemapę,
- `.nojekyll` i workflow wdrożenia statycznego do GitHub Pages.

### Organizacja repozytorium

- rozdzielone pliki HTML, CSS, JavaScript, JSON i SVG,
- dokumentacja planu, jakości, SEO, prawa i statusu,
- osobne, opisane commity,
- zamknięte Issue #4 dotyczące uruchomienia GitHub Pages,
- otwarte Issues dla danych firmy, backendu formularza, realizacji, domeny, analityki i pełnych testów urządzeń,
- formularze Issues dla danych firmy, realizacji i backendu bez ujawniania sekretów.

## Kroki nadal zablokowane danymi właściciela

1. Przekazać zatwierdzoną nazwę firmy, e-mail, telefon, obszar działania i domenę.
2. Przekazać co najmniej trzy zatwierdzone realizacje z prawami do materiałów.
3. Wybrać backend formularza i zatwierdzony adres odbiorczy.
4. Uzupełnić finalne dane w polityce prywatności i zweryfikować dokument.
5. Podjąć decyzję o analityce i mechanizmie zgód.
6. Wykonać testy na pozostałych urządzeniach i przeglądarkach.

## Następna kolejność prac

1. Sprawdzić wyniki najnowszych workflow po korekcie mobilnej.
2. Pobrać artefakty z testów wizualnych i Lighthouse.
3. Poprawić problemy wykryte przez rzeczywiste przebiegi.
4. Uzupełnić pozostałe dane firmy i dodać trzecią zatwierdzoną realizację.
5. Podłączyć i przetestować backend formularza.
6. Sfinalizować dokumenty prawne.
7. Uruchomić `scripts/configure_release.py` z zatwierdzonym adresem HTTPS.
8. Włączyć indeksowanie, dodać Search Console i dopiero wtedy ewentualną analitykę.

## Ważne

- Repozytorium nazywa się `ZE8EZ`.
- Marka widoczna na stronie nazywa się `ZE8ES`.
- Publiczny adres demonstracyjny działa: https://totalnybet-create.github.io/ZE8EZ/
- Potwierdzenie publikacji nie oznacza jeszcze gotowości produkcyjnej ani zgody na indeksowanie.
