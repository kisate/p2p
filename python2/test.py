import socket

HOST, PORT = '', 50001


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
s.bind((HOST, PORT))
s.listen(2)

connection, addres = s.accept()

print addres