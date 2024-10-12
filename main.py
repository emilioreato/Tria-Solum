import installer
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets the current directory to the file's directory # noqa


def install_libraries():  # noqa
    libraries_to_install = installer.Installer.check_libraries_installation_status("installation_status.txt")  # this 3 lines check if the needed modules are installed, if not it installs them # noqa
    if libraries_to_install:  # noqa
        installer.Installer.install_libraries_from_list(libraries_to_install, "installation_status.txt")  # noqa


install_libraries()  # noqa

import sys

import time
import numpy
import ctypes
import math
import random
import copy
import threading
import cv2
import pygame
import pygame_gui
from pygame.locals import *
import pyautogui  # from pyautogui import press  # do not delete this eventhough it is not used, for some reason it increases the render quality # noqa

import clases  # noqa
import dev_mouse  # noqa
from online_utilities import firewall, online_tools, portforwarding
from media import Media


# SETING THINGS UP


pygame.init()  # initialize pygame
game = clases.Game()
game.set_up_window(1.4)


# GENERAL VARIABLES

play_online = False
my_team = "blue"

active_uis = {
    "intro": True,
    "lobby": False,
    "match_creation": False,
    "piece_selection": False,
    "ingame": False,
    "settings": False,
    "chat": False,
}

my_pieces = []
reference_pieces = []
active_pieces = []

selected_piece = None

current_turn = None

online_set_up_done = False

just_clicked_smth = False

follow_mouse = False
shrink_state = False

selected_background = 0

music_pause_state = False  # audio related variables

intro_path = {"video": "resources\\intro\\GambitGames.mp4",  # path of the video and the audio for the intro
              "audio": "resources\\intro\\intro_audio.mp3"}


# USEFUL FUNCTIONS

def setup():
    global piece_selection_menu, config_menu, turn_btn, mini_flag, lobby, sound_player, cursor, match_creation

    sound_player = clases.Sound()  # creating an instance of the sound class to play sfx sounds

    Media.load_media(game.height)
    Media.resize(game.height)

    clases.UI.init()
    config_menu = clases.Menu()
    turn_btn = clases.Turn_Btn()
    mini_flag = clases.Mini_Flags()
    lobby = clases.Lobby()
    match_creation = clases.MatchCreation()
    piece_selection_menu = clases.Piece_Selection_Menu()

    game.create_center_points()

    cursor = clases.Cursor()


def set_up_online(mode):  # this function sets up the server and client objects as adecuate, opens the needed port, checks firewall instalation status and also connects both users though a socket connection
    global port
    port = 8050  # this port seems to work pretty well
    firewall.FirewallRules.check_firewall_installation_status('installation_status.txt', port)

    local_ip = online_tools.Online.get_local_ip()
    print(local_ip)

    portforwarding.Portforwarding.initialize()
    if not portforwarding.Portforwarding.check_ports(port):
        portforwarding.Portforwarding.open_port(local_ip, port, port, "TCP")

    if mode == "server":
        global sckt
        sckt = online_tools.Client()
        ip = input("Ingrese la clave de la partida:").strip()
        sckt.set_up_client(ip, port)
    elif mode == "client":
        sckt = online_tools.Server()
        # print("La clave de tu partida es:", online_tools.Online.get_public_ip())
        sckt.set_up_server(port)

    global online_set_up_done
    online_set_up_done = True


