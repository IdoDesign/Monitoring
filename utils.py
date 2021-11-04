import socket
import os

def ping(hostname):
    command = "ping -c 1 {}".format(hostname)
    response = os.system(command)
    if response == 0:
        return True
    else:
        return False

def tcp_ping(hostname, port):
    try:
        sock = socket.socket()
        res = sock.connect((hostname, port))
        return True
        sock.close()
    except:
        return False