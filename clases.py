import pygame
import os
import pyautogui
import math
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets the current directory to the file's directory


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

    def mover(self, move_x, move_y, change_mana):
        self.pos_x += move_x
        self.pos_y += move_y
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

    # def get_center(self,image):

    @staticmethod
    def is_clicked(mouse_pos, pos):

        distancia = ((pos[0] - mouse_pos[0]) ** 2 + (pos[1] - mouse_pos[1]) ** 2) ** 0.5  # Calcular la distancia entre el cli
        return distancia <= Piece.pieces_dimension//2  # Devuelve True si el clic está dentro del círculo

    def detect_closest_point(self, points_list, mouse_pos):  # AKA transform pixels position to grid placement
        lowest = 10000
        for point in points_list:
            distance = math.sqrt((mouse_pos[0]-point[0])**2 + (mouse_pos[1]-point[1])**2)

            if distance < lowest:
                lowest = distance
                selected_point = point

        return points_list.index(selected_point)


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
