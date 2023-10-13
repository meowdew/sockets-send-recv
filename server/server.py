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

def exit_handler(sig, frame):
    print("Server is shutting down...")
    client_socket.close()
    server_socket.close()
    sys.exit(0)


def receive(socket):
    while True:
        data = client_socket.recv(max_size)
        if not data:
            print(f'No message from client')
            break
        print(f'Received message from client: {data.decode()}')

def send(socket):
    while True:
        message = input('Please enter your message to client: ')
        if not message or message == 'exit':
            print('Exiting server')
            sys.exit(0)
        client_socket.send(message.encode())

def recv_file(socket):
    while True:
        filename = client_socket.recv(max_size).decode()
        if not filename:
            continue
        with open(filename, 'wb') as f:
            while True:
                data = socket.recv(max_size)
                if data:
                    print('file bytes recv')
                    f.write(data)
                else: break



if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_handler)
    print('Server is running and waiting for connections...')
    client_socket, addr = server_socket.accept()
    print(f'Connected Address is {str(addr)}')
    mode = client_socket.recv(max_size).decode()
    if mode == 'message mode':
        recv_thread = threading.Thread(target=receive, args=[client_socket, ])
        send_thread = threading.Thread(target=send, args=[client_socket, ])
        recv_thread.start()
        send_thread.start()
        recv_thread.join()
        send_thread.join()
    elif mode == 'file mode':
        recv_file(client_socket)
        pass
    else:
        pass