def receive_messages():  # This function receives messages from the server while being executed in a thread so it doesnt block the main loop. The messages are in the following format: action-arguments(n). Note that the - (hyphen is a separation marker)
    while True:  # infinite loop while the program is executed
        entry = sckt.recieve()  # reads the message(s) from the buffer and stores them
        print(entry, "recibido")
        for entry in entry.split(";"):  # iterates over each message that are separated by ";".

            if type(entry) == list:
                if entry[-1] == "":
                    entry.pop(-1)  # gets rid of the last item of the list if it is an empty string

            args = entry.split("-")  # gets all the arguments in a list. the fisrt item of the list is the action btw
            print(args)

            match args[0]:  # decides what to do based on the action received
                case "attacked":  # id-id2 . thats the format this case expects to receive. id is the identifier of the attacker and id2 is the identifier of the attacked piece
                    for piece in active_pieces:
                        if piece.id == args[1]:
                            for attacked_piece in active_pieces:
                                if attacked_piece.id == args[2]:
                                    piece.attack(attacked_piece)  # those for loops just find the attacker and the attacked piece in the actieve_pieces list and then this line executes the attack
                                    break

                case "moved":  # id-x-y. thats the format this case expects to receive. id is the identifier of the piece that moved and x and y are the new coordinates
                    piece_id = args[1]
                    for piece in active_pieces:
                        if piece.id == piece_id:
                            # those for loops just find the piece in the actieve_pieces list and then this line executes the move
                            piece.grid_pos_to_pixels(clases.Piece.pov_based_pos_translation(int(args[2])), clases.Piece.pov_based_pos_translation(int(args[3])), bypass_mana=False, change_mana=True)

                case "turn":
                    change_turn()

                case "created":  # specie-x-y-team-hp-mana-agility-defense-damage-id. thats the format this case expects to receive, all the arguments to create a new piece which is going to be exactly the same as the one our enemy created
                    p_specie = args[1]
                    p_x = clases.Piece.pov_based_pos_translation(int(args[2]))
                    p_y = clases.Piece.pov_based_pos_translation(int(args[3]))
                    p_team = args[4]
                    p_hp = int(args[5])
                    p_mana = int(args[6])
                    p_agility = int(args[7])
                    p_defense = int(args[8])
                    p_damage = int(args[9])
                    p_id = args[10]

                    print("info recevibed: ", p_specie, "  ", p_x, "  ", p_y, "  ", p_team, "  ", p_hp, "  ", p_mana, "  ", p_agility, "  ", p_defense, "  ", p_damage, "  ", p_id)

                    if p_specie == "mage":  # based on the specie of the piece we use different clases
                        active_pieces.append(clases.Mage(p_x, p_y, p_team, p_hp, p_mana, p_agility, p_defense, p_damage, specify_id=p_id))
                        print(active_pieces)
                    elif p_specie == "archer":
                        active_pieces.append(clases.Archer(p_x, p_y, p_team, p_hp, p_mana, p_agility, p_defense, p_damage, specify_id=p_id))
                        print(active_pieces)
                    elif p_specie == "knight":
                        active_pieces.append(clases.Knight(p_x, p_y, p_team, p_hp, p_mana, p_agility, p_defense, p_damage, specify_id=p_id))
                        print(active_pieces)

                case "dead":
                    for piece in active_pieces:
                        if piece.id == args[1]:
                            active_pieces.remove(piece)
                    global selected_piece
                    selected_piece = None

                case "exit":
                    print("the enemy has abandoned the game")

                case _:
                    print("unknown command:", args[0])


def assign_teams():  # this function assigns the teams to the players
    global my_team
    if (sckt.mode == "server"):  # choosing of the teams and setting up the socket connection
        my_team = random.choice(["blue", "red"])  # randomly chooses the team of the player
        sckt.send(my_team, delimiter="")
        if my_team == "blue":  # a quick definition of the enemy team
            enemy_team = "red"
        else:
            enemy_team = "blue"
    else:
        enemy_team = sckt.recieve()
        if enemy_team == "blue":  # a quick definition of the enemy team
            my_team = "red"
        else:
            my_team = "blue"


def assign_turn():
    global current_turn
    current_turn = random.choice(["blue", "red"])
    if play_online:
        if (sckt.mode == "server"):
            sckt.send(current_turn, delimiter="")
        else:
            current_turn = sckt.recieve()


def play_intro_video():

    cap = cv2.VideoCapture(intro_path["video"])

    fps = cap.get(cv2.CAP_PROP_FPS)  # Obtener la tasa de frames del video

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    video_clock = pygame.time.Clock()

    start_time = time.time()

    while cap.isOpened():

        ret, frame = cap.read()  # Leer el siguiente frame

        if ret:

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir el frame de OpenCV (BGR) a RGB para Pygame
            frame = cv2.resize(frame, (game.width, game.height))  # Ajustar el tamaño

            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # Convertir a una superficie de Pygame

            game.screen.blit(frame_surface, (0, 0))

            pygame.display.update()

            elapsed_time = time.time() - start_time
            current_frame = int(elapsed_time * fps)

            # Terminar el bucle si se ha llegado al final del video
            if current_frame >= total_frames:
                break

        video_clock.tick(fps+fps*0.01)  # I needed just a little bit more of extra delay

    cap.release()
    active_uis["intro"] = False


