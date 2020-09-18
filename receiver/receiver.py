import socket
import threading
import sys
import time
import logging
import tqdm
import os


class Receiver(threading.Thread):

    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        logging.info(f'New thread started for {ip}:{port}')
        # create the server socket
        # TCP socket
        sock = socket.socket()
        # bind the socket to our local address
        sock.bind((self.ip, self.port))
        sock.listen(5)
        (sock_tuple) = sock.accept()
        self.clientsock = sock_tuple[0]
        self.run()

    def ConvertSecondsToBytes(self, numSeconds):
        return numSeconds*maxSendRateBytesPerSecond

    def ConvertBytesToSeconds(self, numBytes):
        return float(numBytes)/maxSendRateBytesPerSecond

    def run(self):
        logging.info("Listening for incoming connections...")
        # We'll add to this tally as we send() bytes, and subtract from
        # at the schedule specified by (maxSendRateBytesPerSecond)
        bytesAheadOfSchedule = 0
        prevTime = None
        # if below code is executed, that means the sender is connected
        logging.info(f"{self.ip}:{self.port} is connected.")
        # receive the file infos
        # receive using client socket, not server socket
        received = self.clientsock.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = f"{self.port}-{os.path.basename(filename)}"
        # convert to integer
        filesize = int(filesize)

        # start receiving the file from the socket
        # and writing to the file stream
        if not received:
            self.clientsock.close()
            sys.exit()
        elif received == 'killsrv':
            self.clientsock.close()
            sys.exit()
        else:
            progress = tqdm.tqdm(range(
                filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "wb") as f:
                for _ in progress:
                    now = time.time()
                    prevTime = now
                    # read 1024 bytes from the socket (receive)
                    bytes_read = self.clientsock.recv(BUFFER_SIZE)
                    if not bytes_read:
                        # nothing is received
                        # file transmitting is done
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))


 # device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# We'll limit ourself to a 40KB/sec maximum send rate
maxSendRateBytesPerSecond = (40*1024)