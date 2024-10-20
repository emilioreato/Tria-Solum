import os
import math
import numpy
import pygame
import pyautogui
import threading
import wave
import pyaudio
from media import Media, Fonts
from win32con import ENUM_CURRENT_SETTINGS
from win32api import EnumDisplaySettings
import random
import string
from online_utilities import online_tools
import pygame_gui
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
import time


os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets the current directory to the file's directory

# SYSTEM CLASSES


class Game:

    DARK_GREY = (20, 21, 23)
    LIGHT_GREY = (89, 90, 91)

    board_size = 8
    center_points = []

    screen = 0
    width = 0
    height = 0
    screen_height = 0
    timer = 0
    dev_mode = 0

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
                file.write("pfp: resources\\images\\indicator.png \nnickname: Invitado\nslogan: Clan anónimo")  # writes the default values

        else:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            if mode == "read":
                for line in lines:
                    if text_to_search in line:
                        return line

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
        pygame.mixer.music.load(track)  # loads the track
        pygame.mixer.music.play()  # plays the track

    @staticmethod
    def stopmusic():
        pygame.mixer.quit()  # close the pygame mixer


# PIECES CLASSES

class Piece:

    pieces_ids = []

    health_color = (170, 0, 10)
    health_background_color = (33, 3, 3)
    mana_color = (232, 159, 10)
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

    def draw_health_bar(self, my_team, my_team_count, enemy_count):

        if self.team == my_team:
            is_my_piece = True
            mult = 1
        else:
            is_my_piece = False
            mult = 10/12

        if is_my_piece:
            bar_height = mult*Game.height/24
            bar_width = mult*Game.height/5.125
        else:
            bar_height = mult*Game.height/16
            bar_width = mult*Game.height/3.8

        health_percentage = self.hp / self.max_hp  # calculates the length of the health bar in function of the percentage of health
        health_bar_length = int(bar_width * health_percentage)

        mana_percentage = self.mana / self.max_mana  # calculates the length of the mana bar in function of the percentage of mana
        mana_bar_length = int(bar_width * mana_percentage)

        bar_x = (Game.width/15)

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

        pygame.draw.rect(Game.screen, self.health_background_color, (bar_x+x_buff, bar_y+y_buff, bar_width, bar_height))
        pygame.draw.rect(Game.screen, self.health_color, (bar_x+x_buff, bar_y+y_buff, health_bar_length, bar_height))  # Dibuja la barra de vida restante (verde)

        if is_my_piece:

            pygame.draw.rect(Game.screen, self.mana_background_color, (bar_x+x_buff, bar_y+bar_height+y_buff, bar_width, bar_height/2))
            pygame.draw.rect(Game.screen, self.mana_color, (bar_x+x_buff, bar_y+bar_height+y_buff, mana_bar_length, bar_height/2))  # Dibuja la barra de vida restante (verde)

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


class Cards:
    def __init__(self, x, y, name, cost, damage, distance, duration, effect, can_hit_self=False, can_hit_tiles=False, can_hit_allys=False, can_hit_enemies=False):
        self.x = x  # position on the screen
        self.y = y  # position on the screen
        self.name = name
        self.cost = cost
        self.damage = damage
        self.distance = distance
        self.duration = duration
        self.effect = effect
        self.can_hit_self = can_hit_self
        self.can_hit_tiles = can_hit_tiles
        self.can_hit_allys = can_hit_allys
        self.can_hit_enemies = can_hit_enemies

    def can_use_card(self, target, caster):
        """Verifica si la carta puede ser utilizada en el objetivo dado las reglas."""
        distance_to_target = self.calculate_distance(caster, target)

        # Verificar si el objetivo está a la distancia permitida
        if distance_to_target > self.distance:
            print(f"El objetivo está fuera de alcance. Distancia máxima: {self.distance}.")
            return False

        # Verificar si puede golpear al objetivo correcto (enemigos, aliados, etc.)
        if target == caster and not self.can_hit_self:
            print(f"No puedes usar {self.name} en ti mismo.")
            return False

        if target.is_tile and not self.can_hit_tiles:
            print(f"{self.name} no puede ser usada en baldosas vacías.")
            return False

        if target.is_ally(caster) and not self.can_hit_allys:
            print(f"{self.name} no puede afectar a aliados.")
            return False

        if target.is_enemy(caster) and not self.can_hit_enemies:
            print(f"{self.name} no puede afectar a enemigos.")
            return False

        return True


