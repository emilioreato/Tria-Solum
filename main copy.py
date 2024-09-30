from win32con import ENUM_CURRENT_SETTINGS
from win32api import EnumDisplaySettings
import win32con
import win32gui
import pygame
import time
import numpy
import sys
import pygame_gui
import os
import pyautogui
from pyautogui import press  # do not delete this eventhough it is not used, for some reason it increases the render quality
import clases
import ctypes
import math

# GENERAL VARIABLES

follow_mouse = False
minimized_state = False
show_cursor_image = True
center_points = []
active_pieces = []
board_size = 8


# SETING THINGS UP

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets the current directory to the file's directory

pygame.init()  # Inicializar Pygame


def set_up_window(screenratio=1, frame=0):  # is the ratio screen/window
    global screen, width, height, screen_height, timer, dev_mode
    _, screen_height = pyautogui.size()  # gets the current resolution
    height = round(screen_height/screenratio)  # reduces the height
    width = round(height*(16/9))  # sets the aspect ratio to 16:9
    screen = pygame.display.set_mode((width, height), frame)  # sets window resolution

    pygame.display.set_caption("Gambit Game 2024®")  # set a window title

    pygame.display.set_icon(pygame.image.load("resources\\indicator.png"))  # sets window icon

    timer = pygame.time.Clock()  # create a clock object to set fps
    dev_mode = EnumDisplaySettings(None, ENUM_CURRENT_SETTINGS)  # get the OS's fps setting


set_up_window()


def load_resources():

    global bkg_img, icon, cursor_default, close_button, close_button_rect, settings_button, settings_button_rect, minimize_button, minimize_button_rect

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

    minimize_button = pygame.image.load("resources\\icons\\minimize.png").convert_alpha()
    minimize_button = pygame.transform.smoothscale(minimize_button, (height // 24, height // 24))
    minimize_button_rect = minimize_button.get_rect()
    minimize_button_rect.topleft = (height//0.64, height // 25)

    pygame.mixer.music.load('resources\\sounds\\soundtracks\\track1.mp3')
    pygame.mixer.music.set_volume(0.6)


load_resources()


def create_center_points():
    center_points.clear()
    square_size = round(height/13.5)
    for row in range(0, board_size):
        value = row*square_size*math.sqrt(2)/2
        ix = width/2 - value
        iy = height/14 + value
        for elements in range(0, board_size):
            new_point = (ix+elements*square_size*numpy.cos(numpy.deg2rad(45)), iy+elements*square_size*numpy.sin(numpy.deg2rad(45)))
            center_points.append(new_point)


create_center_points()


def set_mouse_usage(visible=False, grab=True):
    global show_cursor_image
    if visible:
        show_cursor_image = False
    else:
        show_cursor_image = True
    pygame.mouse.set_visible(visible)  # both needed for set mouse in virtual mode
    pygame.event.set_grab(grab)


set_mouse_usage()

UI_REFRESH_RATE = timer.tick(dev_mode.DisplayFrequency)/1000
manager = pygame_gui.UIManager((width, height))

pieza1 = clases.Mage(500, 500, 13)


def draw():
    screen.blit(bkg_img, (0, 0))  # display background
    pieza1.draw(screen, pieza1.blue_mage_image)
    screen.blit(close_button, (height//0.6, height // 25))
    screen.blit(settings_button, (height//0.62, height // 25))
    screen.blit(minimize_button, (height//0.64, height // 25))

    """for i in center_points:
        pygame.draw.circle(screen, (255, 255, 255), (i[0], i[1]), 5)"""

    if show_cursor_image:
        screen.blit(cursor_default, pygame.mouse.get_pos())  # display cursor

    pygame.display.flip()  # Actualizar la pantalla #.update()


pygame.mixer.music.play(-1)
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
                elif minimize_button_rect.collidepoint(mouse_pos):  # check if button was clicked
                    minimized_state = not minimized_state
                    if minimized_state:
                        set_up_window(1.4)
                        create_center_points()
                        load_resources()
                        window = pyautogui.getWindowsWithTitle("Gambit Game")[0]
                        window.moveTo(100, 100)
                        clases.Piece.set_dimension(1.4)  # REVISAR ESTOOOOOOOOO
                        set_mouse_usage(True, False)
                    else:
                        pygame.quit(), pygame.init()
                        set_up_window(1, pygame.NOFRAME)
                        create_center_points()
                        load_resources()
                        clases.Piece.set_dimension()
                        set_mouse_usage(False, True)
                        break

        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:
                if follow_mouse:
                    follow_mouse = False
                    pieza1.pos_x, pieza1.pos_y = center_points[pieza1.detect_closest_point(center_points, event.pos)]

        elif event.type == pygame.KEYDOWN:
            if (pygame.key.name(event.key) == "w"):
                pieza1.mover(0, 1, True)
            elif (pygame.key.name(event.key) == "s"):
                pieza1.mover(0, -1, True)
            elif (pygame.key.name(event.key) == "a"):
                pieza1.mover(1, 0, True)
            elif (pygame.key.name(event.key) == "d"):
                pieza1.mover(-1, 0, True)
            elif (pygame.key.name(event.key) == "m"):
                pygame.mixer.music.stop()
            elif (pygame.key.name(event.key) == "escape"):
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw()

    timer.tick(dev_mode.DisplayFrequency)  # set the fps to the maximun possible
