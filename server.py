import socket
import threading
import sys
import concurrent.futures
import time
import logging
import tqdm
import os


class ClientThread(threading.Thread):

    def ConvertSecondsToBytes(self, numSeconds):
        return numSeconds*maxSendRateBytesPerSecond

    def ConvertBytesToSeconds(self, numBytes):
        return float(numBytes)/maxSendRateBytesPerSecond

    def __init__(self, ip, port, clientsock):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        logging.info(f'New thread started for {ip}:{port}')
        self.run()

    def run(self):
        # We'll add to this tally as we send() bytes, and subtract from
        # at the schedule specified by (maxSendRateBytesPerSecond)
        bytesAheadOfSchedule = 0
        prevTime = None
        # if below code is executed, that means the sender is connected
        logging.info(f"{ip}:{port} is connected.")
        # receive the file infos
        # receive using client socket, not server socket
        received = clientsock.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = f"{port}-{os.path.basename(filename)}"
        # convert to integer
        filesize = int(filesize)

        # start receiving the file from the socket
        # and writing to the file stream
        if not received:
            clientsock.close()
            sys.exit()
        elif received == 'killsrv':
            clientsock.close()
            sys.exit()
        else:
            progress = tqdm.tqdm(range(
                filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "wb") as f:
                for _ in progress:
                    now = time.time()
                    if (prevTime != None):
                        bytesAheadOfSchedule -= self.ConvertSecondsToBytes(
                            now-prevTime)
                    prevTime = now
                    # read 1024 bytes from the socket (receive)
                    bytes_read = clientsock.recv(BUFFER_SIZE)
                    if (len(bytes_read) > 0):
                        bytesAheadOfSchedule += len(bytes_read)
                        if (bytesAheadOfSchedule > 0):
                            time.sleep(self.ConvertBytesToSeconds(
                                bytesAheadOfSchedule))
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

# create the server socket
# TCP socket
s = socket.socket()

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections

threads = []

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

s.listen(5)
logging.info("Listening for incoming connections...")
(clientsock, (ip, port)) = s.accept()


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.submit(ClientThread(ip, port, clientsock))
