import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class cipher():
    def __init__(self):
        self.key = os.urandom(32)
        self.iv = os.urandom(16)
        self.cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))

    def encrypt(bytes_to_encrypt):
        encryptor = self.cipher.encryptor()
        return encryptor.update(bytes_to_encrypt) + encryptor.finalize()

    def decrypt(bytes_to_decrypt):
        decryptor = self.cipher.decryptor()
        return dectryptor.update(bytes_to_decrypt) + decryptor.finalize()
