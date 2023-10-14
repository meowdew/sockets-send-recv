#!/usr/bin/python3
import socket
import sys
import signal
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
port = 12345
max_size = 1024
server_socket.bind((host_name, port))
server_socket.listen(3)
running = True


def exit_handler(sig, frame):
    print("Server is shutting down...")
    client_socket.close()
    server_socket.close()
    sys.exit(0)


def receive(socket):
    global running
    while running:
        data = client_socket.recv(max_size)
        if not data:
            print(f'No message from client, dropping connection')
            running = False
            client_socket.close()
            sys.exit(0)
        print(f'Received message from client: {data.decode()}')


def send(socket):
    global running
    while running:
        message = input('Please enter your message to client: ')
        if message == 'exit()':
            print('Exiting server')
            running = False
            client_socket.close()
            sys.exit(0)
        client_socket.send(message.encode())


def recv_file(socket):
    while True:
        filename = client_socket.recv(max_size).decode()
        message = client_socket.recv(max_size).decode()
        if message == 'OK':
            with open(filename, 'wb') as f:
                while True:
                    data = socket.recv(max_size)
                    if not data or data == b'EOF_MARKER':
                        break
                    print(f'Received {len(data)} bytes of file data')
                    f.write(data)
                f.flush()
                print("File received successfully")
        elif message == 'ERROR':
            print('file access error in client')


def send_file(socket):
    while True:
        path = client_socket.recv(max_size).decode()
        try:
            with open(path, 'rb') as f:
                client_socket.send('OK'.encode())
                while True:
                    data = f.read(max_size)
                    if not data: break
                    client_socket.send(data)
                    print(f'Sent {len(data)} bytes of file data')
                client_socket.send(b'EOF_MARKER')
                print('File sent successfully')
        except IOError as e:
            client_socket.send('ERROR'.encode())


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_handler)
    print('Server is running and waiting for connections...')
    client_socket, addr = server_socket.accept()
    print(f'Connected Address is {str(addr)}')
    mode = client_socket.recv(max_size).decode()
    if mode == 'MESSAGE':
        recv_thread = threading.Thread(target=receive, args=[client_socket, ])
        send_thread = threading.Thread(target=send, args=[client_socket, ])
        recv_thread.start()
        send_thread.start()
        recv_thread.join()
        send_thread.join()
    elif mode == 'UPLOAD':
        recv_file(client_socket)
    elif mode == 'DOWNLOAD':
        send_file(client_socket)
    else:
        pass
