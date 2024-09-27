import pygame


class Piece:

    hp = 100
    mana = 100
    agility = 100
    defense = 100
    damage = 100

    def __init__(self, x, y, rad):
        self.pos_x = x
        self.pos_y = y
        self.rad = rad

    def mover(self, move_x, move_y):
        self.pos_x += move_x
        self.pos_y += move_y

    def dibujar(self, screen, color, pos):
        pygame.draw.circle(screen, color, pos, self.rad)

    def is_clicked(self, mouse_pos, pos):
        distancia = ((mouse_pos[0] - pos[0]) ** 2 + (mouse_pos[1] - pos[1]) ** 2) ** 0.5  # Calcular la distancia entre el clic y el centro del círculo
        return distancia <= self.rad  # Devuelve True si el clic está dentro del círculo

    # def get_center(self):
