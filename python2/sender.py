import socket
import re



def mysend(msg, s):
        totalsent = 0
        while totalsent < len(msg):
            sent = s.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

def myreceive():
        chunks = []
        bytes_recd = 0
        while bytes_recd < 256:
            chunk = s.recv(min(256 - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 54000))

s.connect(('31.31.196.78', 11003))

req = """GET /default.aspx HTTP/1.1 \
Host: tulumbas.com:80"""

b = b'1'

print b

s.send(b)

print "smth"

ans = s.recv(4096)

print ans

inp = input()