import socket
import threading
import os
from pathlib import Path
import sys

def handle_client(client_socket, client_address):
    # Process client commands

    while True:
        command = client_socket.recv(256).decode()

        if command == "quit":
            break
        elif command == "get" or command == "put" or command == "ls":
            data_port = int.from_bytes(client_socket.recv(2), 'big')

            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.connect((client_address[0], data_port))

            if command == "get":
                file_name = client_socket.recv(1024).decode()

                try:
                    with open(file_name, "rb") as file:
                        client_socket.send("File found".encode())
                        while True:
                            file_data = file.read(1024)
                            if not file_data:
                                break
                            client_socket.sendall(file_data)
                    # Sending sentinel value to signal the end of the transfer
                    client_socket.send(b"__end_of_file__")
                except FileNotFoundError:
                    client_socket.send("File not found".encode())

            elif command == "put":
                file_name = client_socket.recv(1024).decode()
                with open(file_name, "wb") as file:
                    while True:
                        file_data = client_socket.recv(1024)
                        # Check for sentinel value to break the loop
                        if b"__end_of_file__" in file_data:
                            file_data = file_data.replace(b"__end_of_file__", b"")
                            file.write(file_data)
                            break
                        file.write(file_data)

            elif command == "ls":
                files = "\n".join(os.listdir())
                data_socket.send(files.encode())

            data_socket.close()
        else:
            client_socket.send(b"Unknown command")

    client_socket.close()

def main():
    if len(sys.argv) != 2:
        return 1

    server_port = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', server_port))
    server_socket.listen(5)
    print("Listening for C")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()