def play_intro_audio():
    pygame.mixer.music.load(intro_path["audio"])
    pygame.mixer.music.play()


def finish_program():  # this function closes the program
    global running
    running = False  # in case some thread ends up in the main "while" loop you make sure it stops anyways
    try:
        sckt.send("exit")
    except:
        pass
    try:
        if (sckt.mode == "server"):
            sckt.close()  # you should to close the socket
    except:
        pass
    try:
        portforwarding.Portforwarding.close_port(port)  # when the app is about to close you also need to close the port for security reasons
    except:
        pass
    time.sleep(0.1)
    try:
        stopmusic()
        pygame.quit()
        sys.exit()
    except:
        sys.exit()


def change_turn():  # changes the current turn from blue to red or red to blue
    global current_turn
    if current_turn == "blue":
        current_turn = "red"
    else:
        current_turn = "blue"
    print(f"Turno del equipo {current_turn}")  # Mensaje para depuración


def collidepoint_with_sound(rect, point_pos):  # a modified version of collidepoint() so it plays the click sfx sound when its true. used for btns

    collided = rect.collidepoint(point_pos)

    if collided:
        sound_player.play_sfx(sound_player.SFX[1])
        global just_clicked_smth
        just_clicked_smth = True
        return True
    return False


def get_at_with_sound(rect, relative_pos):  # the same as collidepoint_with_sound() but for irregular images
    collided = rect.get_at(relative_pos)
    if collided:
        sound_player.play_sfx(sound_player.SFX[1])
        global just_clicked_smth
        just_clicked_smth = True
        return True
    return False


# this function is used to check if the rect of an element is allowed to be used in the current ui. excellent for button that you want to be active only in certain ui like the lobby and not in the ingame.
def check_ui_allowance(element_in_media_rect_list):

    use_in = element_in_media_rect_list["use_rect_in"]

    if type(use_in) == list:
        for possible_use in use_in:
            if active_uis[possible_use] == True:
                return True
    else:
        if use_in == "all" or active_uis[use_in] == True:
            return True
    return False


def set_mouse_usage(visible=False, grab=True):
    if visible:
        clases.Cursor.show_cursor = False
    else:
        clases.Cursor.show_cursor = True
    pygame.mouse.set_visible(visible)  # both needed for set mouse in virtual mode
    pygame.event.set_grab(grab)


def draw():

    game.screen.blit(Media.backgrounds[selected_background], (0, 0))  # displaying background

    if (ite0 == 400 and active_uis["ingame"]):
        print("wow", len(active_pieces))

    if active_uis["lobby"]:
        lobby.draw()
    if active_uis["settings"]:
        config_menu.run(show_music=True)

    game.screen.blit(Media.sized["x_btn"], (Media.metrics["x_btn"]["x"], Media.metrics["x_btn"]["y"]))  # displaying btns
    game.screen.blit(Media.sized["shrink_btn"], (Media.metrics["shrink_btn"]["x"], Media.metrics["shrink_btn"]["y"]))
    game.screen.blit(Media.sized["minimize_btn"], (Media.metrics["minimize_btn"]["x"], Media.metrics["minimize_btn"]["y"]))
    game.screen.blit(Media.sized["setting_btn"], (Media.metrics["setting_btn"]["x"], Media.metrics["setting_btn"]["y"]))

    if active_uis["piece_selection"]:  # what has to be shown when the piece selection menu is active (reference pieces to chosse from and the menu itself which is the background)

        piece_selection_menu.draw(my_team)

    mini_flag.draw(current_turn)
    turn_btn.draw()

    my_team_count = 0
    enemy_count = 0
    for piece in active_pieces:    # displaying all pieces and their health and mana bars
        if piece.team == my_team:
            my_team_count += 1
        else:
            enemy_count += 1
        piece.draw(game.screen, piece.image)
        piece.draw_health_bar(my_team, my_team_count, enemy_count)

    if clases.Cursor.show_cursor:  # displaying cursor
        cursor.draw()

    # for i in game.center_points:
    #    pygame.draw.circle(game.screen, (255, 255, 255), (i[0], i[1]), a)

    pygame.display.flip()  # update the screen. /    .update() also works


def stopmusic():
    pygame.mixer.quit()  # close the pygame mixer


window = pyautogui.getWindowsWithTitle("Gambit Game")[0]  # find the program window in the OS so later its position can be changed when maximizing the window

