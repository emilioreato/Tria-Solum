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
sound_player = clases.Sound()  # creating an instance of the sound class to play sfx sounds

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets the current directory to the file's directory

pygame.init()  # Inicializar Pygame
pygame.mixer.init()  # Inicializar el mixer para audios de Pygame
pygame.mixer.music.set_volume(0.4)

game.set_up_window()
clases.Piece.set_dimension()  # sets the adecuate dimension for the pieces

game.load_resources()
game.create_center_points()


# GENERAL VARIABLES

active_pieces = [
    clases.Mage(5, 5, 30, "blue"),
    clases.Mage(4, 4, 30, "red"),
    clases.Archer(6, 6, 30, "red"),
    clases.Archer(7, 7, 30, "blue"),
    clases.Knight(1, 1, 30, "red"),
    clases.Knight(2, 6, 30, "blue")
]
selected_piece = None

show_config_menu = False

follow_mouse = False
shrink_state = False
show_cursor_image = True
cursor = game.cursor_default

selected_background = 0  # backgrounds related variables

music_pause_state = False  # audio related variables
current_volume = 0.5

generated_values = []
generation_count = 0


clases.UI.init()
config_menu = clases.Menu()


# USEFUL FUNCTIONS

def collidepoint_with_sound(rect, point_pos):  # a modified version of collidepoint() so it plays the click sfx sound when its true. used for btns

    collided = rect.collidepoint(point_pos)

    if collided:
        sound_player.play_on_thread(sound_player.SFX[1])
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

    game.screen.blit(game.x_btn, (game.x_btn_metrics["x"], game.x_btn_metrics["y"]))  # displaying btns
    game.screen.blit(game.shrink_btn, (game.shrink_btn_metrics["x"], game.shrink_btn_metrics["y"]))
    game.screen.blit(game.minimize_btn, (game.minimize_btn_metrics["x"], game.minimize_btn_metrics["y"]))
    game.screen.blit(game.settings_btn, (game.settings_btn_metrics["x"], game.settings_btn_metrics["y"]))

    # for i in game.center_points:
    #    pygame.draw.circle(game.screen, (255, 255, 255), (i[0], i[1]), a)

    if show_config_menu:
        config_menu.run(show_music=show_config_menu)

    if show_cursor_image:  # displaying cursor
        game.screen.blit(cursor, pygame.mouse.get_pos())

    pygame.display.flip()  # update the screen. /    .update() also works


def play_song(playlist=sound_player.PLAYLIST):  # a function that plays a random song from the playlist with no repetitions for iterations_without_repeating calls

    def generate():
        while True:

            global generation_count, generated_values

            iterations_without_repeating = 6

            generation_count += 1  # increase the generations count

            if generation_count > iterations_without_repeating:  # Si hemos alcanzado el número de generaciones, reinicia la lista
                generated_values = []
                generation_count = 1  # Reinicia el contador

            if len(generated_values) == len(playlist):  # Si la lista de valores generados es igual a la lista de elementos, reiniciamos también la lista de elementos disponibles
                generated_values = []

            item = random.choice(playlist)  # selec a random song from playlist that has not been selected yet
            while item in generated_values:
                item = random.choice(playlist)

            generated_values.append(item)
            yield item  # yield to return the item

    track = next(generate())

    pygame.mixer.music.load(track)  # loads the track
    print(f"Reproduciendo: {track}")

    pygame.mixer.music.play()  # plays the track


def stopmusic():
    pygame.mixer.quit()  # close the pygame mixer


# varibles needed to control fps
start_time = time.time()  # Record the starting time
loop_count = 0


# this variables "ite" just count how many repetitions the loop has made and when some event should be analized
ite0 = 0
ite1 = 0
ite2 = 0

