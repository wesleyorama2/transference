#!/usr/bin/env python
# https://jtannas-python-skeleton.readthedocs.io/en/latest/source/bin.html
# https://abseil.io/docs/python/guides/flags

from sender.sender import Sender
from receiver.receiver import Receiver
import logging
import socket
import concurrent.futures

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")
ip = "127.0.0.1"
port = 5001

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.submit(Receiver(ip, port))

s = Sender(ip, port)
s.send_file(input())
