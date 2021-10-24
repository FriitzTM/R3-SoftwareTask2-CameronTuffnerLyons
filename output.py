import socket
import selectors
import types

#used to monitor the socket
sel = selectors.DefaultSelector()

# ip and port info
host = '127.0.0.1'
port = 65432

#socket is initialized with same ip and port as client listens for a connection to be made
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print('listening on', (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

#accepts the connection made by the client and initializes the data variable with the required information and placeholders.
def accept_wrapper(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

#Processess the incoming data from the client and prints the data as a string. It also closes the server if the client disconnects.
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024) 
        if recv_data:
            data.outb = recv_data
        else:
            sel.unregister(sock)
            sock.close()
    
        print(data.outb.decode('utf-8'))
            

#loopback function used to detect and start processing incomming data
while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)





