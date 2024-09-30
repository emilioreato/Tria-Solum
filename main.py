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
import random

# GENERAL VARIABLES

follow_mouse = False
minimized_state = False
show_cursor_image = True
center_points = []
active_pieces = [
    clases.Mage(500, 500, 13, "blue"),
    clases.Mage(700, 700, 13, "red"),
    clases.Archer(1000, 600, 13, "red"),
    clases.Archer(900, 700, 13, "blue"),
    clases.Knight(1000, 900, 13, "red"),
    clases.Knight(900, 1100, 13, "blue")
]
selected_piece = None
board_size = 8

selected_background = 0
BACKGROUNDS_AMOUNT = 7

music_pause_state = False
generated_values = []
draw_music_slider = False
generation_count = 0
PLAYLIST = [
    "resources\\sounds\\soundtracks\\track1 (gerilim).mp3",
    "resources\\sounds\\soundtracks\\track2 (saver dontrikh).mp3",
    "resources\\sounds\\soundtracks\\track3 (vioglt dontrikh).mp3"
]


# SETING THINGS UP

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets the current directory to the file's directory

pygame.init()  # Inicializar Pygame
pygame.mixer.init()  # Inicializar el mixer para audios de Pygame


def set_up_window(screenratio=1, frame=0):  # is the ratio screen/window
    global screen, width, height, screen_height, timer, dev_mode
    _, screen_height = pyautogui.size()  # gets the current resolution
    height = round(screen_height/screenratio)  # reduces the height
    width = round(height*(16/9))  # sets the aspect ratio to 16:9
    screen = pygame.display.set_mode((width, height), frame)  # sets window resolution

    pygame.display.set_caption("Gambit Game 2024®")  # set a window title

    pygame.display.set_icon(pygame.image.load("resources\\images\\indicator.png").convert_alpha())  # sets window icon

    timer = pygame.time.Clock()  # create a clock object to set fps
    dev_mode = EnumDisplaySettings(None, ENUM_CURRENT_SETTINGS)  # get the OS's fps setting


set_up_window()
# clases.Piece.set_dimension()  # sets the adecuate dimension for the pieces


