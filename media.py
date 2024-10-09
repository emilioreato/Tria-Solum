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

            "lobby_background": pygame.image.load("resources\\images\\menu\\lobby.png").convert_alpha(),
        }

        Media.resize_metrics(height)

    def resize_metrics(height):

        Media.metrics = {  # DONT MAKE A KEY "MAKE_RECT" TRUE BECAUSE IT WONT MATTER, IT WONT MAKE THE RECTANGLE ANYWAY. later in the code the rectangles are created when in the keys there is the keyword "make_rect" so if you dont want the rect, just doesnt even speficy it
            "cursor_default": {"w": height * 0.805 // 43, "h": height // 43, "make_rect": False},
            "cursor_hand": {"w": height * 0.805 // 43, "h": height // 43, "make_rect": False},
            "x_btn": {"x": height//0.58, "y": height // 40, "w": height // 24, "h": height // 24},
            "shrink_btn": {"x": height//0.6, "y": height // 40, "w": height // 24, "h": height // 24},
            "minimize_btn": {"x": height//0.62, "y": height // 40, "w": height // 24, "h": height // 24},
            "setting_btn": {"x": height//0.64, "y": height // 40, "w": height // 24, "h": height // 24},
            "music_btn": {"x": height/0.78, "y": height / 8, "w": height / 28, "h": height / 28},

            "lobby_background": {"x": height / 2 - (height / 2.4)*(16/9), "y":  height / 2 - (height / 2.4), "w": (height / 1.2)*(16/9), "h": height / 1.2, "make_rect": False},
        }

    def resize(height):

        Media.sized = {}
        for key in Media.bare_imgs.keys():
            Media.sized.update({key: Media.scale(Media.bare_imgs[key], Media.metrics[key]["w"], Media.metrics[key]["h"])})

        Media.rects = {}
        for key in Media.bare_imgs.keys():
            if not "make_rect" in Media.metrics[key].keys():
                Media.rects.update({key: Media.sized[key].get_rect()})
                Media.rects[key].topleft = (Media.metrics[key]["x"], Media.metrics[key]["y"])  # if "x" in Media.metrics[key].keys() else (0, 0)

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
