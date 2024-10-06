import pygame
import math
import pyautogui
def dev_mouse():
    width = pyautogui.size()[0]
    height = pyautogui.size()[1]
    pos = (width / pygame.mouse.get_pos()[0] , (height / pygame.mouse.get_pos()[1]))
    pos_x , pos_y = pos
    debbug_pos_x = math.trunc(pos_x * 1000) / 1000
    debbug_pos_y = math.trunc(pos_y * 1000) / 1000
    debbug_pos = (debbug_pos_x , debbug_pos_y)
    print (f"dev_mouse: {debbug_pos}")
    
