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
import numpy as np
import ctypes
import math
import random
import copy
import threading
import cv2
import re
import pyperclip
import pygame
import pygame_gui
from pygame.locals import *
import pyautogui  # from pyautogui import press  # do not delete this eventhough it is not used, for some reason it increases the render quality # noqa

import clases  # noqa
import dev_mouse  # noqa
from online_utilities import firewall, online_tools, portforwarding
from media import Media, Fonts


# SETING THINGS UP
#
#


pygame.init()  # initialize pygame
game = clases.Game()
game.set_up_window(1.35)


# GENERAL VARIABLES
#
#

# my_team = "blue"

active_uis = {
    "intro": True,
    "lobby": False,
    "join_match": False,
    "join_match_ready": False,
    "match_creation": False,
    "match_creation_ready": False,
    "piece_selection": False,
    "ingame": False,
    "configuration": False,
    "chat": False,
    "donations": False,
    "profile": False,
    "end": False,
}

players_info = {
    "me": {"nickname": game.replace_line_in_txt("user_info\\data.txt", "nickname", "", mode="read"),
           "slogan": game.replace_line_in_txt("user_info\\data.txt", "slogan", "", mode="read"),
           "profile_picture": game.replace_line_in_txt("user_info\\data.txt", "pfp", "", mode="read"),
           },
    "enemy": {"nickname": "Enemigo",
              "slogan": "",
              "profile_picture": "default",
              },
}


my_pieces = []
active_pieces = []

conection_state = False

selected_piece = None

match_configured = False  # variables related to the state of te communication at the start of the match
# pieces_have_been_chosen = False

current_turn = None

# global movement_indicator
# movement_indicator = None

global fps_checking_rate
fps_checking_rate = 1

global i_have_chosen_pieces
i_have_chosen_pieces = False

global start_end_game_transition
start_end_game_transition = False
global transition_timer
transition_timer = False

global sckt_set_up
sckt_set_up = False
global port_opened
port_opened = False
global ready_to_receive
ready_to_receive = False

global just_clicked
just_clicked = False
just_clicked_smth = False

global accepted_revenge
accepted_revenge = False

global typing
typing = False

follow_mouse = False
maximize_state = False

selected_background = 0

music_pause_state = False  # audio related variables
current_volume = 0


intro_path = {"video": "resources\\intro\\GambitGames.mp4",  # path of the video and the audio for the intro
              "audio": "resources\\intro\\intro_audio.mp3"}

# PROGRAM FUNCTIONS
#
#


def setup():

    global piece_selection_menu, timer, turn_history, end_menu, name_bar, donations_menu, warning_manager, chat_menu, profile_menu, slider_menu, turn_btn, mini_flag, lobby, sound_player, cursor, match_creation, join_match, fps, configuration_menu

    sound_player = clases.Sound()  # creating an instance of the sound class to play sfx sounds

    Media.load_media(game.height)
    Media.resize(game.height)

    clases.UI.init()
    slider_menu = clases.Slider_Menu()
    turn_btn = clases.Turn_Btn()
    mini_flag = clases.Mini_Flags()
    lobby = clases.Lobby()
    match_creation = clases.MatchCreation()
    join_match = clases.JoinMatch(manager)
    piece_selection_menu = clases.Piece_Selection_Menu()
    configuration_menu = clases.Configuration_Menu()
    profile_menu = clases.Profile_Menu(manager)
    chat_menu = clases.Chat(manager)
    warning_manager = clases.Warning()
    donations_menu = clases.Donation_Menu()
    name_bar = clases.Name_Bar()
    end_menu = clases.End_Game_Menu()
    timer = clases.Timer()
    turn_history = clases.Turn_History()

    fps = game.dev_mode.DisplayFrequency

    game.create_center_points()

    cursor = clases.Cursor()


def set_up_ports_and_firewall(check_again=False):

    global port, conection_state, port_opened
    port = 8050  # this port seems to work pretty well
    firewall.FirewallRules.check_firewall_installation_status('installation_status.txt', port)

    local_ip = online_tools.Online.get_local_ip()
    print(local_ip)

    portforwarding.Portforwarding.initialize()
    if not portforwarding.Portforwarding.check_ports(port):
        portforwarding.Portforwarding.open_port(local_ip, port, port, "TCP")

    if check_again:
        if portforwarding.Portforwarding.check_ports(port):
            port_opened = True


def set_up_online(mode):  # this function sets up the server and client objects as adecuate, opens the needed port, checks firewall instalation status and also connects both users though a socket connection

    global conection_state, sckt_set_up, port_opened

    if not port_opened:
        set_up_ports_and_firewall()

    if mode == "client":

        if not sckt_set_up:  # only if its the first time being executed it set ups the sckt
            global sckt
            sckt = online_tools.Client()

        clases.ClockAnimation.set_animation_status(False)

        entered_text = join_match.input_texto.get_text()

        sckt.set_up_client(entered_text.strip(), port)
        print(f"Texto ingresado: {entered_text}")

        clases.JoinMatch.show_ingresar_btn = True
        active_uis["join_match"] = False
        active_uis["join_match_ready"] = True

        sound_player.play_sfx(sound_player.SFX[3])

        conection_state = True

    elif mode == "server":

        if not sckt_set_up:
            sckt = online_tools.Server()
            sckt.set_up_server(port)

        online_tools.Online.public_ip = online_tools.Online.get_public_ip()

        if online_tools.Online.public_ip == "error":  # in case get_public_ip has returned an error
            clases.Warning.warn("Problema al obtener IP", "No se pudo obtener la IP pública de la API. Puedes buscar tu IP en Internet y eso también funcionará como clave. Deberás pasarsela a tu rival.", 40)
            online_tools.Online.public_ip = "error"

        clases.MatchCreation.render_ip_text()

        active_uis["match_creation"] = False
        active_uis["match_creation_ready"] = True

        sound_player.play_sfx(sound_player.SFX[3])

        sckt.server_wait_for_connection()
        conection_state = True

    sckt_set_up = True


