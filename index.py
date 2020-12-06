import pygame
import numpy as np
import pygame_gui
import time

width, height = 501, 550

numOfCellX, numOfCellY = 50, 50

cellWidth = (width-1)/numOfCellX
cellHeight = (height-50)/numOfCellY

pygame.init()
BG_Color = (28, 28, 28)

screen = pygame.display.set_mode([width, height])
manager = pygame_gui.UIManager((width, height))
gameState = np.zeros([width, height])

speed = 0.1
solitude = 2
poblation = 3

speedButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 510), (100, 30)),
                                           text='Speed Up',
                                           manager=manager)

slowButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((110, 510), (100, 30)),
                                          text='Slow down',
                                          manager=manager)
solitudeLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((215, 515), (100, 20)),
                                            text='Solitude: ' + str(solitude),
                                            manager=manager)

solitudePlusButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((320, 505), (20, 20)),
                                                  text='+',
                                                  manager=manager)

solitudeMinusButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((320, 525), (20, 20)),
                                                   text='-',
                                                   manager=manager)

PoblationLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((345, 515), (100, 20)),
                                             text='Poblation: ' +
                                             str(poblation),
                                             manager=manager)

poblationPlusButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 505), (20, 20)),
                                                   text='+',
                                                   manager=manager)

poblationMinusButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 525), (20, 20)),
                                                    text='-',
                                                    manager=manager)


clock = pygame.time.Clock()

gameState[1, 3] = 1
gameState[1, 2] = 1
gameState[1, 1] = 1

screen.fill(BG_Color)

pause = False
running = True

while running:
    newGameState = np.copy(gameState)

    time_delta = clock.tick(60)/1000.0

    ev = pygame.event.get()

    screen.fill(BG_Color)
    for event in ev:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pause = not pause

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == speedButton:
                    speed = speed/1.5
                elif event.ui_element == slowButton:
                    speed = speed*1.5
                elif event.ui_element == solitudePlusButton:
                    solitude = solitude + 1
                    solitudeLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((215, 515), (100, 20)),
                                                                text='Solitude: ' +
                                                                str(solitude),
                                                                manager=manager)
                elif event.ui_element == solitudeMinusButton:
                    solitude = solitude - 1
                    solitudeLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((215, 515), (100, 20)),
                                                                text='Solitude: ' +
                                                                str(solitude),
                                                                manager=manager)
                elif event.ui_element == poblationPlusButton:
                    poblation = poblation + 1
                    PoblationLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((345, 515), (100, 20)),
                                                                text='Poblation: ' +
                                                                str(poblation),
                                                                manager=manager)
                elif event.ui_element == poblationMinusButton:
                    poblation = poblation - 1
                    PoblationLabel = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((345, 515), (100, 20)),
                                                                text='Poblation: ' +
                                                                str(poblation),
                                                                manager=manager)

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:

            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX/cellWidth)
                             ), int(np.floor(posY/cellHeight))
            if mouseClick[0] == True:
                newGameState[celX, celY] = 1
            else:
                newGameState[celX, celY] = 0
        manager.process_events(event)
    manager.update(time_delta)

    manager.draw_ui(screen)

    for y in range(0, numOfCellY):
        for x in range(0, numOfCellX):
            if not pause:
                nNeight = gameState[(x-1) % numOfCellX, (y-1) % numOfCellY] + gameState[(x-1) % numOfCellX, (y) % numOfCellY] +\
                    gameState[(x-1) % numOfCellX, (y+1) % numOfCellY] + gameState[(x) % numOfCellX, (y-1) % numOfCellY] +\
                    gameState[(x) % numOfCellX, (y+1) % numOfCellY] + gameState[(x+1) % numOfCellX, (y-1) % numOfCellY] +\
                    gameState[(x+1) % numOfCellX, (y) % numOfCellY] +\
                    gameState[(x+1) % numOfCellX, (y+1) % numOfCellY]

                if gameState[x, y] == 0 and nNeight == poblation:
                    newGameState[x, y] = 1
                elif gameState[x, y] == 1 and nNeight < solitude or nNeight > poblation:
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
    time.sleep(speed)
    pygame.display.flip()

pygame.quit()
