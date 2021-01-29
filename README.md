# Social Insight 

Aplikacja dostępna pod adresem [http://social-insight.tk:8081](http://social-insight.tk:8081)


## Sposób uruchomienia
1. Instalowanie zależności: `pip install -r requirements.txt`
2. Kompilacja tłumaczeń: `flask translate compile`
3. Uruchomienie aplikacji: `flask run`
4. Wgranie przykładowego pliku (opcjonalnie) `flask example <nazwa>`


## Domyślni użytkownicy
Po uruchomieniu aplikacji zawsze tworzeni są dwaj domyślni użytkownicy:
- **Admin** (Email: social.insight.noreply@gmail.com; Hasło: password)
- **Zwykły użytkownik** (Email: user@test.com; Hasło: password)


## Zewnętrzne zależności
- **Biblioteka wkhtmltopdf** - generowanie pdf - w systemie Linux można ją zainstalować za pomocą polecenia `sudo apt install -y wkhtmltopdf`.
W systemie Windows należy pobrać bibliotekę z [tej strony](https://wkhtmltopdf.org/downloads.html), 
a następnie należy dodać do zmiennej środowiskowej path ścieżkę do katalogu bin (domyślnie C:\Program Files\wkhtmltopdf\bin)

- **Zestaw narzędzi GTK+** - Konwersja svg do png - w systemie linux powinien być zainstalowany.
Dla Windows najprostsze znalezione rozwiązanie to instalacja UniConverter, który można pobrać z
[tej strony](https://downloads.sk1project.net/uniconvertor/2.0rc4/uniconvertor-2.0rc4-win64_headless.msi)
i następne dodanie do zmiennej środowiskowej path ścieżki do podkatalogu dlls
(domyślnie C:\Program Files\UniConvertor-2.0rc4\dlls)


## Bugi

- Dla Linux konwersja wykresów z svg do png na których są emotikony powoduje błąd. Wyświetlany jest wtedy komunikat o błędzie.
- Dla Windows równoległe generowanie plików pdf powoduje błąd ponieważ biblioteka Cairo nie jest bezpieczna dla wątków. Co ciekawe dla Linuxa już jest.

## Autorzy
- Radosław Pluta
- Łukasz Klimkiewicz
- Jacek Stasiak
