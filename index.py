import pygame
import numpy as np
import time

WIDTH, HEIGHT = 500, 500
nX, nY = 25, 25
xSize = WIDTH/nX
ySize = HEIGHT/nY

pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])

BG_COLOR = (10, 10, 10)
status = np.zeros((nX, nY))


pauseExect = False
running = True
while running:

    newstatus = np.copy(status)

    screen.fill(BG_COLOR)
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX/xSize)), int(np.floor(posY/ySize))
            newstatus[celX, celY] = 1

    for x in range(0, nX):
        for y in range(0, nY):
            if not pauseExect:
                n_neigh = status[(x-1) % nX, (y-1) % nY] + status[(x) % nX, (y-1) % nY] + \
                    status[(x+1) % nX, (y-1) % nY] + status[(x-1) % nX, (y) % nY] + \
                    status[(x+1) % nX, (y) % nY] + status[(x-1) % nX, (y+1) % nY] + \
                    status[(x) % nX, (y+1) % nY] + \
                    status[(x+1) % nX, (y+1) % nY]

                # Rule 1: Una celula muerta con 3 vecinas revive
                if status[x, y] == 0 and n_neigh == 3:
                    newstatus[x, y] = 1

                # Rule 2: Una celula viva con mas de 3 vecinos o menos de 2 muere
                elif status[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newstatus[x, y] = 0

            poly = [(x*xSize, y*ySize),
                    ((x+1)*xSize, y*ySize),
                    ((x+1)*xSize, (y+1)*ySize),
                    (x*xSize, (y+1)*ySize)]

            if newstatus[x, y] == 1:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
            else:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
    status = np.copy(newstatus)
    time.sleep(0.1)
    pygame.display.flip()

pygame.quit()
