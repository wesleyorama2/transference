import tqdm
import logging
import os
import socket


class Sender ():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # create the client socket
        self.s = socket.socket()
        logging.info(f'initalized sender')

    def send_file(self, filename):
        # get the file size
        filesize = os.path.getsize(filename)

        logging.info(f"Connecting to {self.host}:{self.port}")
        self.s.connect((self.host, self.port))
        logging.info("Client connected.")

        # send the filename and filesize
        self.s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        # start sending the file
        progress = tqdm.tqdm(range(
            filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            for _ in progress:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in
                # busy networks
                self.s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

    def __del__(self):
        self.s.close()



# the ip address or hostname of the server, the receiver
host = "127.0.0.1"
# the port, let's use 5001
port = 5001


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # send 4096 bytes each time step

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

# Figure this out
# with Sender(host, port) as s:
#     s.send_file(input())
