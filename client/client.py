#!/usr/bin/python3
import socket
import sys
import signal
import threading
import os

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
port = 12345
max_size = 1024

def exit_handler(sig, frame):
    print("Client is shutting down...")
    client_socket.close()
    sys.exit(0)

def receive_msg():
    while True:
        data = client_socket.recv(max_size)
        if not data:
            print(f'No message from server')
            break
        print(f'Received message from server: {data.decode()}')

def send_msg():
    while True:
        message = input('Please enter your message to server: ')
        if message is None or message == 'exit':
            print('Exiting client')
            sys.exit(0)
        client_socket.send(message.encode())

def send_file():
    while True:
        path = input("Please input path of the file: ")
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        if not dirname and not basename:
            print('invalid path, please re-input')
            continue
        client_socket.send(basename.encode())
        with open(path, 'rb') as f:
            while True:
                line = f.read(max_size)
                if line:
                    print('file bytes sent')
                    client_socket.send(line)
                else: break



def menu():
    print('-------------SOCKET SEND & RECEIVE--------------')
    print('* Please Choose an option')
    print('1. SEND/RECEIVE MESSAGE')
    print('2. SEND/RECEIVE FILE')
    option = input('* ')
    option = int(option)
    if option == 1 or option == 2:
        return option
    return None

if __name__ == '__main__':
    client_socket.connect((host_name, port))
    signal.signal(signal.SIGINT, exit_handler)
    op = menu()
    if op == 1:
        client_socket.send('message mode'.encode())
        recv_thread = threading.Thread(target=receive_msg)
        send_thread = threading.Thread(target=send_msg)
        recv_thread.start()
        send_thread.start()
        recv_thread.join()
        send_thread.join()
    elif op == 2:
        client_socket.send('file mode'.encode())
        send_file()
        pass
    else:
        pass