def load_resources():

    global backgrounds, music_button_rect, music_button, cursor_default, close_button, close_button_rect, settings_button, settings_button_rect, minimize_button, minimize_button_rect

    backgrounds = []
    for i in range(0, BACKGROUNDS_AMOUNT):
        print(i)
        bkg_img = pygame.image.load(f"resources\\images\\background{i}.png").convert()  # load some images, converts it for optimization and then scales them.
        bkg_img = pygame.transform.smoothscale(bkg_img, (width, height))
        backgrounds.append(bkg_img)

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

    music_button = pygame.image.load("resources\\icons\\music.png").convert_alpha()
    music_button = pygame.transform.smoothscale(music_button, (height // 24, height // 24))
    music_button_rect = music_button.get_rect()
    music_button_rect.topleft = (height//0.66, height // 25)


load_resources()


def create_center_points():
    center_points.clear()  # clean previous points (wrongly sized probably)
    square_size = height/13.55
    for row in range(0, board_size):  # create 8 rows
        value = row*square_size*math.sqrt(2)/2  # how much each row should go back on x axis
        ix = width/2 - value  # first point on the row x value (base value for entire row)
        iy = height/14.1 + value  # first point on the row y value (base value for entire row)
        for elements in range(0, board_size):  # create 8 elements in each row (columns)
            # create a tuple with the x and y coor of each point and then append it to the points list.
            new_point = (round(ix+elements*square_size*numpy.cos(numpy.deg2rad(45))), round(iy+elements*square_size*numpy.sin(numpy.deg2rad(45))))
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


def draw():
    screen.blit(backgrounds[selected_background], (0, 0))  # displaying background
    for piece in active_pieces:    # displaying all pieces
        piece.draw(screen, piece.image)
    screen.blit(close_button, (height//0.6, height // 25))  # displaying buttons
    screen.blit(settings_button, (height//0.62, height // 25))
    screen.blit(minimize_button, (height//0.64, height // 25))
    screen.blit(music_button, (height//0.66, height // 25))

    if draw_music_slider:  # displaying music slider
        pass

    for i in center_points:
        pygame.draw.circle(screen, (255, 255, 255), (i[0], i[1]), 40)

    if show_cursor_image:  # displaying cursor
        screen.blit(cursor_default, pygame.mouse.get_pos())

    pygame.display.flip()  # update the screen. /    .update() also works


def play_song(playlist=PLAYLIST):  # a function that plays a random song from the playlist with no repetitions for iterations_without_repeating calls

    def generate():
        while True:

            global generation_count, generated_values

            iterations_without_repeating = 2

            generation_count += 1  # Aumenta el contador de generaciones

            if generation_count > iterations_without_repeating:  # Si hemos alcanzado el número de generaciones, reinicia la lista
                generated_values = []
                generation_count = 1  # Reinicia el contador

            if len(generated_values) == len(playlist):  # Si la lista de valores generados es igual a la lista de elementos, reiniciamos también la lista de elementos disponibles
                generated_values = []

            item = random.choice(playlist)  # Selecciona un elemento aleatorio que no haya sido generado
            while item in generated_values:
                item = random.choice(playlist)

            generated_values.append(item)
            yield item  # Usamos yield para devolver el elemento

    track = next(generate())

    pygame.mixer.music.load(track)  # loads the track
    print(f"Reproduciendo: {track}")

    pygame.mixer.music.play()  # plays the track

    pygame.mixer.music.set_volume(0.2)


def stopmusic():
    pygame.mixer.quit()  # close the pygame mixer


run = True
iterations = 0
init_time = time.time()
while run:  # Main loop

    iterations += 1  # iterator used to control events

    if iterations % 500 == 0 and not music_pause_state:
        if not pygame.mixer.music.get_busy():
            play_song()
            # pygame.mixer.music.pause()
            # pygame.mixer.music.unpause()
            # pygame.mixer.music.play(-1)

    if follow_mouse and selected_piece != None:
        active_pieces[selected_piece].pos_x, active_pieces[selected_piece].pos_y = event.pos
    else:
        pass

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                mouse_pos = event.pos  # get the current mouse position

                for piece in active_pieces:  # Checks if any piece was clicked
                    if piece.is_clicked(mouse_pos, (piece.pos_x, piece.pos_y)):  # Comprobar si el clic está dentro del circulo
                        print("pieza clickeada")
                        follow_mouse = True
                        selected_piece = active_pieces.index(piece)

                if close_button_rect.collidepoint(mouse_pos):  # check if button was clicked
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
                elif music_button_rect.collidepoint(mouse_pos):  # check if button was clicked
                    draw_music_slider = True

        if event.type == pygame.MOUSEBUTTONUP:

            mouse_pos = event.pos  # get the current mouse position

            if event.button == 1:
                if follow_mouse:
                    follow_mouse = False
                    which_point = active_pieces[selected_piece].detect_closest_point(center_points, event.pos)
                    active_pieces[selected_piece].pos_x, active_pieces[selected_piece].pos_y = center_points[which_point]
                    active_pieces[selected_piece].grid_pos_x, active_pieces[selected_piece].grid_pos_y = piece.b64index_to_grid(which_point)  # sets the grid pos to the adecuate one

            elif event.button == 2:
                if music_button_rect.collidepoint(mouse_pos):  # check if button was clicked
                    music_pause_state = not music_pause_state
                    if music_pause_state:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        elif event.type == pygame.KEYDOWN:  # if a key was pressed
            if (pygame.key.name(event.key) == "w" and selected_background < BACKGROUNDS_AMOUNT-1):  # used to change into diff background images
                selected_background += 1
            elif (pygame.key.name(event.key) == "s" and selected_background > 0):
                selected_background -= 1

            elif (pygame.key.name(event.key) == "a"):
                active_pieces[0].mover(1, 0, True)
            elif (pygame.key.name(event.key) == "d"):
                active_pieces[0].mover(-1, 0, True)
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
