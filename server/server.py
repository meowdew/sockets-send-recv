#!/usr/bin/python3
import socket
import sys
import signal

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
port = 12345
server_socket.bind((host_name, port))
server_socket.listen(3)

def exit_handler(sig, frame):
    print("Server is shutting down...")
    client_socket.close()
    server_socket.close()
    sys.exit(0)



if __name__ == '__main__':
    print('Server is running and waiting for connections...')
    client_socket, addr = server_socket.accept()
    print(f'Connected Address is {str(addr)}')
    buffer = 'hello'
    buffer_max_size = 256
    while True:
        signal.signal(signal.SIGINT, exit_handler)
        data = client_socket.recv(256)
        if data is None:
            print('Error while receiving data')
            sys.exit(0)
        print(f"Server: received data from client --> {data.decode()}")
        client_socket.send('Success!'.encode())