def receive_messages():  # This function receives messages from the server while being executed in a thread so it doesnt block the main loop. The messages are in the following format: action-arguments(n). Note that the - (hyphen is a separation marker)

    global match_configured

    while True:  # infinite loop while the program is executed

        entry = sckt.recieve()  # reads the message(s) from the buffer and stores them
        print(entry, "recibido")

        for entry in entry.split(";"):  # iterates over each message that are separated by ";".

            if entry == "":
                continue  # gets rid of the last item of the list if it is an empty string

            args = entry.split("-")  # gets all the arguments in a list. the fisrt item of the list is the action btw
            print(args)

            for i, arg in enumerate(args):
                args[i] = arg.replace("=G?", "-")  # this lines replaces the =G? with - so it doesnt break the chat and the format. before sending the msg the enemy replace the possible - with =G?. its just encriptation

            match args[0]:  # decides what to do based on the action received

                case "attacked":  # id-id2 . thats the format this case expects to receive. id is the identifier of the attacker and id2 is the identifier of the attacked piece
                    for piece in active_pieces:
                        if piece.id == args[1]:
                            for attacked_piece in active_pieces:
                                if attacked_piece.id == args[2]:
                                    piece.attack(attacked_piece)  # those for loops just find the attacker and the attacked piece in the actieve_pieces list and then this line executes the attack
                                    break

                case "moved":  # id-x-y-change_mana. thats the format this case expects to receive. id is the identifier of the piece that moved and x and y are the new coordinates
                    piece_id = args[1]
                    for piece in active_pieces:
                        if piece. id == piece_id:
                            # those for loops just find the piece in the actieve_pieces list and then this line executes the move
                            piece.grid_pos_to_pixels(clases.Piece.pov_based_pos_translation(int(args[2])), clases.Piece.pov_based_pos_translation(int(args[3])), bypass_mana=False, change_mana=args[4])
                    sound_player.play_sfx(sound_player.SFX[1])

                case "turn_n_clk_update":
                    print("recibido el cambio de turno", args[1], args[2])
                    change_turn_n_timer(False, (float(args[1]), float(args[2])))

                case "latencyerror":
                    timer.set_timer(clases.Timer.my_remaining_time-int(args[1])*1000*2)

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
                        # active_pieces.append(clases.Mage(p_x, p_y, p_team, p_hp, p_mana, p_agility, p_defense, p_damage, specify_id=p_id))
                        active_pieces.insert(0, clases.Mage(p_x, p_y, p_team, p_hp, p_mana, p_agility, p_defense, p_damage, specify_id=p_id))
                        print(active_pieces)
                    elif p_specie == "archer":
                        # active_pieces.append(clases.Archer(p_x, p_y, p_team, p_hp, p_mana, p_agility, p_defense, p_damage, specify_id=p_id))
                        active_pieces.insert(0, clases.Archer(p_x, p_y, p_team, p_hp, p_mana, p_agility, p_defense, p_damage, specify_id=p_id))

                        print(active_pieces)
                    elif p_specie == "knight":
                        # active_pieces.append(clases.Knight(p_x, p_y, p_team, p_hp, p_mana, p_agility, p_defense, p_damage, specify_id=p_id))
                        active_pieces.insert(0, clases.Knight(p_x, p_y, p_team, p_hp, p_mana, p_agility, p_defense, p_damage, specify_id=p_id))

                        print(active_pieces)

                case "dead":  # if our enemy kills a piece, it sends us this message so we can remove it from the active_pieces list
                    for piece in active_pieces:
                        if piece.id == args[1]:
                            active_pieces.remove(piece)

                    if check_win()[0]:  # in case 0 pieces are left, we win
                        global start_end_game_transition
                        start_end_game_transition = True

                    global selected_piece
                    selected_piece = None

                case "chat":  # if the enemy as sent us a msg lets print it on the chat
                    clases.Chat.add(players_info["enemy"]["nickname"], args[1], time.strftime("%H:%M"))

                case "exit":
                    print("the enemy has abandoned the game")

                case "image":

                    sckt.send("ready_to_receive_image")
                    # print("sended ready_to_receive_image")

                    img = receive_image_bytes(sckt, args[1])  # in args 1 comes the size of the image

                    Media.pfp["enemy_original"] = img  # saving the enemy pfp without processing

                    Media.pfp["enemy"] = Media.opencv_to_pygame(img, (game.height/11.65, game.height/11.65))  # saving the sized enemy pfp

                case "ready_to_receive_image":
                    # print("changing value")
                    global ready_to_receive
                    ready_to_receive = True

                case "setup_client":  # this is only planned to be received by the client. the server sends it the info and then the clint replies with its own info
                    # gets the info the server sent
                    global enemy_team, my_team, current_turn
                    enemy_team = args[1]
                    my_team = args[2]
                    current_turn = args[3]

                    if not "Tú" == args[4]:  # if the user nickname is not the default ("Tú") then we rename it
                        players_info["enemy"]["nickname"] = args[4]
                    else:  # if the user hasnt changed his name and he is called "Tú" we rename him as Enemigo
                        players_info["enemy"]["nickname"] = "Enemigo"

                    players_info["enemy"]["slogan"] = args[5]

                case "set_me_up":  # this is received by the client
                    # sending its own info to the server
                    slogan = players_info["me"]["slogan"]
                    slogan.replace("-", "=G?")  # encrypt this so it doesnt corrupt the format of the msg sended

                    global accepted_revenge
                    while not accepted_revenge and active_uis["end"]:
                        time.sleep(0.05)
                    accepted_revenge = False

                    sckt.send("ready-"+players_info["me"]["nickname"]+"-"+slogan)

                    time.sleep(0.15)

                    # pfp_path = game.replace_line_in_txt("user_info\\data.txt", "pfp", "", mode="read")
                    # pfp_bytes = Media.process_image(pfp_path)

                    send_image(sckt, Media.pfp["me_processed"])

                    time.sleep(0.3)

                    sckt.send("me_client_has_sent_eveything")
                    # print("sendddddding me_client_has_send_eveything")

                case "ready":  # this is received by both, server and client

                    if sckt.mode == "server":  # the server receives the info from the client

                        if not "Tú" == args[1]:  # if the user nickname is not the default ("Tú") then we rename it
                            players_info["enemy"]["nickname"] = args[1]
                        else:  # if the user hasnt changed his name and he is called "Tú" we rename him as Enemy
                            players_info["enemy"]["nickname"] = "Enemigo"

                        players_info["enemy"]["slogan"] = args[2]

                    else:
                        match_configured = True

                case "me_client_has_sent_eveything":  # this is received by the server
                    match_configured = True

                case "pieces_have_been_chosen":  # case used to know when the enemy has chosen his pieces and get into the ingame

                    global i_have_chosen_pieces
                    while not i_have_chosen_pieces:
                        # print("nigggk")
                        time.sleep(0.05)

                    my_pieces = [piece for piece in active_pieces if piece.team == my_team]  # This will filter out all odd numbers from the list

                    for piece in my_pieces:  # sends the comand to create your chosen pieces in the enemy active_pieces list
                        sckt.send(f"created-{piece.specie}-{piece.grid_pos_x}-{piece.grid_pos_y}-{piece.team}-{piece.hp}-{piece.mana}-{piece.agility}-{piece.defense}-{piece.damage}-{piece.id}")

                    my_pieces = {}  # clear pieces list
                    active_uis["ingame"] = True  # start the game
                    active_uis["piece_selection"] = False
                    i_have_chosen_pieces = False

                    timer.set_timers(300, "all", measure=True)  # start the timers
                    timer.update_texts()

                case _:
                    print("unknown command:", args[0])


