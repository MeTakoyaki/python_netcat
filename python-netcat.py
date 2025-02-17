import socket
import subprocess
import threading
import sys
import argparse
import os

# Fungsi untuk mengeksekusi perintah yang diterima
def execute_command(command, current_directory):
    if command.startswith("cd "):
        # Fungsi khusus untuk menangani perintah `cd`
        try:
            directory = command[3:].strip()
            os.chdir(directory)  # Mengubah direktori
            current_directory = os.getcwd()  # Mendapatkan direktori baru
            return f"Changed directory to {current_directory}"
        except Exception as e:
            return f"Error changing directory: {str(e)}"
    
    # Perintah lainnya
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, cwd=current_directory)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode()}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Fungsi untuk menangani setiap koneksi client
def handle_client(client_socket):
    print("[*] Client connected.")
    
    current_directory = os.getcwd()  # Direktori kerja awal

    while True:
        try:
            # Menerima perintah dari client
            client_socket.send(f"{current_directory} $ ".encode())  # Menampilkan prompt dengan direktori
            command = client_socket.recv(1024).decode().strip()

            if not command:
                break

            print(f"[*] Executing command: {command}")

            # Mengeksekusi perintah dan mengirimkan hasilnya ke client
            result = execute_command(command, current_directory)
            
            # Jika berhasil mengubah direktori, update direktori aktif
            if command.startswith("cd "):
                current_directory = os.getcwd()
            
            # Hanya kirimkan hasil perintah jika berbeda dari hasil sebelumnya
            client_socket.send(result.encode())

        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

# Fungsi untuk server mode
def server_mode(host, port):
    # Membuat socket server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # Menangani client dalam thread terpisah
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Fungsi untuk client mode
def client_mode(host, port):
    # Membuat socket client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("[*] Connected to the server.")

    while True:
        # Mengambil input perintah dari user
        command = input("Enter command to execute (or 'exit' to quit): ")

        if command.lower() == 'exit':
            print("[*] Exiting...")
            break

        # Mengirimkan perintah ke server
        client.send(command.encode())

        # Menerima dan menampilkan hasil perintah
        result = client.recv(4096).decode()
        print(f"[*] Output:\n{result}")

    client.close()

# Fungsi utama untuk memilih mode (server atau client)
def main():
    parser = argparse.ArgumentParser(description="NetCat Remote Command Executor")
    parser.add_argument('-m', '--mode', choices=['server', 'client'], required=True, help="Mode to run: 'server' or 'client'")
    parser.add_argument('-t', '--target', default='localhost', help="Target IP (for client) or host to listen (for server)")
    parser.add_argument('-p', '--port', type=int, default=5555, help="Port to connect/listen on")

    args = parser.parse_args()

    if args.mode == 'server':
        # Menjalankan server mode
        server_mode(args.target, args.port)
    elif args.mode == 'client':
        # Menjalankan client mode
        client_mode(args.target, args.port)

if __name__ == '__main__':
    main()
