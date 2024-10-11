import pygame


class Media:

    BACKGROUNDS_AMOUNT = 7

    def __init__(self):
        pass

    def load_media(height):

        Media.bare_backgrounds = []
        for i in range(0, Media.BACKGROUNDS_AMOUNT):
            Media.bare_backgrounds.append(pygame.image.load(f"resources\\images\\background{i}.png"))  # load some images, converts it for optimization and then scales them.

        Media.bare_imgs = {
            "cursor_default": pygame.image.load("resources\\icons\\cursor_default.png").convert_alpha(),
            "cursor_hand": pygame.image.load("resources\\icons\\cursor_hand.png").convert_alpha(),
            "x_btn": pygame.image.load("resources\\icons\\x.png").convert_alpha(),
            "shrink_btn": pygame.image.load("resources\\icons\\shrink.png").convert_alpha(),
            "minimize_btn": pygame.image.load("resources\\icons\\minimize.png").convert_alpha(),
            "setting_btn": pygame.image.load("resources\\icons\\setting.png").convert_alpha(),
            "music_btn": pygame.image.load("resources\\icons\\music.png").convert_alpha(),

            "lobby_background": pygame.image.load("resources\\images\\pure_background.png").convert(),
            "lobby_ui": pygame.image.load("resources\\images\\menu\\lobby_ui.png").convert(),
            "crear_btn": pygame.image.load("resources\\images\\menu\\crear.png").convert(),
            "unirse_btn": pygame.image.load("resources\\images\\menu\\unirse.png").convert(),
        }

        Media.resize_metrics(height)

    def resize_metrics(height):
        width = height*(16/9)

        Media.metrics = {  # DONT MAKE A KEY "MAKE_RECT" TRUE BECAUSE IT WONT MATTER, IT WONT MAKE THE RECTANGLE ANYWAY. later in the code the rectangles are created when in the keys there is the keyword "make_rect" so if you dont want the rect, just doesnt even speficy it
            "cursor_default": {"w": 30 * 0.805, "h": 30, "make_rect": False},
            "cursor_hand": {"w": 30 * 0.805, "h": 30, "make_rect": False},
            "x_btn": {"x": height//0.58, "y": height // 40, "w": height // 24, "h": height // 24, "use_rect_in": "all"},
            "shrink_btn": {"x": height//0.6, "y": height // 40, "w": height // 24, "h": height // 24, "use_rect_in": "all"},
            "minimize_btn": {"x": height//0.62, "y": height // 40, "w": height // 24, "h": height // 24, "use_rect_in": "all"},
            "setting_btn": {"x": height//0.64, "y": height // 40, "w": height // 24, "h": height // 24, "use_rect_in": "ingame"},
            "music_btn": {"x": height/0.78, "y": height / 8, "w": height / 28, "h": height / 28, "use_rect_in": "settings"},

            "lobby_background": {"x": 0, "y":  0, "w": width+1, "h": height, "make_rect": False},
            "lobby_ui": {"x": width/2 - ((height*(1920/1160))/1.4)/2, "y":  height/6, "w": (height*(1920/1160))/1.4, "h": height/1.4, "make_rect": False},
            "crear_btn": {"x": width/2-((height*(1280/240))/20)/2, "y":  height/2.6, "w": (height*(1280/240))/20, "h": height/20, "use_rect_in": "lobby"},
            "unirse_btn": {"x": width/2-((height*(1280/243))/20)/2, "y":  height/2.3, "w": (height*(1280/243))/20, "h": height/20, "use_rect_in": "lobby"},
        }

    def resize(height):

        Media.sized = {}
        for key in Media.bare_imgs.keys():
            Media.sized.update({key: Media.scale(Media.bare_imgs[key], Media.metrics[key]["w"], Media.metrics[key]["h"])})

        Media.rects = {}
        for key in Media.bare_imgs.keys():
            if not "make_rect" in Media.metrics[key].keys():
                Media.rects.update({key: {"rect": Media.sized[key].get_rect(), "use_rect_in": Media.metrics[key]["use_rect_in"]}})
                Media.rects[key]["rect"].topleft = (Media.metrics[key]["x"], Media.metrics[key]["y"])  # if "x" in Media.metrics[key].keys() else (0, 0)

        Media.backgrounds = []
        for bkg in Media.bare_backgrounds:
            Media.backgrounds.append(pygame.transform.smoothscale(bkg, (round(height*(16/9)), height)))

    @staticmethod
    def convert(image, mode="default"):  # a function used to convert the images to the pygame format. you can choose between normal or alpha mode
        if mode == "alpha":
            return image.convert_alpha()
        return image.convert()

    @staticmethod
    def scale(image, size_x, size_y):
        return pygame.transform.smoothscale(image, (size_x, size_y))


"""
    Media.rects_list = (Media.x_btn_rect,
                            Media.music_btn_rect,
                            Media.shrink_btn_rect,
                            Media.minimize_btn_rect,
                            Media.settings_btn_rect
                            )
"""