class Deck:
    def __init__(self):
        self.cards = {
            "knight": [],
            "mage": [],
            "archer": [],
            "neutral": []
        }
        self.create_deck()

    def create_deck(self):  # creates the deck with all the cards # have yet to make the cards

        knight_card = Cards(x=0, y=0, name="Espada", cost=1, damage=5, distance=1, duration=0, effect="Causa daño", can_hit_self=False)
        knight_card2 = Cards(x=0, y=0, name="salto", cost=1, damage=5, distance=1, duration=0, effect="Causa daño", can_hit_self=False)
        mage_card = Cards(x=0, y=0, name="Magia", cost=2, damage=7, distance=3, duration=0, effect="Causa daño", can_hit_self=False)
        archer_card = Cards(x=0, y=0, name="Flecha", cost=1, damage=3, distance=2, duration=0, effect="Causa daño", can_hit_self=False)
        neutral_card = Cards(x=0, y=0, name="Curación", cost=2, damage=0, distance=1, duration=2, effect="Recupera vida", can_hit_self=True)

        for _ in range(4):  # Crear 4 duplicados por carta, entre parentesis va la cantidad de cartas que queres que haya en el mazo
            self.cards["knight"].append(knight_card)
            self.cards["knight"].append(knight_card2)
            self.cards["mage"].append(mage_card)
            self.cards["archer"].append(archer_card)
            self.cards["neutral"].append(neutral_card)

    def shuffle_deck(self):
        for card_type in self.cards:
            random.shuffle(self.cards[card_type])

    def draw_card(self, card_type):
        if self.cards[card_type]:
            return self.cards[card_type].pop(0)  # Devuelve la primera carta del tipo solicitado
        else:
            print(f"No hay más cartas de tipo {card_type}.")
            return None


