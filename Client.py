from pynput import keyboard
import socket
import selectors
import types

sel = selectors.DefaultSelector()

# ip and port info
host = '127.0.0.1'
port = 65432

#     direction array info is for wheel direction and is sorted as follows:
#        [<top-left>, <top-right>, <bot-left>,  <bot-right>]
direction = ['f', 'f', 'f', 'f']

#global variables to store speed and direction info to be used for formatting.
speed = '000'

# follows same sorting as direction array
Outbound = b'[f000][f000][f000][f000]'

#initializes the connection to the server using non-blocking sockets and creates a data object holding all the relevent info required to send the outbound message
def start_connections():
    global Outbound
    server_addr = (host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)    
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(connid=1,
                                     msg_total= sum(Outbound),
                                     recv_total=0,
                                     messages=Outbound,
                                     outb=b'')
    sel.register(sock, events, data=data)

#updates the Outbound message with the most recent version and passes the message to outbound of the data object which is then sent to the server
def service_connection(key):
    global Outbound
    sock = key.fileobj
    data = key.data
    data.messages = Outbound
    if not data.outb and data.messages: #insures messages do not overwrite eachother
        data.outb = data.messages
    if data.outb:
        sent = sock.send(data.outb)
        data.outb = data.outb[sent:]


#must be called first to initialize the connection to the server.
start_connections()

# The main program fuction uses the keyboard object of pynput to detect key inputs and manipulate the global variables. It then constructs a string from these variables which is converted to bytes and sent to the server.

def on_press(key):
    global direction
    global speed
    global Outbound
    try:
        match key.char:
            case ('0'):
                speed = '000'
                print('speed = 0')
                sendData()

            case ('1'):
                speed = '051'
                print('speed = 51')
                sendData()

            case ('2'):
                speed = '102'
                print('speed = 102')
                sendData()

            case ('3'):
                speed = '153'
                print('speed = 153')
                sendData()

            case ('4'):
                speed = '204'
                print('speed = 204')
                sendData()
            
            case ('5'):
                speed = '255'
                print('speed = 255')
                sendData()
            
    except AttributeError:
        match key:
            case (key.up):
                for i in range(4):
                    direction[i] = 'f'
                print('forward')
                sendData()
                
            
            case (key.down):
                for i in range(4):
                    direction[i] = 'r'
                print('reverse')
                sendData()
               
            
            case (key.left):
                for i in range(4):
                    if i == 0 or i == 2:
                        direction[i] = 'r'
                    else:
                        direction[i] = 'f'
                print('left')
                sendData()



                

            case (key.right):
                for i in range(4):
                    if i == 0 or i == 2:
                        direction[i] = 'f'
                    else:
                        direction[i] = 'r'
                print('right')
                sendData()

# string of data to be sent is created, converted to bytes and set to the Outbound variable. this bytes variale is then sent to the server through the function service_connection.
def sendData():
    global direction
    global speed
    global Outbound
    outboundString = '[' + direction[0] + speed + ']' + '[' + direction[1] + speed + ']' + '[' + direction[2] + speed + ']' + '[' + direction[3] + speed + ']'

    Outbound = bytes(outboundString, 'utf-8')
    events = sel.select(timeout=None)
    for key, mask in events:
        service_connection(key)

# placeholder function that is not relevent to this code
def on_release(key):
    pass

# creates pynput keyboard listener that is used to detects key strokes
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
