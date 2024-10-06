import pygame
import math
import pyautogui


def dev_mouse(screenratio=1):
    _, screen_height = pyautogui.size()  # gets the current resolution
    height = round(screen_height/screenratio)  # reduces the height
    print(f"{height / pygame.mouse.get_pos()[0]:.3f}", f"{height / pygame.mouse.get_pos()[1]:.3f}")  # returns the percentaje values based on height
