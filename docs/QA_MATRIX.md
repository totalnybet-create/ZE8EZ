# Macierz testów ZE8ES

## Automatyczne kontrole

- `python scripts/quality_check.py` — struktura HTML, SEO, linki, lokalne zasoby, SVG i podstawy dostępności.
- GitHub Actions: `Quality checks` — uruchamia kontrolę statyczną po zmianach.
- GitHub Actions: `Lighthouse audit` — uruchamia stronę lokalnie i zapisuje raporty Performance, Accessibility, Best Practices oraz SEO jako artefakt.

## Szerokości referencyjne

| Widok | Szerokość | Najważniejsze elementy do sprawdzenia |
|---|---:|---|
| Duży desktop | 1440 px | proporcje hero, położenie grafiki, długość wierszy, pięć kart usług |
| Laptop | 1024 px | przejście hero do jednej kolumny, odstępy, karuzela i proces |
| Tablet | 768 px | menu mobilne, układ dwóch kolumn, formularz i FAQ |
| Telefon | 390 px | łamanie nagłówków, przyciski na całą szerokość, brak poziomego przewijania |
| Mały telefon | 320 px | minimalne odstępy, czytelność tekstu, pola formularza i grafika hero |

## Kryteria akceptacji

- brak poziomego przewijania na całej stronie,
- jeden nagłówek `h1` i poprawna hierarchia kolejnych nagłówków,
- wszystkie elementy interaktywne dostępne klawiaturą,
- widoczny fokus klawiatury,
- menu zamyka się po wyborze pozycji oraz po zmianie szerokości,
- karuzela działa przyciskami, klawiaturą i gestem dotykowym,
- automatyczne animacje są ograniczane przez `prefers-reduced-motion`,
- FAQ prawidłowo aktualizuje `aria-expanded`,
- formularz blokuje wysłanie niepełnych danych i wyświetla komunikat,
- wszystkie lokalne obrazy i arkusze ładują się bez błędów 404,
- strona błędu 404 zachowuje identyfikację wizualną marki,
- wynik Lighthouse jest rejestrowany po każdej większej zmianie.

## Kontrole przed publikacją produkcyjną

- zastąpienie demonstracyjnych realizacji prawdziwymi materiałami,
- zatwierdzenie nazwy firmy, danych kontaktowych i treści prawnych,
- wybór domeny i ustawienie adresów kanonicznych,
- podłączenie formularza do bezpiecznego endpointu,
- włączenie ochrony antyspamowej i ograniczenia liczby wysyłek,
- dodanie analityki dopiero po przygotowaniu mechanizmu zgód,
- końcowy test na fizycznym telefonie i komputerze,
- podniesienie progów Lighthouse po usunięciu ostrzeżeń.
