import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


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
        padder = padding.PKCS7(algorithms.AES(self.key).block_size).padder()
        padded_data = padder.update(bytes_to_encrypt) + padder.finalize()
        encryptor = self.cipher.encryptor()
        return encryptor.update(padded_data) + encryptor.finalize()

    def decrypt(self, bytes_to_decrypt):
        padder = padding.PKCS7(algorithms.AES(self.key).block_size).unpadder()
        decryptor = self.cipher.decryptor()
        decrypted_data = decryptor.update(bytes_to_decrypt)
        return padder.update(decrypted_data) + padder.finalize()
