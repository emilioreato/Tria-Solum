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

# SETING THINGS UP

game = clases.Game()
sfx_player = clases.Sound()  # creating an instance of the sound class to play sfx sounds

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets the current directory to the file's directory

pygame.init()  # Inicializar Pygame
pygame.mixer.init()  # Inicializar el mixer para audios de Pygame

game.set_up_window()
clases.Piece.set_dimension()  # sets the adecuate dimension for the pieces

game.load_resources()
game.create_center_points()


# GENERAL VARIABLES

active_pieces = [
    clases.Mage(5, 5, 11, "blue"),
    clases.Mage(4, 4, 11, "red"),
    clases.Archer(6, 6, 11, "red"),
    clases.Archer(7, 7, 11, "blue"),
    clases.Knight(1, 1, 11, "red"),
    clases.Knight(2, 6, 5, "blue")
]
selected_piece = None

follow_mouse = False
minimized_state = False
show_cursor_image = True

selected_background = 0  # backgrounds related variables

music_pause_state = False  # song related variables
generated_values = []
draw_music_slider = False
generation_count = 0


# USEFUL FUNCTIONS

def colindepoint_with_sound(rect, point_pos):  # a modified version of collidepoint() so it plays the click sfx sound when its true. used for buttons

    collided = rect.collidepoint(point_pos)

    if collided:
        sfx_player.play_on_thread(game.SFX[1])
        return True
    return False


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
    game.screen.blit(game.backgrounds[selected_background], (0, 0))  # displaying background

    for piece in active_pieces:    # displaying all pieces
        piece.draw(game.screen, piece.image)

    game.screen.blit(game.close_button, (game.height//0.6, game.height // 25))  # displaying buttons
    game.screen.blit(game.settings_button, (game.height//0.62, game.height // 25))
    game.screen.blit(game.minimize_button, (game.height//0.64, game.height // 25))
    game.screen.blit(game.music_button, (game.height//0.66, game.height // 25))

    if draw_music_slider:  # displaying music slider
        pass

    # for i in game.center_points:
    #    pygame.draw.circle(game.screen, (255, 255, 255), (i[0], i[1]), a)

    if show_cursor_image:  # displaying cursor
        game.screen.blit(game.cursor_default, pygame.mouse.get_pos())

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

    # print(iterations)

    # checks if its due to play another song every 600 iterations. it can be bypassed by being the fisrt iteration. when pause is enabled you cant play music
    if (iterations % 600 == 0 or (iterations == 0 and time.time()-init_time < 20)) and not music_pause_state:
        if not pygame.mixer.music.get_busy():
            play_song()

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

                if colindepoint_with_sound(game.close_button_rect, mouse_pos):  # check if button was clicked
                    pygame.quit()
                    sys.exit()
                elif colindepoint_with_sound(game.minimize_button_rect, mouse_pos):  # check if button was clicked
                    minimized_state = not minimized_state
                    if minimized_state:
                        game.set_up_window(1.4)
                        clases.Piece.set_dimension()
                        game.create_center_points()
                        game.load_resources()
                        window = pyautogui.getWindowsWithTitle("Gambit Game")[0]
                        window.moveTo(100, 100)

                        piece.resize(active_pieces)
                        set_mouse_usage(True, False)
                    else:
                        pygame.quit(), pygame.init()
                        game.set_up_window(1, pygame.NOFRAME)
                        clases.Piece.set_dimension()
                        game.create_center_points()
                        game.load_resources()

                        piece.resize(active_pieces)
                        set_mouse_usage(False, True)
                        break
                elif colindepoint_with_sound(game.music_button_rect, mouse_pos):  # check if button was clicked
                    draw_music_slider = True
                elif colindepoint_with_sound(game.settings_button_rect, mouse_pos):  # check if button was clicked
                    pass

        if event.type == pygame.MOUSEBUTTONUP:

            mouse_pos = event.pos  # get the current mouse position

            if event.button == 1:

                if follow_mouse:

                    sfx_player.play_on_thread(game.SFX[5])

                    follow_mouse = False
                    which_point = active_pieces[selected_piece].detect_closest_point(event.pos)
                    # active_pieces[selected_piece].pos_x, active_pieces[selected_piece].pos_y = game.center_points[which_point]
                    gx, gy = piece.b64index_to_grid(which_point)  # gets the grid conversion of the coincident point
                    active_pieces[selected_piece].grid_pos_to_pixels(gx, gy, change_mana=True)  # sets the grid pos to the adecuate one, as well as the pos_x which is the pixel position

            elif event.button == 3:
                if game.music_button_rect.collidepoint(mouse_pos):  # check if button was clicked
                    music_pause_state = not music_pause_state
                    if music_pause_state:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        elif event.type == pygame.KEYDOWN:  # if a key was pressed
            if (pygame.key.name(event.key) == "t" and selected_background < game.BACKGROUNDS_AMOUNT-1):  # used to change into diff background images
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
                stopmusic()
                pygame.quit()
                sys.exit()

            # print(active_pieces[selected_piece].mana)
        elif event.type == pygame.QUIT:
            stopmusic()
            pygame.quit()
            sys.exit()

    draw()

    game.timer.tick(game.dev_mode.DisplayFrequency)  # set the fps to the maximun possible

    iterations += 1  # iterator used to control events
