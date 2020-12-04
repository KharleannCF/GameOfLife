import pygame
import numpy as np
import time

width, height = 500, 500

numOfCellX, numOfCellY = 50, 50

cellWidth = width/numOfCellX
cellHeight = height/numOfCellY

pygame.init()
BG_Color = (28, 28, 28)

screen = pygame.display.set_mode([width, height])

gameState = np.zeros([width, height])


gameState[1, 3] = 1
gameState[1, 2] = 1
gameState[1, 1] = 1

screen.fill(BG_Color)

pause = False
running = True

while running:
    newGameState = np.copy(gameState)
    ev = pygame.event.get()
    screen.fill(BG_Color)
    for event in ev:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pause = not pause
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX/cellWidth)
                             ), int(np.floor(posY/cellHeight))
            if newGameState[celX, celY] == 1:
                newGameState[celX, celY] = 0
            else:
                newGameState[celX, celY] = 1

    for y in range(0, numOfCellY):
        for x in range(0, numOfCellX):
            if not pause:
                nNeight = gameState[(x-1) % numOfCellX, (y-1) % numOfCellY] + gameState[(x-1) % numOfCellX, (y) % numOfCellY] +\
                    gameState[(x-1) % numOfCellX, (y+1) % numOfCellY] + gameState[(x) % numOfCellX, (y-1) % numOfCellY] +\
                    gameState[(x) % numOfCellX, (y+1) % numOfCellY] + gameState[(x+1) % numOfCellX, (y-1) % numOfCellY] +\
                    gameState[(x+1) % numOfCellX, (y) % numOfCellY] +\
                    gameState[(x+1) % numOfCellX, (y+1) % numOfCellY]

                if gameState[x, y] == 0 and nNeight == 3:
                    newGameState[x, y] = 1
                elif gameState[x, y] == 1 and nNeight < 2 or nNeight > 3:
                    newGameState[x, y] = 0
            poly = [((x)*cellWidth, (y)*cellHeight),
                    ((x+1)*cellWidth, (y)*cellHeight),
                    ((x+1)*cellWidth, (y+1)*cellHeight),
                    ((x)*cellWidth, (y+1)*cellHeight)]

            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    gameState = np.copy(newGameState)
    time.sleep(0.1)
    pygame.display.flip()

pygame.quit()