UI_REFRESH_RATE = game.timer.tick(game.dev_mode.DisplayFrequency)/1000
manager = pygame_gui.UIManager((game.width, game.height))

# varibles needed to control fps
start_time = time.time()  # Record the starting time
loop_count = 0

if active_uis["intro"]:
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.6)
    # THE INTRO VIDEO IS PLAYED WHILE SETTING OTHER "HEAVY" THINGS UP
    video_t = threading.Thread(target=play_intro_video)
    audio_t = threading.Thread(target=play_intro_audio)
    video_t.start()
    audio_t.start()

    # SETTING SOME THINGS
    setup()

    # ONCE IT FINISHES LOADING EVERYTHING IT WAITS FOR THE VIDEO TO END
    while active_uis["intro"] == True:
        time.sleep(0.05)
    pygame.mixer.music.set_volume(0.4)
else:
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.4)
    setup()
set_mouse_usage(False, True)
active_uis["lobby"] = True

for song in sound_player.UI_SONGS:  # plays and specefically selects the song that should be played in the lobby
    if "track10" in song:
        pygame.mixer.music.load(song)  # loads the track
        pygame.mixer.music.play()  # plays the track
        break

# this variables "ite" just count how many repetitions the loop has made and when some event should be analized
ite0 = 0
ite1 = 0
ite2 = 0

