import socket
import sys

def start_client(server_host='localhost', server_port=9090):
    """
    Запускает TCP-клиента, который подключается к серверу, отправляет строки и получает эхо.
    Цикл продолжается до тех пор, пока пользователь не введет 'exit'.
    
    Параметры:
    - server_host: IP-адрес или доменное имя сервера (по умолчанию 'localhost').
    - server_port: Порт сервера (по умолчанию 9090).
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_host, server_port))
        print(f"[INFO] Соединение с сервером {server_host}:{server_port} установлено")
    except socket.error as e:
        print(f"[ERROR] Не удалось подключиться к серверу {server_host}:{server_port}. Ошибка: {e}")
        sys.exit()
    
    try:
        while True:
            user_input = input("Введите строку для отправки на сервер (или 'exit' для выхода): ")
            if not user_input:
                print("[WARNING] Пустая строка не отправляется")
                continue
            data = user_input.encode('utf-8')
            client_socket.sendall(data)
            print(f"[INFO] Отправлено на сервер: {user_input}")
    
            # Прием данных от сервера
            received_data = client_socket.recv(1024)
            if not received_data:
                print("[WARNING] Сервер отключился")
                break
            echoed_message = received_data.decode('utf-8').strip()
            print(f"[INFO] Получено от сервера: {echoed_message}")
    
            if user_input.lower() == 'exit':
                print("[INFO] Завершение работы клиента по команде 'exit'")
                break
    except KeyboardInterrupt:
        print("\n[INFO] Завершение работы клиента по запросу пользователя")
    finally:
        client_socket.close()
        print("[INFO] Соединение с сервером закрыто")

if __name__ == "__main__":
    SERVER_HOST = 'localhost'  # Замените на IP-адрес сервера при необходимости
    SERVER_PORT = 9090
    start_client(SERVER_HOST, SERVER_PORT)