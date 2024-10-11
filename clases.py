import os
import math
import numpy
import pygame
import pyautogui
import threading
import wave
import pyaudio
from media import Media
from win32con import ENUM_CURRENT_SETTINGS
from win32api import EnumDisplaySettings
import random
import string


os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets the current directory to the file's directory


class Game:

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

    def convert_img(image, mode="default"):  # a function used to convert the images to the pygame format. you can choose between normal or alpha mode
        if mode == "alpha":
            return image.convert_alpha()
        return image.convert()


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

        if track in Sound.generated_tracks:
            print("not working")

        Sound.generated_tracks.append(track)

        pygame.mixer.music.load(track)  # loads the track
        pygame.mixer.music.play()  # plays the track

        if len(Sound.generated_tracks) > (len(Sound.PLAYLIST)-5):
            Sound.generated_tracks.pop(0)


class Piece:

    pieces_dimension = 0

    pieces_ids = []

    health_color = (170, 0, 10)
    health_background_color = (30, 0, 0)
    mana_color = (224, 159, 7)
    mana_background_color = (74, 52, 0)

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

        bar_width = Game.height/6.4
        bar_height = Game.height/64

        health_percentage = self.hp / self.max_hp  # Calcula la longitud de la barra de vida en función del porcentaje de vida
        health_bar_length = int(bar_width * health_percentage)

        mana_percentage = self.mana / self.max_mana  # Calcula la longitud de la barra de vida en función del porcentaje de vida
        mana_bar_length = int(bar_width * mana_percentage)

        bar_x = (Game.width/16.991)  # Mueve un poco la barra a la izquierda de la pieza
        if self.team == my_team:

            bar_y = (Game.height/1.095)  # Ajusta para colocar la barra debajo de la pieza
            bar_y = bar_y - my_team_count * 75
        else:

            bar_y = (Game.height/22)
            bar_y = bar_y + enemy_count * 75 - Game.height/6

        Game.screen.blit(Media.scale(self.original_image, Game.height/20, Game.height/20), (Game.width/16.991, bar_y))
        pygame.draw.rect(Game.screen, self.health_color, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(Game.screen, self.health_background_color, (bar_x, bar_y, health_bar_length, bar_height))  # Dibuja la barra de vida restante (verde)

        pygame.draw.rect(Game.screen, self.mana_color, (bar_x, bar_y+bar_height, bar_width, bar_height))
        pygame.draw.rect(Game.screen, self.mana_background_color, (bar_x, bar_y+bar_height, mana_bar_length, bar_height))  # Dibuja la barra de vida restante (verde)

    @ classmethod
    def set_dimension(cls, mult=1, screenratio=1):
        cls.pieces_dimension = round((Game.height // 14) / mult)
        print("pieces_dimension:", cls.pieces_dimension)

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

            # print(Piece.get_amount_of_grid_move(old_x, old_y, limited_x, limited_y))

            if change_mana:
                if self.mana > 0:
                    self.mana -= Piece.get_amount_of_grid_move(old_x, old_y, limited_x, limited_y)
                    # print(old_x, old_y, limited_x, limited_y, self.get_amount_of_grid_move(old_x, old_y, limited_x, limited_y), self.mana)

    def draw(self, screen, img, pos=0):
        # print(self.pos_x, self.pos_y)

        if pos:
            screen.blit(img, (pos[0]-Piece.pieces_dimension//2, pos[1]-Piece.pieces_dimension//2))
        else:
            screen.blit(img, (self.pos_x-Piece.pieces_dimension//2, self.pos_y-Piece.pieces_dimension//2))
        # pygame.draw.circle(screen, color, pos, self.rad)

    @ staticmethod
    def pov_based_pos_translation(x):  # it translated the coodinates of the enemy's pieces so you always see yours as the closest ones to the bottom of the screen, independently of the color.
        return abs(x-Game.board_size+1)  # it just inverts the board in x and y

    @ staticmethod
    def is_clicked(mouse_pos, pos):
        distancia = ((pos[0] - mouse_pos[0]) ** 2 + (pos[1] - mouse_pos[1]) ** 2) ** 0.5  # Calcular la distancia entre el cli
        return distancia <= Piece.pieces_dimension//2  # Devuelve True si el clic está dentro del círculo

    @ staticmethod
    def resize(active_pieces):
        for piece in active_pieces:
            piece.grid_pos_to_pixels(piece.grid_pos_x, piece.grid_pos_y, change_mana=False, bypass_mana=True, update_variables=True)
            piece.image = Piece.smoothscale_images(piece.original_image)

    @ staticmethod
    def smoothscale_images(image_to_scale):
        # print(image_to_scale)
        return pygame.transform.smoothscale(image_to_scale, (Piece.pieces_dimension, Piece.pieces_dimension))


class Mage(Piece):

    def __init__(self, x, y, team, hp, mana, agility, defense, damage, specify_id=None, pos_mode="grid"):

        super().__init__(x, y, team, hp, mana, agility, defense, damage, specify_id, pos_mode)

        self.specie = "mage"

        Mage.loadimages()

        if (team == "blue"):
            self.original_image = Mage.blue_mage_original_image
            self.image = Mage.blue_mage_image

        else:
            self.original_image = Mage.red_mage_original_image
            self.image = Mage.red_mage_image

    def loadimages():
        Mage.red_mage_original_image = Media.convert(pygame.image.load("resources\\images\\red_mage.png"), "alpha")
        Mage.red_mage_image = Piece.smoothscale_images(Mage.red_mage_original_image)
        Mage.blue_mage_original_image = Media.convert(pygame.image.load("resources\\images\\blue_mage.png"), "alpha")
        Mage.blue_mage_image = Piece.smoothscale_images(Mage.blue_mage_original_image)


class Archer(Piece):

    def __init__(self, x, y, team, hp, mana, agility, defense, damage, specify_id=None, pos_mode="grid"):
        super().__init__(x, y, team, hp, mana, agility, defense, damage, specify_id, pos_mode)

        self.specie = "archer"

        Archer.loadimages()

        if (team == "blue"):
            self.original_image = Archer.blue_archer_original_image
            self.image = Archer.blue_archer_image

        else:
            self.original_image = Archer.red_archer_original_image
            self.image = Archer.red_archer_image

    def loadimages():
        Archer.red_archer_original_image = Media.convert(pygame.image.load("resources\\images\\red_archer.png"), "alpha")
        Archer.red_archer_image = Piece.smoothscale_images(Archer.red_archer_original_image)
        Archer.blue_archer_original_image = Media.convert(pygame.image.load("resources\\images\\blue_archer.png"), "alpha")
        Archer.blue_archer_image = Piece.smoothscale_images(Archer.blue_archer_original_image)


class Knight(Piece):

    def __init__(self, x, y, team, hp, mana, agility, defense, damage, specify_id=None, pos_mode="grid"):
        super().__init__(x, y, team, hp, mana, agility, defense, damage, specify_id, pos_mode)

        self.specie = "knight"

        Knight.loadimages()

        if (team == "blue"):
            self.original_image = Knight.blue_knight_original_image
            self.image = Knight.blue_knight_image

        else:
            self.original_image = Knight.red_knight_original_image
            self.image = Knight.red_knight_image

    def loadimages():
        Knight.red_knight_original_image = Media.convert(pygame.image.load("resources\\images\\red_knight.png"), "alpha")
        Knight.red_knight_image = Piece.smoothscale_images(Knight.red_knight_original_image)

        Knight.blue_knight_original_image = Media.convert(pygame.image.load("resources\\images\\blue_knight.png"), "alpha")
        Knight.blue_knight_image = Piece.smoothscale_images(Knight.blue_knight_original_image)

        # Knight.blue_knight_bar_image = Media.scale(Knight.blue_knight_original_image, Game.height/20,Game.height/20)


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


class Menu:

    def __init__(self):

        config_menu_alpha_image = Game.convert_img(pygame.image.load("resources\\images\\menu\\config_menu.png"), "alpha")
        Menu.config_menu_alpha_image = pygame.transform.smoothscale(config_menu_alpha_image, (Game.height / 2, Game.height / 2))

        self.sliders = [
            Slider(UI.config_menu_pos, (250, 20), 0.4, 0, 1)  # ,
            # Slider((UI.center[0], UI.center[1]+75), (300, 40), 0.5, 50, 100),
            # Slider((UI.center[0], UI.center[1]+150), (1000, 20), 0.5, 300, 100)
        ]

    def run(self, show_music):
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        Game.screen.blit(Menu.config_menu_alpha_image, (Game.height/0.8, Game.height / 10))  # displaying its background

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
                        slider.current_value = new_value
                else:
                    slider.hovered = False

                slider.render()
                # slider.display_value(self.app)


class Piece_Selection_Menu:

    already_executed = False

    def __init__(self):

        Piece_Selection_Menu.metrics = {"x": Game.height/0.693, "y": Game.height / 6.83, "w": Game.height / (1.6*2), "h": Game.height / 1.6}
        Piece_Selection_Menu.original_image = pygame.image.load("resources\\images\\menu\\piece_selection_menu.png")
        Piece_Selection_Menu.image = Media.convert(pygame.transform.smoothscale(Piece_Selection_Menu.original_image,
                                                                                (Piece_Selection_Menu.metrics["w"], Piece_Selection_Menu.metrics["h"])), "alpha")

        Piece_Selection_Menu.images_placement = [{"x": Game.height/0.66, "y": Game.height / 3.49},
                                                 {"x": Game.height/0.66, "y": Game.height / 2.7},
                                                 {"x": Game.height/0.66, "y": Game.height / 2.25}]

    @ staticmethod
    def draw(my_team):
        Game.screen.blit(Piece_Selection_Menu.image, (Piece_Selection_Menu.metrics["x"], Piece_Selection_Menu.metrics["y"]))


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
        print("moved")

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


class Lobby:

    def __init__(self):
        pass

    def draw(self):

        Game.screen.blit(Media.sized["lobby_background"], (0, 0))
        Game.screen.blit(Media.sized["lobby_ui"], (Media.metrics["lobby_ui"]["x"], Media.metrics["lobby_ui"]["y"]))
        Game.screen.blit(Media.sized["crear_btn"], (Media.metrics["crear_btn"]["x"], Media.metrics["crear_btn"]["y"]))
        Game.screen.blit(Media.sized["unirse_btn"], (Media.metrics["unirse_btn"]["x"], Media.metrics["unirse_btn"]["y"]))

        Game.screen.blit(Media.sized["x_btn"], (Media.metrics["x_btn"]["x"], Media.metrics["x_btn"]["y"]))  # displaying btns
        Game.screen.blit(Media.sized["shrink_btn"], (Media.metrics["shrink_btn"]["x"], Media.metrics["shrink_btn"]["y"]))
        Game.screen.blit(Media.sized["minimize_btn"], (Media.metrics["minimize_btn"]["x"], Media.metrics["minimize_btn"]["y"]))
        Game.screen.blit(Media.sized["setting_btn"], (Media.metrics["setting_btn"]["x"], Media.metrics["setting_btn"]["y"]))

        # print(Cursor.show_cursor)
        if Cursor.show_cursor:
            Cursor.draw()

        pygame.display.flip()


class Cursor:

    show_cursor = True

    image = None

    def __init__(self):
        Cursor.image = Media.sized["cursor_default"]

    @staticmethod
    def draw():
        Game.screen.blit(Cursor.image, pygame.mouse.get_pos())