init_time = time.time()  # saves the time when the loop was entered
while True:  # Main loop

    # checks if its due to play another song every 600 iterations. it can be bypassed by being the fisrt iteration. when pause is enabled you cant play music
    if (ite0 >= 600 or (ite0 == 0 and time.time()-init_time < 20)):
        if not music_pause_state:  # you also have to check if the music is not paused
            ite0 = 0
            if not pygame.mixer.music.get_busy():
                play_song()

    if follow_mouse:  # when you are moving a piece you want it to follow your mouse, so you update the piece position to be exactly the same as your mouse's
        if selected_piece != None:
            active_pieces[selected_piece].pos_x, active_pieces[selected_piece].pos_y = event.pos

    for event in pygame.event.get():  # manage events

        if event.type == pygame.MOUSEMOTION:  # checks for btns(their rectangles) being hovered
            if (ite1 >= 15):
                ite1 = 0
                cursor = game.cursor_default
                for rect in game.rects_list:
                    if rect.collidepoint(event.pos):  # check if every btn was hovered
                        cursor = game.cursor_hand
                        break

            if (ite2 >= 8):
                ite2 = 0
                pygame.mixer.music.set_volume(config_menu.sliders[0].current_value)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # then event.pos is used and it only tells the position of the mouse when the event occured

                for piece in active_pieces:  # Checks if any piece was clicked
                    if piece.is_clicked(event.pos, (piece.pos_x, piece.pos_y)):  # Comprobar si el clic está dentro del circulo
                        print("pieza clickeada")
                        follow_mouse = True
                        selected_piece = active_pieces.index(piece)

                if collidepoint_with_sound(game.x_btn_rect, event.pos):  # check if btn was clicked
                    time.sleep(0.4)
                    pygame.quit()
                    sys.exit()
                elif collidepoint_with_sound(game.shrink_btn_rect, event.pos):  # check if btn was clicked
                    shrink_state = not shrink_state  # pulsator to conmutator logic
                    window = pyautogui.getWindowsWithTitle("Gambit Game")[0]  # find the program window in the OS so its position can be changed

                    if shrink_state:
                        window.moveTo(180, 100)  # move the window
                        game.set_up_window(1.4)
                        clases.Piece.set_dimension()
                        game.create_center_points()
                        game.load_resources()
                        piece.resize(active_pieces)
                        set_mouse_usage(True, False)
                    else:
                        game.set_up_window(1, pygame.NOFRAME)
                        clases.Piece.set_dimension()
                        window.moveTo(0, 0)  # move the window
                        game.create_center_points()
                        game.load_resources()
                        piece.resize(active_pieces)
                        set_mouse_usage(False, True)
                        break
                elif collidepoint_with_sound(game.minimize_btn_rect, event.pos):  # check if btn was clicked
                    window = pyautogui.getWindowsWithTitle("Gambit Game")[0]  # find the game window in the OS
                    window.minimize()  # minimize the window
                elif collidepoint_with_sound(game.settings_btn_rect, event.pos):  # check if btn was clicked
                    show_config_menu = not show_config_menu

            elif event.button == 3:
                if game.music_btn_rect.collidepoint(event.pos):  # check if btn was clicked
                    music_pause_state = not music_pause_state
                    if music_pause_state:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                if follow_mouse:  # if we were moving a piece
                    follow_mouse = False

                    sound_player.play_on_thread(sound_player.SFX[5])

                    which_point = active_pieces[selected_piece].detect_closest_point(event.pos)  # event pos is the mouse position at the moment of the event
                    gx, gy = piece.b64index_to_grid(which_point)  # gets the grid conversion of the coincident point
                    if not piece.check_for_pieces_in_the_grid_coordinates(active_pieces, gx, gy):
                        active_pieces[selected_piece].grid_pos_to_pixels(gx, gy, change_mana=True)  # sets the grid pos to the adecuate one, as well as the pos_x which is the pixel position
                    else:
                        active_pieces[selected_piece].grid_pos_to_pixels(active_pieces[selected_piece].grid_pos_x, active_pieces[selected_piece].grid_pos_y, change_mana=True)
                    print(active_pieces[selected_piece].mana)

        elif event.type == pygame.KEYDOWN:  # if a key was pressed
            if (pygame.key.name(event.key) == "t" and selected_background < game.BACKGROUNDS_AMOUNT-1):  # used to change into diff background images
                selected_background += 1
            elif (pygame.key.name(event.key) == "g" and selected_background > 0):
                selected_background -= 1

            elif (pygame.key.name(event.key) == "w"):
                active_pieces[selected_piece].move(-1, 0, True)
                # active_pieces[selected_piece].place(0, 7, True)
            elif (pygame.key.name(event.key) == "s"):
                active_pieces[selected_piece].move(1, 0, True)
                # active_pieces[selected_piece].place(0, 0, True)
            elif (pygame.key.name(event.key) == "a"):
                active_pieces[selected_piece].move(0, 1, True)
                # active_pieces[selected_piece].place(7, 0, True)
            elif (pygame.key.name(event.key) == "d"):
                active_pieces[selected_piece].move(0, -1, True)
                # active_pieces[selected_piece].place(7, 7, True)
            elif (pygame.key.name(event.key) == "m"):
                pygame.mixer.music.stop()
            elif (pygame.key.name(event.key) == "escape"):
                time.sleep(0.4)
                stopmusic()
                pygame.quit()
                sys.exit()

        elif event.type == pygame.QUIT:
            time.sleep(0.4)
            stopmusic()
            pygame.quit()
            sys.exit()

    draw()

    ite0 += 1  # iterator used to control events
    ite1 += 1
    ite2 += 1

    # FPS CONTER
    loop_count += 1  # Increment the counter on each loop
    if time.time() - start_time >= 1:
        print(loop_count)
        loop_count = 0
        start_time = time.time()

    game.timer.tick(game.dev_mode.DisplayFrequency)  # set the fps to the maximun possible
