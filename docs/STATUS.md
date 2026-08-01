# Status projektu ZE8ES

Aktualizacja: 2026-08-01

## Stan bieżący

Etap utwardzenia wersji rozwojowej został wdrożony na gałęzi `main`. Strona ma kompletną strukturę, warstwę wizualną, interakcje oraz automatyczną infrastrukturę kontroli. Nie jest jeszcze wersją produkcyjną, ponieważ brakuje zatwierdzonych danych firmy, prawdziwych realizacji, backendu formularza i potwierdzonego adresu publicznego.

## Wykonane

### Interfejs i treść

- marka ZE8ES oraz własny znak SVG,
- ciemny interfejs premium z akcentami fioletowo-niebieskimi,
- responsywny nagłówek i dostępne menu mobilne,
- autorska grafika hero SVG z laptopem, telefonem, panelami i orbitami,
- osobna warstwa precyzyjnych poprawek dla 1440, 1024, 768, 390 i 320 px,
- pięć obszarów usług,
- animowane wskaźniki standardów realizacji,
- dostępna karuzela trzech koncepcji demonstracyjnych,
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
- workflow Pages zatrzymujący publikację po błędzie kontroli statycznej lub konfiguracji wydania.

### SEO i publikacja

- favicon SVG i strona błędu 404,
- metadane podstawowe i Open Graph bez niepotwierdzonego `og:url`,
- usunięty niepotwierdzony adres GitHub Pages z robots i sitemap,
- indeksowanie wersji rozwojowej zablokowane w `robots.txt`,
- pusta, poprawna składniowo sitemap do czasu potwierdzenia adresu,
- procedura wydania SEO w `docs/SEO_RELEASE.md`,
- konfigurator, który po podaniu adresu HTTPS ustawi canonical, `og:url`, robots i sitemapę,
- `.nojekyll` i workflow wdrożenia statycznego do GitHub Pages.

### Organizacja repozytorium

- rozdzielone pliki HTML, CSS, JavaScript, JSON i SVG,
- dokumentacja planu, jakości, SEO, prawa i statusu,
- osobne, opisane commity,
- Issues dla danych firmy, backendu formularza, realizacji i GitHub Pages,
- formularze Issues dla danych firmy, realizacji i backendu bez ujawniania sekretów.

## Kroki zablokowane danymi lub ustawieniami właściciela

1. W `Settings → Pages` ustawić źródło `GitHub Actions`.
2. Potwierdzić publiczny adres HTTPS i wynik wdrożenia.
3. Przekazać zatwierdzoną nazwę firmy, e-mail, telefon, obszar działania i domenę.
4. Przekazać co najmniej trzy zatwierdzone realizacje z prawami do materiałów.
5. Wybrać backend formularza i zatwierdzony adres odbiorczy.
6. Uzupełnić finalne dane w polityce prywatności i zweryfikować dokument.
7. Podjąć decyzję o analityce i mechanizmie zgód.
8. Wykonać testy na fizycznym telefonie, tablecie i komputerze.

## Kolejność po odblokowaniu

1. Potwierdzić działanie GitHub Pages.
2. Pobrać artefakty z testów wizualnych i Lighthouse.
3. Poprawić ewentualne problemy wykryte przez rzeczywiste przebiegi.
4. Uzupełnić dane firmy i prawdziwe portfolio.
5. Podłączyć i przetestować backend formularza.
6. Sfinalizować dokumenty prawne.
7. Uruchomić `scripts/configure_release.py` z potwierdzonym adresem HTTPS.
8. Włączyć indeksowanie, dodać Search Console i dopiero wtedy ewentualną analitykę.

## Ważne

- Repozytorium nazywa się `ZE8EZ`.
- Marka widoczna na stronie nazywa się `ZE8ES`.
- Publiczny adres GitHub Pages nie został jeszcze potwierdzony przez dostępne narzędzia.
- Dostępne połączenie nie pozwala przełączyć ustawienia Pages ani odczytać pełnych logów workflow uruchomionych przez push.
- Samo dodanie workflow nie jest dowodem jego pomyślnego wykonania; wyniki należy sprawdzić w zakładce Actions.
