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

game = clases.Game()
reproductor_sfx = clases.Sonido()  # creating an instance of the sound class to play sfx sounds
follow_mouse = False
minimized_state = False
show_cursor_image = True
active_pieces = [
    clases.Mage(500, 500, 13, "blue"),
    clases.Mage(700, 700, 13, "red"),
    clases.Archer(1000, 600, 13, "red"),
    clases.Archer(900, 700, 13, "blue"),
    clases.Knight(1000, 900, 13, "red"),
    clases.Knight(900, 1100, 13, "blue")
]
selected_piece = None


selected_background = 0  # backgrounds related variables
BACKGROUNDS_AMOUNT = 7

music_pause_state = False  # song related variables
generated_values = []
draw_music_slider = False
generation_count = 0

# SETING THINGS UP

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets the current directory to the file's directory

pygame.init()  # Inicializar Pygame
pygame.mixer.init()  # Inicializar el mixer para audios de Pygame


game.set_up_window()
# clases.Piece.set_dimension()  # sets the adecuate dimension for the pieces


def load_resources():

    global backgrounds, music_button_rect, music_button, cursor_default, close_button, close_button_rect, settings_button, settings_button_rect, minimize_button, minimize_button_rect

    backgrounds = []
    for i in range(0, BACKGROUNDS_AMOUNT):
        print(i)
        bkg_img = pygame.image.load(f"resources\\images\\background{i}.png").convert()  # load some images, converts it for optimization and then scales them.
        bkg_img = pygame.transform.smoothscale(bkg_img, (game.width, game.height))
        backgrounds.append(bkg_img)

    cursor_default = pygame.image.load("resources\\icons\\cursor_default.png").convert_alpha()
    cursor_default = pygame.transform.smoothscale(cursor_default, (game.screen_height * 0.805 // 43, game.screen_height // 43))

    close_button = pygame.image.load("resources\\icons\\x.png").convert_alpha()
    close_button = pygame.transform.smoothscale(close_button, (game.height // 24, game.height // 24))
    close_button_rect = close_button.get_rect()
    close_button_rect.topleft = (game.height//0.6, game.height // 25)

    settings_button = pygame.image.load("resources\\icons\\setting.png").convert_alpha()
    settings_button = pygame.transform.smoothscale(settings_button, (game.height // 24, game.height // 24))
    settings_button_rect = settings_button.get_rect()
    settings_button_rect.topleft = (game.height//0.62, game.height // 25)

    minimize_button = pygame.image.load("resources\\icons\\minimize.png").convert_alpha()
    minimize_button = pygame.transform.smoothscale(minimize_button, (game.height // 24, game.height // 24))
    minimize_button_rect = minimize_button.get_rect()
    minimize_button_rect.topleft = (game.height//0.64, game.height // 25)

    music_button = pygame.image.load("resources\\icons\\music.png").convert_alpha()
    music_button = pygame.transform.smoothscale(music_button, (game.height // 24, game.height // 24))
    music_button_rect = music_button.get_rect()
    music_button_rect.topleft = (game.height//0.66, game.height // 25)


load_resources()


game.create_center_points()


def set_mouse_usage(visible=False, grab=True):
    global show_cursor_image
    if visible:
        show_cursor_image = False
    else:
        show_cursor_image = True
    pygame.mouse.set_visible(visible)  # both needed for set mouse in virtual mode
    pygame.event.set_grab(grab)


set_mouse_usage()

UI_REFRESH_RATE = game.timer.tick(game.dev_mode.DisplayFrequency)/1000
manager = pygame_gui.UIManager((game.width, game.height))


def draw():
    game.screen.blit(backgrounds[selected_background], (0, 0))  # displaying background

    for piece in active_pieces:    # displaying all pieces
        piece.draw(game.screen, piece.image)

    game.screen.blit(close_button, (game.height//0.6, game.height // 25))  # displaying buttons
    game.screen.blit(settings_button, (game.height//0.62, game.height // 25))
    game.screen.blit(minimize_button, (game.height//0.64, game.height // 25))
    game.screen.blit(music_button, (game.height//0.66, game.height // 25))

    if draw_music_slider:  # displaying music slider
        pass

    # for i in game.center_points:
    #    pygame.draw.circle(game.screen, (255, 255, 255), (i[0], i[1]), 40)

    if show_cursor_image:  # displaying cursor
        game.screen.blit(cursor_default, pygame.mouse.get_pos())

    pygame.display.flip()  # update the screen. /    .update() also works


def play_song(playlist=game.PLAYLIST):  # a function that plays a random song from the playlist with no repetitions for iterations_without_repeating calls

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
                        game.set_up_window(1.4)
                        game.create_center_points()
                        load_resources()
                        window = pyautogui.getWindowsWithTitle("Gambit Game")[0]
                        window.moveTo(100, 100)
                        clases.Piece.set_dimension(1.4)  # REVISAR ESTOOOOOOOOO
                        set_mouse_usage(True, False)
                    else:
                        pygame.quit(), pygame.init()
                        game.set_up_window(1, pygame.NOFRAME)
                        game.create_center_points()
                        load_resources()
                        clases.Piece.set_dimension()
                        set_mouse_usage(False, True)
                        break
                elif music_button_rect.collidepoint(mouse_pos):  # check if button was clicked
                    draw_music_slider = True

        if event.type == pygame.MOUSEBUTTONUP:

            mouse_pos = event.pos  # get the current mouse position

            if event.button == 1:
                reproductor_sfx.reproducir_en_hilo(game.SFX[1])

                if follow_mouse:
                    follow_mouse = False
                    which_point = active_pieces[selected_piece].detect_closest_point(event.pos)
                    # active_pieces[selected_piece].pos_x, active_pieces[selected_piece].pos_y = game.center_points[which_point]
                    gx, gy = piece.b64index_to_grid(which_point)  # gets the grid conversion of the coincident point
                    active_pieces[selected_piece].grid_pos_to_pixels(gx, gy, True)  # sets the grid pos to the adecuate one, as well as the pos_x which is the pixel position

            elif event.button == 3:
                if music_button_rect.collidepoint(mouse_pos):  # check if button was clicked
                    music_pause_state = not music_pause_state
                    if music_pause_state:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        elif event.type == pygame.KEYDOWN:  # if a key was pressed
            if (pygame.key.name(event.key) == "t" and selected_background < BACKGROUNDS_AMOUNT-1):  # used to change into diff background images
                selected_background += 1
            elif (pygame.key.name(event.key) == "g" and selected_background > 0):
                selected_background -= 1

            elif (pygame.key.name(event.key) == "w"):
                active_pieces[selected_piece].move(-2, 0, True)
                # active_pieces[selected_piece].place(0, 7, True)
            elif (pygame.key.name(event.key) == "s"):
                active_pieces[selected_piece].move(2, 0, True)
                # active_pieces[selected_piece].place(0, 0, True)
            elif (pygame.key.name(event.key) == "a"):
                active_pieces[selected_piece].move(0, 2, True)
                # active_pieces[selected_piece].place(7, 0, True)
            elif (pygame.key.name(event.key) == "d"):
                active_pieces[selected_piece].move(0, -2, True)
                # active_pieces[selected_piece].place(7, 7, True)
            elif (pygame.key.name(event.key) == "m"):
                pygame.mixer.music.stop()
            elif (pygame.key.name(event.key) == "escape"):
                pygame.quit()
                sys.exit()

            # print(active_pieces[selected_piece].mana)
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw()

    game.timer.tick(game.dev_mode.DisplayFrequency)  # set the fps to the maximun possible
