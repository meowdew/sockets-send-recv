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
running = True


def exit_handler(sig, frame):
    print("Client is shutting down...")
    client_socket.close()
    sys.exit(0)


def receive_msg():
    global running
    while running:
        data = client_socket.recv(max_size)
        if not data:
            print(f'No message from server, dropping connection')
            running = False
            client_socket.close()
            sys.exit(0)
        print(f'Received message from server: {data.decode()}')


def send_msg():
    global running
    while running:
        message = input('Please enter your message to server: ')
        if message == 'exit()':
            running = False
            client_socket.close()
            sys.exit(0)
        client_socket.send(message.encode())


def upload_file():
    while True:
        path = input("Please input path of the file: ")
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        if not dirname and not basename:
            print('invalid path, please re-input')
            continue
        client_socket.send(basename.encode())
        try:
            with open(path, 'rb') as f:
                client_socket.send('OK'.encode())
                while True:
                    data = f.read(max_size)
                    if not data:
                        break
                    client_socket.send(data)
                    print(f'Sent {len(data)} bytes of file data')
                client_socket.send(b'EOF_MARKER')
                print('File sent successfully')
        except IOError as e:
            client_socket.send('ERROR'.encode())


def download_file():
    while True:
        path = input("Please input path of the file: ")
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        if not dirname and not basename:
            print('invalid path, please re-input')
            continue
        client_socket.send(path.encode())
        message = client_socket.recv(max_size).decode()
        if message == 'OK':
            with open(basename, 'wb') as f:
                while True:
                    data = client_socket.recv(max_size)
                    if not data or data == b'EOF_MARKER':
                        break
                    print(f'Received {len(data)} bytes from server')
                    f.write(data)
                f.flush()
                print('File Received successfully')
        elif message == 'ERROR':
            print(f'Failed to access such a file, please try again')
            continue


def menu():
    print('-------------SOCKET SEND & RECEIVE--------------')
    print('* Please Choose an option')
    print('1. SEND/RECEIVE MESSAGE')
    print('2. UPLOAD FILE')
    print('3. DOWNLOAD FILE')
    print('------------------------------------------------')
    option = input('* ')
    option = int(option)
    if option == 1 or option == 2 or option == 3:
        return option
    return None


if __name__ == '__main__':
    client_socket.connect((host_name, port))
    signal.signal(signal.SIGINT, exit_handler)
    op = menu()
    if op == 1:
        client_socket.send('MESSAGE'.encode())
        recv_thread = threading.Thread(target=receive_msg)
        send_thread = threading.Thread(target=send_msg)
        recv_thread.start()
        send_thread.start()
        recv_thread.join()
        send_thread.join()
    elif op == 2:
        client_socket.send('UPLOAD'.encode())
        upload_file()
    elif op == 3:
        client_socket.send('DOWNLOAD'.encode())
        download_file()
    else:
        pass
