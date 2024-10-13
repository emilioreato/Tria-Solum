import pygame


class Media:

    BACKGROUNDS_AMOUNT = 7

    pieces_size = None

    def __init__(self):
        pass

    def load_media(height):

        Media.bare_backgrounds = []
        for i in range(0, Media.BACKGROUNDS_AMOUNT):
            Media.bare_backgrounds.append(pygame.image.load(f"resources\\images\\background{i}.png"))  # load some images, converts it for optimization and then scales them.

        Media.bare_imgs = {
            "red_mage": pygame.image.load("resources\\images\\red_mage.png").convert_alpha(),
            "blue_mage": pygame.image.load("resources\\images\\blue_mage.png").convert_alpha(),
            "red_archer": pygame.image.load("resources\\images\\red_archer.png").convert_alpha(),
            "blue_archer": pygame.image.load("resources\\images\\blue_archer.png").convert_alpha(),
            "red_knight": pygame.image.load("resources\\images\\red_knight.png").convert_alpha(),
            "blue_knight": pygame.image.load("resources\\images\\blue_knight.png").convert_alpha(),

            "cursor_default": pygame.image.load("resources\\icons\\cursor_default.png").convert_alpha(),
            "cursor_hand": pygame.image.load("resources\\icons\\cursor_hand.png").convert_alpha(),
            "x_btn": pygame.image.load("resources\\icons\\x.png").convert_alpha(),
            "shrink_btn": pygame.image.load("resources\\icons\\shrink.png").convert_alpha(),
            "minimize_btn": pygame.image.load("resources\\icons\\minimize.png").convert_alpha(),
            "setting_btn": pygame.image.load("resources\\icons\\setting.png").convert_alpha(),
            "music_btn": pygame.image.load("resources\\icons\\music.png").convert_alpha(),
            "copy_btn": pygame.image.load("resources\\images\\menu\\paperclip_copy.png").convert_alpha(),

            "team_bar": pygame.image.load("resources\\images\menu\\my_team_bar.png").convert_alpha(),

            "clk_0": pygame.image.load("resources\\icons\\clock\\0.png").convert_alpha(),
            "clk_1": pygame.image.load("resources\\icons\\clock\\1.png").convert_alpha(),
            "clk_2": pygame.image.load("resources\\icons\\clock\\2.png").convert_alpha(),
            "clk_3": pygame.image.load("resources\\icons\\clock\\3.png").convert_alpha(),
            "clk_4": pygame.image.load("resources\\icons\\clock\\4.png").convert_alpha(),

            "piece_selection_ui": pygame.image.load("resources\\images\\menu\\piece_selection_menu.png").convert(),
            "support_ui": pygame.image.load("resources\\images\\menu\\support_ui.png").convert(),
            "lobby_ui": pygame.image.load("resources\\images\\menu\\lobby_ui.png").convert(),

            "lobby_background": pygame.image.load("resources\\images\\pure_background.png").convert(),

            "volver_btn": pygame.image.load("resources\\images\\menu\\volver.png").convert(),
            "crear_btn": pygame.image.load("resources\\images\\menu\\crear.png").convert(),
            "unirse_btn": pygame.image.load("resources\\images\\menu\\unirse.png").convert(),
            "generar_btn": pygame.image.load("resources\\images\\menu\\generar_clave_de_partida.png").convert(),
            "ingresar_btn": pygame.image.load("resources\\images\\menu\\ingresar.png").convert(),
        }

        Media.resize_metrics(height)

    def resize_metrics(height):
        width = height*(16/9)

        Media.pieces_size = height/14

        Media.metrics = {  # DONT MAKE A KEY "MAKE_RECT" TRUE BECAUSE IT WONT MATTER, IT WONT MAKE THE RECTANGLE ANYWAY. later in the code the rectangles are created when in the keys there is the keyword "make_rect" so if you dont want the rect, just doesnt even speficy it
            "red_mage": {"x": 0, "y": 0, "w": Media.pieces_size, "h": Media.pieces_size, "make_rect": False},
            "blue_mage": {"x": 0, "y": 0, "w": Media.pieces_size, "h": Media.pieces_size, "make_rect": False},
            "red_archer": {"x": 0, "y": 0, "w": Media.pieces_size, "h": Media.pieces_size, "make_rect": False},
            "blue_archer": {"x": 0, "y": 0, "w": Media.pieces_size, "h": Media.pieces_size, "make_rect": False},
            "red_knight": {"x": 0, "y": 0, "w": Media.pieces_size, "h": Media.pieces_size, "make_rect": False},
            "blue_knight": {"x": 0, "y": 0, "w": Media.pieces_size, "h": Media.pieces_size, "make_rect": False},

            "cursor_default": {"w": 30 * 0.805, "h": 30, "make_rect": False},
            "cursor_hand": {"w": 30 * 0.805, "h": 30, "make_rect": False},
            "x_btn": {"x": height//0.58, "y": height // 40, "w": height // 24, "h": height // 24, "use_rect_in": "all"},
            "shrink_btn": {"x": height//0.6, "y": height // 40, "w": height // 24, "h": height // 24, "use_rect_in": "all"},
            "minimize_btn": {"x": height//0.62, "y": height // 40, "w": height // 24, "h": height // 24, "use_rect_in": "all"},
            "setting_btn": {"x": height//0.64, "y": height // 40, "w": height // 24, "h": height // 24, "use_rect_in": "ingame"},
            "music_btn": {"x": height/0.78, "y": height / 8, "w": height / 28, "h": height / 28, "use_rect_in": "settings"},
            "copy_btn": {"x": height/1, "y": height / 2.05, "w": height / 28, "h": height / 28, "use_rect_in": ("match_creation_ready", "donations")},

            "team_bar": {"x": 0, "y": 0, "w": (height / 10) * (1280/528), "h": height / 10, "make_rect": False},

            "clk_0": {"x": height/0.957, "y": height / 2.578, "w": height / 22, "h": height / 22, "make_rect": False},
            "clk_1": {"x": height/0.957, "y": height / 2.578, "w": height / 22, "h": height / 22, "make_rect": False},
            "clk_2": {"x": height/0.957, "y": height / 2.578, "w": height / 22, "h": height / 22, "make_rect": False},
            "clk_3": {"x": height/0.957, "y": height / 2.578, "w": height / 22, "h": height / 22, "make_rect": False},
            "clk_4": {"x": height/0.957, "y": height / 2.578, "w": height / 22, "h": height / 22, "make_rect": False},


            "piece_selection_ui": {"x": height/0.693, "y":  height / 6.83, "w": height / (1.6*2), "h": height / 1.6, "make_rect": False},
            "support_ui": {"x": width/2 - ((height*(1920/1160))/1.4)/2, "y":  height/7, "w": (height*(1920/1160))/1.4, "h": height/1.4, "make_rect": False},
            "lobby_ui": {"x": width/2 - ((height*(1920/1160))/1.4)/2, "y":  height/7, "w": (height*(1920/1160))/1.4, "h": height/1.4, "make_rect": False},

            "lobby_background": {"x": 0, "y":  0, "w": width+1, "h": height, "make_rect": False},

            "volver_btn": {"x": width/2-((height*(1280/240))/20)/2, "y":  height/1.6, "w": (height*(1280/240))/20, "h": height/20, "use_rect_in": ("match_creation", "join_match", "match_creation_ready", "join_match_ready")},
            "crear_btn": {"x": width/2-((height*(1280/240))/20)/2, "y":  height/2.6, "w": (height*(1280/240))/20, "h": height/20, "use_rect_in": "lobby"},
            "unirse_btn": {"x": width/2-((height*(1280/243))/20)/2, "y":  height/2.1, "w": (height*(1280/243))/20, "h": height/20, "use_rect_in": "lobby"},
            "generar_btn": {"x": width/2-((height*(1280/240))/20)/2, "y":  height/2.6, "w": (height*(1280/240))/20, "h": height/20, "use_rect_in": "match_creation"},
            "ingresar_btn": {"x": width/2-((height*(1280/240))/20)/2, "y":  height/1.8, "w": (height*(1280/240))/20, "h": height/20, "use_rect_in": ("match_creation_ready", "join_match_ready")},

        }

    def resize(height):

        Media.sized = {}
        for key in Media.bare_imgs.keys():
            Media.sized.update({key: Media.scale(Media.bare_imgs[key], Media.metrics[key]["w"], Media.metrics[key]["h"])})

        Media.specific_copies = {}
        for key in Media.bare_imgs.keys():
            if "mage" in key or "archer" in key or "knight" in key:
                # these images correspond to the mini images for the health and mana bar
                Media.specific_copies.update({key+"_bar": Media.scale(Media.bare_imgs[key], Media.metrics[key]["w"]*1.2, Media.metrics[key]["h"]*1.22)})
                # these correspond to the big images in the piece selection menu
                Media.specific_copies.update({key+"_piece_selection_image": Media.scale(Media.bare_imgs[key], Media.metrics[key]["w"]*1.5, Media.metrics[key]["h"]*1.5)})

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
