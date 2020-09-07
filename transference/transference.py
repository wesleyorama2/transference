# https://jtannas-python-skeleton.readthedocs.io/en/latest/source/bin.html
from sender.sender import Sender   # "myapp" case
import sys
import os
sys.path.append(os.path.realpath('.'))

s = Sender("127.0.0.1", 5001)
s.send_file(input())
