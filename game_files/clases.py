import os
import sys
import math
import numpy
import pygame
import pyautogui
import threading
from media import Media, Fonts
from win32con import ENUM_CURRENT_SETTINGS
from win32api import EnumDisplaySettings
import random
import string
from online_utilities import online_tools
import pygame_gui
from PyQt5.QtWidgets import QApplication, QFileDialog
import time


os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets the current directory to the file's directory

# SYSTEM CLASSES


class Game:

    DARK_GREY = (20, 21, 23)
    LIGHT_GREY = (89, 90, 91)
    MID_GREY = (33, 35, 37)
    CREME = (231, 205, 169)

    board_size = 8
    center_points = []

    screen = 0
    width = 0
    height = 0
    screen_height = 0
    timer = 0
    dev_mode = 0

    current_fps_render = pygame.Surface((width, height))  # empty surface

    BACKGROUNDS_AMOUNT = 7

    rects_list = []

    def __init__(self):  # init method for evety piece where it gets another ingame values assigned
        pass

    def create_center_points(self):
        Game.center_points.clear()  # clean previous points (wrongly sized probably)
        square_size = Game.height/13.52

        for row in range(0, Game.board_size):  # create 8 rows
            value = row*square_size*math.sqrt(2)/2  # how much each row should go back on x axis
            ix = Game.width/2 - value  # first point on the row x value (base value for entire row)
            iy = Game.height/14.05 + value  # first point on the row y value (base value for entire row)
            for elements in range(0, Game.board_size):  # create 8 elements in each row (columns)
                # create a tuple with the x and y coor of each point and then append it to the points list.
                new_point = (round(ix+elements*square_size*numpy.cos(numpy.deg2rad(45))), round(iy+elements*square_size*numpy.sin(numpy.deg2rad(45))))
                Game.center_points.append(new_point)

    def set_up_window(self, screenratio=1, with_frame=0):  # is the ratio screen/window

        _, Game.screen_height = pyautogui.size()  # gets the current resolution
        Game.height = round(Game.screen_height/screenratio)  # reduces the height
        Game.width = round(Game.height*(16/9))  # sets the aspect ratio to 16:9

        Game.screen = pygame.display.set_mode((Game.width, Game.height), with_frame)  # sets window resolution

        pygame.display.set_caption("Gambit Game 2024®")  # set a window title

        pygame.display.set_icon(pygame.image.load("resources\\icons\\icon.png").convert_alpha())  # sets window icon

        Game.timer = pygame.time.Clock()  # create a clock object to set fps
        Game.dev_mode = EnumDisplaySettings(None, ENUM_CURRENT_SETTINGS)  # get the OS's fps setting

    @staticmethod
    def open_file_dialog():  # create an pyqt app to select the profile picture file
        app = QApplication(sys.argv)
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, "Selecciona un archivo", "", "Todos los Archivos (*);;Archivos de Texto (*.txt)", options=options)
        return file_path

    @staticmethod
    def replace_line_in_txt(file_path, text_to_search, new_line, mode):  # specific function to save user data and preferences in a txt file

        if not os.path.exists(file_path):  # creates the file if it doesnt exist
            with open(file_path, 'w') as file:
                file.write("pfp: resources\\images\\indicator.png \nnickname: Tú\nslogan: Clan anónimo")  # writes the default values

        else:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            if mode == "read":
                for line in lines:
                    if text_to_search in line:
                        print("".join(line.split(": ")[1:]).strip())
                        return "".join(line.split(": ")[1:]).strip()  # this returns the exact information i want. not the whole line

                        # return line
            else:
                with open(file_path, 'w') as file:
                    print("writing")
                    for line in lines:
                        if text_to_search in line:
                            file.write(new_line + '\n')
                        else:
                            file.write(line)

    @staticmethod
    def smooth_movement(x, n=2):
        return (x**n) / (x**n + 1)


class Sound:

    SFX = [os.path.join("resources\\sounds\\sfx", archivo)  # This list contains all the paths of the sfx files
           for archivo in os.listdir("resources\\sounds\\sfx")]

    UI_SONGS = [os.path.join("resources\\sounds\\soundtracks", archivo)  # This list contains all the paths that contain "ui" on their name, aka, soundtrack files for the matches
                for archivo in os.listdir("resources\\sounds\\soundtracks")
                if os.path.isfile(os.path.join("resources\\sounds\\soundtracks", archivo)) and "ui" in archivo.lower()]

    PLAYLIST = [os.path.join("resources\\sounds\\soundtracks", archivo)  # This list contains all the paths that contain "ingame" on their name, aka, soundtrack files for the matches
                for archivo in os.listdir("resources\\sounds\\soundtracks")
                if os.path.isfile(os.path.join("resources\\sounds\\soundtracks", archivo)) and "ingame" in archivo.lower()]

    generated_tracks = []

    file = None

    def __init__(self):
        pass

    @staticmethod
    def play_sfx(sfx):
        sfx_channel = pygame.mixer.find_channel()  # Encuentra un canal disponible
        if sfx_channel is None:
            sfx_channel = pygame.mixer.Channel(pygame.mixer.get_num_channels())  # Si no hay canal disponible, crea uno nuevo
        sound_effect = pygame.mixer.Sound(sfx)  # Cargar efecto de sonido
        sfx_channel.play(sound_effect)  # Reproducir el efecto en el canal

    @staticmethod
    def play_song_on_thread():  # execute the playing of the sound in a thread so the main program doesnt get blocked
        threading.Thread(target=Sound.play_song).start()

    @staticmethod
    def play_song():  # a function that plays a random song from the playlist with no repetitions for iterations_without_repeating calls

        filtered_playlist = [song for song in Sound.PLAYLIST if song not in Sound.generated_tracks]  # selec a random song from playlist that has not been selected yet

        track = random.choice(filtered_playlist)

        Sound.generated_tracks.append(track)

        Sound.play(track)

        if len(Sound.generated_tracks) > (len(Sound.PLAYLIST)-5):
            Sound.generated_tracks.pop(0)

    @staticmethod
    def play(track):
        pygame.mixer.music.stop()  # Stops the currently playing music
        pygame.mixer.music.unload()
        pygame.mixer.music.load(track)  # loads the track
        pygame.mixer.music.play()  # plays the track

    @staticmethod
    def stopmusic():
        pygame.mixer.quit()  # close the pygame mixer


# PIECES CLASSES

