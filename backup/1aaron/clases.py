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
import random


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

    def load_resources(self):

        # global backgrounds, music_btn_rect, music_btn, cursor_default, close_btn, close_btn_rect, settings_btn, settings_btn_rect, minimize_btn, minimize_btn_rect

        Game.backgrounds = []
        for i in range(0, Game.BACKGROUNDS_AMOUNT):
            bkg_img = pygame.image.load(f"resources\\images\\background{i}.png").convert()  # load some images, converts it for optimization and then scales them.
            bkg_img = pygame.transform.smoothscale(bkg_img, (Game.width, Game.height))
            Game.backgrounds.append(bkg_img)

        cursor_default = pygame.image.load("resources\\icons\\cursor_default.png").convert_alpha()
        Game.cursor_default = pygame.transform.smoothscale(cursor_default, (Game.screen_height * 0.805 // 43, Game.screen_height // 43))
        cursor_hand = pygame.image.load("resources\\icons\\cursor_hand.png").convert_alpha()
        Game.cursor_hand = pygame.transform.smoothscale(cursor_hand, (Game.screen_height * 0.805 // 43, Game.screen_height // 43))

        Game.x_btn_metrics = {"x": Game.height//0.58, "y": Game.height // 40, "w": Game.height // 24, "h": Game.height // 24}
        x_btn = pygame.image.load("resources\\icons\\x.png").convert_alpha()
        Game.x_btn = pygame.transform.smoothscale(x_btn, (Game.x_btn_metrics["w"], Game.x_btn_metrics["h"]))
        Game.x_btn_rect = Game.x_btn.get_rect()
        Game.x_btn_rect.topleft = (Game.x_btn_metrics["x"], Game.x_btn_metrics["y"])

        Game.shrink_btn_metrics = {"x": Game.height//0.6, "y": Game.height // 40, "w": Game.height // 24, "h": Game.height // 24}
        shrink_btn = pygame.image.load("resources\\icons\\shrink.png").convert_alpha()
        Game.shrink_btn = pygame.transform.smoothscale(shrink_btn, (Game.shrink_btn_metrics["w"], Game.shrink_btn_metrics["h"]))
        Game.shrink_btn_rect = Game.shrink_btn.get_rect()
        Game.shrink_btn_rect.topleft = (Game.shrink_btn_metrics["x"], Game.shrink_btn_metrics["y"])

        Game.minimize_btn_metrics = {"x": Game.height//0.62, "y": Game.height // 40, "w": Game.height // 24, "h": Game.height // 24}
        minimize_btn = pygame.image.load("resources\\icons\\minimize.png").convert_alpha()
        Game.minimize_btn = pygame.transform.smoothscale(minimize_btn, (Game.minimize_btn_metrics["w"], Game.minimize_btn_metrics["h"]))
        Game.minimize_btn_rect = Game.minimize_btn.get_rect()
        Game.minimize_btn_rect.topleft = (Game.minimize_btn_metrics["x"], Game.minimize_btn_metrics["y"])

        Game.settings_btn_metrics = {"x": Game.height//0.655, "y": Game.height // 40, "w": Game.height // 24, "h": Game.height // 24}
        settings_btn = pygame.image.load("resources\\icons\\setting.png").convert_alpha()
        Game.settings_btn = pygame.transform.smoothscale(settings_btn, (Game.settings_btn_metrics["w"], Game.settings_btn_metrics["h"]))
        Game.settings_btn_rect = Game.settings_btn.get_rect()
        Game.settings_btn_rect.topleft = (Game.settings_btn_metrics["x"], Game.settings_btn_metrics["y"])

        Game.music_btn_metrics = {"x": Game.height/0.78, "y": Game.height // 8, "w": Game.height // 28, "h": Game.height // 28}  # x coordinate, y coordinate, width measure, height measure
        music_btn = pygame.image.load("resources\\icons\\music.png").convert_alpha()
        Game.music_btn = pygame.transform.smoothscale(music_btn, (Game.music_btn_metrics["w"], Game.music_btn_metrics["h"]))
        Game.music_btn_rect = Game.music_btn.get_rect()
        Game.music_btn_rect.topleft = (Game.music_btn_metrics["x"], Game.music_btn_metrics["y"])

        Game.rects_list = (Game.x_btn_rect,
                           Game.music_btn_rect,
                           Game.shrink_btn_rect,
                           Game.minimize_btn_rect,
                           Game.settings_btn_rect
                           )

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

    def convert_img(image, mode="default"):  # a function used to convert the images to the pygame format. you can choose between normal or alpha mode
        if mode == "alpha":
            return image.convert_alpha()
        return image.convert()


class Sound:

    SFX = [os.path.join("resources\\sounds\\sfx", archivo)  # This list contains all the paths of the sfx files
           for archivo in os.listdir("resources\\sounds\\sfx")]

    PLAYLIST = [os.path.join("resources\\sounds\\soundtracks", archivo)  # This list contains all the paths that contain "ingame" on their name, aka, soundtrack files for the matches
                for archivo in os.listdir("resources\\sounds\\soundtracks")
                if os.path.isfile(os.path.join("resources\\sounds\\soundtracks", archivo)) and "ingame" in archivo.lower()]

    generated_tracks = []

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
    def play_on_thread(file):  # execute the playing of the sound in a thread so the main program doesnt get blocked
        Sound.file = file
        threading.Thread(target=Sound.play).start()

    @staticmethod
    def play_song(playlist):  # a function that plays a random song from the playlist with no repetitions for iterations_without_repeating calls
        # playlist = copy.deepcopy(t)

        filtered_playlist = [song for song in playlist if song not in Sound.generated_tracks]  # selec a random song from playlist that has not been selected yet

        track = random.choice(filtered_playlist)

        if track in Sound.generated_tracks:
            print("not working")

        Sound.generated_tracks.append(track)

        pygame.mixer.music.load(track)  # loads the track
        pygame.mixer.music.play()  # plays the track

        if len(Sound.generated_tracks) > (len(playlist)-5):
            Sound.generated_tracks.pop(0)


class Piece:

    init_hp = 100  # define some default values for ingame variables
    init_mana = 11
    init_agility = 100
    init_defense = 100
    init_damage = 100

    pieces_dimension = 0

    def __init__(self, x, y, team):  # init method for evety piece where it gets another ingame values assigned
        self.team = team
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

    def check_for_pieces_in_the_grid_coordinates(self, active_pieces, x, y):
        for piece in active_pieces:
            if (piece.grid_pos_x == x and piece.grid_pos_y == y):
                return True
        return False

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
        # print(image_to_scale)
        return pygame.transform.smoothscale(image_to_scale, (Piece.pieces_dimension, Piece.pieces_dimension))


class Mage(Piece):

    def __init__(self, x, y, mana, team):
        super().__init__(x, y, team)
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
        Mage.red_mage_image = Game.convert_img(pygame.image.load("resources\\images\\red_mage.png"), "alpha")
        Mage.blue_mage_image = Game.convert_img(pygame.image.load("resources\\images\\blue_mage.png"), "alpha")


class Archer(Piece):

    def __init__(self, x, y, mana, team):
        super().__init__(x, y, team)
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
        Archer.red_archer_image = Game.convert_img(pygame.image.load("resources\\images\\red_archer.png"), "alpha")
        Archer.blue_archer_image = Game.convert_img(pygame.image.load("resources\\images\\blue_archer.png"), "alpha")


class Knight(Piece):

    def __init__(self, x, y, mana, team):
        super().__init__(x, y, team)
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
        Knight.red_knight_image = Game.convert_img(pygame.image.load("resources\\images\\red_knight.png"), "alpha")
        Knight.blue_knight_image = Game.convert_img(pygame.image.load("resources\\images\\blue_knight.png"), "alpha")


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
            Game.screen.blit(Game.music_btn, (Game.music_btn_metrics["x"], Game.music_btn_metrics["y"]))
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
