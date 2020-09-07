# import sys
# sys.path.insert(0, '../')
from sender.sender import Sender

s = Sender("127.0.0.1", 5001)
s.send_file(input())