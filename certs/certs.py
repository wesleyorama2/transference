#!/usr/bin/env python

import datetime
import os
import sys
import random
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key


class certs():
    KEY_LENGTH = 8192

    def __init__(self, key_size=KEY_LENGTH):
        self.key_size = key_size

    def generate(self):
        self.key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
        )

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u"transference"),
        ])
        self.cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            self.key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=10)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(u"tranference")]),
            critical=False,
        ).sign(self.key, hashes.SHA256())


def encryptKey(key, pubKeyBytes):
    pubKey = load_pem_public_key(pubKeyBytes)
    return pubKey.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
    )


def decryptKey(encyptedKey, privateKey):
    return privateKey.decrypt(
        encyptedKey,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
    )