init_time = time.time()  # saves the time when the loop was entered
while True:  # Main loop

    if (ite0 >= 600 or (ite0 == 0 and 1 < time.time()-init_time < 20)):  # checks if its necessary to play another song every 600 iterations. it can be bypassed by being the fisrt iteration. when pause is enabled you cant play music
        if not music_pause_state:  # you also have to check if the music is not paused
            ite0 = 0
            if not pygame.mixer.music.get_busy():
                sound_player.play_song_on_thread()

    if follow_mouse:  # when you are moving a piece you want it to follow your mouse, so you update the piece position to be exactly the same as your mouse's
        if selected_piece != None:
            active_pieces[selected_piece].pos_x, active_pieces[selected_piece].pos_y = event.pos

    for event in pygame.event.get():  # manage events

        if event.type == pygame.MOUSEMOTION or just_clicked_smth:  # checks for btns(their rectangles) being hovered and in that case changes the cursor image
            if just_clicked_smth:
                event.pos = pygame.mouse.get_pos()

            if (ite1 >= 12 or just_clicked_smth):  # just_clicked_smth is used because you want to proccess the new cursor image as soon as possible after you clike a btn meaning the ui might have changed and there would be no longer a botton in that same spot
                just_clicked_smth = False
                ite1 = 0
                clases.Cursor.image = Media.sized["cursor_default"]
                for values in Media.rects.values():
                    rect = values["rect"]
                    use_in = values["use_rect_in"]

                    if type(use_in) == list:    # if the btn is used in multiple uis, it checks if the current ui is active then checks if the btn is being hovered and if it is, it changes the cursor image to a hand
                        for possible_use in use_in:
                            print(possible_use)
                            if possible_use == "all" or active_uis[possible_use] == True:
                                if rect.collidepoint(event.pos):  # check if every btn was hovered
                                    clases.Cursor.image = Media.sized["cursor_hand"]
                                    break
                    else:
                        if use_in == "all" or active_uis[use_in] == True:
                            if rect.collidepoint(event.pos):  # check if every btn was hovered
                                clases.Cursor.image = Media.sized["cursor_hand"]
                                break

            if (ite2 >= 8):
                ite2 = 0
                pygame.mixer.music.set_volume(config_menu.sliders[0].current_value)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # then event.pos is used and it only tells the position of the mouse when the event occured

                for piece in active_pieces:  # Checks if any piece was clicked

                    if piece.is_clicked(event.pos, (piece.pos_x, piece.pos_y)):  # Comprobar si el clic está dentro del circulo
                        print("pieza clickeada")

                        if piece.team == my_team:
                            selected_piece = active_pieces.index(piece)
                            if (current_turn == "blue" and active_pieces[selected_piece].team == "blue") or (current_turn == "red" and active_pieces[selected_piece].team == "red"):
                                follow_mouse = True
                            elif (current_turn == "blue" and active_pieces[selected_piece].team == "red") or (current_turn == "red" and active_pieces[selected_piece].team == "blue"):
                                print("No es tu turno")
                        elif current_turn == my_team and selected_piece != None:
                            if play_online:
                                sckt.send(f"attacked-{active_pieces[selected_piece].id}-{piece.id}")
                            active_pieces[selected_piece].attack(piece)

                        if piece.hp <= 0 and selected_piece != None:
                            if play_online:
                                sckt.send(f"dead-{piece.id}")
                            if piece == active_pieces[selected_piece]:
                                selected_piece = None
                            active_pieces.remove(piece)

                if active_uis["ingame"]:
                    if my_team == current_turn or not play_online:
                        if turn_btn.rect.collidepoint(event.pos) and get_at_with_sound(turn_btn.image_mask, (event.pos[0] - turn_btn.rect.x, event.pos[1] - turn_btn.rect.y)):  # Verify if the position of the mouse is inside the rectangle and if the click was on a visible pixel # noqa
                            change_turn()
                            if play_online:
                                sckt.send("turn")
                            print("changed turn")

                if check_ui_allowance(Media.rects["setting_btn"]) and collidepoint_with_sound(Media.rects["setting_btn"]["rect"], event.pos):  # check if btn was clicked
                    active_uis["settings"] = not active_uis["settings"]
                elif collidepoint_with_sound(Media.rects["x_btn"]["rect"], event.pos):  # check if btn was clicked
                    finish_program()
                elif collidepoint_with_sound(Media.rects["minimize_btn"]["rect"], event.pos):  # check if btn was clicked
                    window = pyautogui.getWindowsWithTitle("Gambit Game")[0]  # find the game window in the OS
                    window.minimize()  # minimize the window
                elif collidepoint_with_sound(Media.rects["shrink_btn"]["rect"], event.pos):  # check if btn was clicked
                    shrink_state = not shrink_state  # pulsator to conmutator logic
                    if shrink_state:
                        window.moveTo(game.width//6, game.height//7)  # move the window
                        game.set_up_window(1.4)
                        game.create_center_points()
                        Media.resize_metrics(game.height)
                        Media.resize(game.height)
                        clases.Piece.resize(active_pieces)
                        set_mouse_usage(True, False)
                    else:
                        game.set_up_window(1, pygame.NOFRAME)
                        window.moveTo(0, 0)
                        game.create_center_points()
                        Media.resize_metrics(game.height)
                        Media.resize(game.height)
                        clases.Piece.resize(active_pieces)
                        set_mouse_usage(False, True)

                # GOING THROUGH THE MENUS
                elif check_ui_allowance(Media.rects["crear_btn"]) and collidepoint_with_sound(Media.rects["crear_btn"]["rect"], event.pos):  # check if btn was clicked
                    print("crear")
                    active_uis["lobby"] = False
                    active_uis["match_creation"] = True
                elif check_ui_allowance(Media.rects["generar_btn"]) and collidepoint_with_sound(Media.rects["generar_btn"]["rect"], event.pos):  # check if btn was clicked
                    print("okk")
                    clases.ClockAnimation.show_clock_animation = True
                    if (play_online):
                        threading.Thread(target=set_up_online, args=("server",), daemon=True).start()
                    else:
                        online_set_up_done = True
                        clases.MatchCreation.show_ingresar_btn = True
                elif check_ui_allowance(Media.rects["ingresar_btn"]) and collidepoint_with_sound(Media.rects["ingresar_btn"]["rect"], event.pos):  # check if btn was clicked
                    if (play_online):
                        assign_teams()
                    assign_turn()
                    if online_set_up_done:
                        clases.MatchCreation.show_ingresar_btn = False
                        active_uis["match_creation"] = False
                        active_uis["piece_selection"] = True

                if active_uis["piece_selection"]:
                    for i in range(3):  # Checks if any piece was clicked
                        if clases.Piece.is_clicked(event.pos, (piece_selection_menu.reference_piece_info[i]["x"]+(Media.pieces_size*1.5)/2, piece_selection_menu.reference_piece_info[i]["y"]+(Media.pieces_size*1.5)/2), mult=1.5):
                            follow_mouse = True
                            match piece_selection_menu.reference_piece_info[i]["specie"]:
                                case "mage":
                                    piece = clases.Mage(0, 0, my_team, 20, 20, 20, 20, 2)
                                case "archer":
                                    piece = clases.Archer(0, 0, my_team, 20, 20, 20, 20, 2)
                                case "knight":
                                    piece = clases.Knight(0, 0, my_team, 20, 20, 20, 20, 2)

                            active_pieces.append(piece)
                            selected_piece = active_pieces.index(piece)

                            break

            elif event.button == 3:
                if Media.rects["music_btn"]["rect"].collidepoint(event.pos):  # check if btn was clicked
                    music_pause_state = not music_pause_state
                    if music_pause_state:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                if follow_mouse:  # if we were moving a piece

                    follow_mouse = False

                    sound_player.play_sfx(sound_player.SFX[5])

                    which_point = active_pieces[selected_piece].detect_closest_point(event.pos)  # event pos is the mouse position at the moment of the event
                    gx, gy = piece.b64index_to_grid(which_point)  # gets the grid conversion of the coincident point
                    if not piece.check_for_pieces_in_the_grid_coordinates(active_pieces, gx, gy):
                        active_pieces[selected_piece].grid_pos_to_pixels(gx, gy, change_mana=True)  # sets the grid pos to the adecuate one, as well as the pos_x which is the pixel position
                    else:
                        active_pieces[selected_piece].grid_pos_to_pixels(active_pieces[selected_piece].grid_pos_x, active_pieces[selected_piece].grid_pos_y, change_mana=True)
                    # print(active_pieces[selected_piece].mana)

                    if active_uis["ingame"] and play_online:
                        sckt.send(f"moved-{active_pieces[selected_piece].id}-{active_pieces[selected_piece].grid_pos_x}-{active_pieces[selected_piece].grid_pos_y}")  # "moved":  # [id]-[x]-[y]

                    elif active_uis["piece_selection"]:
                        my_pieces = [piece for piece in active_pieces if piece.team == my_team]  # This will filter out all odd numbers from the list
                        if (len(my_pieces) >= 3):
                            active_uis["piece_selection"] = False

                            if play_online:
                                msg = "Pieces have been chosen. Start."
                                sckt.send(msg, delimiter="")
                                while True:
                                    received = sckt.recieve()  # waits for the other player to catchup
                                    if (received == msg):
                                        break
                                for piece in my_pieces:  # sends the comand to create your chosen pieces in the enemy active_pieces list
                                    sckt.send(f"created-{piece.specie}-{piece.grid_pos_x}-{piece.grid_pos_y}-{piece.team}-{piece.hp}-{piece.mana}-{piece.agility}-{piece.defense}-{piece.damage}-{piece.id}")

                                threading.Thread(target=receive_messages, daemon=True).start()
                            my_pieces = {}
                            active_uis["ingame"] = True

        elif event.type == pygame.KEYDOWN:  # if a key was pressed
            if (pygame.key.name(event.key) == "t" and selected_background < game.BACKGROUNDS_AMOUNT-1):  # used to change into diff background images
                selected_background += 1
            elif (pygame.key.name(event.key) == "g" and selected_background > 0):
                selected_background -= 1
            elif (pygame.key.name(event.key)) == "f":
                dev_mouse.dev_mouse(1.4)  # prints the coordinates of the mouse, used for developing reasons.
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
            elif (pygame.key.name(event.key) == "n"):
                clases.Sound.play_song_on_thread()
            elif (pygame.key.name(event.key) == "h"):
                if selected_piece != None:
                    active_pieces[selected_piece].hp -= 1

            elif (pygame.key.name(event.key) == "escape"):
                finish_program()

        elif event.type == pygame.QUIT:
            finish_program()

    if active_uis["ingame"] or active_uis["piece_selection"]:
        draw()
    elif active_uis["lobby"]:
        lobby.draw()
    elif active_uis["match_creation"]:
        match_creation.draw()
        if online_set_up_done:
            clases.ClockAnimation.show_clock_animation = False

    ite0 += 1  # iterator used to control events
    ite1 += 1
    ite2 += 1

    # FPS CONTER
    loop_count += 1  # Increment the counter on each loop
    if time.time() - start_time >= 0.5:
        print(loop_count/0.5)
        loop_count = 0
        start_time = time.time()

    game.timer.tick(game.dev_mode.DisplayFrequency)  # set the fps to the maximun possible

    """
                        if play_online:
                        set_up_online()
                    if (play_online):
                        assign_teams()
                    assign_turn()
    
    """
