from win32con import ENUM_CURRENT_SETTINGS
from win32api import EnumDisplaySettings
import pygame
import time
import numpy
import sys
import pygame_gui
import os
import pyautogui
from pyautogui import press  # do not delete this eventhough it is not used, for some reason it increases the render quality
import clases

# SETING THINGS UP

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets the current directory to the file's directory

pygame.init()  # Inicializar Pygame

_, screen_height = pyautogui.size()  # gets the current resolution
screenratio = 1  # is the ratio screen/window
height = round(screen_height/screenratio)  # reduces the height
width = round(height*(16/9))  # sets the aspect ratio to 16:9
screen = pygame.display.set_mode([width, height])  # sets window resolution

pygame.display.set_caption("Gambit")  # set a window title


def load_images():

    global bkg_img, cursor_default, close_button, close_button_rect, settings_button, settings_button_rect

    bkg_img = pygame.image.load("resources\\background.png").convert()  # load some images, converts it for optimization and then scales them.
    bkg_img = pygame.transform.smoothscale(bkg_img, (width, height))

    cursor_default = pygame.image.load("resources\\icons\\cursor_default.png").convert_alpha()
    cursor_default = pygame.transform.smoothscale(cursor_default, (screen_height * 0.805 // 43, screen_height // 43))

    close_button = pygame.image.load("resources\\icons\\x.png").convert_alpha()
    close_button = pygame.transform.smoothscale(close_button, (height // 24, height // 24))
    close_button_rect = close_button.get_rect()
    close_button_rect.topleft = (height//0.6, height // 25)

    settings_button = pygame.image.load("resources\\icons\\setting.png").convert_alpha()
    settings_button = pygame.transform.smoothscale(settings_button, (height // 24, height // 24))
    settings_button_rect = settings_button.get_rect()
    settings_button_rect.topleft = (height//0.62, height // 25)


load_images()


timer = pygame.time.Clock()  # create a clock object to set fps
dev_mode = EnumDisplaySettings(None, ENUM_CURRENT_SETTINGS)  # get the OS's fps setting

pygame.mouse.set_visible(False)  # both needed for set mouse in virtual mode
pygame.event.set_grab(True)

UI_REFRESH_RATE = timer.tick(dev_mode.DisplayFrequency)/1000
manager = pygame_gui.UIManager((width, height))


pieza1 = clases.Mage(500, 500, 13)

# board = [[""]*8]*8
# print(board)

"""color_claro = (255, 255, 255)  # Blanco
color_oscuro = (0, 0, 0)
tamano_cuadrado = (height-200) // 8  # Dividir el ancho de la ventana entre 8"""

follow_mouse = False


def draw():
    screen.blit(bkg_img, (0, 0))  # display background
    pieza1.draw(screen, pieza1.blue_mage_image)
    screen.blit(close_button, (height//0.6, height // 25))
    screen.blit(settings_button, (height//0.62, height // 25))

    screen.blit(cursor_default, pygame.mouse.get_pos())  # display cursor

    pygame.display.flip()  # Actualizar la pantalla #.update()


run = True
while run:  # Main loop

    # print(pieza1.pos_x, pieza1.pos_y)

    if follow_mouse:
        pieza1.pos_x, pieza1.pos_y = event.pos
    else:
        pass

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Obtener la posición del ratón
                mouse_pos = event.pos

                if pieza1.is_clicked(mouse_pos, (pieza1.pos_x, pieza1.pos_y)):  # Comprobar si el clic está dentro del circulo
                    print("pieza clickeada")
                    follow_mouse = True

                elif close_button_rect.collidepoint(mouse_pos):  # check if button was clicked
                    pygame.quit()
                    sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:
                follow_mouse = False
            """for fila in board:
                for rect in fila:
                    mouse_pos = event.pos
                    print((pieza1.pos_x, pieza1.pos_y))
                    if rect.collidepoint(mouse_pos):
                        pieza1.pos_x, pieza1.pos_y = rect.center
                        print("fifjei")
                        break"""

        elif event.type == pygame.KEYDOWN:
            if (pygame.key.name(event.key) == "w"):
                pieza1.mover(0, 1, True)
            elif (pygame.key.name(event.key) == "s"):
                pieza1.mover(0, -1, True)
            elif (pygame.key.name(event.key) == "a"):
                pieza1.mover(1, 0, True)
            elif (pygame.key.name(event.key) == "d"):
                pieza1.mover(-1, 0, True)
            elif (pygame.key.name(event.key) == "escape"):
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw()

    timer.tick(dev_mode.DisplayFrequency)  # set the fps to the maximun possible