def match_set_up():

    # restarting all the variables for a new game
    global my_pieces, active_pieces, match_configured
    my_pieces = []
    active_pieces = []

    if sckt.mode == "server":

        global enemy_team, my_team, current_turn, nickname, slogan

        my_team = random.choice(["blue", "red"])  # randomly chooses the team of the player

        if my_team == "blue":  # a quick definition of the enemy team
            enemy_team = "red"
        else:
            enemy_team = "blue"

        current_turn = random.choice(["blue", "red"])  # randomly chooses the team of the player

        slogan = players_info["me"]["slogan"]
        slogan.replace("-", "=G?")  # encrypt this so it doesnt corrupt the format of the msg sended

        sckt.send("setup_client-"+my_team+"-"+enemy_team+"-"+current_turn+"-"+players_info["me"]["nickname"]+"-"+slogan)

        time.sleep(0.15)

        # pfp_path = game.replace_line_in_txt("user_info\\data.txt", "pfp", "", mode="read")
        # pfp_bytes = Media.process_image(pfp_path)
        send_image(sckt, Media.pfp["me_processed"])  # sending our profile picture to the client (opponent)"""

        # print("image sended")
        time.sleep(0.3)

        sckt.send("set_me_up")
        # print("set_me_uprrrrrrrrrrrrrrrrr")

    while True:
        time.sleep(0.05)
        if match_configured:
            break

    if sckt.mode == "server":
        sckt.send("ready")

    active_uis["join_match_ready"] = False
    active_uis["match_creation_ready"] = False
    active_uis["end"] = False
    i_have_chosen_pieces = False
    active_uis["piece_selection"] = True  # after the turns have been assigned then we want to go into the piece selection menu

    clases.MatchCreation.show_ingresar_btn = False
    clases.ClockAnimation.set_animation_status(False)

    name_bar.resize(players_info["me"]["nickname"], players_info["me"]["slogan"], players_info["enemy"]["nickname"], players_info["enemy"]["slogan"])


def send_image(scktt, image_bytes):

    image_size = len(image_bytes)

    scktt.send("image-"+str(image_size))

    time.sleep(0.15)

    # print("waiting")

    if scktt.mode == "server":
        global ready_to_receive
        while not ready_to_receive:
            time.sleep(0.05)  # wait for the client to be ready to receive the image
        ready_to_receive = False
    else:
        sckt.recieve()

    time.sleep(0.15)

    print(f"about to send {len(image_bytes) / 1024} fragments")

    for byte in range(0, len(image_bytes), 1024):
        print("sending fragment")
        end = byte + 1024

        if end > len(image_bytes):  # Si el índice final excede el tamaño de la imagen
            end = len(image_bytes)  # Ajustamos el final al tamaño de la imagen

        scktt.send_not_encoded(image_bytes[byte:end])

    scktt.send_not_encoded(b"")  # Enviar el delimitador al final


def receive_image_bytes(scktt, image_size):

    # image_size = int(scktt.recieve())   # Recibir el tamaño de la imagen

    received_image_bytes = b""  # Crear un contenedor para almacenar los bytes recibidos

    while len(received_image_bytes) < int(image_size):
        print("receiving fragment")

        fragment = scktt.recieve_not_encoded()  # Recibir un fragmento de imagen
        if fragment == "":  # Si es el delimitador vacío, terminamos. esto es en caso de q se haya perdido algun paquete y entonces no quede espetando infinitamente
            break
        received_image_bytes += fragment  # Concatenar el fragmento recibido

    return received_image_bytes


def play_intro_video():

    Media.play_intro_video(intro_path["video"], game)

    active_uis["intro"] = False


def play_intro_audio():
    clases.Sound.play(intro_path["audio"])
    while pygame.mixer.music.get_busy():
        time.sleep(0.3)
    pygame.mixer.music.stop()


def finish_program():  # this function closes the program
    global running
    running = False  # in case some thread ends up in the main "while" loop you make sure it stops anyways
    try:
        sound_player.stopmusic()
        pygame.quit()
    except:
        pass
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
    sys.exit()


def change_turn_n_timer(send=False, args=()):  # changes the current turn from blue to red or red to blue

    global current_turn, my_team

    if current_turn == my_team:  # this part of the code manages the timer information sending. this is executed everytime any player changes the turn.

        print("this is the end of my turn. i get its duration")
        info = timer.start_counting_my_turn()   # this returns the seconds my turn lasted and the current time in order
        print("set_timers is being executed", info[0])
        timer.set_timers(clases.Timer.my_remaining_time-info[0], "me")

    else:
        info2 = timer.update_enemy(args[0], args[1])
        if info2[0]:
            print("LATENCY ERROR- fixing it")
            sckt.send(f"latencyerror-{info2[1]}")

        timer.start_counting_my_turn()

    if current_turn == "blue":  # this lines of code change the current turn
        current_turn = "red"
    else:
        current_turn = "blue"

    if send:
        sckt.send(f"turn_n_clk_update-{clases.Timer.my_remaining_time:.3f}-{info[1]:.3f}")
        print("timer sending: " + f"turn_n_clk_update-{clases.Timer.my_remaining_time:.3f}-{info[1]:.3f}" + "               ", clases.Timer.my_remaining_time)
    print(f"Turno del equipo {current_turn}")  # Mensaje para depuración


def check_win():  # checks if some team has won and in that case it returns true and the winning team

    red = blue = 0

    for piece in active_pieces:
        if piece.team == "blue":
            blue += 1
        else:
            red += 1

    if red == 0:
        return True, "blue"
    elif blue == 0:
        return True, "red"

    return False, "none"


def collidepoint_with_sound(rect, point_pos):  # a modified version of collidepoint() so it plays the click sfx sound when its true. used for btns

    collided = rect.collidepoint(point_pos)

    if collided:
        sound_player.play_sfx(sound_player.SFX[0])
        global just_clicked_smth
        just_clicked_smth = True
        return True
    return False


def get_at_with_sound(rect, relative_pos):  # the same as collidepoint_with_sound() but for irregular images
    collided = rect.get_at(relative_pos)
    if collided:
        sound_player.play_sfx(sound_player.SFX[0])
        global just_clicked_smth
        just_clicked_smth = True
        return True
    return False


