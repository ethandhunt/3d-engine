import socket
import threading

def rcv(conn):
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            return conn.recv(msg_length).decode(FORMAT)

def send(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

class client:
    def __init__(self, conn):
        self.conn = conn
        self.pos = (0, 0)
    
    def updatePos(self, pos):
        self.pos = pos
    
    def rcv(self):
        return rcv(self.conn)
    
    def send(self, message):
        send(self.conn, message)


HEADER = 64
PORT = 55555
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)
print(ADDR)
try:
    server.bind(ADDR)
except Exception:
    print('Error binding server, port may already be in use')
    print(f'IP: {IP}')
    print(f'PORT: {PORT}')
    input('Press enter to exit')

CLIENTS = []

def handleClient(conn, addr):
    print(f'{addr} Connected')
    thisClient = client(conn)
    CLIENTS.append(thisClient)
    try:
        while True:
            msg = thisClient.rcv()
            print(f'{addr}>{msg}')
            if msg == 'MAPREQ':
                thisClient.send(MAP)
            elif msg == 'GETPLAYERS':
                array = []
                for player in CLIENTS:
                    if player.pos != thisClient.pos:
                        array += [str(player.pos[0]) + ':' + str(player.pos[1])]
                print(','.join(array))
                thisClient.send(','.join(array))
            elif msg == 'QUIT':
                raise Exception
            else:
                thisClient.updatePos(msg.split(':'))
    except:
        try:
            CLIENTS.remove(thisClient)
            print(f'{addr} Disconnected')
        except: pass

with open('map.txt') as f:
    MAP = f.read()
server.listen()
print(f'Server Name: {socket.gethostname()}')
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handleClient, args=(conn, addr))
    thread.start()