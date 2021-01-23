
import threading
import sys
import requests
import time
import json
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
        self.url = None
        logging.info(f'New thread started for {ip}:{port}')
        # create the server socket
        # TCP socket

        logging.info("socket generated")
        # bind the socket to our local address

        self.run()

    def ConvertSecondsToBytes(self, numSeconds):
        return numSeconds*maxSendRateBytesPerSecond

    def ConvertBytesToSeconds(self, numBytes):
        return float(numBytes)/maxSendRateBytesPerSecond

    def WaitForCert(self):
        self.url = input("URL from person sending file: ")
        data = requests.get(f'{self.url}-cert')
        payload = data.json()
        if "certSize" not in payload and "pubKey" not in payload:
            print("cert payload keys invalid")
            sys.exit()
        elif int(payload["certSize"]) != len(payload["pubKey"]):
            print("Cert not same size as certsize")

            sys.exit()
        return payload["pubKey"]

    def send_key(self, cert):
        key = self.ciph.key
        encryptedKey = encryptKey(key, cert)
        base64_key = base64.b64encode(encryptedKey)
        encryptedIV = encryptKey(self.ciph.iv, cert)
        base64_iv = base64.b64encode(encryptedIV)
        encryptedKeySize = len(encryptedKey)
        encryptedIVSize = len(encryptedIV)
        self.payload = {
            'encryptedKeySize': encryptedKeySize,
            'encryptedIVSize': encryptedIVSize,
            'key': base64_key.decode("utf-8"),
            'iv': base64_iv.decode("utf-8")
        }
        url = f'{self.url}-key'
        _ = requests.post(url, data=json.dumps(self.payload))

    def run(self):
        logging.info("Listening for incoming connections...")
        cert = self.WaitForCert()
        self.send_key(cert)
        data = requests.get(f'{self.url}')
        payload = data.json()
        fn = f'{self.port}-{os.path.basename(payload["filename"])}'
        encFN = fn + ".enc"
        encrypted_file_data = ""
        with open(encFN, "wb") as f:
            f.write(bytes(payload["file"], 'utf-8'))
        with open(encFN, "rb") as f:
            data = f.read()
            encrypted_file_data = base64.b64decode(data)
        with open(fn, "wb") as f:
            f.write(self.ciph.decrypt(encrypted_file_data))
        os.remove(encFN)

        # # We'll add to this tally as we send() bytes, and subtract from
        # # at the schedule specified by (maxSendRateBytesPerSecond)
        # bytesAheadOfSchedule = 0
        # prevTime = None
        # # if below code is executed, that means the sender is connected
        # logging.info(f"{self.ip}:{self.port} is connected.")
        # # receive the file infos
        # # receive using client socket, not server socket
        # received = self.clientsock.recv(BUFFER_SIZE).decode()
        # _, filename, filesize, data = received.split(SEPARATOR)
        # # remove absolute path if there is
        # filename = f"{self.port}-{os.path.basename(filename)}"
        # enc_filename = filename + ".enc"
        # # convert to integer
        # filesize = int(filesize)
        # data = data.encode()
        # filesize -= len(data)

        # # start receiving the file from the socket
        # # and writing to the file stream
        # if not received:

        #     print("not received")
        #     sys.exit()
        # elif received == 'killsrv':

        #     print("killsrv")
        #     sys.exit()
        # else:
        #     print("receiving")
        #     progress = tqdm.tqdm(range(
        #         filesize), f"Receiving {enc_filename}", unit="B", unit_scale=True, unit_divisor=1024)
        #     data_remaining = filesize
        #     with open(enc_filename, "wb") as f:
        #         f.write(data)
        #         while data_remaining > 0:
        #             now = time.time()
        #             prevTime = now
        #             # read 1024 bytes from the socket (receive)
        #             if data_remaining < BUFFER_SIZE:
        #                 bytes_read =
        #             else:
        #                 bytes_read =
        #             data_remaining -= len(bytes_read)

        #             # write to the file the bytes we just received
        #             f.write(bytes_read)
        #             # update the progress bar
        #             progress.update(len(bytes_read))

        #     encrypted_file_data = ""
        #     with open(enc_filename, "rb") as f:
        #         data = f.read()
        #         encrypted_file_data = base64.b64decode(data)

        #     with open(filename, "wb") as f:
        #         f.write(self.ciph.decrypt(encrypted_file_data))


        #     os.remove(enc_filename)
 # device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# We'll limit ourself to a 40KB/sec maximum send rate
maxSendRateBytesPerSecond = (40*1024)
