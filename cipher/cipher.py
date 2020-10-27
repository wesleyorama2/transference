import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class cipher():
    def __init__(self, key=None, iv=None):
        if key == None:
            self.key = os.urandom(32)
        else:
            self.key = key
        if iv == None:
            self.iv = os.urandom(16)
        else:
            self.iv = iv

        self.cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))

    def encrypt(self, bytes_to_encrypt):
        encryptor = self.cipher.encryptor()
        return encryptor.update(bytes_to_encrypt) + encryptor.finalize()

    def decrypt(self, bytes_to_decrypt):
        decryptor = self.cipher.decryptor()
        return decryptor.update(bytes_to_decrypt) + decryptor.finalize()
