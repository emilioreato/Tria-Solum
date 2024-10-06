import pygame


class Media:

    def load_media():

        Media.backgrounds = []
        for i in range(0, Media.BACKGROUNDS_AMOUNT):
            bkg_img = pygame.image.load(f"resources\\images\\background{i}.png")  # load some images, converts it for optimization and then scales them.
            bkg_img = pygame.transform.smoothscale(bkg_img, (Media.width, Media.height))
            Media.backgrounds.append(bkg_img)

        cursor_default = pygame.image.load("resources\\icons\\cursor_default.png")
        Media.cursor_default = pygame.transform.smoothscale(cursor_default, (Media.screen_height * 0.805 // 43, Media.screen_height // 43))
        cursor_hand = pygame.image.load("resources\\icons\\cursor_hand.png")
        Media.cursor_hand = pygame.transform.smoothscale(cursor_hand, (Media.screen_height * 0.805 // 43, Media.screen_height // 43))

        Media.x_btn_metrics = {"x": Media.height//0.58, "y": Media.height // 40, "w": Media.height // 24, "h": Media.height // 24}
        x_btn = pygame.image.load("resources\\icons\\x.png")
        Media.x_btn = pygame.transform.smoothscale(x_btn, (Media.x_btn_metrics["w"], Media.x_btn_metrics["h"]))
        Media.x_btn_rect = Media.x_btn.get_rect()
        Media.x_btn_rect.topleft = (Media.x_btn_metrics["x"], Media.x_btn_metrics["y"])

        Media.shrink_btn_metrics = {"x": Media.height//0.6, "y": Media.height // 40, "w": Media.height // 24, "h": Media.height // 24}
        shrink_btn = pygame.image.load("resources\\icons\\shrink.png")
        Media.shrink_btn = pygame.transform.smoothscale(shrink_btn, (Media.shrink_btn_metrics["w"], Media.shrink_btn_metrics["h"]))
        Media.shrink_btn_rect = Media.shrink_btn.get_rect()
        Media.shrink_btn_rect.topleft = (Media.shrink_btn_metrics["x"], Media.shrink_btn_metrics["y"])

        Media.minimize_btn_metrics = {"x": Media.height//0.62, "y": Media.height // 40, "w": Media.height // 24, "h": Media.height // 24}
        minimize_btn = pygame.image.load("resources\\icons\\minimize.png")
        Media.minimize_btn = pygame.transform.smoothscale(minimize_btn, (Media.minimize_btn_metrics["w"], Media.minimize_btn_metrics["h"]))
        Media.minimize_btn_rect = Media.minimize_btn.get_rect()
        Media.minimize_btn_rect.topleft = (Media.minimize_btn_metrics["x"], Media.minimize_btn_metrics["y"])

        Media.settings_btn_metrics = {"x": Media.height//0.655, "y": Media.height // 40, "w": Media.height // 24, "h": Media.height // 24}
        settings_btn = pygame.image.load("resources\\icons\\setting.png")
        Media.settings_btn = pygame.transform.smoothscale(settings_btn, (Media.settings_btn_metrics["w"], Media.settings_btn_metrics["h"]))
        Media.settings_btn_rect = Media.settings_btn.get_rect()
        Media.settings_btn_rect.topleft = (Media.settings_btn_metrics["x"], Media.settings_btn_metrics["y"])

        Media.music_btn_metrics = {"x": Media.height/0.78, "y": Media.height // 8, "w": Media.height // 28, "h": Media.height // 28}  # x coordinate, y coordinate, width measure, height measure
        music_btn = pygame.image.load("resources\\icons\\music.png")
        Media.music_btn = pygame.transform.smoothscale(music_btn, (Media.music_btn_metrics["w"], Media.music_btn_metrics["h"]))
        Media.music_btn_rect = Media.music_btn.get_rect()
        Media.music_btn_rect.topleft = (Media.music_btn_metrics["x"], Media.music_btn_metrics["y"])

        Media.rects_list = (Media.x_btn_rect,
                            Media.music_btn_rect,
                            Media.shrink_btn_rect,
                            Media.minimize_btn_rect,
                            Media.settings_btn_rect
                            )

    @staticmethod
    def resize(cls, image, size_x, size_y, do_convert, convert_mode="default"):
        image = pygame.transform.smoothscale(image, (size_x, size_y))
        if do_convert:
            if convert_mode == "default":
                return image.convert()
            return image.convert_alpha()
        return image