class Piece:

    pieces_ids = []

    health_color = (155, 8, 15)
    health_background_color = (33, 3, 3)
    mana_color = (220, 159, 30)
    mana_background_color = (76, 55, 5)

    def __init__(self, x, y, team, hp, mana, agility, defense, damage, specify_id=None, pos_mode="grid"):  # init method for evety piece where it gets another ingame values assigned
        self.max_hp = hp
        self.max_mana = mana
        self.team = team
        self.grid_pos_x = x
        self.grid_pos_y = y
        self.pos_x = 0
        self.pos_y = 0

        self.specie = None

        if (specify_id == None):
            self.id = Piece.generate_id()
        else:
            self.id = specify_id

        if pos_mode == "grid":
            Piece.grid_pos_to_pixels(self, x, y, bypass_mana=True, change_mana=False)
        else:  # it should be "pixels"
            self.pos_x = x
            self.pos_y = y

        self.hp = hp
        self.mana = mana
        self.agility = agility
        self.defense = defense
        self.damage = damage

        self.image = 0
        self.original_image = 0

    @staticmethod
    def generate_id():  # Generates a unique id for each piece
        chars = string.ascii_lowercase + string.digits  # Includes lowercase letters and digits
        my_id = ''.join(random.choice(chars) for _ in range(4))
        for piece_id in Piece.pieces_ids:
            if piece_id == my_id:
                return Piece.generate_id()
        Piece.pieces_ids.append(my_id)
        return my_id

    def modify_hp(self, change):

        self.hp += change

    def attack(self, atacked_piece):
        atacked_piece.modify_hp(0 - self.damage)

    def draw_bars(self, my_team, my_team_count, enemy_count):

        if self.team == my_team:
            is_my_piece = True
            mult = 1
        else:
            is_my_piece = False
            mult = 10/12

        # MAXIMUN VALUES, LIKE THE TOTAL WIDTH AND THE HEIGHT

        if is_my_piece:
            bar_height = mult*Game.height/24  # this is the height of my pieces bar
            bar_width = mult*Game.height/5.122  # this is the maximum width of the bar, the 100%
        else:
            bar_height = mult*Game.height/16  # this is the height of the enemy pieces bar
            bar_width = mult*Game.height/3.64  # this is the maximum width of the bar, the 100%

        # THE WIDTH OF THE SECOND RECTANGLE WHICH INDICATES THE PERCENTAJE

        health_percentage = self.hp / self.max_hp  # calculates the length of the health bar in function of the percentage of health
        health_bar_length = int(bar_width * health_percentage)

        mana_percentage = self.mana / self.max_mana  # calculates the length of the mana bar in function of the percentage of mana
        mana_bar_length = int(bar_width * mana_percentage)

        bar_x = (Game.width/15.4)  # this is the base position on which the bars will be draw. like the separation form the margin

        if is_my_piece:
            bar_y = (Game.height/1.14) - my_team_count * Game.height/9.4
        else:
            bar_y = (Game.height/8) + enemy_count * Game.height/9.4 * mult

        if is_my_piece:
            Game.screen.blit(Media.specific_copies[self.team+"_"+self.specie+"_team_bar"], (Game.width/60, bar_y+Game.height/120))
        else:
            Game.screen.blit(Media.sized[self.team+"_"+self.specie], (Game.width/60, bar_y+Game.height/120))

        x_buff = Game.width/79 * mult
        y_buff = Game.height/54 * mult

        health_bg_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        health_bg_surface.set_alpha(180)  # Ajusta el nivel de transparencia (0 a 255)
        health_bg_surface.fill(self.health_background_color)
        health_surface = pygame.Surface((health_bar_length, bar_height), pygame.SRCALPHA)
        health_surface.set_alpha(180)  # Ajusta el nivel de transparencia (0 a 255)
        health_surface.fill(self.health_color)
        Game.screen.blit(health_bg_surface, (bar_x + x_buff, bar_y + y_buff))
        Game.screen.blit(health_surface, (bar_x + x_buff, bar_y + y_buff))

        # this two lines were the previuos version of the 5 lines above where the rect wasnt transparent

        """pygame.draw.rect(Game.screen, self.health_background_color, (bar_x+x_buff, bar_y+y_buff, bar_width, bar_height))
        pygame.draw.rect(Game.screen, self.health_color, (bar_x+x_buff, bar_y+y_buff, health_bar_length, bar_height))  # Dibuja la barra de vida restante (verde)
        """
        if is_my_piece:

            mana_bg_surface = pygame.Surface((bar_width, bar_height // 2), pygame.SRCALPHA)
            mana_bg_surface.set_alpha(192)  # Ajusta el nivel de transparencia (0 a 255)
            mana_bg_surface.fill(self.mana_background_color)
            mana_surface = pygame.Surface((mana_bar_length, bar_height // 2), pygame.SRCALPHA)
            mana_surface.set_alpha(185)  # Ajusta el nivel de transparencia (0 a 255)
            mana_surface.fill(self.mana_color)
            Game.screen.blit(mana_bg_surface, (bar_x + x_buff, bar_y + bar_height + y_buff))
            Game.screen.blit(mana_surface, (bar_x + x_buff, bar_y + bar_height + y_buff))
            # this two lines were the previuos version of the 5 lines above where the rect wasnt transparent
            """
            pygame.draw.rect(Game.screen, self.mana_background_color, (bar_x+x_buff, bar_y+bar_height+y_buff, bar_width, bar_height/2))
            pygame.draw.rect(Game.screen, self.mana_color, (bar_x+x_buff, bar_y+bar_height+y_buff, mana_bar_length, bar_height/2))  # Dibuja la barra de vida restante (verde)
            """

            Game.screen.blit(Media.sized["team_bar"], (bar_x, bar_y))
        else:
            Game.screen.blit(Media.sized["enemy_bar"], (bar_x, bar_y))

    @ staticmethod
    def b64index_to_grid(index):  # it return the conversion from a 1d array index to a 2d array index (used to convert points_list index to the board/grid index)
        return index % Game.board_size, index // Game.board_size

    @ staticmethod
    def grid_to_b64index(x, y):  # it returns the opposite conversion of b64index_to_grid. given 2d array coordinates it converts them to a 1d array coordinate
        return y*Game.board_size + x

    def grid_pos_to_pixels(self, grid_x, grid_y, change_mana=False, bypass_mana=False, update_variables=True):  # this function changes the position of the pieces images based on the grid coordinates passed

        if (grid_x < 0):  # this checks for the new position to not surpase grid limits
            grid_x = 0
        elif (grid_x > Game.board_size-1):
            grid_x = Game.board_size-1
        if (grid_y < 0):
            grid_y = 0
        elif (grid_y > Game.board_size-1):
            grid_y = Game.board_size-1

        point_x, point_y = Game.center_points[Piece.grid_to_b64index(grid_x, grid_y)]

        movement_amount = Piece.get_amount_of_grid_move(grid_x, grid_y,  self.grid_pos_x,  self.grid_pos_y)
        if (bypass_mana or self.mana >= movement_amount):  # only if the piece has enough mana can actually move
            if change_mana:  # this has to be above the next if conditional becuase there it updates the value of self.grid_pos_x
                if self.mana > 0:
                    self.mana -= movement_amount  # gets the mana variation which is the same as the squared moved

            # print(self.mana)

            if update_variables:  # maybe you dont want to set the new converted values to the variables, maybe you just want the output, thats why.
                self.grid_pos_x = grid_x  # updates de grid coordinates value
                self.grid_pos_y = grid_y
                self.pos_x = point_x  # updates de pixel position value
                self.pos_y = point_y

            return point_x, point_y, grid_x, grid_y  # it returns specifically two tuples with the pixels values and the grid values
        else:
            self.pos_x, self.pos_y = Game.center_points[Piece.grid_to_b64index(self.grid_pos_x, self.grid_pos_y)]
            return None, None, None, None

    @ staticmethod
    def check_for_pieces_in_the_grid_coordinates(active_pieces, x, y):
        for piece in active_pieces:
            if (piece.grid_pos_x == x and piece.grid_pos_y == y):
                return True
        return False

    @ staticmethod
    def detect_closest_point(mouse_pos):  # AKA transform pixels position to grid placement (opposite of grid_pos_to_pixels())
        lowest = 10000
        for point in Game.center_points:  # iterate every point
            # calculate the length of the vector formed between the point and the mouse position (the distance between where the user dropped the piece and the current point)
            distance = math.sqrt((mouse_pos[0]-point[0])**2 + (mouse_pos[1]-point[1])**2)

            if distance < lowest:  # if the distance is lower than all the others measured, save it as the lowest
                lowest = distance
                selected_point = point

        return Game.center_points.index(selected_point)  # return the position(index) in the points array of the closest point

    @ staticmethod
    def get_amount_of_grid_move(old_x, old_y, new_x, new_y):  # it is used to calculate mana variation

        movement_on_x = abs(new_x-old_x)
        movement_on_y = abs(new_y-old_y)

        mayor = max(movement_on_x, movement_on_y)
        menor = min(movement_on_x, movement_on_y)

        resto = mayor - menor
        mayor = mayor - resto

        return round(mayor+resto)  # returns how many squares/ positions the move imlpied. the amount of squared the piece moved. moving diagonally counts as just 1 square.

    def move(self, move_x, move_y, change_mana):

        old_x = self.grid_pos_x
        old_y = self.grid_pos_y

        _, _, limited_x, limited_y = self.grid_pos_to_pixels(self.grid_pos_x + move_x, self.grid_pos_y + move_y, False)

        if (limited_x != None):

            if change_mana:  # print(Piece.get_amount_of_grid_move(old_x, old_y, limited_x, limited_y))
                if self.mana > 0:
                    self.mana -= Piece.get_amount_of_grid_move(old_x, old_y, limited_x, limited_y)
                    # print(old_x, old_y, limited_x, limited_y, self.get_amount_of_grid_move(old_x, old_y, limited_x, limited_y), self.mana)

    def draw(self, screen, img, pos=0):

        if pos:
            screen.blit(img, (pos[0]-Media.pieces_size//2, pos[1]-Media.pieces_size//2))
        else:
            screen.blit(img, (self.pos_x-Media.pieces_size//2, self.pos_y-Media.pieces_size//2))
        # pygame.draw.circle(screen, color, pos, self.rad)

    @ staticmethod
    def pov_based_pos_translation(x):  # it translated the coodinates of the enemy's pieces so you always see yours as the closest ones to the bottom of the screen, independently of the color.
        return abs(x-Game.board_size+1)  # it just inverts the board in x and y

    @ staticmethod
    def is_clicked(mouse_pos, pos, mult=1):  # to check if a piece was clicked (works for general circles as well)
        distancia = ((pos[0] - mouse_pos[0]) ** 2 + (pos[1] - mouse_pos[1]) ** 2) ** 0.5  # Calcular la distancia entre el cli
        return distancia <= (Media.pieces_size*mult)//2  # Devuelve True si el clic está dentro del círculo

    @ staticmethod
    def resize(active_pieces):
        for piece in active_pieces:
            piece.grid_pos_to_pixels(piece.grid_pos_x, piece.grid_pos_y, change_mana=False, bypass_mana=True, update_variables=True)
            piece.image = Media.scale(piece.original_image, Media.pieces_size, Media.pieces_size)


class Mage(Piece):

    def __init__(self, x, y, team, hp, mana, agility, defense, damage, specify_id=None, pos_mode="grid"):

        super().__init__(x, y, team, hp, mana, agility, defense, damage, specify_id, pos_mode)

        self.specie = "mage"

        # Mage.loadimages()

        if (team == "blue"):
            self.original_image = Media.bare_imgs["blue_mage"]
            self.image = Media.sized["blue_mage"]

        else:
            self.original_image = Media.bare_imgs["red_mage"]
            self.image = Media.sized["red_mage"]


class Archer(Piece):

    def __init__(self, x, y, team, hp, mana, agility, defense, damage, specify_id=None, pos_mode="grid"):
        super().__init__(x, y, team, hp, mana, agility, defense, damage, specify_id, pos_mode)

        self.specie = "archer"

        # Archer.loadimages()

        if (team == "blue"):
            self.original_image = Media.bare_imgs["blue_archer"]
            self.image = Media.sized["blue_archer"]

        else:
            self.original_image = Media.bare_imgs["red_archer"]
            self.image = Media.sized["red_archer"]


class Knight(Piece):

    def __init__(self, x, y, team, hp, mana, agility, defense, damage, specify_id=None, pos_mode="grid"):
        super().__init__(x, y, team, hp, mana, agility, defense, damage, specify_id, pos_mode)

        self.specie = "knight"

        # Knight.loadimages()

        if (team == "blue"):
            self.original_image = Media.bare_imgs["blue_knight"]
            self.image = Media.sized["blue_knight"]

        else:
            self.original_image = Media.bare_imgs["red_knight"]
            self.image = Media.sized["red_knight"]

# ingame objects classes


# UI CLASSES


class Lobby:

    def __init__(self):
        pass

    def draw(self):

        Game.screen.blit(Media.sized["lobby_ui"], (Media.metrics["lobby_ui"]["x"], Media.metrics["lobby_ui"]["y"]))
        Game.screen.blit(Media.sized["crear_btn"], (Media.metrics["crear_btn"]["x"], Media.metrics["crear_btn"]["y"]))
        Game.screen.blit(Media.sized["unirse_btn"], (Media.metrics["unirse_btn"]["x"], Media.metrics["unirse_btn"]["y"]))
        Game.screen.blit(Media.sized["perfil_btn"], (Media.metrics["perfil_btn"]["x"], Media.metrics["perfil_btn"]["y"]))


class Donation_Menu:

    def __init__(self):
        pass

    def draw(self):

        Game.screen.blit(Media.sized["donations_ui"], (Media.metrics["donations_ui"]["x"], Media.metrics["donations_ui"]["y"]))


class MatchCreation:

    show_ingresar_btn = False

    show_ip_copy_button = False

    ip_text = None
    ip_text_rect = None

    def __init__(self):
        pass

    def draw(self):

        Game.screen.blit(Media.sized["lobby_ui"], (Media.metrics["lobby_ui"]["x"], Media.metrics["lobby_ui"]["y"]))
        Game.screen.blit(Media.sized["generar_btn"], (Media.metrics["generar_btn"]["x"], Media.metrics["generar_btn"]["y"]))

        if MatchCreation.show_ingresar_btn:
            Game.screen.blit(Media.sized["ingresar_btn"], (Media.metrics["ingresar_btn"]["x"], Media.metrics["ingresar_btn"]["y"]))
        if MatchCreation.show_ip_copy_button:
            Game.screen.blit(Media.sized["copy_btn"], (Media.metrics["copy_btn"]["x"], Media.metrics["copy_btn"]["y"]))
            Game.screen.blit(MatchCreation.ip_text, MatchCreation.ip_text_rect)

        ClockAnimation.draw()

    def render_ip_text():
        MatchCreation.ip_text = Fonts.ip_text.render(f"Clave: {online_tools.Online.public_ip}", True, Game.DARK_GREY)
        MatchCreation.ip_text_rect = MatchCreation.ip_text.get_rect(center=(Game.width/2,  Game.height/1.98))


class JoinMatch:

    show_ingresar_btn = False

    def __init__(self, manager):

        JoinMatch.resize(manager)

        JoinMatch.hide_input()

    def draw(self):

        Game.screen.blit(Media.sized["lobby_ui"], (Media.metrics["lobby_ui"]["x"], Media.metrics["lobby_ui"]["y"]))

        ClockAnimation.draw()

        if JoinMatch.show_ingresar_btn:
            Game.screen.blit(Media.sized["ingresar_btn"], (Media.metrics["ingresar_btn"]["x"], Media.metrics["ingresar_btn"]["y"]))

    @staticmethod
    def resize(manager):
        JoinMatch.input_rect = pygame.Rect()
        JoinMatch.input_texto = pygame_gui.elements.UITextEntryLine(relative_rect=JoinMatch.input_rect, manager=manager)

        JoinMatch.boton_rect = pygame.Rect()
        JoinMatch.boton_conectar = pygame_gui.elements.UIButton(relative_rect=JoinMatch.boton_rect, text='Conectar', manager=manager)

        JoinMatch.hide_input()

        JoinMatch.input_texto.set_dimensions((Media.join_match_metrics["text_input"]["w"], Media.join_match_metrics["text_input"]["h"]))  # Cambiar tamaño
        JoinMatch.input_texto.set_position((Media.join_match_metrics["text_input"]["x"], Media.join_match_metrics["text_input"]["y"]))   # Cambiar posición
        JoinMatch.boton_conectar.set_dimensions((Media.join_match_metrics["btn_conectar"]["w"], Media.join_match_metrics["btn_conectar"]["h"]))  # Cambiar tamaño
        JoinMatch.boton_conectar.set_position((Media.join_match_metrics["btn_conectar"]["x"], Media.join_match_metrics["btn_conectar"]["y"]))   # Cambiar posición

    @staticmethod
    def show_input():
        JoinMatch.input_texto.show()
        JoinMatch.boton_conectar.show()

    @staticmethod
    def hide_input():
        JoinMatch.input_texto.hide()
        JoinMatch.input_texto.set_text("Ingrese la clave")

        JoinMatch.boton_conectar.hide()


class Piece_Selection_Menu:

    already_executed = False

    def __init__(self):
        pass

    @ staticmethod
    def draw(my_team):
        Game.screen.blit(Media.sized["piece_selection_ui"], (Media.metrics["piece_selection_ui"]["x"], Media.metrics["piece_selection_ui"]["y"]))

        for i in range(3):  # drawing the images as the reference pieces
            Game.screen.blit(Media.specific_copies[my_team+"_"+Media.piece_selection_reference_info[i]["specie"]+"_piece_selection_image"],
                             (Media.piece_selection_reference_info[i]["x"], Media.piece_selection_reference_info[i]["y"]))


class Configuration_Menu:

    nickname_input_focused = False
    slogan_input_focused = False

    @staticmethod
    def draw(ingame):

        Game.screen.blit(Media.sized["configuration_ui"], (Media.metrics["configuration_ui"]["x"], Media.metrics["configuration_ui"]["y"]))

        if not ingame:
            Game.screen.blit(Media.sized["apoyanos_btn"], (Media.metrics["apoyanos_btn"]["x"], Media.metrics["apoyanos_btn"]["y"]))

        else:

            Game.screen.blit(Timer.latency_render, (Media.metrics["configuration_ui"]["x"]+Game.height/2, Media.metrics["configuration_ui"]["y"]+Game.height/3))  # THIS SHOWS THE LATENCY OF THE CONNECTION

        Game.screen.blit(Game.current_fps_render, (Media.metrics["configuration_ui"]["x"]+Game.height/1.3, Media.metrics["configuration_ui"]["y"]+Game.height/2))  # THIS SHOWS THE FPS


class Profile_Menu:

    def __init__(self, manager):

        Profile_Menu.resize(manager)

        Profile_Menu.hide_input()

    @staticmethod
    def resize(manager):

        Profile_Menu.nickname_input = pygame.Rect()
        Profile_Menu.nickname_input = pygame_gui.elements.UITextEntryLine(relative_rect=Profile_Menu.nickname_input, manager=manager)

        Profile_Menu.slogan_input = pygame.Rect()
        Profile_Menu.slogan_input = pygame_gui.elements.UITextEntryLine(relative_rect=Profile_Menu.slogan_input, manager=manager)

        Profile_Menu.hide_input()

        Profile_Menu.nickname_input.set_dimensions((Media.profile_menu_metrics["nickname_input"]["w"], Media.profile_menu_metrics["nickname_input"]["h"]))  # Cambiar tamaño
        Profile_Menu.nickname_input.set_position((Media.profile_menu_metrics["nickname_input"]["x"], Media.profile_menu_metrics["nickname_input"]["y"]))   # Cambiar posición
        Profile_Menu.slogan_input.set_dimensions((Media.profile_menu_metrics["slogan_input"]["w"], Media.profile_menu_metrics["slogan_input"]["h"]))  # Cambiar tamaño
        Profile_Menu.slogan_input.set_position((Media.profile_menu_metrics["slogan_input"]["x"], Media.profile_menu_metrics["slogan_input"]["y"]))   # Cambiar posición

    @staticmethod
    def show_input():
        Profile_Menu.nickname_input.show()
        Profile_Menu.slogan_input.show()

    @staticmethod
    def hide_input(def_text_nick="Ingrese un apodo", def_text_slog="Ingrese un lema"):
        Profile_Menu.nickname_input.hide()
        Profile_Menu.nickname_input.set_text(Game.replace_line_in_txt("user_info\\data.txt", "nickname", "", mode="read"))
        # Profile_Menu.nickname_input_focused = False

        Profile_Menu.slogan_input.hide()
        Profile_Menu.slogan_input.set_text(Game.replace_line_in_txt("user_info\\data.txt", "slogan", "", mode="read"))
        # Profile_Menu.slogan_input_focused = False

    @staticmethod
    def draw(my_pfp):
        Game.screen.blit(Media.sized["perfil_ui"], (Media.metrics["perfil_ui"]["x"], Media.metrics["perfil_ui"]["y"]))

        Game.screen.blit(my_pfp, (Media.metrics["seleccionar_foto_btn"]["x"]+Game.height/3, Media.metrics["seleccionar_foto_btn"]["y"]-Game.height/30))

        Game.screen.blit(Media.sized["seleccionar_foto_btn"], (Media.metrics["seleccionar_foto_btn"]["x"], Media.metrics["seleccionar_foto_btn"]["y"]))
        Game.screen.blit(Media.sized["guardar_apodo_btn"], (Media.metrics["guardar_apodo_btn"]["x"], Media.metrics["guardar_apodo_btn"]["y"]))
        Game.screen.blit(Media.sized["guardar_lema_btn"], (Media.metrics["guardar_lema_btn"]["x"], Media.metrics["guardar_lema_btn"]["y"]))


class End_Game_Menu:

    def __init__(self) -> None:
        End_Game_Menu.winner_text = ""
        End_Game_Menu.resize()

    @staticmethod
    def draw():
        Game.screen.blit(Media.sized["end_ui"], (Media.metrics["end_ui"]["x"], Media.metrics["end_ui"]["y"]))

        Game.screen.blit(Media.sized["volver_btn"], (Media.metrics["volver_btn"]["x"], Media.metrics["volver_btn"]["y"]))
        Game.screen.blit(Media.sized["revancha_btn"], (Media.metrics["revancha_btn"]["x"], Media.metrics["revancha_btn"]["y"]))

        Game.screen.blit(End_Game_Menu.winner_text, (Game.width//2-End_Game_Menu.winner_text.get_width()/2, Game.height//2))

        ClockAnimation.draw()

    @staticmethod
    def resize(winner=""):  # this is alose used as set winner function
        if winner != "":
            End_Game_Menu.winner_text = winner  # this variable is used because the user may want to resize the window while the game is running, so the text should re-render with the same winner as before even if the winner isnt passed as an argument
        End_Game_Menu.winner_text = Fonts.nickname_name_bar.render(End_Game_Menu.winner_text, True, Game.DARK_GREY)


class Name_Bar:

    def __init__(self) -> None:
        Name_Bar.resize()

    @staticmethod
    def draw(my_pfp, enemy_pfp):

        pfp_offset = Game.height/160

        # YOUR BAR

        y_offset = Game.height/1.89

        Game.screen.blit(my_pfp, (Media.metrics["name_bar"]["x"]+pfp_offset, Media.metrics["name_bar"]["y"]+pfp_offset+y_offset))  # +Game.height/60

        Game.screen.blit(Media.sized["name_bar"], (Media.metrics["name_bar"]["x"], Media.metrics["name_bar"]["y"]+y_offset))
        Game.screen.blit(Name_Bar.my_nickname_text, (Media.metrics["name_bar"]["x"]+Game.height/7.8, Media.metrics["name_bar"]["y"]+Game.height/80+y_offset))
        Game.screen.blit(Name_Bar.my_slogan_text, (Media.metrics["name_bar"]["x"]+Game.height/7, Media.metrics["name_bar"]["y"]+Game.height/17.5+y_offset))

        # ENEMY BAR

        Game.screen.blit(enemy_pfp, (Media.metrics["name_bar"]["x"]+pfp_offset, Media.metrics["name_bar"]["y"]+pfp_offset))  # +Game.height/60

        Game.screen.blit(Media.sized["name_bar"], (Media.metrics["name_bar"]["x"], Media.metrics["name_bar"]["y"]))
        Game.screen.blit(Name_Bar.enemy_nickname_text, (Media.metrics["name_bar"]["x"]+Game.height/7.8, Media.metrics["name_bar"]["y"]+Game.height/80))
        Game.screen.blit(Name_Bar.enemy_slogan_text, (Media.metrics["name_bar"]["x"]+Game.height/7, Media.metrics["name_bar"]["y"]+Game.height/17.5))

    @staticmethod
    def resize(my_nickname="Tú", my_slogan="Clan desconocido", enemy_nickname="Enemigo", enemy_slogan="Clan desconocido."):
        Name_Bar.enemy_nickname_text = Fonts.nickname_name_bar.render(enemy_nickname, True, Game.DARK_GREY)
        Name_Bar.enemy_slogan_text = Fonts.slogan_name_bar.render(enemy_slogan, True, Game.DARK_GREY)

        Name_Bar.my_nickname_text = Fonts.nickname_name_bar.render(my_nickname, True, Game.DARK_GREY)
        Name_Bar.my_slogan_text = Fonts.slogan_name_bar.render(my_slogan, True, Game.DARK_GREY)


class Chat:

    focused = False

    msj_history = [
        # {"text": {"person": , "date": , "msg": , "msg_lines": }, "render": } this is the format of the elements it contains
    ]

    def __init__(self, manager) -> None:
        # Chat.input_r = pygame.Rect()
        # Chat.input = pygame_gui.elements.UITextEntryLine(relative_rect=Chat.input_r, manager=manager)

        Chat.resize(manager)

        Chat.hide_input()

    @staticmethod
    def draw():

        def borrar_antes_de_n_coincidencias(texto, coincidencia, cantidad_coincidencias_en_cual_cortar):
            # Encontrar todas las posiciones de las coincidencias en el string
            posiciones = [i for i in range(len(texto)) if texto.startswith(coincidencia, i)]

            # Verificar si hay al menos tres coincidencias
            if len(posiciones) >= cantidad_coincidencias_en_cual_cortar:
                # Cortar el string desde el final de la tercera coincidencia
                return texto[posiciones[cantidad_coincidencias_en_cual_cortar-1] + len(coincidencia):]
            else:
                # Si no hay tres coincidencias, devolver el string original
                return texto

        Game.screen.blit(Media.sized["chat_ui"], (Media.metrics["chat_ui"]["x"], Media.metrics["chat_ui"]["y"]))

        # rect4 = pygame.rect.Rect(Media.useful_rects_metrics["send_btn_chat"]["x"], Media.useful_rects_metrics["send_btn_chat"]["y"], Media.useful_rects_metrics["send_btn_chat"]["w"], Media.useful_rects_metrics["send_btn_chat"]["h"])
        # pygame.draw.rect(Game.screen, (255, 255, 125), rect4)

        max_chat_height = Media.metrics["chat_ui"]["h"]*0.67
        chat_init_height = Media.metrics["chat_ui"]["y"]+Media.metrics["chat_ui"]["h"]-Media.metrics["chat_ui"]["h"]*0.16

        # chat_init_height2 = Media.metrics["chat_ui"]["h"]*0.16

        # pygame.draw.rect(Game.screen, (255, 255, 125), pygame.rect.Rect(Media.metrics["chat_ui"]["x"]-50, Media.metrics["chat_ui"]["y"]+Media.metrics["chat_ui"]["h"]-max_chat_height-chat_init_height2, 70, max_chat_height))

        chars_height = round(Media.fonts_metrics["chat_msg_font"]+Media.fonts_metrics["chat_msg_font"]*0.08)

        max_lines_amount = int(max_chat_height//chars_height)

        total_lines = 0

        for msg_being_rendered in Chat.msj_history:

            total_lines += msg_being_rendered["msg_info"]["lines"]

            distance_from_init = total_lines*chars_height

            if total_lines > max_lines_amount:

                excedent_lines = total_lines-max_lines_amount

                distance_from_init = max_lines_amount*chars_height

                # splited_msg = msg_being_rendered["msg_info"]["msj"].split("\n")

                msg_content_formatted = "[" + msg_being_rendered["msg_info"]["date"] + "] " + msg_being_rendered["msg_info"]["person"].capitalize() + " : " + msg_being_rendered["msg_info"]["msj"]

                splited_msg = Fonts.transform_text_line_to_paragraph(msg_content_formatted, 33, join=False)

                # cut_msg = borrar_antes_de_n_coincidencias(splited_msg[0], "\n", excedent_lines-1)

                # print(cut_msg)

                cut_msg = "\n".join(splited_msg[0][excedent_lines:])

                render_to_show = Fonts.chat_msg_font.render(cut_msg, True, Game.LIGHT_GREY)

                Game.screen.blit(render_to_show, (Media.metrics["chat_ui"]["x"]+Game.height/80, chat_init_height-distance_from_init))

                break

            else:
                render_to_show = msg_being_rendered["render"]

            Game.screen.blit(render_to_show, (Media.metrics["chat_ui"]["x"]+Game.height/80, chat_init_height-distance_from_init))

    def add(person, msg_content, date):  # time.strftime("%H:%M")

        msg_content.replace("\n", "")  # deleting all possible \n made by the user

        msg_content_formatted = "[" + date + "] " + person.capitalize() + " : " + msg_content   # it adds the date and the person's name to the message because its going to be shown all together

        formatted_msg = Fonts.transform_text_line_to_paragraph(msg_content_formatted, 33)  # this slipts the text into multuple lines if it's too long

        print(formatted_msg[0])

        msg = {"person": person, "date": date, "msj": msg_content, "lines": formatted_msg[1]}  # this saves important info about the message coupled with the message itself

        render = Fonts.chat_msg_font.render(formatted_msg[0], True, Game.LIGHT_GREY)  # this generates a visual render of the message

        Chat.msj_history.insert(0, {"msg_info": msg, "render": render})  # we store both the render and the info about the message in an dict and add that to the general list of messages
        # we insert the message at the start of the list so then we can go thought the list more easily

    @ staticmethod
    def resize(manager):
        try:
            Chat.input.kill()
        except:
            pass
        Chat.input_r = pygame.Rect()
        Chat.input = pygame_gui.elements.UITextEntryLine(relative_rect=Chat.input_r, manager=manager)

        Chat.input.set_position((Media.chat_input_metrics["x"], Media.chat_input_metrics["y"]))   # Cambiar posición
        Chat.input.set_dimensions((Media.chat_input_metrics["w"], Media.chat_input_metrics["h"]))  # Cambiar tamaño

        # this following lines of code resize the already exisiting messages so they fit the new size of the chat. they get rendered again
        copy_msj_history = Chat.msj_history.copy()  # we make a copy of the list of messages
        Chat.msj_history = []  # we delete the original list of messages
        for msg in reversed(copy_msj_history):  # this is reversed because we need to go from the last message to the first one as they are added on position 0 of the list
            Chat.add(msg["msg_info"]["person"], msg["msg_info"]["msj"], msg["msg_info"]["date"])

    @ staticmethod
    def show_input():
        Chat.input.show()

    @ staticmethod
    def hide_input():
        Chat.input.hide()
        Chat.focused = False


class Warning:

    show_warning = False
    duration = 1
    text_line_length = 28
    played_sound = False
    sound = True

    def __init__(self) -> None:
        pass

    @ staticmethod
    def draw():

        if Warning.show_warning:
            """
            old code:
            # this following 4 lines calculate the x offset for the whole warning image and text so it makes a cool looking animation. we use smooth_movent() to transform lineal time to a curve.
            # animation_duration = Warning.duration*0.25  # this sets the duration of the movemnt to 25% of the total duration of the warning
            # current_time = numpy.interp(time.time()-Warning.init_time, [0, animation_duration], [0, Warning.duration])  # i think there is another way of doing this but it makes
            """
            if Warning.sound:
                if not Warning.played_sound and time.time()-Warning.init_time > Warning.duration*0.025:  # this is the duration of the movement of the warning image and text

                    try:
                        Sound.play_sfx(Sound.SFX[2])
                        Warning.played_sound = True
                    except:
                        pass

            animation_duration = Warning.duration*0.16  # the duration of the animation is 16% of the total duration of  the warning
            if animation_duration > 2:  # and it has a max value of two seconds
                animation_duration = 2

            current_time = numpy.interp(time.time()-Warning.init_time, [0, animation_duration], [0, 3])  # this tells that the 25% of the duration of the warning is the duration of the movement and it scales it to a (0-3) range 3 being the end of the curve based on the visualisation of the formula of smooth_movement().
            coeficient = Game.smooth_movement(current_time, 3)  # this 3 is the power of the curve and how fast it moves.
            x_anim = numpy.interp(coeficient, [0, 1], [0-Media.metrics["warning_ui"]["w"]*1.1, 0])  # this is the actual offset of the image and text and we multiply the width by 1.1 so it moves a little bit more than the width of the image away of the screen

            Game.screen.blit(Media.sized["warning_ui"], (Media.metrics["warning_ui"]["x"] + x_anim, Media.metrics["warning_ui"]["y"]))
            Game.screen.blit(Warning.title, (Media.metrics["warning_ui"]["x"]+Game.height/12 + x_anim, Media.metrics["warning_ui"]["y"]+Game.height/45))
            Game.screen.blit(Warning.message, (Media.metrics["warning_ui"]["x"]+Game.height/40 + x_anim, Media.metrics["warning_ui"]["y"]+Game.height/13.2))

            if time.time() - Warning.init_time > Warning.duration:
                Warning.show_warning = False
                Warning.sound = True

    @ staticmethod
    def warn(title, message, duration, sound=True):

        Warning.title = Fonts.warning_title_font.render(title, True, Game.LIGHT_GREY)

        max_width = Media.metrics["warning_ui"]["w"] - Game.height/80
        max_chars_per_line = max_width//(pygame.font.SysFont("Times New Roman", Media.fonts_metrics["chat_msg_font"]).render("x", True, (0, 0, 0)).get_width())  # this is the max number of characters that can be in a line calculated based on the width of one rendered char

        Warning.message = Fonts.warning_message_font.render(Fonts.transform_text_line_to_paragraph(message, max_chars_per_line)[0], True, Game.LIGHT_GREY)
        Warning.duration = duration
        Warning.sound = sound
        Warning.show_warning = True
        Warning.played_sound = False
        Warning.init_time = time.time()


class Timer:

    latency = 0
    turn_beginning = 0
    my_remaining_time = 0
    enemy_remaining_time = 0
    iteration_time_counter = 0

    # my_timer_last_value = 0

    def __init__(self):
        Timer.update_enemy(0, time.time())
        Timer.set_timers(300)  # 671
        Timer.update_texts()

    @staticmethod
    def set_timers(seconds, which="all", measure=False):

        if measure:
            Timer.turn_beginning = time.time()
            Timer.iteration_time_counter = time.time()

        # Timer.my_timer_last_value = Timer.my_remaining_time

        if which == "me" or which == "all":
            Timer.my_remaining_time = seconds

        if which == "enemy" or which == "all":
            Timer.enemy_remaining_time = seconds

    @staticmethod
    def update_enemy(passed_enemy_remaining_time, time_when_sent):

        Timer.latency = (time.time() - time_when_sent)/1000  # latency in miliseconds
        Timer.latency_render = Fonts.latency.render(f"{(Timer.latency*1000*2):.1f} ms", True, Game.MID_GREY)

        if Timer.latency < 1500:
            Timer.enemy_remaining_time = passed_enemy_remaining_time
        else:
            Timer.enemy_remaining_time = passed_enemy_remaining_time - Timer.latency*1000*2
            return True, Timer.latency

        return False, 0

    @staticmethod
    def start_counting_my_turn():  # this function everytime its called saves the time of that moment and returns the difference in seconds between the last time it was called. used to measure how much my turn lasts
        x = Timer.turn_beginning
        Timer.turn_beginning = time.time()
        return Timer.turn_beginning-x, Timer.turn_beginning

    @staticmethod
    def who_run_out_of_time(my_team, enemy_team):
        if Timer.my_remaining_time <= 0:
            return my_team
        else:
            return enemy_team

    @staticmethod
    def update_texts():
        render = Fonts.timer.render(Timer.formatting_secs(Timer.my_remaining_time), True, Game.CREME)
        render.set_alpha(72)
        rotated_surface = pygame.transform.rotate(render, 45)  # Rotar la superficie del texto en el ángulo deseado
        rotated_rect = rotated_surface.get_rect(center=(Game.height/0.73, Game.height/1.97))  # Obtener el rectángulo de la superficie rotada y centrarlo en la posición deseada
        Timer.my_timer = (rotated_surface, rotated_rect)

        render = Fonts.timer.render(Timer.formatting_secs(Timer.enemy_remaining_time), True, Game.CREME)
        render.set_alpha(72)
        rotated_surface = pygame.transform.rotate(render, -45)  # Rotar la superficie del texto en el ángulo deseado
        rotated_rect = rotated_surface.get_rect(center=(Game.height/0.73, Game.height/2.85))  # Obtener el rectángulo de la superficie rotada y centrarlo en la posición deseada
        Timer.enemy_timer = (rotated_surface, rotated_rect)

    @staticmethod
    def draw_timer():

        Game.screen.blit(Timer.my_timer[0], Timer.my_timer[1].topleft)  # Dibujar la superficie rotada en la pantalla
        Game.screen.blit(Timer.enemy_timer[0], Timer.enemy_timer[1].topleft)  # Dibujar la superficie rotada en la pantalla

    @staticmethod
    def update_n_draw(current_turn, my_team):

        iteration_time = time.time() - Timer.iteration_time_counter

        if iteration_time > 0.33:  # this gets executed 3 time per second
            Timer.iteration_time_counter = time.time()

            if current_turn == my_team:
                Timer.my_remaining_time -= iteration_time
            else:
                Timer.enemy_remaining_time -= iteration_time

            if Timer.my_remaining_time <= 0 or Timer.enemy_remaining_time <= 0:
                return True

            Timer.update_texts()

        Timer.draw_timer()  # this blits the images in the screen so it gets refreshed every frame

        return False

    def formatting_secs(seconds):
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{int(minutes)}:{int(remaining_seconds):02d}"


class ClockAnimation:

    current_clock_metrics = None

    direction = 0

    show_clock_animation = False

    clock_animation_ite = 0

    def __init__(self) -> None:
        pass

    def draw():
        if ClockAnimation.show_clock_animation:
            if 0 <= ClockAnimation.clock_animation_ite < 40:
                i = 0
            if 40 <= ClockAnimation.clock_animation_ite < 60:
                i = 1
            if 60 <= ClockAnimation.clock_animation_ite < 80:
                i = 2
            if 80 <= ClockAnimation.clock_animation_ite < 100:
                i = 3
            if 100 <= ClockAnimation.clock_animation_ite <= 140:
                i = 4
            Game.screen.blit(Media.sized[f"clk_{i}"], (ClockAnimation.current_clock_metrics[0], ClockAnimation.current_clock_metrics[1]))
            if ClockAnimation.clock_animation_ite <= 0:
                ClockAnimation.direction = 1
            elif ClockAnimation.clock_animation_ite >= 140:
                ClockAnimation.direction = -1

            ClockAnimation.clock_animation_ite += ClockAnimation.direction

        else:
            ClockAnimation.clock_animation_ite = 0

    def set_animation_status(state, ui=None):  # When I want to change the animation state I also specify the measures I want to display it with. That is, I want to specify the position, but that is already configured for each UI, so you just pass the UI name

        if ui != None:  # if we just want to turn the animation off then you dont need to pass the ui name
            ClockAnimation.current_clock_metrics = Media.clock_animation_metrics[ui]

        ClockAnimation.show_clock_animation = state


class UI:
    # @staticmethod
    def init():
        UI.font = pygame.font.Font(None, 30)
        UI.sfont = pygame.font.Font(None, 20)
        UI.lfont = pygame.font.Font(None, 40)
        UI.xlfont = pygame.font.Font(None, 50)
        UI.center = (Game.screen.get_size()[0]//2, Game.screen.get_size()[1]//2)
        UI.config_menu_pos = (round(Game.screen.get_size()[0]/1.21), round(Game.screen.get_size()[1]/7.7))
        UI.half_width = Game.screen.get_size()[0]//2
        UI.half_height = Game.screen.get_size()[1]//2

        UI.fonts = {
            'sm': UI.sfont,
            'm': UI.font,
            'l': UI.lfont,
            'xl': UI.xlfont
        }


class Slider_Menu:

    def __init__(self):

        self.sliders = [
            Slider(Media.slider_metrics["pos"], Media.slider_metrics["size"], 0.4, 0, 1)  # ,
        ]

    def run(self, show_music):
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        if show_music:

            Game.screen.blit(Media.sized["music_btn"], (Media.metrics["music_btn"]["x"], Media.metrics["music_btn"]["y"]))

            for slider in self.sliders:
                if slider.container_rect.collidepoint(mouse_pos):
                    if mouse[0]:
                        slider.grabbed = True
                if not mouse[0]:
                    slider.grabbed = False
                if slider.btn_rect.collidepoint(mouse_pos):
                    slider.hover()
                if slider.grabbed:
                    slider.move_slider(mouse_pos)
                    slider.hover()
                    new_value = slider.get_value()
                    if slider.current_value != new_value:
                        slider.current_value = round(new_value, 2)
                else:
                    slider.hovered = False

                slider.render()
                # slider.display_value(self.app)


class Slider:

    UNSELECTED = "darkgray"
    SELECTED = "white"
    btnSTATES = {
        True: SELECTED,
        False: UNSELECTED
    }

    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int):
        self.pos = pos
        self.size = size
        self.hovered = False
        self.grabbed = False

        self.current_value = initial_val

        self.slider_left_pos = self.pos[0] - (size[0]//2)
        self.slider_right_pos = self.pos[0] + (size[0]//2)
        self.slider_top_pos = self.pos[1] - (size[1]//2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos-self.slider_left_pos)*initial_val  # <- percentage

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.btn_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10, self.size[1])

        # label
        self.text = UI.fonts['m'].render(str(int(self.get_value())), True, "white", None)
        self.label_rect = self.text.get_rect(center=(self.pos[0], self.slider_top_pos - 15))

    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.btn_rect.centerx = pos
        # print("moved")

    def hover(self):
        self.hovered = True

    def render(self):
        pygame.draw.rect(Game.screen, "black", self.container_rect)
        pygame.draw.rect(Game.screen, Slider.btnSTATES[self.hovered], self.btn_rect)

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        btn_val = self.btn_rect.centerx - self.slider_left_pos

        return (btn_val/val_range)*(self.max-self.min)+self.min

    def display_value(self):
        self.text = UI.fonts['m'].render(str(int(self.get_value())), True, "white", None)
        Game.screen.blit(self.text, self.label_rect)


class Turn_Btn:

    def __init__(self):
        Turn_Btn.resize()

    def draw(self):

        Game.screen.blit(Media.sized["turn_btn"], Turn_Btn.rect)

    @staticmethod
    def resize():
        Turn_Btn.rect = Media.sized["turn_btn"].get_rect()
        Turn_Btn.rect.topleft = (Media.metrics["turn_btn"]["x"], Media.metrics["turn_btn"]["y"])
        Turn_Btn.image_mask = pygame.mask.from_surface(Media.sized["turn_btn"])


class Turn_History:

    def __init__(self):
        Turn_History.resize()

    def draw(self):

        Game.screen.blit(Media.sized["turn_next_btn"], Turn_History.rect_next)
        Game.screen.blit(Media.sized["turn_prev_btn"], Turn_History.rect_prev)

    @staticmethod
    def resize():
        Turn_History.rect_next = Media.sized["turn_next_btn"].get_rect()
        Turn_History.rect_next.topleft = (Media.metrics["turn_next_btn"]["x"], Media.metrics["turn_next_btn"]["y"])
        Turn_History.image_mask_next = pygame.mask.from_surface(Media.sized["turn_next_btn"])

        Turn_History.rect_prev = Media.sized["turn_prev_btn"].get_rect()
        Turn_History.rect_prev.topleft = (Media.metrics["turn_prev_btn"]["x"], Media.metrics["turn_prev_btn"]["y"])
        Turn_History.image_mask_prev = pygame.mask.from_surface(Media.sized["turn_prev_btn"])


class Mini_Flags:

    def __init__(self):

        Mini_Flags.resize()

    def draw(self, current_turn):
        if current_turn == "blue":
            Game.screen.blit(Media.sized["mini_flag_blue"], Mini_Flags.rect)
        else:
            Game.screen.blit(Media.sized["mini_flag_red"], Mini_Flags.rect)

    @staticmethod
    def resize():
        Mini_Flags.rect = Media.sized["mini_flag_blue"].get_rect()
        Mini_Flags.rect.topleft = (Media.metrics["mini_flag_blue"]["x"], Media.metrics["mini_flag_blue"]["y"])


class Cursor:

    show_cursor = True

    image = None

    def __init__(self):
        Cursor.image = Media.sized["cursor_default"]

    @ staticmethod
    def draw():
        Game.screen.blit(Cursor.image, pygame.mouse.get_pos())


class Particle:

    # Colores cálidos balanceados
    PARTICLE_COLORS = [
        (255, 180, 70),  # Naranja claro
        (255, 100, 50),  # Rojo anaranjado
        (220, 80, 70),   # Rojo cálido
        (200, 60, 50)    # Bordo oscuro
    ]

    # Color dorado para las partículas grandes
    GOLD_COLOR = (255, 215, 0)

    def __init__(self, x, y, origin_x, origin_y, target_x, target_y, color, size_factor=1, speed_factor=1):
        self.x = x
        self.y = y
        self.color = color
        self.size = int(random.choices([1, 2, 3], weights=[30, 50, 20])[0] * size_factor)  # Tamaño variable
        self.speed_x = random.uniform(-0.105, 0.105) * speed_factor  # Velocidad incrementada
        self.speed_y = random.uniform(-0.105, 0.105) * speed_factor  # Velocidad incrementada
        self.angle = random.uniform(-math.pi / 4, math.pi / 4)  # Dirección inicial aleatoria
        self.angle_change = random.uniform(-0.1, 0.1)  # Variación de ángulo para simular movimiento fluido
        self.lifetime = self.calculate_lifetime(x, y, origin_x, origin_y, target_x, target_y)

    def calculate_lifetime(self, x, y, origin_x, origin_y, target_x, target_y):
        # Calculamos la distancia al segmento
        distance = Particle.distance_from_segment(x, y, origin_x, origin_y, target_x, target_y)

        # Umbral de desviación de la partícula con respecto al hilo
        max_distance = 0.1 * math.sqrt((target_x - origin_x) ** 2 + (target_y - origin_y) ** 2)  # 10% de la longitud total del hilo

        deviation_percent = min(distance / max_distance, 0.1)  # Limitar la desviación al 10%

        # Cálculo de vida en función de la desviación
        if deviation_percent >= 0.1:
            lifetime = 1  # Si está a 1/10 de la distancia, vida es 1ms
        else:
            # lifetime = 400 * (1 - deviation_percent / 0.1)  # 400ms para desviación 1%, 0ms para desviación 10%
            normalized_deviation = deviation_percent / 0.1  # Normaliza a un rango [0, 1]
            lifetime = 400 / (1 + 5 * normalized_deviation)

        return lifetime

    def move(self):
        # Movimiento con cambio de dirección suave
        self.angle += self.angle_change
        self.speed_x = math.cos(self.angle) * 0.105  # Velocidad incrementada
        self.speed_y = math.sin(self.angle) * 0.105  # Velocidad incrementada

        # Introducimos más aleatoriedad para curvar el movimiento
        self.speed_x += random.uniform(-0.05, 0.05)
        self.speed_y += random.uniform(-0.05, 0.05)

        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1  # Disminuir lifetime por fotograma

    def draw(self, surface):
        if self.lifetime > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

    def distance_from_segment(x, y, x1, y1, x2, y2):
        # Vectores de dirección del segmento
        dx = x2 - x1
        dy = y2 - y1
        # Cálculo del producto punto para la proyección
        segment_length_sq = dx * dx + dy * dy
        if segment_length_sq == 0:
            return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)

        t = ((x - x1) * dx + (y - y1) * dy) / segment_length_sq

        # Si t está fuera del rango [0, 1], tomar la distancia a los puntos extremos
        if t < 0:
            closest_x, closest_y = x1, y1
        elif t > 1:
            closest_x, closest_y = x2, y2
        else:
            closest_x = x1 + t * dx
            closest_y = y1 + t * dy

        return math.sqrt((x - closest_x) ** 2 + (y - closest_y) ** 2)


class Movement_Indicator:  # Clase para el Indicador de Movimiento (hilo conector entre posicion inicial y nueva)

    def __init__(self, origin):
        self.origin = origin
        self.particles = []  # Lista para almacenar las partículas
        self.frame_count = 0  # Contador para controlar la actualización cada 4 fotogramas
        self.last_position = None  # Para almacenar la posición anterior del segmento
        self.time_in_same_position = 0  # Tiempo que el segmento ha estado en la misma posición
        self.max_large_particles = 5  # Límite de partículas grandes por fotograma
        self.large_particle_timer = 0  # Temporizador para generar una partícula dorada por segundo

    def h(self):
        print("kklklk manito")

    def create_particle(self, pos, size_factor, color):
        """Crea una nueva partícula y la agrega a la lista de partículas."""
        t = random.uniform(0, 1)
        x = self.origin[0] + t * (pos[0] - self.origin[0])
        y = self.origin[1] + t * (pos[1] - self.origin[1])
        self.particles.append(Particle(x, y, self.origin[0], self.origin[1], pos[0], pos[1], color, size_factor=size_factor))

    def draw(self, pos):
        # Controlar la posición del segmento
        if self.last_position is None:
            self.last_position = pos

        # Verificar si la variación de posición es menor al 4%
        distance_moved = math.sqrt((pos[0] - self.last_position[0]) ** 2 + (pos[1] - self.last_position[1]) ** 2)
        max_distance = math.sqrt((Game.width - 0) ** 2 + (Game.height - 0) ** 2)  # Distancia máxima posible en la pantalla
        movement_percentage = distance_moved / max_distance

        # Si la variación es menor al 4%, aumentar el tiempo en la misma posición
        if movement_percentage < 0.04:
            self.time_in_same_position += 1
        else:
            self.time_in_same_position -= 60  # Resetear si el segmento se mueve demasiado
            if self.time_in_same_position < 0:
                self.time_in_same_position = 0

        # Solo generar una partícula dorada cada segundo
        if self.time_in_same_position >= 240 and random.randint(0, 100) < 6:  # 4 segundos en la misma posición
            self.create_particle(pos, 2, Particle.GOLD_COLOR)

        else:
            # Crear partículas normales
            self.create_particle(pos, 1, random.choice(Particle.PARTICLE_COLORS))

        # Solo recalcular la distancia cada 4 fotogramas
        self.frame_count += 1
        if self.frame_count >= 4:
            self.frame_count = 0  # Reiniciar contador

            # Seleccionar un 25% de las partículas aleatoriamente, pero sin exceder el número total de partículas
            particles_to_check = random.sample(self.particles, min(len(self.particles), max(1, len(self.particles) // 3)))

            # Recalcular la vida de las partículas seleccionadas
            for particle in particles_to_check:
                particle.lifetime = particle.calculate_lifetime(particle.x, particle.y, self.origin[0], self.origin[1], pos[0], pos[1])

        # Actualizar y dibujar las partículas
        to_remove = []  # Lista para almacenar las partículas que deben eliminarse
        for particle in self.particles:
            particle.move()
            particle.draw(Game.screen)

            # Si la partícula ha muerto, agregarla a la lista de eliminación
            if particle.lifetime <= 0:
                to_remove.append(particle)

        # Eliminar partículas muertas
        for particle in to_remove:
            self.particles.remove(particle)

        # Actualizar la posición anterior
        self.last_position = pos
