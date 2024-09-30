import pygame
import os
import pyautogui
import math
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # sets the current directory to the file's directory


class Piece:

    init_hp = 100
    init_mana = 100
    init_agility = 100
    init_defense = 100
    init_damage = 100

    pieces_dimension = 0

    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        # self.rad = rad
        """global init_hp, init_mana, init_agility, init_defense, init_damage
        self.hp = init_hp
        self.mana = init_mana
        self.agility = init_agility
        self.defense = init_defense
        self.damage = init_damage"""
        Mage.set_dimension()

    def set_dimension(mult=1, screenratio=1):
        if Piece.pieces_dimension is 0:
            _, screen_height = pyautogui.size()  # gets the current resolution
            height = round(screen_height/screenratio)  # reduces the height
            Piece.pieces_dimension = round((height // 14) / mult)

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

    def is_clicked(self, mouse_pos, pos):

        distancia = ((pos[0] - mouse_pos[0]) ** 2 + (pos[1] - mouse_pos[1]) ** 2) ** 0.5  # Calcular la distancia entre el cli
        return distancia <= Piece.pieces_dimension//2  # Devuelve True si el clic está dentro del círculo

    def detect_closest_point(self, points_list, mouse_pos):
        lowest = 100000
        for point in points_list:
            distance = math.sqrt((mouse_pos[0]-point[0])**2 + (mouse_pos[1]-point[1])**2)

            if distance < lowest:
                lowest = distance
                selected_point = point

        return points_list.index(selected_point)


class Mage(Piece):

    red_mage_image = pygame.image.load("resources\\red_mage.png")  # .convert()
    blue_mage_image = pygame.image.load("resources\\blue_mage.png")  # .convert()

    def __init__(self, x, y, mana):
        super().__init__(x, y)
        self.mana = mana

        Mage.red_mage_image = pygame.transform.smoothscale(Mage.red_mage_image, (Piece.pieces_dimension, Piece.pieces_dimension))
        Mage.blue_mage_image = pygame.transform.smoothscale(Mage.blue_mage_image, (Piece.pieces_dimension, Piece.pieces_dimension))
