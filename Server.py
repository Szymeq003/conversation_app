import socket
import threading
from datetime import datetime

# Lista połączonych klientów
clients = {}
lock = threading.Lock()


def save_message_to_user_history(user_name, message):
    """Zapisuje wiadomość do pliku bez dodatkowego znacznika czasu (używamy już sformatowanej wiadomości)."""
    file_name = f"historia_{user_name}.txt"
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(message + "\n")


def get_timestamp():
    """Zwraca aktualny czas w formacie [HH:MM:SS]."""
    return datetime.now().strftime("[%H:%M:%S]")


def send_user_chat_history(client_socket, user_name):
    """Wysyła historię czatu do użytkownika po połączeniu."""
    file_name = f"historia_{user_name}.txt"
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            history = file.read()
        if history:
            client_socket.send(f"\nTwoja historia czatu:\n{history}".encode('utf-8'))
        else:
            client_socket.send("\nTwoja historia czatu jest pusta.".encode('utf-8'))
    except FileNotFoundError:
        client_socket.send("\nTwoja historia czatu jest pusta.".encode('utf-8'))


def send_to_client(target_name, message, sender_socket):
    """Wysyła wiadomość prywatną do jednego użytkownika, dodając znacznik czasu."""
    timestamped_message = f"{get_timestamp()} {message}"
    with lock:
        target_socket = next((sock for sock, name in clients.items() if name == target_name), None)
    if target_socket:
        try:
            target_socket.send(timestamped_message.encode('utf-8'))
            # Zapisujemy wiadomość w historii obu użytkowników
            save_message_to_user_history(clients[sender_socket], f"(Do {target_name}): {message}")
            save_message_to_user_history(target_name, f"(Od {clients[sender_socket]}): {message}")
        except:
            target_socket.close()
            with lock:
                del clients[target_socket]
    else:
        sender_socket.send(f"Użytkownik {target_name} nie został znaleziony.".encode('utf-8'))


def list_users(client_socket):
    """Wysyła listę aktualnie podłączonych użytkowników do klienta."""
    with lock:
        users = ", ".join(clients.values())
    if users:
        client_socket.send(f"Aktualni użytkownicy: {users}".encode('utf-8'))
    else:
        client_socket.send("Brak aktywnych użytkowników.".encode('utf-8'))


def send_to_all(sender_socket, message):
    """Wysyła wiadomość do wszystkich użytkowników, dodając znacznik czasu."""
    sender_name = clients[sender_socket]
    timestamped_message = f"{get_timestamp()} (Broadcast od {sender_name}): {message}"

    with lock:
        for client_socket in clients.keys():
            if client_socket != sender_socket:
                try:
                    client_socket.send(timestamped_message.encode('utf-8'))
                except:
                    print(f"Błąd podczas wysyłania do {clients[client_socket]}")

    # Zapisujemy broadcast do historii nadawcy
    save_message_to_user_history(sender_name, f"(Broadcast): {message}")


def handle_client(client_socket, client_address):
    """Obsługuje jednego klienta."""
    try:
        client_socket.send("Podaj swoją nazwę użytkownika: ".encode('utf-8'))
        user_name = client_socket.recv(1024).decode('utf-8').strip()
        send_user_chat_history(client_socket, user_name)

        with lock:
            clients[client_socket] = user_name

        client_socket.send(
            f"Witaj, {user_name}! Możesz teraz wysyłać wiadomości do innych użytkowników.".encode('utf-8'))

        while True:
            data = client_socket.recv(1024).decode('utf-8')

            if data == "*u":
                list_users(client_socket)

            elif data.startswith("/msg "):
                parts = data.split(" ", 2)
                if len(parts) < 3:
                    client_socket.send(
                        "Nieprawidłowa składnia. Użyj: /msg <nazwa_użytkownika> <wiadomość>".encode('utf-8'))
                else:
                    target_name, message = parts[1], parts[2]
                    send_to_client(target_name, f"(Priv od {clients[client_socket]}): {message}", client_socket)

            elif data.startswith("/all "):
                message = data[5:].strip()
                if message:
                    send_to_all(client_socket, message)
                else:
                    client_socket.send("Nie można wysłać pustej wiadomości. Użyj: /all <wiadomość>".encode('utf-8'))

            elif data == "***":
                break

            else:
                client_socket.send(
                    "\nNieprawidłowa komenda. Użyj *u, aby wyświetlić użytkowników, lub /msg, aby wysłać wiadomość.".encode(
                        'utf-8'))

    except ConnectionResetError:
        print(f"Połączenie z {client_address} zostało zakończone.")
    finally:
        with lock:
            if client_socket in clients:
                del clients[client_socket]
        client_socket.close()


# Konfiguracja serwera
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5678))
server_socket.listen(5)
print("Serwer nasłuchuje...")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Połączono z {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
finally:
    server_socket.close()
