import threading, socket

from _thread import *

HOST, PORT = '', 8887

peers = set()
lastid = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(2)

#print stun.get_ip_info(source_port=8887)

def speak(client_connection, client_address) :

    global lastid
    
    thisId = 0

    while True:
            

        request = client_connection.recv(1024)
        
        res = request[0]

        if res == 1 :

            lastid += 1
            thisId = lastid

            print (client_connection)

            ip_bytes = socket.inet_aton(client_address[0])
            
            port_bytes = client_address[1].to_bytes(2, byteorder='big')

            peers.add((thisId, ip_bytes + port_bytes))
            client_connection.send(bytes([1]) + thisId.to_bytes(2, byteorder='big'))

        elif res == 2:
            id = int.from_bytes(request[1:], byteorder='big')
            
            ids = [x[0] for x in peers]

            if id in ids :
                client_connection.send(bytes([2]) + dict(peers)[id])
            else :
                client_connection.send(bytes([3]))

        elif res == 3:
            #peers.remove((thisId, dict(peers)[thisId]))
            try : 
                client_connection.close() 
            except KeyError:
                pass
            return
            

while True:
    client_connection, client_address = s.accept()
    start_new_thread(speak, (client_connection, client_address))