# this function is used to check if the rect of an element is allowed to be used in the current ui. excellent for button that you want to be active only in certain ui like the lobby and not in the ingame.
def check_ui_allowance(element_in_media_rect_list):

    use_in = element_in_media_rect_list["use_rect_in"]

    if type(use_in) == tuple:
        for possible_use in use_in:
            if active_uis[possible_use] == True:
                return True
    else:
        if use_in == "all" or active_uis[use_in] == True:
            return True
    return False


def collect_msg_and_send_it():
    msg_text = chat_menu.input.get_text().strip()  # get the text from the input

    if re.match(r"^[\w\sáéíóúÁÉÍÓÚñÑ.,;:!?()*+\"\'/\n-]*$", msg_text) and 0 < len(msg_text) < 100:  # the message must follow some rules

        clases.Chat.add(players_info["me"]["nickname"], msg_text, time.strftime("%H:%M"))  # add the message to the chat

        clases.Chat.input.set_text("")  # clear the input

        msg_text = msg_text.replace("-", "=G?")  # replace the - symbol with =G? to avoid problems with the protocol. just encrypting it
        sckt.send(f"chat-{msg_text}")  # send the message to the enemy
    elif 0 < len(msg_text):
        clases.Warning.warn("Mensaje inválido", "El mensaje debe tener hasta 100 caracteres y no poseer símbolos extraños.", 5)


def set_mouse_usage(visible=False, grab=True):
    if visible:
        clases.Cursor.show_cursor = False
    else:
        clases.Cursor.show_cursor = True
    pygame.mouse.set_visible(visible)  # both needed for set mouse in virtual mode
    pygame.event.set_grab(grab)


def draw_ingame():

    game.screen.blit(Media.backgrounds[selected_background], (0, 0))  # displaying background

    if not active_uis["piece_selection"]:
        game.screen.blit(Media.sized["chat_btn"], (Media.metrics["chat_btn"]["x"], Media.metrics["chat_btn"]["y"]))

    mini_flag.draw(current_turn)
    turn_btn.draw()
    turn_history.draw()

    if follow_mouse and not active_uis["piece_selection"]:
        global movement_indicator
        movement_indicator.draw(pygame.mouse.get_pos())  # this updates the movement indicator position

    my_team_count = 0
    enemy_count = 0
    for piece in active_pieces:    # displaying all pieces and their health and mana bars

        piece.draw(game.screen, piece.image)
        piece.draw_bars(my_team, my_team_count, enemy_count)

        if piece.team == my_team:
            my_team_count += 1
        else:
            enemy_count += 1

    name_bar.draw(Media.pfp["me"], Media.pfp["enemy"])

    if timer.update_n_draw(current_turn, my_team):
        loser = timer.who_run_out_of_time(my_team, enemy_team)
        if loser == my_team:
            text = f"Has ganado! las piezas {my_team} han dominado el tablero!"
        else:
            text = f"{players_info['enemy']['nickname']} es el ganador! Suerte la próxima..."

        start_end_game_transition = True

    # for i in game.center_points:
    #    pygame.draw.circle(game.screen, (255, 255, 255), (i[0], i[1]), a)


def draw():  # MANAGING THE DRAWING OF THE WHOLE UIs and the menus.

    if not active_uis["ingame"]:
        game.screen.blit(Media.sized["lobby_background"], (0, 0))

    if active_uis["ingame"]:
        draw_ingame()

    elif active_uis["end"]:
        end_menu.draw()

    elif active_uis["lobby"]:
        lobby.draw()

    elif active_uis["profile"]:
        profile_menu.draw(Media.pfp["me_profile_menu"])

    elif active_uis["match_creation"] or active_uis["match_creation_ready"]:

        if active_uis["match_creation_ready"]:
            clases.MatchCreation.show_ingresar_btn = True
            clases.MatchCreation.show_ip_copy_button = True
            clases.ClockAnimation.set_animation_status(False)

        match_creation.draw()

    elif active_uis["join_match"] or active_uis["join_match_ready"]:
        join_match.draw()

    elif active_uis["donations"]:
        donations_menu.draw()

    if active_uis["piece_selection"]:  # what has to be shown when the piece selection menu is active (reference pieces to chose from and the menu itself which is the background)
        draw_ingame()
        piece_selection_menu.draw(my_team)

    if active_uis["chat"]:
        chat_menu.draw()

    if active_uis["configuration"]:
        configuration_menu.draw(active_uis["ingame"])
        slider_menu.run(show_music=True)

    game.screen.blit(Media.sized["x_btn"], (Media.metrics["x_btn"]["x"], Media.metrics["x_btn"]["y"]))  # displaying btns (allways displayed)
    game.screen.blit(Media.sized["maximize_btn"], (Media.metrics["maximize_btn"]["x"], Media.metrics["maximize_btn"]["y"]))
    game.screen.blit(Media.sized["minimize_btn"], (Media.metrics["minimize_btn"]["x"], Media.metrics["minimize_btn"]["y"]))

    clases.Warning.draw()

    if check_ui_allowance(Media.rects["configuration_btn"]):
        game.screen.blit(Media.sized["configuration_btn"], (Media.metrics["configuration_btn"]["x"], Media.metrics["configuration_btn"]["y"]))

    if check_ui_allowance(Media.rects["setting_btn"]):
        game.screen.blit(Media.sized["setting_btn"], (Media.metrics["setting_btn"]["x"], Media.metrics["setting_btn"]["y"]))

    if check_ui_allowance(Media.rects["volver_btn"]):
        game.screen.blit(Media.sized["volver_btn"], (Media.metrics["volver_btn"]["x"], Media.metrics["volver_btn"]["y"]))

    manager.draw_ui(game.screen)

    if clases.Cursor.show_cursor:  # displaying cursor
        cursor.draw()

    pygame.display.flip()  # update the screen. /    .update() also works


# DEFINING ANOTHER SET UP VARIABLES
#
#

window = pyautogui.getWindowsWithTitle("Gambit Game")[0]  # find the program window in the OS so later its position can be changed when maximizing the window

manager = pygame_gui.UIManager((game.width, game.height))
manager.ui_theme.cursor_blink_time = 0.5

try:  # we try opening the ports as soon as possible so the user doesnt waste time.
    threading.Thread(target=set_up_ports_and_firewall, args=(True,), daemon=True).start()
except:
    pass

fps_start_time = time.time()  # varibles needed to record fps  # Record the starting time
loop_count = 0

pygame.mixer.init()

