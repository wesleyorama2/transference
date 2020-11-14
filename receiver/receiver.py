import socket
import threading
import sys
import time
import logging
import tqdm
import os
import base64
from certs.certs import encryptKey


class Receiver(threading.Thread):

    def __init__(self, ip, port, ciph):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.ciph = ciph
        logging.info(f'New thread started for {ip}:{port}')
        # create the server socket
        # TCP socket
        sock = socket.socket()
        logging.info("socket generated")
        # bind the socket to our local address
        sock.bind((self.ip, self.port))
        sock.listen(5)
        logging.info("socket started")
        (sock_tuple) = sock.accept()
        logging.info("socket accepted")
        self.clientsock = sock_tuple[0]
        self.run()

    def ConvertSecondsToBytes(self, numSeconds):
        return numSeconds*maxSendRateBytesPerSecond

    def ConvertBytesToSeconds(self, numBytes):
        return float(numBytes)/maxSendRateBytesPerSecond

    def WaitForCert(self):
        received = self.clientsock.recv(BUFFER_SIZE).decode()
        prefix, certsize, cert = received.split(SEPARATOR)
        if prefix != "cert":
            print("not cert prefix")
            self.clientsock.close()
            sys.exit()
        elif int(certsize) != len(cert):
            print("Cert not same size as certsize")
            self.clientsock.close()
            sys.exit()
        return cert

    def run(self):
        logging.info("Listening for incoming connections...")
        cert = self.WaitForCert()
        encryptedKey = encryptKey(self.ciph.key, cert)
        base64_key = base64.b64encode(encryptedKey)
        self.clientsock.send(
            f"key{SEPARATOR}{len(self.ciph.key)}{SEPARATOR}{base64_key.decode('UTF-8')}".encode())
        encryptedIV = encryptKey(self.ciph.iv, cert)
        base64_iv = base64.b64encode(encryptedIV)
        self.clientsock.send(
            f"iv{SEPARATOR}{len(self.ciph.iv)}{SEPARATOR}{base64_iv.decode('UTF-8')}".encode())
        # We'll add to this tally as we send() bytes, and subtract from
        # at the schedule specified by (maxSendRateBytesPerSecond)
        bytesAheadOfSchedule = 0
        prevTime = None
        # if below code is executed, that means the sender is connected
        logging.info(f"{self.ip}:{self.port} is connected.")
        # receive the file infos
        # receive using client socket, not server socket
        received = self.clientsock.recv(BUFFER_SIZE).decode()
        _, filename, filesize, data = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = f"{self.port}-{os.path.basename(filename)}"
        enc_filename = filename + ".enc"
        # convert to integer
        filesize = int(filesize)
        data = data.encode()
        filesize -= len(data)

        # start receiving the file from the socket
        # and writing to the file stream
        if not received:
            self.clientsock.close()
            print("not received")
            sys.exit()
        elif received == 'killsrv':
            self.clientsock.close()
            print("killsrv")
            sys.exit()
        else:
            print("receiving")
            progress = tqdm.tqdm(range(
                filesize), f"Receiving {enc_filename}", unit="B", unit_scale=True, unit_divisor=1024)
            data_remaining = filesize
            with open(enc_filename, "wb") as f:
                f.write(data)
                while data_remaining > 0:
                    now = time.time()
                    prevTime = now
                    # read 1024 bytes from the socket (receive)
                    if data_remaining < BUFFER_SIZE:
                        bytes_read = self.clientsock.recv(data_remaining)
                    else:
                        bytes_read = self.clientsock.recv(BUFFER_SIZE)
                    data_remaining -= len(bytes_read)

                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))

            encrypted_file_data = ""
            with open(enc_filename, "rb") as f:
                data = f.read()
                encrypted_file_data = base64.b64decode(data)

            with open(filename, "wb") as f:
                f.write(self.ciph.decrypt(encrypted_file_data))


            os.remove(enc_filename)




 # device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# We'll limit ourself to a 40KB/sec maximum send rate
maxSendRateBytesPerSecond = (40*1024)
