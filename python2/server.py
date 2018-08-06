from __future__ import absolute_import
import threading, socket, struct

from thread import *

HOST, PORT = u'', 11009

peers = set()
lastid = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
s.bind((HOST, PORT))
s.listen(2)

#print stun.get_ip_info(source_port=8887)

def speak(client_connection, client_address) :

    global lastid
    
    thisId = 0

    print 'started'

    while True:
            

        request = client_connection.recv(1024)
        
        res = int(request[0])

        print request

        if res == 1 :

            lastid += 1
            thisId = lastid

            print client_connection

            ip_bytes = socket.inet_aton(client_address[0])

            print ip_bytes 

            print client_address
        
            data = '%s:%d' % client_address

            peers.add((thisId, data))
            client_connection.send(bytearray('1%d' % thisId, 'utf-8'))

        elif res == 2:
            id = int(request[1:])
            
            ids = [x[0] for x in peers]

            if id in ids :
                client_connection.send(bytearray('2%s' % dict(peers)[id], 'utf-8'))
                print(dict(peers)[id])
            else :
                client_connection.send(bytearray('3', 'utf-8'))

        elif res == 3:
            #peers.remove((thisId, dict(peers)[thisId]))
            try : 
                client_connection.close() 
            except KeyError:
                pass
            return
            

while True:
    client_connection, client_address = s.accept()

    print client_address

    start_new_thread(speak, (client_connection, client_address))

s.close()