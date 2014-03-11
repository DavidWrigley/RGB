import socket
import time
import threading
import signal
import sys

TCP_IP = "192.168.1.107"
TCP_PORT = 8888
BUFFER_SIZE = 1024

def connect(IP, Port):
    try:
        sock.connect((TCP_IP, TCP_PORT))
        return 0
    except socket.timeout:
        time.sleep(4)
        return 1

def signal_handler(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)
    sys.exit(0)

"""
def Send():
        # Test Suite
        for i in range(8):
                message += ( str(unichr(int(i))) + str(unichr(int(63))) + str(unichr(int(toggle))) + str(unichr(int(0))) + str(unichr(int(0))) )
        if(toggle == 8):
                toggle = 0
        else:
                toggle = 8
        sock.send(message)
        time.sleep(1)
        message = ""
"""
"""        
def Receive():
    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE) # buffer size is 1024 bytes
            print "Received: ", data
        except socket.timeout:
            a = 1
"""
def ensure_Connect():
    while (connect(TCP_IP,TCP_PORT)):
        print "timeout"
    print "connected"

if __name__ == '__main__':

    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal_handler)
    sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_STREAM) # TCP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(5)
    sock.bind(('',0))
    ensure_Connect()
    while (True):
        toggle = 8
        message = ""
        layer = raw_input("layer: ")
        pixel = raw_input("pixel: ")
        red = raw_input("red: ")
        green = raw_input("green: ")
        blue = raw_input("blue: ")
        message += ( str(unichr(int(layer))) + str(unichr(int(pixel))) + str(unichr(int(red))) + str(unichr(int(green))) + str(unichr(int(blue))) )
        try:
            sock.send(message)
        except socket.error:
            print "disconnected, atempting reconnect"
            ensure_Connect()
            sock.send(message)
            
        message = ""
