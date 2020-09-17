#!/usr/bin/env python3
# https://jtannas-python-skeleton.readthedocs.io/en/latest/source/bin.html
# https://abseil.io/docs/python/guides/flags

from sender.sender import Sender
from receiver.receiver import Receiver
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

def run_client(ip, port):
    s = Sender(ip, port)
    s.send_file(input())
    pass

def run_server(ip, port):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(Receiver(ip, port))

def main(argv):
    if FLAGS.type == "server":
        run_server(FLAGS.ip, FLAGS.port)
    elif FLAGS.type == "client":
        run_client(FLAGS.ip, FLAGS.port)
    else:
        print("problems")

if __name__ == '__main__':
    app.run(main)
