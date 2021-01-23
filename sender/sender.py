import tqdm
import uuid
import json
import requests
import logging
import os
import sys
import base64

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from certs.certs import decryptKey
from cipher.cipher import cipher
from time import sleep


class Sender ():
    def __init__(self, host, port, certs):
        self.host = host
        self.port = port
        self.certs = certs
        self.key = None
        self.iv = None
        self.payload = {}
        self.id = None
        # create the client socket
        logging.info('initalized sender')
        logging.info(f'using host: {self.host}')
        logging.info(f'using port: {self.port}')
        logging.info(f"Connecting to {self.host}:{self.port}")

    def generate_code(self):
        print("in generate code")
        self.id = uuid.uuid4()
        logging.critical(
            f"Please give this url to the person receiving the file: {self.host}/{self.id}")

    def send_cert(self):
        self.generate_code()
        pub_key = self.certs.cert.public_bytes(serialization.Encoding.PEM)
        cert_size = len(pub_key)
        self.payload = {
            'certSize': cert_size,
            'pubKey': pub_key.decode("utf-8")
        }
        url = f'{self.host}/{self.id}-cert'
        res = requests.post(url, data=json.dumps(self.payload))
        print(f'send_cert res: {res.text}')

    def calculate_key_size(self, remainder):
        i = 0
        while i < len(remainder):
            if remainder.startswith(f"iv{SEPARATOR}", i):
                return i-1
            i += 1
        return None

    def wait_for_key(self):
        data = requests.get(f'{self.host}/{self.id}-key')
        payload = data.json()

        if "encryptedKeySize" not in payload and "key" not in payload:
            print("key payload keys invalid")
            sys.exit()
        elif int(payload["encryptedKeySize"]) != len(base64.b64decode(payload["key"])):
            print("key not same size as keysize")
            sys.exit()
        if "encryptedIVSize" not in payload and "iv" not in payload:
            print("iv payload keys invalid")
            sys.exit()
        elif int(payload["encryptedIVSize"]) != len(base64.b64decode(payload["iv"])):
            print("iv not same size as ivsize")
            sys.exit()
        return {'key': decryptKey(base64.b64decode(payload["key"]), self.certs.key), 'iv': decryptKey(base64.b64decode(payload["iv"]), self.certs.key)}

    def send_file(self, filename, key):
        encrypted_file = ""
        with open(filename, "rb") as f:
            encrypted_file = cipher(
                key=key["key"], iv=key["iv"]).encrypt(f.read())

        encoded = base64.b64encode(encrypted_file)
        encoded = encoded.decode("UTF-8")

        # get the file size
        filesize = len(encoded)
        self.payload = {
            'filesize': filesize,
            'filename': filename,
            'file': encoded
        }
        url = f'{self.host}/{self.id}'
        _ = requests.post(url, data=json.dumps(self.payload))


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # send 4096 bytes each time step


# Figure this out
# with Sender(host, port) as s:
#     s.send_file(input())