if active_uis["intro"]:

    pygame.mixer.music.set_volume(0.6)
    # THE INTRO VIDEO IS PLAYED WHILE SETTING OTHER "HEAVY" THINGS UP
    threading.Thread(target=play_intro_video).start()
    threading.Thread(target=play_intro_audio).start()

    # SETTING SOME THINGS
    setup()

    # loading the pfp images
    Media.set_up_pfp_image(game)

    # ONCE IT FINISHES LOADING EVERYTHING IT WAITS FOR THE VIDEO TO END
    while active_uis["intro"] == True:
        time.sleep(0.05)
    pygame.mixer.music.set_volume(0.3)

else:
    pygame.mixer.music.set_volume(0.3)
    setup()

    Media.set_up_pfp_image(game)  # loading the pfp images


set_mouse_usage(True, False)
# set_mouse_usage(False, True)
active_uis["lobby"] = True

UI_REFRESH_RATE = pygame.time.Clock().tick(fps)/1000  # UI_REFRESH_RATE = game.timer.tick(fps)/1000


for song in sound_player.UI_SONGS:  # plays and specefically selects the song that should be played in the lobby
    if "track10" in song:
        sound_player.play(song)
        break

# this variables "ite" just count how many repetitions the loop has made and when some event should be analized
ite0 = 0
ite1 = 0
ite2 = 0


# MAIN LOOP
#
#

