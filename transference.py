#!/usr/bin/env python3
# https://jtannas-python-skeleton.readthedocs.io/en/latest/source/bin.html
# https://abseil.io/docs/python/guides/flags

from sender.sender import Sender
from receiver.receiver import Receiver
from certs.certs import certs
from cipher.cipher import cipher
import logging
import socket
import concurrent.futures
import threading
from absl import app
from absl import flags

FLAGS = flags.FLAGS

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

flags.DEFINE_string('ip', '127.0.0.1', 'ip of server')
flags.DEFINE_integer('port', 5001, 'port of server')
flags.DEFINE_string('type', 'server', 'server or client')
flags.DEFINE_integer(
    'keysize', 8192, 'Certificate key size for encrypted transmissions. Do not mess with this unless you know what you are doing.')


def run_client(ip, port, certs):
    s = Sender(ip, port, certs)
    s.send_cert()
    key = s.wait_for_key()
    iv = s.wait_for_iv()
    filename = input()
    s.send_file(filename, key, iv)
    pass


def run_server(ip, port, ciph):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(Receiver(ip, port, ciph))


def main(argv):
    c = certs(key_size=FLAGS.keysize)
    c.generate()
    # print(c.key)
    # print(c.cert)
    ciph = cipher()
    # print(c.encrypt_key(ciph.key))
    if FLAGS.type == "server":
        run_server(FLAGS.ip, FLAGS.port, ciph)
    elif FLAGS.type == "client":
        run_client(FLAGS.ip, FLAGS.port, c)
    else:
        print("problems")


if __name__ == '__main__':
    app.run(main)
