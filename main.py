import pygame
import math
import sys

pygame.init()
WIDTH = 500
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0, 0, 0)

def outTermMap():
    print('\n'.join(' '.join(('#' * y) + (' ' * abs(y-1)) for y in x) for x in MAP))


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
    pygame.draw.rect(window, BLACK, ((0, 0), (WIDTH, HEIGHT)))
    FOV = math.radians(60)
    castResolution = 20
    for i in range(WIDTH):
        rayDir = FOV/WIDTH * (i - WIDTH/2) + dir
        rayX = x
        rayY = y
        # make dist not = 0. Ever
        rayX += math.sin(rayDir) / castResolution
        rayY += math.cos(rayDir) / castResolution
        while math.dist((x, y), (rayX, rayY)) < 100 and not getMap(rayX, rayY):
            rayX += math.sin(rayDir) / castResolution
            rayY += math.cos(rayDir) / castResolution

        lineHeight = 1/max(rayDist(rayX, rayY), 1) * HEIGHT
        pygame.draw.line(window, (min(1/rayDist(rayX, rayY), 1)*255, min(1/rayDist(rayX, rayY), 1)*255, min(1/rayDist(rayX, rayY), 1)*255), (i, (HEIGHT - lineHeight)/2), (i, HEIGHT + (lineHeight - HEIGHT)/2))
    pygame.display.update()

outTermMap()

dir = 0
walkSpeed = 0.1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    render()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        dir -= math.radians(10)
    if keys[pygame.K_RIGHT]:
        dir += math.radians(10)
    if keys[pygame.K_UP]:
        if not getMap(x + math.sin(dir) * walkSpeed, y + math.cos(dir) * walkSpeed):
            x += math.sin(dir) * walkSpeed
            y += math.cos(dir) * walkSpeed
    if keys[pygame.K_DOWN]:
        if not getMap(x - math.sin(dir) * walkSpeed, y - math.cos(dir) * walkSpeed):
            x -= math.sin(dir) * walkSpeed
            y -= math.cos(dir) * walkSpeed