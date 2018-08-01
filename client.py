import threading, socket, random, struct

from threading import Thread

from _thread import *

debug = True

connected = False

mainSocket = 0

loc_port = random.randint(50000, 50100)

class ReplyHandler(Thread):

    
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        global connected
        while True:
            try : 
                mes = mainSocket.recv(1024)
            except ConnectionResetError :
                print ('Other peer has closed the connection')
                connected = False
                break
            else :
                print (mes)


def listeningThread() :

    global connected, mainSocket

    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listening_socket.bind(('', loc_port))
    
    listening_socket.listen(1)
    listening_socket.settimeout(5)

    while not connected:
        try:
            connection, addres = listening_socket.accept()
        except socket.timeout:
            continue
        else:
            print('heard')
            connected = True
            mainSocket = connection
            break        
    
    listening_socket.close()

    #print ('connected but not heard')

def connectionThread(dest_host, dest_port) :

    global connected, mainSocket

    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection_socket.bind(('', loc_port))
    
    while not connected:
        try:
            if debug : 
                connection_socket.connect(('192.168.1.71', dest_port))
            else :
                connection_socket.connect((dest_host, dest_port))
        except socket.error:
            continue
        else:
            print('connected')
            connected = True
            mainSocket = connection_socket
            break        

    #start_new_thread(messageListeningThread, connection_socket)
    
    #connection_socket.send(bytes('simple', 'utf-8'))

    #connection_socket.close()

def connectToPeer(connect_data) :
    
    global connected

    bytes_host = connect_data[:4]
    bytes_port = connect_data[4:]

    dest_host = "{}.{}.{}.{}".format(*struct.unpack('BBBB', bytes_host))
    
    dest_port = int.from_bytes(bytes_port, byteorder='big')

    print ('Connecting to {}:{}'.format(dest_host, dest_port))

    start_new_thread(listeningThread, ())
    start_new_thread(connectionThread, (dest_host, dest_port))

    while not connected :
        continue

   

    thread = ReplyHandler()
    thread.daemon = True
    thread.start()
  
    line = ''

    while line != 'close' and connected:
        
        line = input()
        try : 
            mainSocket.send(bytes(line, 'utf-8'))
        except ConnectionResetError :
            print ('Other peer has closed the connection')
            connected = False
            break
        

    try :
         mainSocket.close()
    except KeyError :
        pass

    print ('Connection closed')


def connectToServer(host, port) :

    global dest_host, dest_port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', loc_port))
    print ('Bound {} port'.format(loc_port))
    server_socket.connect((host, port))

    server_socket.sendall(b'\x01\x00\x00\x00\x00')

    ans = server_socket.recv(4096)

    print (ans)

    print (int.from_bytes(ans[1:], byteorder = 'big'))

    while True:

        print ('Enter ID')

        line = input()

        try : 
            inp = int(line)
        except ValueError :
            inp = 0
            print ('Invalid id')
            continue
        
        if inp == -1 :
            server_socket.sendall(b'\x03' + bytes([2]))

            try :
                server_socket.close()
            except KeyError :
                pass
            break

        server_socket.sendall(b'\x02' + inp.to_bytes(2, byteorder='big'))
        
        ans = server_socket.recv(4096)

        if ans[0] == 2 :
            server_socket.sendall(b'\x03' + bytes([2]))

            try :
                server_socket.close()
            except KeyError :
                pass

            return ans[1:]
        elif ans[0] == 3 :
            print('This id is not registered')

    server_socket.close()
connectToPeer(connectToServer('188.243.49.147', 8887)) 
