import pygame
import math
import pyautogui


class Measure:

    @staticmethod
    def dev_mouse(screenratio=1):
        height = round(Measure.get_height()/screenratio)  # reduces the height
        print(f"{height / pygame.mouse.get_pos()[0]:.3f}", f"{height / pygame.mouse.get_pos()[1]:.3f}")  # returns the percentaje values based on height

    @staticmethod
    def measure_distance(screenratio=1):
        distance = max(abs(Measure.a[0]-Measure.b[0]), abs(Measure.a[1]-Measure.b[1]))

        height = round(Measure.get_height()/screenratio)  # reduces the height
        print(f"{height / distance:.3f}")

    @staticmethod
    def set_point_a():
        Measure.a = pygame.mouse.get_pos()

    @staticmethod
    def set_point_b():
        Measure.b = pygame.mouse.get_pos()

    def get_height():
        _, screen_height = pygame.display.get_surface().get_size()  # pyautogui.size()
        return screen_height
