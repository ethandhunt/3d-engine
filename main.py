import pygame
import math
import sys
import time
<<<<<<< HEAD
import socket
import threading

def send(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def rcv(conn):
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            return conn.recv(msg_length).decode(FORMAT)

class connection:
    def __init__(self, conn):
        self.conn = conn
    
    def rcv(self):
        return rcv(self.conn)
    
    def send(self, msg):
        send(self.conn, msg)

HEADER = 64
FORMAT = 'utf-8'
IP = socket.gethostbyname(input('Enter server name: '))
PORT = 55555
ADDR = (IP, PORT)
print(IP, PORT)
print('Connecting...')
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(ADDR)
SERVER = connection(conn)
playerPositions = []

def playerPos():
    global playerPositions
    global exit
    while True:
        SERVER.send('GETPLAYERS')
        unparsedString = SERVER.rcv()
        if unparsedString == '':
            SERVER.send(f'{x}:{y}')
            continue
        playerPositions = [[float(b) for b in a.split(':')] for a in unparsedString.split(',')]
        SERVER.send(f'{x}:{y}')
        if exit:
            SERVER.send("QUIT")
            sys.exit()
=======
>>>>>>> parent of 42cd706 (Added multiplayer, doesn't let you see people yet tho)

pygame.init()
WIDTH = 500
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

BLACK = (0, 0, 0)

def outTermMap():
    print('\n'.join(' '.join(('#' * y) + (' ' * abs(y-1)) for y in x) for x in MAP))

def drawText(text, size, colour, pos, font='courier', centered=False, updateScreen=False, antiAlias=True, background=(0,0,0)):
    myfont = pygame.font.SysFont(font, size)
    textsurface = myfont.render(text, antiAlias, colour, background)
    x = pos[0]
    y = pos[1]
    if centered:
        window.blit(textsurface, (x - myfont.size(text)[0]//2, y - myfont.size(text)[1]//2))
    else:
        window.blit(textsurface, (x, y))
    if updateScreen:
        pygame.display.update()
    return myfont.size(text)

with open('map.txt') as f:
    rawMap = f.read()
MAP=[]
for mapX, line in enumerate(rawMap.split('\n')):
    MAP += [[]]
    for mapY, char in enumerate(line[::2]):
        MAP[mapX] += [char == '#']
        if char == 'x':
            x = mapX
            y = mapY

def rayDist(rayX, rayY):
    return math.dist((x, y), (rayX, rayY))

def getMap(x, y):
    return MAP[max(min(round(x), len(MAP) - 1), 0)][max(min(round(y), len(MAP[0]) - 1), 0)]

def render():
    FOV = math.radians(60)
    castResolution = 20
<<<<<<< HEAD
    array = []
    rayWidth = 10
    for i in range(WIDTH//rayWidth):
        rayDir = FOV/WIDTH/rayWidth * (i - WIDTH/2/rayWidth) + dir
=======
    for i in range(WIDTH):
        rayDir = FOV/WIDTH * (i - WIDTH/2) + dir
>>>>>>> parent of 42cd706 (Added multiplayer, doesn't let you see people yet tho)
        rayX = x
        rayY = y
        # make dist not = 0. Ever
        rayX += math.sin(rayDir) / castResolution
        rayY += math.cos(rayDir) / castResolution
        iteration = 0
        while iteration < 100 and not getMap(rayX, rayY):
            rayX += math.sin(rayDir) / castResolution * iteration/10
            rayY += math.cos(rayDir) / castResolution * iteration/10
            iteration += 1

        lineHeight = 1/max(rayDist(rayX, rayY), 1) * HEIGHT
        pygame.draw.line(window, (min(1/rayDist(rayX, rayY), 1)*255, min(1/rayDist(rayX, rayY), 1)*255, min(1/rayDist(rayX, rayY), 1)*255), (i, (HEIGHT - lineHeight)/2), (i, HEIGHT + (lineHeight - HEIGHT)/2))
<<<<<<< HEAD
    if playerPositions == []: return
    for player in playerPositions:
        screenX = ((getAngle((x, y), player) - dir)/FOV)*WIDTH
        print(screenX)
        pygame.draw.circle(window, (255, 0, 0), (screenX, HEIGHT//2), max(rayDist(player[0], player[1]), 1) * HEIGHT)
=======
>>>>>>> parent of 42cd706 (Added multiplayer, doesn't let you see people yet tho)

outTermMap()

dir = 0
walkSpeed = 0.1
startTime = time.time()
print('Press esc to exit window')
while True:
    pygame.draw.rect(window, BLACK, ((0, 0), (WIDTH, HEIGHT)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    render()
    dir += math.radians(pygame.mouse.get_rel()[0])
    dir = dir % math.radians(360)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if not getMap(x + math.sin(dir - math.radians(90)) * walkSpeed, y - math.cos(dir + math.radians(90)) * walkSpeed):
            x -= math.sin(dir + math.radians(90)) * walkSpeed
            y -= math.cos(dir + math.radians(90)) * walkSpeed
    if keys[pygame.K_d]:
        if not getMap(x + math.sin(dir + math.radians(90)) * walkSpeed, y + math.cos(dir + math.radians(90)) * walkSpeed):
            x += math.sin(dir + math.radians(90)) * walkSpeed
            y += math.cos(dir + math.radians(90)) * walkSpeed
    if keys[pygame.K_w]:
        if not getMap(x + math.sin(dir) * walkSpeed, y + math.cos(dir) * walkSpeed):
            x += math.sin(dir) * walkSpeed
            y += math.cos(dir) * walkSpeed
    if keys[pygame.K_s]:
        if not getMap(x - math.sin(dir) * walkSpeed, y - math.cos(dir) * walkSpeed):
            x -= math.sin(dir) * walkSpeed
            y -= math.cos(dir) * walkSpeed
    drawText(f'FPS: {int(1/(time.time() - startTime))}', 12, (255, 255, 255), (0, 0))
    startTime = time.time()
    pygame.display.update()