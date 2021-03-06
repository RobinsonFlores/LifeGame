import pygame
import numpy as np
import time
pygame.init()

width, height = 720, 720
screen= pygame.display.set_mode((height, width))
#color del fondo
bg = 25,25,25
# pintamos fondo
screen.fill(bg)

#numero de celdas
nxC, nyC =30, 30

dimCW= width / nxC
dimCH = height/  nyC

#estado de las celdas, 1 viva, 0 muerta
gameState= np.zeros((nxC, nyC))

#automata palo
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

#automata movil
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

#Control de la ejecucion del juego
pauseExect = False

#Bucle de ejecucion

while True:

    newGameState = np.copy(gameState)

    screen.fill(bg)
    time.sleep(0.1)

    #registrar evento de teclado o mouse
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX/dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]






    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:

                #calculamos el numero de vecinos cercanos
                n_neigh =   gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                            gameState[(x)       % nxC, (y - 1) % nyC] + \
                            gameState[(x + 1)   % nxC, (y - 1) % nyC] + \
                            gameState[(x - 1)   % nxC, (y)     % nyC] + \
                            gameState[(x + 1)   % nxC, (y)     % nyC] + \
                            gameState[(x - 1)   % nxC, (y + 1) % nyC] + \
                            gameState[(x)       % nxC, (y + 1) % nyC] + \
                            gameState[(x+1)     % nxC, (y + 1) % nyC]

                #rule 1: una celula muerta con exactamente 3 vecinas vivas, "revive"
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                #rule 2: una celula viva con menos de 2 o mas de 3 vecinas vivas," muere"
                elif gameState[x, y] == 1 and(n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            #creando poligono de cada celda
            poly=[((x)   * dimCW, y * dimCH),
                  ((x+1) * dimCW, y * dimCH),
                  ((x+1) * dimCW, (y+1) * dimCH),
                  ((x)   * dimCW, (y+1)* dimCH)]
            # y dibujar la celda para cada x,y

            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (225, 225, 225), poly, 0)

    # Actualizamos el estado del juego
    gameState = np.copy(newGameState)

    # actualizar pantalla
    pygame.display.flip()

