import pygame
import math
import sys
import time

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
    for i in range(WIDTH):
        rayDir = FOV/WIDTH * (i - WIDTH/2) + dir
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

outTermMap()

dir = 0
walkSpeed = 0.1
startTime = time.time()
print('Press esc to exit')
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