# Uwaga: Gałęzie Frontend i Backend usunięte!!!!
Nie było i nich większej korzyści, a tylko więcej zachodu z mergami, pushami i pullami.
Od teraz wszystko robimy na masterze.


# Social Insight 

**Aplikacja dostępna pod adresem [http://social-insight.tk:8081](http://social-insight.tk:8081)**

## Autorzy
- Radosław Pluta
- Łukasz Klimkiewicz
- Jacek Stasiak

## Podstawowe operacje
Instalowanie zależności: `pip install -r requirements.txt`

Uruchamianie: `flask run`

Czyszczenie bazy: `flask clean`

## Dodatkowe zależności
**Biblioteka wkhtmltopdf** - generowanie pdf - w systemie Linux można ją zainstalować za pomocą polecenia `sudo apt install -y wkhtmltopdf`.
W systemie Windows należy pobrać bibliotekę ze strony [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html).

**Zestaw narzędzi GTK+** - Konwersja svg do png - w systemie linux powinien być zainstalowany.
Dla Windows najprostsze rozwiązanie jakie znalazłem to instalacja UniConverter, który można pobrać
[tutaj](https://downloads.sk1project.net/uniconvertor/2.0rc4/uniconvertor-2.0rc4-win64_headless.msi)
i następne dodanie do zmiennej środowiskowej path ścieżki do podkatalogu dlls
(domyślnie C:\Program Files\UniConvertor-2.0rc4\dlls)


