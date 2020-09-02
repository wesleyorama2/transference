import socket
import tqdm
import threading
import concurrent.futures
import logging
import os
import time


class SendFile(threading.Thread):

    server_data = None

    def __init__(self, server_ip, server_port, file_name, clientsock):
        threading.Thread.__init__(self)
        self.server_ip = server_ip
        self.server_port = server_port
        self.clientsock = clientsock
        self.file_name = file_name
        self.server_data = SendFile.server_data
        logging.info(f'New thread connecting to {server_ip}:{server_port}')
        self.run()

    def run(self):
        logging.info("starting sendfile")
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096  # send 4096 bytes each time step
        filesize = os.path.getsize(self.file_name)

        logging.info(f"[+] Connecting to {self.server_ip}:{self.server_port}")
        logging.info("[+] Connected.")

        # send the filename and filesize
        self.clientsock.send(f"{self.file_name}{SEPARATOR}{filesize}".encode())

        # start sending the file
        progress = tqdm.tqdm(range(
            filesize), f"Sending {self.file_name}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(self.file_name, "rb") as f:
            for _ in progress:
                if self.server_data:
                    logging.info("In in_data")
                    time.sleep(float(self.server_data))
                else:
                    # read the bytes from the file
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        # file transmitting is done
                        break
                    # we use sendall to assure transimission in
                    # busy networks
                    s.sendall(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))
        # # close the socket
        # s.close()


class Receive(threading.Thread):
    def __init__(self, clientsock):
        threading.Thread.__init__(self)
        self.clientsock = clientsock
        self.run()

    def run(self):
        logging.info("starting receive")
        in_data = self.clientsock.recv(1024)
        logging.info("past recv")
        SendFile.server_data = in_data.decode()


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

# the ip address or hostname of the server, the receiver
host = "127.0.0.1"
# the port, let's use 5001
port = 5001
# the name of file we want to send, make sure it exists
filename = input()
# get the file size

# create the client socket
s = socket.socket()
s.connect((host, port))


with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    if s.recv(1024):
        executor.submit(Receive(s))
    else:
        executor.submit(SendFile(host, port, filename, s))
