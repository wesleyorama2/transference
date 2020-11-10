import tqdm
import logging
import os
import socket
import sys
import base64

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from certs.certs import decryptKey


class Sender ():
    def __init__(self, host, port, certs):
        self.host = host
        self.port = port
        self.certs = certs
        self.key = None
        self.iv = None
        # create the client socket
        self.s = socket.socket()
        logging.info('initalized sender')
        logging.info(f'using host: {self.host}')
        logging.info(f'using port: {self.port}')
        logging.info(f"Connecting to {self.host}:{self.port}")
        self.s.connect((self.host, self.port))
        logging.info("Client connected.")

    def send_cert(self):
        pub_key = self.certs.cert.public_bytes(serialization.Encoding.PEM)
        cert_size = len(pub_key)
        self.s.send(f"cert{SEPARATOR}{cert_size}{SEPARATOR}".encode())
        self.s.sendall(pub_key)

    def calculate_key_size(self, remainder):
        i = 0
        while i < len(remainder):
            if remainder.startswith(f"iv{SEPARATOR}", i):
                return i-1
            i+=1
        return None

    def wait_for_key(self):
        received = self.s.recv(BUFFER_SIZE).decode()
<<<<<<< HEAD
        prefix, keySize, key = received.split(SEPARATOR)
        if prefix != "key":
            print("not key prefix")
            self.s.close()
            sys.exit()
        d_key = decryptKey(base64.b64decode(key), self.certs.key)
        if int(keySize) != len(d_key):
            self.s.close()
            sys.exit()
        return key

    def wait_for_iv(self):
        received = self.s.recv(BUFFER_SIZE).decode()
        prefix, ivSize, iv = received.split(SEPARATOR)
        if prefix != "iv":
            print("not iv prefix")
            self.s.close()
            sys.exit()
        d_iv = decryptKey(base64.b64decode(iv), self.certs.key)
        if int(ivSize) != len(d_iv):
            print(f"iv {int(ivSize)} not same size as ivsize {len(d_iv)}")
            self.s.close()
            sys.exit()
        return iv
=======
        prefix, keySize, remainder = received.split(SEPARATOR)
        calculatedKeySize = self.calculate_key_size(remainder)
        keySize = int(keySize)
        if prefix != "key":
            print("not key prefix")
            self.s.close()
            sys.exit()
        elif keySize != calculatedKeySize:
            print("incorrect key size")
            print(f"keySize {keySize} != {calculatedKeySize}")
            self.s.close()
            sys.exit()

        self.key = remainder[:keySize]

        prefix, ivSize, self.iv = remainder[keySize:]
        ivSize = int(ivSize)
        if prefix != "iv":
            print("not iv prefix")
            self.s.close()
            sys.exit()
        elif ivSize != len(self.iv):
            print("incorrect iv size")
            self.s.close()
            sys.exit()
        print(self.key)
        print(self.iv)
>>>>>>> 2b564e7cb58c67187a864deb4c33bd04e3b0270f

    def send_file(self, filename):
        # get the file size
        filesize = os.path.getsize(filename)

        # send the filename and filesize
        self.s.send(f"file{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())

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


# # the ip address or hostname of the server, the receiver
# host = "127.0.0.1"
# # the port, let's use 5001
# port = 5001


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # send 4096 bytes each time step


# Figure this out
# with Sender(host, port) as s:
#     s.send_file(input())
