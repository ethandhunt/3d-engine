import pygame
import colorsys
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

def rotate(point, angle):
    px, py = point
    qx = math.cos(angle) * px - math.sin(angle) * py
    qy = math.sin(angle) * px + math.cos(angle) * py
    return qx, qy

def angle(line):
    v1_theta = math.atan2(line[0][1], line[0][0])
    v2_theta = math.atan2(line[1][1], line[1][0])
    r = (v2_theta - v1_theta) * (180.0 / math.pi)
    if r < 0:
        r % 360
    return r

def getIntersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return 10**16, 10**16

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def getMap(x, y):
    return MAP[max(min(round(x), len(MAP) - 1), 0)][max(min(round(y), len(MAP[0]) - 1), 0)]

def getBounds(origin):
    '''
    Builds an array of lines so that you don't have to check each wall
    Works like this:
    # # # # # # # # #
    # x 1 2 3 4 5 6 #
    # # # 3 # 5 6 7 #
    #   # 4 # 6 7 8 #
    # # # # # # # # #
    Then checks whether line is visible
    A \ _____ / B
    -- \ \ / / --
     C  \/_\/  D
         \ /
          x
    AB: True
    BC: True
    AC: False
    AD: True
    BD: False
    CD: True
    '''
    maxLength = 10

    # Collection of tiles
    array = [(origin)]

    # Generate tile map
    for _ in range(maxLength):
        newTiles = []
        for x, y in array:
              #
            # x #
              #
            for xOffset, yOffset in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
                if not getMap(x + xOffset, y + yOffset):
                    newTiles += [(x + xOffset, y + yOffset)]
        if len(newTiles) == 0:
            break
        array += newTiles
    
        # Remove duplicates
        newArray = []
        for item in array:
            if item not in newArray:
                newArray += [item]
        array = newArray

    # Make lines
    # If edge isn't shared with another tile, make line
    lines = []
    for tileX, tileY in array:
        # Left
        if (tileX-1, tileY) not in array:
            lines += [((tileX - 0.5, tileY - 0.5), (tileX - 0.5, tileY + 0.5))]
        # Right
        if (tileX+1, tileY) not in array:
            lines += [((tileX + 0.5, tileY - 0.5), (tileX + 0.5, tileY + 0.5))]
        # Top
        if (tileX, tileY+1) not in array:
            lines += [((tileX - 0.5, tileY + 0.5), (tileX + 0.5, tileY + 0.5))]
        # Bottom
        if (tileX, tileY-1) not in array:
            lines += [((tileX - 0.5, tileY - 0.5), (tileX + 0.5, tileY - 0.5))]

    # Clean lines
    # If lines share a vertex and continue in the same vector remove the midpoint
    mainCheck = True
    badLines = []
    while mainCheck:
        mainCheck = False
        newLines = []
        iteration = 0
        startLen = len(lines)
        for line1 in lines:
            iteration += 1
            for line2 in lines:
                check = False
                # Invalidation conditions
                if line2 != line1 and line1 not in badLines and line2 not in badLines:
                    # Shares a midpoint
                    if line1[1] == line2[0]:
                        # Shares vector
                        if line1[0][0] == line2[1][0] or line1[0][1] == line2[1][1]:
                            newLines += [(line1[0], line2[1])]
                            check = True
                            lines.remove(line2)
                            startLen -= 1
                            mainCheck = True
                            break
            if not check:
                newLines += [line1]
        lines = newLines
        return lines

def rayDist(rayX, rayY):
    return math.dist((x, y), (rayX, rayY))

def render():
    FOV = math.radians(60)
    castResolution = 50
    backTraceDepth = 10
    lines = getBounds((int(x), int(y)))
    for i in range(WIDTH):
        rayDir = FOV/WIDTH * (i - WIDTH/2) + dir
        sine = math.sin(rayDir) / castResolution
        cosine = math.cos(rayDir) / castResolution
        rayX = x
        rayY = y
        # make dist not = 0. Ever
        rayX += sine
        rayY += cosine
        mins = rayDist(getIntersection(((x, y), (rayX, rayY)), lines[0])[0], getIntersection(((x, y), (rayX, rayY)), lines[0])[1])
        for line in lines:
            intersect = getIntersection(((x, y), (rayX, rayY)), line)
            if rayDist(intersect[0], intersect[1]) < mins:
                mins = rayDist(intersect[0], intersect[1])
                rayX, rayY = intersect
        iteration = 0
        while rayDist(rayX, rayY) < HEIGHT and not getMap(rayX, rayY):
            rayX += sine * iteration
            rayY += cosine * iteration
            iteration += 0.5
        if rayDist(rayX, rayY) < HEIGHT:
            sineIteration = sine * iteration
            cosineIteration = cosine * iteration
            High = (rayX + sineIteration, rayY + cosineIteration)
            Low = (rayX - sineIteration, rayY - cosineIteration)
            if iteration < 1:
                Low = (x, y)
            for _ in range(backTraceDepth):
                MidX = sum([High[0], Low[0]])/2
                MidY = sum([High[1], Low[1]])/2
                if getMap(MidX, MidY):
                    High = (MidX, MidY)
                else:
                    Low = (MidX, MidY)
            rayX = MidX
            rayY = MidY
        lineHeight = 1/max(rayDist(rayX, rayY), 1) * HEIGHT
        pygame.draw.line(window, [min(1/rayDist(rayX, rayY), 1)*255]*3, (i, (HEIGHT - lineHeight)/2), (i, HEIGHT + (lineHeight - HEIGHT)/2))

outTermMap()
print('Press esc to exit')
dir = 0
walkSpeed = 0.1
startTime = time.time()
while True:
    pygame.draw.rect(window, BLACK, ((0, 0), (WIDTH, HEIGHT)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    render()
    dir += math.radians(pygame.mouse.get_rel()[0])
    dir = dir % math.radians(360)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
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