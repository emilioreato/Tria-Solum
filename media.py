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

            "grey_warning": pygame.image.load("resources\\icons\\grey_warning.png").convert_alpha(),
            "cursor_default": pygame.image.load("resources\\icons\\cursor_default.png").convert_alpha(),
            "cursor_hand": pygame.image.load("resources\\icons\\cursor_hand.png").convert_alpha(),
            "x_btn": pygame.image.load("resources\\icons\\x.png").convert_alpha(),
            "shrink_btn": pygame.image.load("resources\\icons\\shrink.png").convert_alpha(),
            "minimize_btn": pygame.image.load("resources\\icons\\minimize.png").convert_alpha(),
            "setting_btn": pygame.image.load("resources\\icons\\setting.png").convert_alpha(),
            "music_btn": pygame.image.load("resources\\icons\\music.png").convert_alpha(),
            "copy_btn": pygame.image.load("resources\\icons\\paperclip_copy.png").convert_alpha(),
            "chat_btn": pygame.image.load("resources\\icons\\chat.png").convert_alpha(),

            "name_bar": pygame.image.load("resources\\images\menu\\name_bar.png").convert_alpha(),
            "team_bar": pygame.image.load("resources\\images\menu\\my_team_bar2.png").convert_alpha(),
            "enemy_bar": pygame.image.load("resources\\images\menu\\enemy_bar3.png").convert_alpha(),

            "clk_0": pygame.image.load("resources\\icons\\clock\\0.png").convert_alpha(),
            "clk_1": pygame.image.load("resources\\icons\\clock\\1.png").convert_alpha(),
            "clk_2": pygame.image.load("resources\\icons\\clock\\2.png").convert_alpha(),
            "clk_3": pygame.image.load("resources\\icons\\clock\\3.png").convert_alpha(),
            "clk_4": pygame.image.load("resources\\icons\\clock\\4.png").convert_alpha(),

            "chat_ui": pygame.image.load("resources\\images\\menu\\chat.png").convert(),
            "configuration_ui": pygame.image.load("resources\\images\\menu\\configuracion_ui.png").convert(),
            "piece_selection_ui": pygame.image.load("resources\\images\\menu\\piece_selection_menu.png").convert(),
            "donations_ui": pygame.image.load("resources\\images\\menu\\donations_ui.png").convert(),
            "lobby_ui": pygame.image.load("resources\\images\\menu\\lobby_ui.png").convert(),
            "perfil_ui": pygame.image.load("resources\\images\\menu\\perfil_ui.png").convert(),
            "warning_ui": pygame.image.load("resources\\images\\menu\\warning.png").convert_alpha(),

            "lobby_background": pygame.image.load("resources\\images\\pure_background.png").convert(),

            "apoyanos_btn": pygame.image.load("resources\\images\\menu\\apoyanos.png").convert(),
            "perfil_btn": pygame.image.load("resources\\images\\menu\\perfil.png").convert(),
            "seleccionar_foto_btn": pygame.image.load("resources\\images\\menu\\seleccionar_foto.png").convert(),
            "guardar_apodo_btn": pygame.image.load("resources\\images\\menu\\guardar_apodo.png").convert(),
            "guardar_lema_btn": pygame.image.load("resources\\images\\menu\\guardar_lema.png").convert(),
            "volver_btn": pygame.image.load("resources\\images\\menu\\volver.png").convert(),
            "crear_btn": pygame.image.load("resources\\images\\menu\\crear.png").convert(),
            "unirse_btn": pygame.image.load("resources\\images\\menu\\unirse.png").convert(),
            "generar_btn": pygame.image.load("resources\\images\\menu\\generar_clave_de_partida.png").convert(),
            "ingresar_btn": pygame.image.load("resources\\images\\menu\\ingresar.png").convert(),
            "configuration_btn": pygame.image.load("resources\\images\\menu\\configuracion.png").convert(),
        }

        Media.resize_metrics(height)

    def resize_metrics(height):
        width = height*(16/9)

        Media.pieces_size = height/14

        Media.fonts_metrics = {
            "nickname_name_bar": height//34,  # height//34,
            "slogan_name_bar": height//48,  # height//34,
            "ip_text": height//42,  # height//34,
            "chat_msg_font": height//52,  # height//44,
            "warning_title_font": height//38,  # height//30,
            "warning_message_font": height//44,  # height//44,
        }

        Media.metrics = {  # DONT MAKE A KEY "MAKE_RECT" TRUE BECAUSE IT WONT MATTER, IT WONT MAKE THE RECTANGLE ANYWAY. later in the code the rectangles are created when in the keys there is the keyword "make_rect" so if you dont want the rect, just doesnt even speficy it
            "red_mage": {"x": 0, "y": 0, "w": Media.pieces_size, "h": Media.pieces_size, "make_rect": False},
            "blue_mage": {"x": 0, "y": 0, "w": Media.pieces_size, "h": Media.pieces_size, "make_rect": False},
            "red_archer": {"x": 0, "y": 0, "w": Media.pieces_size, "h": Media.pieces_size, "make_rect": False},
            "blue_archer": {"x": 0, "y": 0, "w": Media.pieces_size, "h": Media.pieces_size, "make_rect": False},
            "red_knight": {"x": 0, "y": 0, "w": Media.pieces_size, "h": Media.pieces_size, "make_rect": False},
            "blue_knight": {"x": 0, "y": 0, "w": Media.pieces_size, "h": Media.pieces_size, "make_rect": False},

            "grey_warning": {"x": 0, "y": 0, "w": height*(256/232) / 22, "h": height / 22, "make_rect": False},
            "cursor_default": {"w": 30 * 0.805, "h": 30, "make_rect": False},
            "cursor_hand": {"w": 30 * 0.805, "h": 30, "make_rect": False},
            "x_btn": {"x": height//0.58, "y": height // 40, "w": height // 24, "h": height // 24, "use_rect_in": "all"},
            "shrink_btn": {"x": height//0.6, "y": height // 40, "w": height // 24, "h": height // 24, "use_rect_in": "all"},
            "minimize_btn": {"x": height//0.62, "y": height // 40, "w": height // 24, "h": height // 24, "use_rect_in": "all"},
            "setting_btn": {"x": height//0.64, "y": height // 40, "w": height // 24, "h": height // 24, "use_rect_in": ("ingame", "match_creation", "join_match", "match_creation_ready", "join_match_ready")},
            "music_btn": {"x": height/1.972, "y": height / 2.351, "w": height / 28, "h": height / 28, "use_rect_in": "configuration"},
            "copy_btn": {"x": height/1, "y": height / 2.05, "w": height*(225/256) / 28, "h": height / 28, "use_rect_in": "match_creation_ready"},
            "chat_btn": {"x": height/2, "y": height / 30, "w": height / 24, "h": height / 24, "use_rect_in": "ingame"},

            "name_bar": {"x": height/24, "y": height/24, "w": (height / 10) * (1280/278), "h": height / 10, "make_rect": False},
            "team_bar": {"x": 0, "y": 0, "w": (height / 10) * (1280/528), "h": height / 10, "make_rect": False},
            "enemy_bar": {"x": 0, "y": 0, "w": (height / 12) * (1280/391), "h": height / 12, "make_rect": False},

            "clk_0": {"x": 0, "y": 0, "w": height / 22, "h": height / 22, "make_rect": False},
            "clk_1": {"x": 0, "y": 0, "w": height / 22, "h": height / 22, "make_rect": False},
            "clk_2": {"x": 0, "y": 0, "w": height / 22, "h": height / 22, "make_rect": False},
            "clk_3": {"x": 0, "y": 0, "w": height / 22, "h": height / 22, "make_rect": False},
            "clk_4": {"x": 0, "y": 0, "w": height / 22, "h": height / 22, "make_rect": False},

            "chat_ui": {"x": height/0.7, "y":  height / 7.073, "w": (height*(1280/1080)) / (3.5), "h": height / 3.5, "make_rect": False},
            "configuration_ui": {"x": width/2 - ((height*(1920/1160))/1.4)/2, "y":  height/7, "w": (height*(1920/1160))/1.4, "h": height/1.4, "make_rect": False},
            "piece_selection_ui": {"x": height/0.693, "y":  height / 6.83, "w": height / (1.6*2), "h": height / 1.6, "make_rect": False},
            "donations_ui": {"x": width/2 - ((height*(1920/1160))/1.4)/2, "y":  height/7, "w": (height*(1920/1160))/1.4, "h": height/1.4, "make_rect": False},
            "lobby_ui": {"x": width/2 - ((height*(1920/1160))/1.4)/2, "y":  height/7, "w": (height*(1920/1160))/1.4, "h": height/1.4, "make_rect": False},
            "perfil_ui": {"x": width/2 - ((height*(1920/1160))/1.4)/2, "y":  height/7, "w": (height*(1920/1160))/1.4, "h": height/1.4, "make_rect": False},
            "warning_ui": {"x": width/48, "y":  height/1.345, "w": (height*(1280/615))/4.5, "h": height/4.5, "use_rect_in": "all"},


            "lobby_background": {"x": 0, "y":  0, "w": width+1, "h": height, "make_rect": False},

            "apoyanos_btn": {"x": width/2+height/32, "y":  height/1.7, "w": (height*(1280/243))/32, "h": height/32, "use_rect_in": "configuration"},
            "perfil_btn": {"x": width/2+height/32, "y":  height/1.7, "w": (height*(1280/243))/32, "h": height/32, "use_rect_in": "lobby"},
            "seleccionar_foto_btn": {"x": width/2-((height*(1280/243))/20)/2, "y":  height/2.4, "w": (height*(1280/243))/20, "h": height/20, "use_rect_in": "profile"},
            "guardar_apodo_btn": {"x": width/2-((height*(1280/243))/20)/2, "y":  height/2.08, "w": (height*(1280/243))/20, "h": height/20, "use_rect_in": "profile"},
            "guardar_lema_btn": {"x": width/2-((height*(1280/243))/20)/2, "y":  height/1.8, "w": (height*(1280/243))/20, "h": height/20, "use_rect_in": "profile"},
            "volver_btn": {"x": width/2-((height*(1280/240))/28)/2, "y":  height/1.465, "w": (height*(1280/240))/28, "h": height/28, "use_rect_in": ("match_creation", "join_match", "profile", "match_creation_ready", "donations", "join_match_ready", "configuration")},
            "crear_btn": {"x": width/2-((height*(1280/240))/20)/2, "y":  height/2.6, "w": (height*(1280/240))/20, "h": height/20, "use_rect_in": "lobby"},
            "unirse_btn": {"x": width/2-((height*(1280/243))/20)/2, "y":  height/2.1, "w": (height*(1280/243))/20, "h": height/20, "use_rect_in": "lobby"},
            "generar_btn": {"x": width/2-((height*(1280/240))/20)/2, "y":  height/2.6, "w": (height*(1280/240))/20, "h": height/20, "use_rect_in": "match_creation"},
            "ingresar_btn": {"x": width/2-((height*(1280/240))/20)/2, "y":  height/1.8, "w": (height*(1280/240))/20, "h": height/20, "use_rect_in": ("match_creation_ready", "join_match_ready")},
            "configuration_btn": {"x": width/2-((height*(1280/222))/32)-height/32, "y":  height/1.7, "w": (height*(1280/222))/32, "h": height/32, "use_rect_in": "lobby"},
        }

        Media.piece_selection_reference_info = [{"x": height/0.64, "y": height / 3, "specie": "mage"},
                                                {"x": height/0.64, "y": height / 2.25, "specie": "archer"},
                                                {"x": height/0.64, "y": height / 1.7, "specie": "knight"}]

        Media.join_match_metrics = {"text_input": {"x": width // 2 - (height/5)/2, "y": height // 2 - 50, "w": height/5, "h": 50},
                                    "btn_conectar": {"x": width // 2 + (height/5)/2, "y": height // 2 - 50, "w": height/50+80, "h": 50},
                                    }

        Media.profile_menu_metrics = {"nickname_input": {"x": height/1.81, "y": height / 2.09, "w": height/5, "h": height/18.5},
                                      "slogan_input": {"x": height/1.81, "y": height / 1.805, "w": height/5, "h": height/18.5},
                                      }

        Media.chat_input_metrics = {"x": Media.metrics["chat_ui"]["x"]+height/100,
                                    "y": Media.metrics["chat_ui"]["y"]+height/4.13,
                                    "w": height/4.2,
                                    "h": height/26, }

        Media.useful_rects_metrics = {"wallet_btc": {"x": height/1.536, "y": height / 1.65, "w": height/7.5, "h": height/39, "use_rect_in": "donations"},
                                      "wallet_eth": {"x": height/0.973, "y": height / 1.65, "w": height/7.5, "h": height/39, "use_rect_in": "donations"},
                                      "send_btn_chat": {"x": Media.metrics["chat_ui"]["x"]+height/3.55, "y": Media.metrics["chat_ui"]["y"]+height/4.05, "w": height/28, "h": height/34, "use_rect_in": "chat"},
                                      }

        Media.slider_metrics = (height/1.35, height / 2.25)

        Media.clock_animation_metrics = {
            "match_creation": (height/0.957, height / 2.578),
            "match_creation_ready": (height/0.957, height / 1.4),
            "join_match_ready": (height/1.166, height / 2.216),
            "join_match": (height/0.957, height / 1.6)
        }

        Media.do_not_use_for_hover = [  # the list of images or rects that should not change the cursor when hovered
            "warning_ui"
        ]

    def resize(height):

        Media.sized = {}
        for key in Media.bare_imgs.keys():
            Media.sized.update({key: Media.scale(Media.bare_imgs[key], Media.metrics[key]["w"], Media.metrics[key]["h"])})

        Media.specific_copies = {}
        for key in Media.bare_imgs.keys():
            if "mage" in key or "archer" in key or "knight" in key:
                # these images correspond to the mini images for the health and mana bar
                Media.specific_copies.update({key+"_team_bar": Media.scale(Media.bare_imgs[key], Media.metrics[key]["w"]*1.2, Media.metrics[key]["h"]*1.2)})
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

        Media.useful_rects = {}
        for key, value in Media.useful_rects_metrics.items():
            Media.useful_rects.update({key: {"rect": pygame.Rect(value["x"], value["y"], value["w"], value["h"]), "use_rect_in": value["use_rect_in"]}})

        Media.fused_rect_list = []  # fuses all the rectangles in a single list
        for rect in Media.rects.items():
            Media.fused_rect_list.append(rect)
        for rect in Media.useful_rects.items():
            Media.fused_rect_list.append(rect)

        Fonts.resize_fonts()

    @staticmethod
    def convert(image, mode="default"):  # a function used to convert the images to the pygame format. you can choose between normal or alpha mode
        if mode == "alpha":
            return image.convert_alpha()
        return image.convert()

    @staticmethod
    def scale(image, size_x, size_y):
        return pygame.transform.smoothscale(image, (size_x, size_y))


class Fonts:

    def resize_fonts():

        Fonts.nickname_name_bar = pygame.font.SysFont("Times New Roman", Media.fonts_metrics["nickname_name_bar"])
        Fonts.slogan_name_bar = pygame.font.SysFont("Times New Roman", Media.fonts_metrics["slogan_name_bar"])

        Fonts.ip_text = pygame.font.SysFont("Times New Roman", Media.fonts_metrics["ip_text"])
        Fonts.chat_msg_font = pygame.font.SysFont("Times New Roman", Media.fonts_metrics["chat_msg_font"])
        Fonts.warning_title_font = pygame.font.SysFont("Times New Roman", Media.fonts_metrics["warning_title_font"])
        Fonts.warning_message_font = pygame.font.SysFont("Times New Roman", Media.fonts_metrics["warning_message_font"])

    def transform_text_line_to_paragraph(text, max_length, join=True):
        words = text.split()  # Dividir el texto en palabras
        resultado = []
        linea_actual = ""

        for palabra in words:
            # Si agregar la palabra a la línea actual no excede la longitud máxima
            if len(linea_actual) + len(palabra) + 1 <= max_length:
                if linea_actual:  # Si ya hay palabras en la línea, agregar un espacio antes
                    linea_actual += " " + palabra
                else:
                    linea_actual = palabra
            elif len(palabra) > max_length:
                """chars_available = max_length - len(linea_actual) - 2
                if chars_available > 1:
                    linea_actual += " " + palabra[:chars_available+1] + "-"
                    resultado.append(linea_actual)
                    palabra = palabra[chars_available:]
                else:
                    resultado.append(linea_actual)"""
                if len(linea_actual) > 0:
                    resultado.append(linea_actual)
                palabra_dividida = [palabra[i:i+max_length-1]+"-" for i in range(0, len(palabra), max_length-1)]
                palabra_dividida[-1] = palabra_dividida[-1][:-1]  # Eliminar el último guión de la última linea
                resultado.extend(palabra_dividida[:-1])
                linea_actual = palabra_dividida[-1]  # Agregar la última parte a la nueva línea actual

            else:  # Si la palabra excede el límite, agregar la línea actual al resultado y empezar una nueva
                resultado.append(linea_actual)
                linea_actual = palabra

        # Agregar la última línea si tiene contenido
        if linea_actual:
            resultado.append(linea_actual)

        if join:
            return ("\n".join(resultado), len(resultado))  # returns the formatted msg and the number of lines it has
        else:
            return (resultado, len(resultado))
