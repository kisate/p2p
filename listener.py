import socket


def mysend(msg):
        totalsent = 0
        while totalsent < 3:
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



print('a')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 55000))
s.listen(2)

#print stun.get_ip_info(source_port=8887)
while True:
    client_connection, client_address = s.accept()
    request = client_connection.recv(1024)
    print ((request, client_connection, client_address))

    http_response = """\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(bytearray(http_response, 'utf-8'))
    #client_connection.close()