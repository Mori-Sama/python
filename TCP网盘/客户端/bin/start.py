import socket
import os, sys
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(('127.0.0.1',9000))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core import src


if __name__ == '__main__':
    src.run()

