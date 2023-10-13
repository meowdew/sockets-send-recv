#!/usr/bin/python3
import socket
import sys
import signal

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
port = 12345

def exit_handler(sig, frame):
    print("Server is shutting down...")
    client_socket.close()
    sys.exit(0)


if __name__ == '__main__':
    client_socket.connect((host_name, port))
    while True:
        signal.signal(signal.SIGINT, exit_handler)
        message = input("Please enter your message sending to server: ")
        if message is None or message == 'exit':
            print('Stopping client...')
            sys.exit(0)
        client_socket.send(message.encode())
        data = client_socket.recv(1024)
        if data is None:
            print('Received 0 bytes from server')
        print(f'Received message from server {data.decode()}')
