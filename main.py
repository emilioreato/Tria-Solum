import clases

from win32con import ENUM_CURRENT_SETTINGS
from win32api import EnumDisplaySettings
import serial
import pygame
import time
import numpy
import sys
import serial.tools.list_ports
import pygame_gui
import os
import webbrowser
# do not delete this eventhough it is not used, for some reason it increases the render quality
from pyautogui import press

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()  # Inicializar Pygame

info = pygame.display.Info()  # Seteando las dimesiones de la ventana 16:9
screen_height = info.current_h
screenratio = 1.4  # 1.5 is the ratio screen/window
height = round(screen_height/screenratio)
width = height*(1920/1080)
screen = pygame.display.set_mode([width, height])

pygame.display.set_caption("Gambit")  # ponemos un titulo

bkg_img = pygame.image.load("resources\\background.png").convert()
bkg_img = pygame.transform.smoothscale(bkg_img, (width, height))


# Cargar una imagen (reemplaza con la ruta de tu imagen)
# image_path = "ruta_a_tu_imagen.png"
# image = pygame.image.load(image_path)

# Escalar la imagen si es necesario para que se ajuste a la ventana
# image = pygame.transform.scale(image, (width, height))

# Configurar el reloj para controlar los FPS
timer = pygame.time.Clock()
dev_mode = EnumDisplaySettings(None, ENUM_CURRENT_SETTINGS)  # get the fps OS setting
timer.tick(dev_mode.DisplayFrequency)  # fps of the window
# fps config for pygame_gui

pygame.mouse.set_visible(True)  # both needed for set mouse in virtual mode
pygame.event.set_grab(False)

UI_REFRESH_RATE = timer.tick(dev_mode.DisplayFrequency)/1000
manager = pygame_gui.UIManager((width, height))

pieza1 = clases.Piece(5, 5, 20)

board = [[""]*8]*8

print(board)

color_claro = (255, 255, 255)  # Blanco
color_oscuro = (0, 0, 0)
follow_mouse = False

tamano_cuadrado = (height-200) // 8  # Dividir el ancho de la ventana entre 8
while True:

    screen.blit(bkg_img, (0, 0))

    print(pieza1.pos_x, pieza1.pos_y)

    """for fila in range(8):
        for columna in range(8):
            # Alternar colores
            if (fila + columna) % 2 == 0:
                color = color_claro
            else:
                color = color_oscuro

            # Dibujar el cuadrado
            board[fila][columna] = pygame.draw.rect(screen, color, (300+columna * tamano_cuadrado, 100+fila * tamano_cuadrado, tamano_cuadrado, tamano_cuadrado))
            """
    if follow_mouse:
        pieza1.pos_x, pieza1.pos_y = event.pos
    else:
        pass
    pieza1_circle = pieza1.dibujar(screen, pygame.Color(50, 50, 10), (pieza1.pos_x, pieza1.pos_y))

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Obtener la posición del ratón
                mouse_pos = event.pos

                # Comprobar si el clic está dentro del cuadrado
                if pieza1.is_clicked(mouse_pos, (pieza1.pos_x, pieza1.pos_y)):
                    print("¡Clic en el cuadrado!")
                    follow_mouse = True
        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:
                follow_mouse = False
            for fila in board:
                for rect in fila:
                    mouse_pos = event.pos
                    print((pieza1.pos_x, pieza1.pos_y))
                    if rect.collidepoint(mouse_pos):
                        pieza1.pos_x, pieza1.pos_y = rect.center
                        print("fifjei")
                        break

        elif event.type == pygame.KEYDOWN:
            if (pygame.key.name(event.key) == "w"):
                pieza1.mover(0, 1)
            elif (pygame.key.name(event.key) == "s"):
                pieza1.mover(0, -1)
            elif (pygame.key.name(event.key) == "a"):
                pieza1.mover(1, 0)
            elif (pygame.key.name(event.key) == "d"):
                pieza1.mover(-1, 0)
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dibujar la imagen en la ventana
    # screen.blit(image, (0, 0))

    # Actualizar la pantalla
    pygame.display.flip()
    # time.sleep(1)

    # Mantener 144 FPS
    timer.tick(dev_mode.DisplayFrequency)
