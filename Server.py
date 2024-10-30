import socket

# Tworzenie gniazda serwerowego
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Konfiguracja adresu i portu serwera
server_address = ('localhost', 5678)
server_socket.bind(server_address)

# Nasłuchiwanie na połączenia
server_socket.listen(1)
print("Serwer czeka na połączenie...")

# Akceptacja połączenia od klienta
client_socket, client_address = server_socket.accept()
print(f"Połączono z {client_address}")

try:
    while True:
        # Odbieranie wiadomości od klienta
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            print(f"Klient: {data}")
            if "***" in data:
                print("Klient zakończył połączenie.")
                break  # Zakończenie połączenia

        # Wysyłanie wiadomości do klienta
        response_message = input("Serwer: ")
        client_socket.send(response_message.encode('utf-8'))
        if "***" in response_message:
            print("Serwer zakończył połączenie.")
            break  # Zakończenie połączenia

except ConnectionResetError:
    print("Połączenie zostało zakończone przez klienta.")
finally:
    # Zamykanie połączeń
    client_socket.close()
    server_socket.close()
