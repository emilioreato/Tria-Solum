import os
import math
import numpy
import pygame
import pyautogui
import threading
import wave
import pyaudio
from win32con import ENUM_CURRENT_SETTINGS
from win32api import EnumDisplaySettings


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

    PLAYLIST = [os.path.join("resources\\sounds\\soundtracks", archivo)  # This list contains all the paths that contain "ingame" on their name, aka, soundtrack files for the matches
                for archivo in os.listdir("resources\\sounds\\soundtracks")
                if os.path.isfile(os.path.join("resources\\sounds\\soundtracks", archivo)) and "ingame" in archivo.lower()]

    SFX = [os.path.join("resources\\sounds\\sfx", archivo)  # This list contains all the paths of the sfx files
           for archivo in os.listdir("resources\\sounds\\sfx")]

    def __init__(self):  # init method for evety piece where it gets another ingame values assigned
        pass

    def load_resources(self):

        # global backgrounds, music_button_rect, music_button, cursor_default, close_button, close_button_rect, settings_button, settings_button_rect, minimize_button, minimize_button_rect

        Game.backgrounds = []
        for i in range(0, Game.BACKGROUNDS_AMOUNT):
            bkg_img = pygame.image.load(f"resources\\images\\background{i}.png").convert()  # load some images, converts it for optimization and then scales them.
            bkg_img = pygame.transform.smoothscale(bkg_img, (Game.width, Game.height))
            Game.backgrounds.append(bkg_img)

        cursor_default = pygame.image.load("resources\\icons\\cursor_default.png").convert_alpha()
        Game.cursor_default = pygame.transform.smoothscale(cursor_default, (Game.screen_height * 0.805 // 43, Game.screen_height // 43))

        close_button = pygame.image.load("resources\\icons\\x.png").convert_alpha()
        Game.close_button = pygame.transform.smoothscale(close_button, (Game.height // 24, Game.height // 24))
        Game.close_button_rect = Game.close_button.get_rect()
        Game.close_button_rect.topleft = (Game.height//0.6, Game.height // 25)

        settings_button = pygame.image.load("resources\\icons\\setting.png").convert_alpha()
        Game.settings_button = pygame.transform.smoothscale(settings_button, (Game.height // 24, Game.height // 24))
        Game.settings_button_rect = Game.settings_button.get_rect()
        Game.settings_button_rect.topleft = (Game.height//0.62, Game.height // 25)

        minimize_button = pygame.image.load("resources\\icons\\minimize.png").convert_alpha()
        Game.minimize_button = pygame.transform.smoothscale(minimize_button, (Game.height // 24, Game.height // 24))
        Game.minimize_button_rect = Game.minimize_button.get_rect()
        Game.minimize_button_rect.topleft = (Game.height//0.64, Game.height // 25)

        music_button = pygame.image.load("resources\\icons\\music.png").convert_alpha()
        Game.music_button = pygame.transform.smoothscale(music_button, (Game.height // 24, Game.height // 24))
        Game.music_button_rect = Game.music_button.get_rect()
        Game.music_button_rect.topleft = (Game.height//0.66, Game.height // 25)

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

        pygame.display.set_icon(pygame.image.load("resources\\images\\indicator.png").convert_alpha())  # sets window icon

        Game.timer = pygame.time.Clock()  # create a clock object to set fps
        Game.dev_mode = EnumDisplaySettings(None, ENUM_CURRENT_SETTINGS)  # get the OS's fps setting


class Sound:

    file = None

    def __init__(self):
        pass

    @staticmethod
    def play():
        wf = wave.open(Sound.file, 'rb')  # open audio file
        p = pyaudio.PyAudio()  # inicialize pyaudio
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),  # open audio stream
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(1024)  # read and play audio data
        while data:
            stream.write(data)
            data = wf.readframes(1024)
        stream.stop_stream()  # stop the stream
        stream.close()
        p.terminate()  # finish pyaudio

    @staticmethod
    def play_on_thread(file):
        # Ejecutar la reproducción del sonido en un hilo para no bloquear el programa
        Sound.file = file
        threading.Thread(target=Sound.play).start()


class Piece:

    init_hp = 100  # define some default values for ingame variables
    init_mana = 11
    init_agility = 100
    init_defense = 100
    init_damage = 100

    pieces_dimension = 0

    def __init__(self, x, y):  # init method for evety piece where it gets another ingame values assigned
        self.grid_pos_x = x
        self.grid_pos_y = y
        self.pos_x = 0
        self.pos_y = 0
        Piece.grid_pos_to_pixels(self, x, y, bypass_mana=True, change_mana=False)

        self.hp = Piece.init_hp
        self.mana = Piece.init_mana
        self.agility = Piece.init_agility
        self.defense = Piece.init_defense
        self.damage = Piece.init_damage

        self.image = 0
        self.original_image = 0

    @classmethod
    def set_dimension(cls, mult=1, screenratio=1):
        # if Piece.pieces_dimension 0:
        # _, screen_height = pyautogui.size()  # gets the current resolution
        # height = round(screen_height/screenratio)  # reduces the height
        cls.pieces_dimension = round((Game.height // 14) / mult)
        print(cls.pieces_dimension)

    @staticmethod
    def b64index_to_grid(index):  # it return the conversion from a 1d array index to a 2d array index (used to convert points_list index to the board/grid index)
        return index % Game.board_size, index // Game.board_size

    @staticmethod
    def grid_to_b64index(x, y):  # it returns the opposite conversion of b64index_to_grid. given 2d array coordinates it converts them to a 1d array coordinate
        return y*Game.board_size + x

    def grid_pos_to_pixels(self, grid_x, grid_y, change_mana=False, bypass_mana=False, update_variables=True):  # this function

        # print(self.get_amount_of_grid_move(old_x, old_y, limited_x, limited_y))

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

    @staticmethod
    def detect_closest_point(mouse_pos):  # AKA transform pixels position to grid placement (opposite of grid_pos_to_pixels())
        lowest = 10000
        for point in Game.center_points:  # iterate every point
            # calculate the length of the vector formed between the point and the mouse position (the distance between where the user dropped the piece and the current point)
            distance = math.sqrt((mouse_pos[0]-point[0])**2 + (mouse_pos[1]-point[1])**2)

            if distance < lowest:  # if the distance is lower than all the others measured, save it as the lowest
                lowest = distance
                selected_point = point

        return Game.center_points.index(selected_point)  # return the position(index) in the points array of the closest point

    @staticmethod
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

    @staticmethod
    def is_clicked(mouse_pos, pos):
        distancia = ((pos[0] - mouse_pos[0]) ** 2 + (pos[1] - mouse_pos[1]) ** 2) ** 0.5  # Calcular la distancia entre el cli
        return distancia <= Piece.pieces_dimension//2  # Devuelve True si el clic está dentro del círculo

    def resize(self, active_pieces):
        for piece in active_pieces:
            piece.grid_pos_to_pixels(piece.grid_pos_x, piece.grid_pos_y, change_mana=False, bypass_mana=True, update_variables=True)
            piece.image = Piece.smoothscale_images(piece.original_image)

    def smoothscale_images(image_to_scale):
        print(image_to_scale)
        return pygame.transform.smoothscale(image_to_scale, (Piece.pieces_dimension, Piece.pieces_dimension))


class Mage(Piece):

    red_mage_image = pygame.image.load("resources\\images\\red_mage.png")  # .convert()
    blue_mage_image = pygame.image.load("resources\\images\\blue_mage.png")  # .convert()

    def __init__(self, x, y, mana, team):
        super().__init__(x, y)
        self.mana = mana

        Mage.loadimages()

        if (team == "blue"):
            self.original_image = Mage.blue_mage_image
            # print(self.original_image)
            self.image = Piece.smoothscale_images(self.original_image)

        else:
            self.original_image = Mage.red_mage_image
            self.image = Piece.smoothscale_images(self.original_image)

    def loadimages():
        Mage.red_mage_image = pygame.image.load("resources\\images\\red_mage.png")  # .convert()
        Mage.blue_mage_image = pygame.image.load("resources\\images\\blue_mage.png")  # .convert()


class Archer(Piece):

    red_archer_image = pygame.image.load("resources\\images\\red_archer.png")  # .convert()
    blue_archer_image = pygame.image.load("resources\\images\\blue_archer.png")  # .convert()

    def __init__(self, x, y, mana, team):
        super().__init__(x, y)
        self.mana = mana

        Archer.loadimages()

        if (team == "blue"):
            self.original_image = Archer.blue_archer_image
            # print(self.original_image)
            self.image = Piece.smoothscale_images(self.original_image)

        else:
            self.original_image = Archer.red_archer_image
            self.image = Piece.smoothscale_images(self.original_image)

    def loadimages():
        Archer.red_archer_image = pygame.image.load("resources\\images\\red_archer.png")  # .convert()
        Archer.blue_archer_image = pygame.image.load("resources\\images\\blue_archer.png")  # .convert()


class Knight(Piece):

    red_knight_image = pygame.image.load("resources\\images\\red_knight.png")  # .convert()
    blue_knight_image = pygame.image.load("resources\\images\\blue_knight.png")  # .convert()

    def __init__(self, x, y, mana, team):
        super().__init__(x, y)
        self.mana = mana

        Knight.loadimages()

        if (team == "blue"):
            self.original_image = Knight.blue_knight_image
            # print(self.original_image)
            self.image = Piece.smoothscale_images(self.original_image)

        else:
            self.original_image = Knight.red_knight_image
            self.image = Piece.smoothscale_images(self.original_image)

    def loadimages():
        Knight.red_knight_image = pygame.image.load("resources\\images\\red_knight.png")  # .convert()
        Knight.blue_knight_image = pygame.image.load("resources\\images\\blue_knight.png")  # .convert()
