import socket
import sys
import os

def print_working_directory():
    print("Current working directory:", os.getcwd())
    print("Files in the working directory:")
    for file in os.listdir():
        print(" -", file)

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <server_machine> <server_port>")
        return 1

    server_machine = sys.argv[1]
    server_port = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_machine, server_port))

    print_working_directory()
    while True:
        command = input("ftp> ")

        cmd_parts = command.split(' ')
        main_cmd = cmd_parts[0]
        client_socket.send(main_cmd.encode())

        if main_cmd == "quit":
            break
        elif main_cmd == "get" or main_cmd == "put" or main_cmd == "ls":
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.bind(('0.0.0.0', 0))

            data_port = data_socket.getsockname()[1]
            client_socket.send(data_port.to_bytes(2, 'big'))

            data_socket.listen(1)
            data_conn, _ = data_socket.accept()

            if main_cmd == "get":
                file_name = cmd_parts[1]
                client_socket.send(file_name.encode())

                status = client_socket.recv(1024).decode()
                if status == "File not found":
                    print("File not found on the server.")
                else:
                    with open(file_name, "wb") as file:
                        while True:
                            file_data = client_socket.recv(1024)
                            # Check for sentinel value to break the loop
                            if b"__end_of_file__" in file_data:
                                file_data = file_data.replace(b"__end_of_file__", b"")
                                file.write(file_data)
                                break
                            file.write(file_data)

            elif main_cmd == "put":
                file_name = cmd_parts[1]
                client_socket.send(file_name.encode())

                try:
                    with open(file_name, "rb") as file:
                        while True:
                            file_data = file.read(1024)
                            if not file_data:
                                break
                            #data_conn.sendall(file_data)
                            client_socket.sendall(file_data)
                    # Sending sentinel value to signal the end of the transfer
                    client_socket.send(b"__end_of_file__")
                except FileNotFoundError:
                    print(f"File '{file_name}' not found in the client's directory.")

            elif main_cmd == "ls":
                files = data_conn.recv(1024).decode()
                print("Files on the server:")
                print(files)

            data_conn.close()
            data_socket.close()

if __name__ == "__main__":
    main()