class Inventory:
    def __init__(self):
        self.cards = {
            "knight": [],
            "mage": [],
            "archer": [],
            "neutral": []
        }

    def add_card(self, card, card_type):
        if len(self.cards[card_type]) < 3:
            self.cards[card_type].append(card)
        else:
            print(f"No puedes tener más de 3 cartas de tipo {card_type}.")

    def refill_inventory(self, deck):
        for card_type in self.cards:
            while len(self.cards[card_type]) < 3:
                new_card = deck.draw_card(card_type)
                if new_card:
                    self.add_card(new_card, card_type)
                else:
                    break  # Salir si no hay más cartas para robar

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

    def __init__(self, manager):
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
        font = pygame.font.Font(None, Game.height//34)
        MatchCreation.ip_text = font.render(f"Clave: {online_tools.Online.public_ip}", True, Game.DARK_GREY)
        MatchCreation.ip_text_rect = MatchCreation.ip_text.get_rect(center=(Game.width/2,  Game.height/1.98))


class JoinMatch:

    show_ingresar_btn = False

    def __init__(self, manager):
        JoinMatch.input_rect = pygame.Rect()
        JoinMatch.input_texto = pygame_gui.elements.UITextEntryLine(relative_rect=JoinMatch.input_rect, manager=manager)

        JoinMatch.boton_rect = pygame.Rect()
        JoinMatch.boton_conectar = pygame_gui.elements.UIButton(relative_rect=JoinMatch.boton_rect, text='Conectar', manager=manager)

        JoinMatch.resize()

        JoinMatch.hide_input()

    def draw(self):

        Game.screen.blit(Media.sized["lobby_ui"], (Media.metrics["lobby_ui"]["x"], Media.metrics["lobby_ui"]["y"]))

        ClockAnimation.draw()

        if JoinMatch.show_ingresar_btn:
            Game.screen.blit(Media.sized["ingresar_btn"], (Media.metrics["ingresar_btn"]["x"], Media.metrics["ingresar_btn"]["y"]))

    @staticmethod
    def resize():
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

    @staticmethod
    def draw():

        Game.screen.blit(Media.sized["configuration_ui"], (Media.metrics["configuration_ui"]["x"], Media.metrics["configuration_ui"]["y"]))

        Game.screen.blit(Media.sized["apoyanos_btn"], (Media.metrics["apoyanos_btn"]["x"], Media.metrics["apoyanos_btn"]["y"]))


class Profile_Menu:

    def __init__(self, manager):
        Profile_Menu.nickname_input = pygame.Rect()
        Profile_Menu.nickname_input = pygame_gui.elements.UITextEntryLine(relative_rect=Profile_Menu.nickname_input, manager=manager)

        Profile_Menu.slogan_input = pygame.Rect()
        Profile_Menu.slogan_input = pygame_gui.elements.UITextEntryLine(relative_rect=Profile_Menu.slogan_input, manager=manager)

        Profile_Menu.resize()

        Profile_Menu.hide_input()

    @staticmethod
    def resize():
        Profile_Menu.nickname_input.set_dimensions((Media.profile_menu_metrics["nickname_input"]["w"], Media.profile_menu_metrics["nickname_input"]["h"]))  # Cambiar tamaño
        Profile_Menu.nickname_input.set_position((Media.profile_menu_metrics["nickname_input"]["x"], Media.profile_menu_metrics["nickname_input"]["y"]))   # Cambiar posición
        Profile_Menu.slogan_input.set_dimensions((Media.profile_menu_metrics["slogan_input"]["w"], Media.profile_menu_metrics["slogan_input"]["h"]))  # Cambiar tamaño
        Profile_Menu.slogan_input.set_position((Media.profile_menu_metrics["slogan_input"]["x"], Media.profile_menu_metrics["slogan_input"]["y"]))   # Cambiar posición

    @staticmethod
    def show_input():
        Profile_Menu.nickname_input.show()
        Profile_Menu.slogan_input.show()

    @staticmethod
    def hide_input():
        Profile_Menu.nickname_input.hide()
        Profile_Menu.slogan_input.hide()

    @staticmethod
    def draw():
        Game.screen.blit(Media.sized["perfil_ui"], (Media.metrics["perfil_ui"]["x"], Media.metrics["perfil_ui"]["y"]))

        Game.screen.blit(Media.sized["seleccionar_foto_btn"], (Media.metrics["seleccionar_foto_btn"]["x"], Media.metrics["seleccionar_foto_btn"]["y"]))
        Game.screen.blit(Media.sized["guardar_apodo_btn"], (Media.metrics["guardar_apodo_btn"]["x"], Media.metrics["guardar_apodo_btn"]["y"]))
        Game.screen.blit(Media.sized["guardar_lema_btn"], (Media.metrics["guardar_lema_btn"]["x"], Media.metrics["guardar_lema_btn"]["y"]))


class Chat:

    def __init__(self) -> None:
        pass

    @staticmethod
    def draw():
        Game.screen.blit(Media.sized["chat_ui"], (Media.metrics["chat_ui"]["x"], Media.metrics["chat_ui"]["y"]))


class Warning:

    show_warning = False
    duration = 1
    text_line_length = 28
    played_sound = False
    sound = True

    def __init__(self) -> None:
        pass

    @staticmethod
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
            Game.screen.blit(Warning.title, (Media.metrics["warning_ui"]["x"]+Game.height/12 + x_anim, Media.metrics["warning_ui"]["y"]+Game.height/40))
            Game.screen.blit(Warning.message, (Media.metrics["warning_ui"]["x"]+Game.height/40 + x_anim, Media.metrics["warning_ui"]["y"]+Game.height/13.2))
            if time.time() - Warning.init_time > Warning.duration:
                Warning.show_warning = False
                Warning.sound = True

    @ staticmethod
    def warn(title, message, duration, sound=True):

        Warning.title = Fonts.warning_title_font.render(title, True, Game.LIGHT_GREY)
        Warning.message = Fonts.warning_messsage_font.render(Fonts.insertar_salto_linea_sin_cortar_palabras(message, 38), True, Game.LIGHT_GREY)
        Warning.duration = duration
        Warning.sound = sound
        Warning.show_warning = True
        Warning.played_sound = False
        Warning.init_time = time.time()


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
            Slider(Media.slider_metrics, (250, 20), 0.4, 0, 1)  # ,
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

        Turn_Btn.metrics = {"x": Game.height/1, "y": Game.height / 1.4, "w": Game.height / (5/1.512), "h": Game.height / 5}
        Turn_Btn.original_image = Media.convert(pygame.image.load("resources\\images\\menu\\turn_btn.png"), "alpha")
        Turn_Btn.image = pygame.transform.smoothscale(Turn_Btn.original_image, (Turn_Btn.metrics["w"], Turn_Btn.metrics["h"]))
        Turn_Btn.rect = Turn_Btn.image.get_rect()
        Turn_Btn.rect.topleft = (Turn_Btn.metrics["x"], Turn_Btn.metrics["y"])
        Turn_Btn.image_mask = pygame.mask.from_surface(Turn_Btn.image)

    def draw(self):

        Game.screen.blit(Turn_Btn.image, Turn_Btn.rect)


class Mini_Flags:

    def __init__(self):

        Mini_Flags.metrics = {"x": Game.height/0.905, "y": Game.height / 1.137, "w": Game.height / 14, "h": Game.height / 14}
        Mini_Flags.original_image_red = Media.convert(pygame.image.load("resources\\images\\flag_red.png"), "alpha")
        Mini_Flags.original_image_blue = Media.convert(pygame.image.load("resources\\images\\flag_blue.png"), "alpha")
        Mini_Flags.image_red = pygame.transform.smoothscale(Mini_Flags.original_image_red, (Mini_Flags.metrics["w"], Mini_Flags.metrics["h"]))
        Mini_Flags.image_blue = pygame.transform.smoothscale(Mini_Flags.original_image_blue, (Mini_Flags.metrics["w"], Mini_Flags.metrics["h"]))
        Mini_Flags.rect = Mini_Flags.image_red.get_rect()
        Mini_Flags.rect.topleft = (Mini_Flags.metrics["x"], Mini_Flags.metrics["y"])

    def draw(self, current_turn):
        if current_turn == "blue":
            Game.screen.blit(Mini_Flags.image_blue, Mini_Flags.rect)
        else:
            Game.screen.blit(Mini_Flags.image_red, Mini_Flags.rect)


class Cursor:

    show_cursor = True

    image = None

    def __init__(self):
        Cursor.image = Media.sized["cursor_default"]

    @ staticmethod
    def draw():
        Game.screen.blit(Cursor.image, pygame.mouse.get_pos())
