import socket
import threading
import subprocess
import os

class NetCat:
    def __init__(self, ip, port, listen=False):
        self.ip = ip
        self.port = port
        self.listen = listen
        self.current_directory = os.getcwd()

    def run(self):
        if self.listen:
            self.start_server()
        else:
            self.start_client()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, self.port))
        server.listen(5)
        print(f"[*] Listening on {self.ip}:{self.port}")

        while True:
            client_socket, addr = server.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        client_socket.send(f"Connected. Current directory: {self.current_directory}\n".encode())

        while True:
            try:
                client_socket.send(f"{self.current_directory} $ ".encode())
                command = client_socket.recv(1024).decode().strip()
                
                if not command:
                    continue
                
                if command.lower() == "exit":
                    client_socket.send(b"Goodbye!\n")
                    client_socket.close()
                    break
                
                if command.startswith("cd "):
                    directory = command[3:].strip()
                    try:
                        os.chdir(directory)
                        self.current_directory = os.getcwd()
                        response = f"Changed directory to {self.current_directory}\n"
                    except Exception as e:
                        response = f"Error: {str(e)}\n"
                else:
                    response = self.execute_command(command)

                client_socket.send(response.encode())

            except Exception as e:
                client_socket.send(f"Error: {str(e)}\n".encode())
                break

    def execute_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, cwd=self.current_directory)
            return output.decode()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.output.decode()}\n"
        except Exception as e:
            return f"Unexpected error: {str(e)}\n"

    def start_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.ip, self.port))
        print("[*] Connected to the server.")

        while True:
            try:
                prompt = client.recv(1024).decode()
                command = input(prompt)
                client.send(command.encode())

                if command.lower() == "exit":
                    print("[*] Exiting...")
                    break

                response = client.recv(4096).decode()
                print(response, end="")

            except KeyboardInterrupt:
                print("\n[*] Exiting...")
                client.send(b"exit")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                break

        client.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Python NetCat Remote Shell")
    parser.add_argument("-t", "--target", required=True, help="Target IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Port number")
    parser.add_argument("-l", "--listen", action="store_true", help="Listen mode (server)")

    args = parser.parse_args()

    nc = NetCat(args.target, args.port, args.listen)
    nc.run()
