# Aplikacja Czatu z Historią Wiadomości

Ten projekt to prosta aplikacja czatu zaimplementowana w języku Python. Serwer przechowuje historię wiadomości w bazie danych SQLite, a klient może wysyłać i odbierać wiadomości, w tym wiadomości prywatne oraz wiadomości nadawane do wszystkich użytkowników.

## Funkcje

- **Wielowątkowy Klient i Serwer**: Umożliwia jednoczesne połączenie i komunikację wielu użytkowników.
- **Historia Wiadomości**: Przechowuje historię czatu w bazie danych SQLite.
- **Komendy Użytkowników**:
  - Wyświetlanie listy użytkowników (`*u`)
  - Wysyłanie wiadomości prywatnej (`/msg <nazwa_użytkownika> <wiadomość>`)
  - Nadawanie wiadomości do wszystkich (`/all <wiadomość>`)
  - Zakończenie połączenia (`***`)

## Instrukcje Instalacji

### Wymagania

- Python 3.x
- SQLite3

### Instalacja

1. Sklonuj repozytorium lub pobierz kod źródłowy.
2. Upewnij się, że masz zainstalowane Python 3 i SQLite3 na swoim komputerze.

### Uruchamianie Serwera

1. Przejdź do katalogu zawierającego kod serwera.
2. Uruchom skrypt serwera:
    ```bash
    python server.py
    ```
3. Serwer rozpocznie nasłuchiwanie na `localhost` na porcie `5678`.

### Uruchamianie Klienta

1. Przejdź do katalogu zawierającego kod klienta.
2. Uruchom skrypt klienta:
    ```bash
    python client.py
    ```
3. Połącz się z serwerem, wprowadzając swoją nazwę użytkownika i rozpocznij czatowanie!

## Kod Serwera

```python
# server.py

import socket
import threading
from datetime import datetime
import sqlite3

# Kod do konfiguracji i obsługi serwera oraz klientów
# (Pełny kod udostępniony wcześniej w konwersacji)

# Tworzenie tabel bazy danych
create_tables()

# Główna pętla serwera do akceptowania połączeń klientów
try:
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
finally:
    server_socket.close()
