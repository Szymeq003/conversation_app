import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except ConnectionResetError:
            print("Połączenie z serwerem zostało zakończone.")
            break

def send_messages(client_socket):
    # Pierwsze wysyłanie: podanie nazwy użytkownika
    user_name = input()
    client_socket.send(user_name.encode('utf-8'))

    print("\nDostępne komendy:")
    print("*u - wyświetlenie listy użytkowników")
    print("/msg <nazwa_użytkownika> <wiadomość> - wysłanie wiadomości prywatnej")
    print("*** - zakończenie połączenia")
    print("/all - wysłanie wiadomości do wszystkich użytkowników\n")
    print("\nWpisz komendę: \n")

    while True:
        message = input()

        if message == "***":
            client_socket.send(message.encode('utf-8'))
            print("Zakończono połączenie.")
            client_socket.close()
            break
        client_socket.send(message.encode('utf-8'))

# Konfiguracja klienta
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5678))
print("Połączono z serwerem.")

# Uruchamianie wątków dla odbioru i wysyłania wiadomości
recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
send_thread = threading.Thread(target=send_messages, args=(client_socket,))

recv_thread.start()
send_thread.start()

recv_thread.join()
send_thread.join()

client_socket.close()
