import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading
import logging
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def execute(cmd):
    """Menjalankan command shell dan mengembalikan outputnya"""
    cmd = cmd.strip()
    if not cmd:
        return "No command entered."
    try:
        output = subprocess.check_output(shlex.split(cmd),stderr = subprocess.STDOUT)
        return output.decode(errors="ignore")
    except Exception as e:
        return f'Failed to execute command: {e}'

class NetCat : 
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self) :
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self) :
        """Mode Client : Menghubungkan ke server dan mengirim data"""
        try:
            self.socket.connect((self.args.target, self.args.port))
            self.socket.settimeout(2) # set timeout agar tidak menunggu tanpa batas
            if self.buffer:
                self.socket.send(self.buffer)
        
            while True:
                try:
                    response = self.socket.recv(4096)
                    if not response:
                        break
                    print(response.decode(errors="ignore"), end="")
                    sys.stdout.flush() # memastikan output langsung muncul

                    buffer = input(">")+"\n"
                    self.socket.send(buffer.encode())
                except socket.timeout:
                    pass # jika timeout, lanjutkan loop tanpa error
                except Exception as e:
                    print(f'Error receiving data : {e}')
                    break
        except KeyboardInterrupt :
            print ("User Terminated.")
        finally:
            print("[+] Closing connection ...")
            self.socket.close()

    def listen(self) :
        """Mode Server : Mendengarkan koneksi di port tertentu"""
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        logging.info(f"Listening on {self.args.target}:{self.args.port}...")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True :
                try:
                    client_socket, _= self.socket.accept()
                    print("[+] New connection received!")
                    executor.submit(self.handle, client_socket)
                except KeyboardInterrupt:
                    print("\n[+] Server shutting down!")
                    self.socket.close()
                    sys.exit()

    def handle(self, client_socket):
        """Menangani koneksi dari klien"""
        try:
            if self.args.execute:
                output = execute(self.args.execute)
                client_socket.send(output.encode())

            elif self.args.upload:
                file_buffer = b""
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    file_buffer += data
                with open(self.args.upload, 'wb') as f:
                    f.write(file_buffer)
                client_socket.send(f"Saved file {self.args.upload}\n".encode())
            
            elif self.args.command:
                while True :
                    try :
                        client_socket.send(b"BHP:# ")
                        cmd_buffer = client_socket.recv(4096).decode().strip()
                        if not cmd_buffer:
                            break
                        response = execute(cmd_buffer)
                        client_socket.send(response.encode()+b"\n")
                    except Exception as e:
                        client_socket.send(f"Error : {e}\n".encode())
                        break
        except Exception as e :
            logging.error(f"Connection error : {e}")
        finally:
            logging.info("[+] Closing client connection.")
            client_socket.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool', 
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            '''Example:
               netcat.py -t 192.168.1.108 -p 5555 -l -c #command shell
               netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt #upload to file
               netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat/etc/passwd\" #execute command
               echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 #echo text to server port 135
               netcat.py -t 192.168.1.108 -p 5555 #connect to server
               '''
            ),
        )
    parser.add_argument('-c','--command', action='store_true', help='command shell')
    parser.add_argument('-e','--execute', help='execute specified command')
    parser.add_argument('-l','--listen', action='store_true', help='listen')
    parser.add_argument('-p','--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t','--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u','--upload', help='upload file')

    args = parser.parse_args()
    buffer = sys.stdin.read() if not args.listen else None

    nc = NetCat(args, buffer.encode() if buffer else None)
    nc.run()


