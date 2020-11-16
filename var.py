import threading
import sys

def init():

    global token
    if len(sys.argv) != 2:
        print('Invalid number of arguments: need one argument specifying discord token')
        exit(0)
    token = sys.argv[1]

    global inbuf
    inbuf = []
    global inbuf_mutex
    inbuf_mutex = threading.Lock()

    global outbuf
    outbuf = []
    global outbuf_mutex
    outbuf_mutex = threading.Lock()

    global destination
    destination = None