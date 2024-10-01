import pygame
import os
import pyautogui
import math
import numpy
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

    PLAYLIST = [
        "resources\\sounds\\soundtracks\\track1 (gerilim).mp3",
        "resources\\sounds\\soundtracks\\track2 (saver dontrikh).mp3",
        "resources\\sounds\\soundtracks\\track3 (vioglt dontrikh).mp3"
    ]
    SFX = [
        "resources\\sounds\\soundtracks\\track1 (gerilim).mp3",
        "resources\\sounds\\soundtracks\\track2 (saver dontrikh).mp3",
        "resources\\sounds\\soundtracks\\track3 (vioglt dontrikh).mp3"
    ]

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

        pygame.display.set_icon(pygame.image.load("resources\\images\\indicator.png").convert_alpha())  # sets window icon

        Game.timer = pygame.time.Clock()  # create a clock object to set fps
        Game.dev_mode = EnumDisplaySettings(None, ENUM_CURRENT_SETTINGS)  # get the OS's fps setting


class Piece:

    init_hp = 100  # define some default values for ingame variables
    init_mana = 100
    init_agility = 100
    init_defense = 100
    init_damage = 100

    pieces_dimension = 0

    def __init__(self, x, y):  # init method for evety piece where it gets another ingame values assigned
        self.pos_x = x
        self.pos_y = y
        self.grid_pos_x = 0
        self.grid_pos_y = 0

        self.hp = Piece.init_hp
        self.mana = Piece.init_mana
        self.agility = Piece.init_agility
        self.defense = Piece.init_defense
        self.damage = Piece.init_damage

        self.image = 0

        Piece.set_dimension()

    @classmethod
    def set_dimension(cls, mult=1, screenratio=1):
        # if Piece.pieces_dimension 0:
        _, screen_height = pyautogui.size()  # gets the current resolution
        height = round(screen_height/screenratio)  # reduces the height
        Piece.pieces_dimension = round((height // 14) / mult)
        print(Piece.pieces_dimension)

    @staticmethod
    def b64index_to_grid(index):
        return index // 8, index % 8

    @staticmethod
    def grid_to_b64index(x, y):
        return y*8 + x

    def grid_pos_to_pixels(self, grid_x, grid_y):

        point_x, point_y = Game.center_points[Piece.grid_to_b64index(grid_x, grid_y)]
        self.grid_pos_x = grid_x
        self.grid_pos_y = grid_y

        self.pos_x = point_x
        self.pos_y = point_y

    def mover(self, move_x, move_y, change_mana):
        index_x = self.grid_pos_x + move_x
        index_y = self.grid_pos_y + move_y

        self.grid_pos_to_pixels(index_x, index_y)

        if change_mana:
            if self.mana > 0:
                self.mana -= 1

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

    def detect_closest_point(self, mouse_pos):  # AKA transform pixels position to grid placement
        lowest = 10000
        for point in Game.center_points:
            distance = math.sqrt((mouse_pos[0]-point[0])**2 + (mouse_pos[1]-point[1])**2)

            if distance < lowest:
                lowest = distance
                selected_point = point

        return Game.center_points.index(selected_point)


class Mage(Piece):

    red_mage_image = pygame.image.load("resources\\images\\red_mage.png")  # .convert()
    blue_mage_image = pygame.image.load("resources\\images\\blue_mage.png")  # .convert()

    def __init__(self, x, y, mana, team):
        super().__init__(x, y)
        self.mana = mana

        Mage.red_mage_image = pygame.transform.smoothscale(Mage.red_mage_image, (Piece.pieces_dimension, Piece.pieces_dimension))
        Mage.blue_mage_image = pygame.transform.smoothscale(Mage.blue_mage_image, (Piece.pieces_dimension, Piece.pieces_dimension))

        if (team == "blue"):
            self.image = Mage.blue_mage_image
        else:
            self.image = Mage.red_mage_image


class Archer(Piece):

    red_archer_image = pygame.image.load("resources\\images\\red_archer.png")  # .convert()
    blue_archer_image = pygame.image.load("resources\\images\\blue_archer.png")  # .convert()

    def __init__(self, x, y, mana, team):
        super().__init__(x, y)
        self.mana = mana

        Archer.red_archer_image = pygame.transform.smoothscale(Archer.red_archer_image, (Piece.pieces_dimension, Piece.pieces_dimension))
        Archer.blue_archer_image = pygame.transform.smoothscale(Archer.blue_archer_image, (Piece.pieces_dimension, Piece.pieces_dimension))

        if (team == "blue"):
            self.image = Archer.blue_archer_image
        else:
            self.image = Archer.red_archer_image


class Knight(Piece):

    red_knight_image = pygame.image.load("resources\\images\\red_knight.png")  # .convert()
    blue_knight_image = pygame.image.load("resources\\images\\blue_knight.png")  # .convert()

    def __init__(self, x, y, mana, team):
        super().__init__(x, y)
        self.mana = mana

        Knight.red_knight_image = pygame.transform.smoothscale(Knight.red_knight_image, (Piece.pieces_dimension, Piece.pieces_dimension))
        Knight.blue_knight_image = pygame.transform.smoothscale(Knight.blue_knight_image, (Piece.pieces_dimension, Piece.pieces_dimension))

        if (team == "blue"):
            self.image = Knight.blue_knight_image
        else:
            self.image = Knight.red_knight_image
