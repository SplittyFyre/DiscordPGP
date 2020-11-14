import threading

def init():
    global inbuf
    inbuf = []
    global inbuf_mutex
    inbuf_mutex = threading.Lock()

    global outbuf
    outbuf = []
    global outbuf_mutex
    outbuf_mutex = threading.Lock()