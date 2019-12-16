# play streams from NVR (model: K9604-W)
#
# based on: https://gist.github.com/maxious/c8915a436b532ab09e61bf937295a5d2#file-stream-socket-py
# view output via: python3 stream.socket.py | ffplay -i pipe:
# or can write to file
write_to_files = False
import socket
import time
import datetime
import sys
import os

TCP_IP = '192.168.0.234'
TCP_PORT = 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.settimeout(2)
s.setblocking(1)
"""
**************************************************************************************
* Avoid socket.error: [Errno 98] Address already in use exception
* The SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state,
* without waiting for its natural timeout to expire.
**************************************************************************************
"""
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.connect((TCP_IP, TCP_PORT))
s.send(b'GET /bubble/live?ch=0&stream=0 HTTP/1.1\r\n\r\n')
data = s.recv(1142)

s.send(b'\xaa\x00\x00\x00\x15\x0a\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')
#                                                  ^^ ch number    ^^ stream number                                               

if write_to_files:
    timestamp = datetime.datetime.now().isoformat().replace(":", "-")
    h264 = open(timestamp + '-socket.h264', 'wb')
else:
    h264 = sys.stdout.buffer

try:
    while True:
        try:
            data = s.recv(1541)
            h264.write(data)

        except BlockingIOError:
            time.sleep(.1)
            pass

# https://docs.python.org/2/howto/sockets.html#disconnecting
except BrokenPipeError:
    print("shutting down") if write_to_files else None
    s.shutdown(1)
    s.close()
except KeyboardInterrupt:
    print("shutting down") if write_to_files else None
    h264.close()
    g711.close() if write_to_files else None
    dump.close() if write_to_files else None
    s.shutdown(1)
    s.close()