init_time = time.time()  # saves the time when the loop was entered
while True:

    if start_end_game_transition:  # this is used when the matches ends and there is a transition between the finished ingame and the menu

        if transition_timer == False:

            for song in sound_player.UI_SONGS:  # plays and specefically selects the song that should be played in the lobby
                if "12" in song:
                    sound_player.play(song)
                    break
            # sound_player.play(sound_player.UI_SONGS[11])

            animation_start_time = time.time()
            transition_timer = True

        if time.time() - animation_start_time > 2:
            active_uis["ingame"] = False
            active_uis["end"] = True
            transition_timer = False
            start_end_game_transition = False

            if check_win()[1] == my_team:
                if my_team == "red":
                    x = "rojas"
                else:
                    x = "azules"
                text = f"Has ganado! las piezas {x} han dominado el tablero!"
            else:
                text = f"{players_info['enemy']['nickname'].capitalize()} es el ganador! Suerte la próxima..."
            end_menu.resize(text)

    if (ite0 >= 600 or (ite0 == 0 and 1 < time.time()-init_time < 20)):  # checks if its necessary to play another song every 600 iterations. it can be bypassed by being the fisrt iteration. when pause is enabled you cant play music
        if not music_pause_state:  # you also have to check if the music is not paused
            ite0 = 0
            if not pygame.mixer.music.get_busy():
                sound_player.play_song_on_thread()

    if follow_mouse:  # when you are moving a piece you want it to follow your mouse, so you update the piece position to be exactly the same as your mouse's
        if selected_piece != None:
            active_pieces[selected_piece].pos_x, active_pieces[selected_piece].pos_y = event.pos

    for event in pygame.event.get():  # manage events

        manager.process_events(event)  # pass the event to the manager

        if event.type == pygame.MOUSEMOTION or just_clicked_smth:  # checks for btns(their rectangles) being hovered and in that case changes the cursor image
            if just_clicked_smth:
                event.pos = pygame.mouse.get_pos()

            if (ite1 >= 8 or just_clicked_smth):  # just_clicked_smth is used because you want to proccess the new cursor image as soon as possible after you clike a btn meaning the ui might have changed and there would be no longer a botton in that same spot
                just_clicked_smth = False
                ite1 = 0

                clases.Cursor.image = Media.sized["cursor_default"]

                for values in Media.fused_rect_list:
                    rect = values[1]["rect"]
                    use_in = values[1]["use_rect_in"]

                    if f"{values[0]}" in Media.do_not_use_for_hover:  # this checks if the btn is not supposed to change the cursor image when hovered
                        continue

                    if type(use_in) == tuple:    # if the btn is used in multiple uis, it checks if the current ui is active then checks if the btn is being hovered and if it is, it changes the cursor image to a hand
                        for possible_use in use_in:

                            if possible_use == "all" or active_uis[possible_use] == True:
                                if rect.collidepoint(event.pos):  # check if every btn was hovered
                                    clases.Cursor.image = Media.sized["cursor_hand"]
                                    break
                    else:
                        if use_in == "all" or active_uis[use_in] == True:
                            if rect.collidepoint(event.pos):  # check if every btn was hovered
                                clases.Cursor.image = Media.sized["cursor_hand"]
                                break

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:  # then event.pos is used and it only tells the position of the mouse when the event occured

                just_clicked = True

                if warning_manager.show_warning:  # this 3 lines of code let the user hide the shown warning if 20% of the total time of the warining have passed since it was shown by doing a click somewhere else on the screen
                    if not Media.rects["warning_ui"]["rect"].collidepoint(event.pos) and time.time()-warning_manager.init_time > clases.Warning.duration*0.2:
                        clases.Warning.show_warning = False

                for piece in active_pieces:  # Checks if any piece was clicked

                    if piece.is_clicked(event.pos, (piece.pos_x, piece.pos_y)):  # checks if the piece has been clicked by checking if the mouse position is inside the piece's circle. i_have_chosen_pieces is used to prevent the player from selecting more pieces than allowed
                        print("pieza clickeada")

                        if piece.team == my_team:
                            selected_piece = active_pieces.index(piece)

                            if (current_turn == active_pieces[selected_piece].team) or i_have_chosen_pieces:
                                follow_mouse = True

                                global movement_indicator
                                movement_indicator = clases.Movement_Indicator((piece.pos_x, piece.pos_y))  # this creates the object of the magic string that connects the previos posicition and the new position of the piece

                            else:
                                print("No es tu turno")

                        elif current_turn == my_team and selected_piece != None:

                            sckt.send(f"attacked-{active_pieces[selected_piece].id}-{piece.id}")
                            active_pieces[selected_piece].attack(piece)

                        if piece.hp <= 0 and selected_piece != None:

                            sckt.send(f"dead-{piece.id}")

                            if piece == active_pieces[selected_piece]:
                                selected_piece = None
                            active_pieces.remove(piece)

                            if check_win()[0]:
                                start_end_game_transition = True

                if active_uis["ingame"]:

                    if my_team == current_turn:  # if its players turn and the player clicked in the turn button then its changed and notifies the other player
                        if turn_btn.rect.collidepoint(event.pos) and get_at_with_sound(turn_btn.image_mask, (event.pos[0] - turn_btn.rect.x, event.pos[1] - turn_btn.rect.y)):  # Verify if the position of the mouse is inside the rectangle and if the click was on a visible pixel # noqa
                            change_turn_n_timer(send=True)

                    if turn_history.rect_next.collidepoint(event.pos) and get_at_with_sound(turn_history.image_mask_next, (event.pos[0] - turn_history.rect_next.x, event.pos[1] - turn_history.rect_next.y)):  # Verify if the position of the mouse is inside the rectangle and if the click was on a visible pixel # noqa
                        print("CLICKED NEXT")

                    elif turn_history.rect_prev.collidepoint(event.pos) and get_at_with_sound(turn_history.image_mask_prev, (event.pos[0] - turn_history.rect_prev.x, event.pos[1] - turn_history.rect_prev.y)):  # Verify if the position of the mouse is inside the rectangle and if the click was on a visible pixel # noqa
                        print("CLICKED PREV")

                if check_ui_allowance(Media.rects["setting_btn"]) and collidepoint_with_sound(Media.rects["setting_btn"]["rect"], event.pos):  # check if btn was clicked

                    active_uis["configuration"] = not active_uis["configuration"]

                    if active_uis["join_match"] or active_uis["join_match_ready"]:
                        join_match.show_input()

                    if active_uis["configuration"]:
                        join_match.hide_input()

                elif collidepoint_with_sound(Media.rects["x_btn"]["rect"], event.pos):  # check if btn was clicked
                    finish_program()

                elif collidepoint_with_sound(Media.rects["minimize_btn"]["rect"], event.pos):  # check if btn was clicked
                    window = pyautogui.getWindowsWithTitle("Gambit Game")[0]  # find the game window in the OS
                    window.minimize()  # minimize the window

                elif check_ui_allowance(Media.rects["chat_btn"]) and collidepoint_with_sound(Media.rects["chat_btn"]["rect"], event.pos):  # check if btn was clicked
                    active_uis["chat"] = not active_uis["chat"]
                    if active_uis["chat"]:
                        clases.Chat.show_input()
                    else:
                        clases.Chat.hide_input()

                elif check_ui_allowance(Media.rects["seleccionar_foto_btn"]) and collidepoint_with_sound(Media.rects["seleccionar_foto_btn"]["rect"], event.pos):  # check if btn was clicked
                    selected_file_path = game.open_file_dialog()

                    if selected_file_path.endswith('.png'):  # check if the file is a png
                        game.replace_line_in_txt("user_info\\data.txt", "pfp", f"pfp: {selected_file_path}", mode="write")  # update the value of the profile picture in the data.txt file
                        sound_player.play_sfx(sound_player.SFX[3])
                        Media.set_up_pfp_image(game)

                    else:
                        clases.Warning.warn("Imágen inválida", "La imágen debe ser formato PNG y es recomendable que no supere una resolución de 512x512 [1:1].", 8)

                elif check_ui_allowance(Media.rects["guardar_apodo_btn"]) and collidepoint_with_sound(Media.rects["guardar_apodo_btn"]["rect"], event.pos):  # check if btn was clicked

                    entry = profile_menu.nickname_input.get_text().strip()  # get the text from the input

                    if re.search(r"^[A-Za-z0-9._\-]{5,12}$", entry):  # the nickname must follow some rules

                        game.replace_line_in_txt("user_info\\data.txt", "nickname", f"nickname: {entry}", mode="write")  # update the value of the nickname
                        sound_player.play_sfx(sound_player.SFX[3])
                        clases.Profile_Menu.nickname_input.set_text(entry)  # Borrar el texto cuando se haga focus
                        # clases.Profile_Menu.nickname_input_focused = False

                    else:
                        clases.Warning.warn("Apodo inválido", "El apodo debe tener entre 5 y 12 caracteres y solo puede poseer los siguientes símbolos: (._-).", 8)  # if the nickname is invalid, show a warning

                elif check_ui_allowance(Media.rects["guardar_lema_btn"]) and collidepoint_with_sound(Media.rects["guardar_lema_btn"]["rect"], event.pos):  # check if btn was clicked

                    entry = profile_menu.slogan_input.get_text().strip()  # get the text from the input

                    if re.search(r"^[A-Za-z0-9._\-,;:]{3,30}$", entry):  # the slogan must follow some rules

                        game.replace_line_in_txt("user_info\\data.txt", "slogan", f"slogan: {entry}", mode="write")  # update the value of the slogan
                        sound_player.play_sfx(sound_player.SFX[3])
                        clases.Profile_Menu.slogan_input.set_text(entry)  # Borrar el texto cuando se haga focus
                        # clases.Profile_Menu.slogan_input_focused = False

                    else:
                        clases.Warning.warn("Lema inválido", "El lema debe tener entre 3 y 30 caracteres y no poseer símbolos extraños.", 8)

                elif check_ui_allowance(Media.rects["revancha_btn"]) and collidepoint_with_sound(Media.rects["revancha_btn"]["rect"], event.pos):
                    # here you have to make it wait for the opponent to accept the rematch

                    clases.ClockAnimation.set_animation_status(True, "end")

                    match_configured = False

                    accepted_revenge = True

                    threading.Thread(target=match_set_up, daemon=True).start()

                elif check_ui_allowance(Media.useful_rects["send_btn_chat"]) and collidepoint_with_sound(Media.useful_rects["send_btn_chat"]["rect"], event.pos):  # if the send btn was clicked

                    collect_msg_and_send_it()

                elif collidepoint_with_sound(Media.rects["maximize_btn"]["rect"], event.pos):  # if the maximize btn was clicked resize eveything to the due size

                    maximize_state = not maximize_state  # pulsator to conmutator logic

                    if maximize_state:

                        window.moveTo(game.width//6, game.height//7)  # move the window
                        game.set_up_window(1.4)

                        manager = pygame_gui.UIManager((game.width, game.height))  # as we cant change the size of the manager, we have to create a new one

                        set_mouse_usage(True, False)

                    else:
                        game.set_up_window(1, pygame.NOFRAME)
                        window.moveTo(0, 0)

                        manager = pygame_gui.UIManager((game.width, game.height))

                        set_mouse_usage(False, True)

                    game.create_center_points()
                    Media.resize_metrics(game.height)
                    Media.resize(game.height)
                    Fonts.resize_fonts()
                    clases.Piece.resize(active_pieces)

                    join_match.resize(manager)
                    if active_uis["join_match"]:
                        join_match.show_input()

                    chat_menu.resize(manager)
                    if not active_uis["chat"]:
                        chat_menu.hide_input()

                    profile_menu.resize(manager)
                    if active_uis["profile"]:
                        profile_menu.show_input()

                    slider_menu = clases.Slider_Menu()

                    name_bar.resize(players_info["me"]["nickname"], players_info["me"]["slogan"], players_info["enemy"]["nickname"], players_info["enemy"]["slogan"])
                    turn_btn.resize()
                    turn_history.resize()
                    mini_flag.resize()

                    Media.set_up_pfp_image(game)  # resizing the pfps
                    Media.pfp["enemy"] = Media.opencv_to_pygame(Media.pfp["enemy_original"], (game.height/11.65, game.height/11.65))

                    timer.update_texts()

                    manager.ui_theme.cursor_blink_time = 0.5

                # GOING THROUGH THE MENUS
                elif check_ui_allowance(Media.rects["configuration_btn"]) and collidepoint_with_sound(Media.rects["configuration_btn"]["rect"], event.pos):
                    for uis in active_uis:
                        active_uis[uis] = False
                    active_uis["configuration"] = True

                elif check_ui_allowance(Media.rects["apoyanos_btn"]) and collidepoint_with_sound(Media.rects["apoyanos_btn"]["rect"], event.pos):
                    active_uis["configuration"] = False
                    active_uis["donations"] = True

                elif check_ui_allowance(Media.rects["perfil_btn"]) and collidepoint_with_sound(Media.rects["perfil_btn"]["rect"], event.pos):
                    active_uis["lobby"] = False
                    active_uis["profile"] = True
                    clases.Profile_Menu.nickname_input.show()
                    clases.Profile_Menu.slogan_input.show()

                elif check_ui_allowance(Media.rects["crear_btn"]) and collidepoint_with_sound(Media.rects["crear_btn"]["rect"], event.pos):  # check if btn was clicked
                    active_uis["lobby"] = False
                    active_uis["match_creation"] = True

                elif check_ui_allowance(Media.rects["generar_btn"]) and collidepoint_with_sound(Media.rects["generar_btn"]["rect"], event.pos):  # check if btn was clicked

                    clases.ClockAnimation.set_animation_status(True, "match_creation")

                    for song in sound_player.UI_SONGS:  # plays and specefically selects the song that should be played in the match creation menu
                        if "(searching match)" in song:
                            sound_player.play(song)
                            break

                    threading.Thread(target=set_up_online, args=("server",), daemon=True).start()

                elif check_ui_allowance(Media.rects["copy_btn"]) and collidepoint_with_sound(Media.rects["copy_btn"]["rect"], event.pos):
                    pyperclip.copy(online_tools.Online.public_ip)
                    clases.Warning.warn("Clave de partida copiada", "La clave de partida ha sido exitosamente copiada al portapapeles.", 3, sound=False)

                elif check_ui_allowance(Media.useful_rects["wallet_btc"]) and collidepoint_with_sound(Media.useful_rects["wallet_btc"]["rect"], event.pos):
                    pyperclip.copy("bc1q3s6pxmt6dalfee05nr3wx3wtha2jxd680cfqzu")
                    clases.Warning.warn("Wallet copiada", "La dirección de la billetera Bitcoin ha sido copiada al portapapeles.", 3, sound=False)

                elif check_ui_allowance(Media.useful_rects["wallet_eth"]) and collidepoint_with_sound(Media.useful_rects["wallet_eth"]["rect"], event.pos):
                    pyperclip.copy("0x75e029dEE704ec1dA8a294c331B4009b49289d42")
                    clases.Warning.warn("Wallet copiada", "La dirección de la billetera Ethereum ha sido copiada al portapapeles (red: ERC20).", 3,  sound=False)

                elif check_ui_allowance(Media.rects["unirse_btn"]) and collidepoint_with_sound(Media.rects["unirse_btn"]["rect"], event.pos):

                    active_uis["lobby"] = False
                    active_uis["join_match"] = True
                    join_match.show_input()

                elif conection_state and check_ui_allowance(Media.rects["ingresar_btn"]) and collidepoint_with_sound(Media.rects["ingresar_btn"]["rect"], event.pos):  # check if btn was clicked

                    if active_uis["join_match_ready"]:
                        join_match.hide_input()  # if the user came from the joining match ui then hide the input as it souldnt be changed anymore

                    clases.ClockAnimation.set_animation_status(True, "join_match_ready")  # show the clock animation

                    threading.Thread(target=receive_messages, daemon=True).start()  # once the user created all his pieces, start listening for the enemy's moves and requests. the team and turn assignations was already done before entring the piece selection menu

                    threading.Thread(target=match_set_up, daemon=True).start()  # start the match set up in a thread so the teams and the turns get assigned and commited. this is started in a thread so it doesnt stop the main loop while the opponent is yet to press "ingresar"

                elif check_ui_allowance(Media.rects["volver_btn"]) and collidepoint_with_sound(Media.rects["volver_btn"]["rect"], event.pos):

                    if active_uis["match_creation"] or active_uis["match_creation_ready"]:
                        active_uis["lobby"] = True
                        active_uis["match_creation"] = False
                        active_uis["match_creation_ready"] = False

                    elif active_uis["join_match"] or active_uis["join_match_ready"]:
                        active_uis["lobby"] = True
                        active_uis["join_match"] = False
                        active_uis["join_match_ready"] = False
                        join_match.hide_input()

                    elif active_uis["configuration"]:
                        active_uis["lobby"] = True
                        active_uis["configuration"] = False

                    elif active_uis["profile"]:
                        active_uis["lobby"] = True
                        active_uis["profile"] = False
                        clases.Profile_Menu.nickname_input.hide()
                        clases.Profile_Menu.slogan_input.hide()

                    elif active_uis["donations"]:
                        active_uis["configuration"] = True
                        active_uis["donations"] = False

                    elif active_uis["end"]:
                        active_uis["end"] = False
                        active_uis["lobby"] = True

                    clases.ClockAnimation.set_animation_status(False)

                if active_uis["piece_selection"] and not i_have_chosen_pieces:
                    for i in range(3):  # Checks if any piece was clicked
                        if clases.Piece.is_clicked(event.pos, (Media.piece_selection_reference_info[i]["x"]+(Media.pieces_size*1.5)/2, Media.piece_selection_reference_info[i]["y"]+(Media.pieces_size*1.5)/2), mult=1.5):

                            follow_mouse = True
                            match Media.piece_selection_reference_info[i]["specie"]:
                                case "mage":
                                    piece = clases.Mage(0, 0, my_team, 20, 20, 20, 20, 2)
                                case "archer":
                                    piece = clases.Archer(0, 0, my_team, 20, 20, 20, 20, 2)
                                case "knight":
                                    piece = clases.Knight(0, 0, my_team, 20, 20, 20, 20, 2)

                            active_pieces.append(piece)
                            selected_piece = active_pieces.index(piece)

                            break

                if clases.Chat.input.get_relative_rect().collidepoint(event.pos):
                    print("clicked innn")
                    clases.Chat.focused = True
                else:
                    clases.Chat.focused = False

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

                    try:
                        print("movement indicator deleted")
                        del movement_indicator  # try deleting the magic string
                    except:
                        pass

                    change_mana = True
                    if active_uis["piece_selection"]:  # if the player is creating is alignment of pieces then dont consume their mana
                        change_mana = False

                    sound_player.play_sfx(sound_player.SFX[1])  # play the sound for when a piece is dropped on the board

                    which_point = active_pieces[selected_piece].detect_closest_point(event.pos)  # event pos is the mouse position at the moment of the event
                    gx, gy = piece.b64index_to_grid(which_point)  # gets the grid conversion of the coincident point
                    if not piece.check_for_pieces_in_the_grid_coordinates(active_pieces, gx, gy):  # if there is no piece in the new grid coordinates
                        active_pieces[selected_piece].grid_pos_to_pixels(gx, gy, change_mana=change_mana)  # sets the grid pos to the adecuate one, as well as the pos_x which is the pixel position

                        if active_uis["ingame"]:  # if we are in the ingame and playing online then send the other user the move info
                            sckt.send(f"moved-{active_pieces[selected_piece].id}-{active_pieces[selected_piece].grid_pos_x}-{active_pieces[selected_piece].grid_pos_y}-{change_mana}")
                            # this is the format of the message: moved-[id]-[x]-[y]

                    else:  # if there is a piece in that exact spot then move the piece to the old coodinates before being moved by the user
                        active_pieces[selected_piece].grid_pos_to_pixels(active_pieces[selected_piece].grid_pos_x, active_pieces[selected_piece].grid_pos_y, change_mana=change_mana)
                    # print(active_pieces[selected_piece].mana)

                    if active_uis["piece_selection"] and not i_have_chosen_pieces:

                        my_pieces = [piece for piece in active_pieces if piece.team == my_team]  # This will filter out all odd numbers from the list

                        if (len(my_pieces) == 3):

                            sckt.send("pieces_have_been_chosen", delimiter="")

                            # active_uis["ingame"] = True  # start the game
                            # active_uis["piece_selection"] = False

                            name_bar.resize(players_info["me"]["nickname"], players_info["me"]["slogan"], players_info["enemy"]["nickname"], players_info["enemy"]["slogan"])

                            i_have_chosen_pieces = True

        if event.type == pygame.KEYDOWN:  # if a key was pressed

            print(pygame.key.name(event.key))

            if (pygame.key.name(event.key) == "o" and selected_background < game.BACKGROUNDS_AMOUNT-1):  # used to change into diff background images
                selected_background += 1

            elif (pygame.key.name(event.key) == "p" and selected_background > 0):
                selected_background -= 1

            elif (pygame.key.name(event.key)) == "f":
                dev_mouse.Measure.dev_mouse()  # prints the coordinates of the mouse, used for developing reasons.

            elif (pygame.key.name(event.key)) == "g":
                dev_mouse.Measure.set_point_a()  # prints the coordinates of the mouse, used for developing reasons.

            elif (pygame.key.name(event.key)) == "h":
                dev_mouse.Measure.set_point_b()  # prints the coordinates of the mouse, used for developing reasons.

            elif (pygame.key.name(event.key)) == "j":
                dev_mouse.Measure.measure_distance()  # prints the coordinates of the mouse, used for developing reasons.

            # elif (pygame.key.name(event.key) == "w"):
            #    active_pieces[selected_piece].move(-1, 0, True)

            elif (pygame.key.name(event.key) == "return") and clases.Chat.focused:
                collect_msg_and_send_it()
                clases.Chat.input.focus()

            elif (pygame.key.name(event.key) == "m"):
                try:
                    sound_player.stopmusic()
                except:
                    pass
                music_pause_state = True
                pygame.mixer.init()

            elif (pygame.key.name(event.key) == "n"):
                clases.Sound.play_song_on_thread()

            elif (pygame.key.name(event.key) == "x"):
                if selected_piece != None:
                    active_pieces[selected_piece].hp -= 1

            elif (pygame.key.name(event.key) == "escape"):
                finish_program()

        elif event.type == pygame.QUIT:
            finish_program()

        # MANAGING PYGAME_GUI EVENTS

        if event.type == pygame_gui.UI_BUTTON_PRESSED:  # Si se presiona el botón "conectar"
            if event.ui_element == join_match.boton_conectar:

                if re.search(r"^(\d{1,3}\.){3}\d{1,3}$", join_match.input_texto.get_text()):

                    threading.Thread(target=set_up_online, args=("client",), daemon=True).start()
                    clases.ClockAnimation.set_animation_status(True, "join_match")

                else:
                    clases.Warning.warn("Clave Inválida", "La clave de partida introducida no es válida ya que no sigue el formato x.x.x.x.", 5)

        if (ite2 >= 10) or just_clicked:

            just_clicked = False
            ite2 = 0

            if slider_menu.sliders[0].current_value != current_volume:  # if the volume slider was moved (current_value not matching current_volume(last set volume)), it changes the volume of the music
                # print(slider_menu.sliders[0].current_value)
                pygame.mixer.music.set_volume(slider_menu.sliders[0].current_value)  # sets the new volume
                current_volume = slider_menu.sliders[0].current_value  # updates the current volume

    manager.update(UI_REFRESH_RATE)  # update the ui manager at a rate of [fps] time per second

    # DRAWING IN THE SCREEN AND REGULATING FPS

    draw()  # calling the main draw function

    ####

    ite0 += 1  # iterator used to control some events
    ite1 += 1
    ite2 += 1

    # FPS COUNTER

    loop_count += 1  # Increment the counter on each loop
    if time.time() - fps_start_time >= fps_checking_rate:
        current_fps = int(loop_count/fps_checking_rate)
        clases.Game.current_fps_render = Fonts.latency.render(f"{current_fps} fps", True, game.MID_GREY)
        global fps_cheking_rate
        if current_fps < fps/1.15:  # if current_fps are 15% lower than expected then lets reduce the sampling rate so it boosts performance.
            fps_checking_rate = 3
        else:
            fps_checking_rate = 0.5

        loop_count = 0
        fps_start_time = time.time()

    game.timer.tick(fps)  # set the fps to the maximun possible
