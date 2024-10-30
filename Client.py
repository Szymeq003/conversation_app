import socket

# Tworzenie gniazda klienckiego
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Konfiguracja adresu i portu serwera
server_address = ('192.168.0.89', 5678)

try:
    # Nawiązywanie połączenia z serwerem
    client_socket.connect(server_address)
    print("Połączono z serwerem.")

    while True:
        # Wysyłanie wiadomości do serwera
        message = input("Klient: ")
        client_socket.send(message.encode('utf-8'))
        if "***" in message:
            print("Klient zakończył połączenie.")
            break  # Zakończenie połączenia

        # Odbieranie wiadomości od serwera
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Serwer: {data}")
        if "***" in data:
            print("Serwer zakończył połączenie.")
            break  # Zakończenie połączenia

except ConnectionResetError:
    print("Połączenie zostało zakończone przez serwer.")
finally:
    # Zamykanie gniazda
    client_socket.close()
