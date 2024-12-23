
import socket
import threading
import sys

def handle_client(conn, addr):
    """
    Обрабатывает соединение с клиентом.
    Принимает данные порциями по 1 КБ и отправляет их обратно (эхо).
    Цикл продолжается до тех пор, пока клиент не отправит 'exit'.
    Выводит служебные сообщения о событиях.
    """
    print(f"[INFO] Подключен клиент {addr}")
    try:
        while True:
            data = conn.recv(1024)  # Прием данных порциями по 1 КБ
            if not data:
                # Данные не получены, клиент отключился
                print(f"[INFO] Клиент {addr} отключился")
                break
            message = data.decode('utf-8').strip()
            print(f"[INFO] Получены данные от клиента {addr}: {message}")
            if message.lower() == 'exit':
                print(f"[INFO] Клиент {addr} отправил команду выхода")
                break
            conn.sendall(data)  # Отправка данных обратно клиенту
            print(f"[INFO] Отправлены данные клиенту {addr}: {message}")
    except ConnectionResetError:
        print(f"[WARNING] Соединение с клиентом {addr} было сброшено")
    finally:
        conn.close()

def start_server(host='', port=9090):
    """
    Запускает TCP-эхо-сервер.
    
    Параметры:
    - host: IP-адрес для прослушивания (по умолчанию все интерфейсы).
    - port: Порт для прослушивания (по умолчанию 9090).
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host, port))
    except socket.error as e:
        print(f"[ERROR] Не удалось привязать сокет к адресу {host}:{port}. Ошибка: {e}")
        sys.exit()
    
    server_socket.listen(5)  # Максимум 5 подключений в очереди
    print(f"[INFO] Сервер запущен и слушает порт {port}")
    
    try:
        while True:
            conn, addr = server_socket.accept()
            # Создаем новый поток для обработки клиента
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.daemon = True  # Поток будет закрыт при завершении основного потока
            client_thread.start()
            print(f"[INFO] Начато прослушивание порта {port}")
    except KeyboardInterrupt:
        print("\n[INFO] Остановка сервера по запросу пользователя")
    finally:
        server_socket.close()
        print("[INFO] Сервер остановлен")

if __name__ == "__main__":
    HOST = ''  # Пустая строка означает, что сервер будет доступен на всех интерфейсах
    PORT = 9090  # Вы можете изменить порт при необходимости
    start_server(HOST, PORT)