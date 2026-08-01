# Publikacja SEO ZE8ES

## Stan rozwojowy

Do czasu potwierdzenia publicznego adresu:

- `robots.txt` blokuje indeksowanie,
- `sitemap.xml` nie zawiera niepotwierdzonych adresów,
- nie dodajemy `canonical`, `og:url` ani absolutnego `og:image`,
- polityka prywatności pozostaje oznaczona jako `noindex,nofollow`.

## Dane wymagane przed włączeniem indeksowania

- potwierdzony adres HTTPS,
- decyzja: domena własna czy GitHub Pages,
- nazwa firmy i dane kontaktowe,
- finalny tytuł oraz opis strony,
- finalna grafika Open Graph w obsługiwanym formacie rastrowym,
- finalna polityka prywatności,
- prawdziwe materiały portfolio.

## Kolejność wdrożenia

1. Potwierdzić, że publiczny adres zwraca HTTP 200.
2. Potwierdzić brak błędów 404 dla CSS, JavaScript i SVG.
3. Ustawić w `index.html` absolutny adres `canonical`.
4. Dodać `og:url` i absolutny adres `og:image`.
5. Wpisać potwierdzone adresy do `sitemap.xml`.
6. Ustawić w `robots.txt` `Allow: /` i odnośnik do sitemap.
7. Zweryfikować stronę w Search Console.
8. Przesłać sitemapę dopiero po wdrożeniu finalnych treści.
9. Uruchomić końcowy Lighthouse i test linków.
10. Potwierdzić, że dokumenty robocze nadal nie są indeksowane.

## Kryterium ukończenia

Indeksowanie można włączyć dopiero wtedy, gdy strona jest dostępna przez HTTPS, zawiera zatwierdzone dane i nie ma demonstracyjnych wyników przedstawionych jako prawdziwe realizacje.
