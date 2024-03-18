# 按钮类
import pygame
pygame.init()


class Button:
    def __init__(self, screen_width:int, screen_height:int) -> None:
        button_width, button_height = 200, 65


        # 加载按钮图片
        start_button_img = pygame.image.load("img\ksyx3.jpg")
        retract_button_img = pygame.image.load("img\hq.jpg")
        quit_button_img = pygame.image.load("img\\tcyx2.jpg")

        start_button_img = pygame.transform.scale(start_button_img, (button_width, button_height))
        retract_button_img = pygame.transform.scale(retract_button_img, (button_width, button_height))
        quit_button_img = pygame.transform.scale(quit_button_img, (button_width, button_height))
        # # 设置按钮位置

        start_button_rect = start_button_img.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        retract_button_rect = retract_button_img.get_rect(center=(screen_width // 2, screen_height // 2 - 25))
        quit_button_rect = quit_button_img.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

        self.button_dict = {
            "start_button": (start_button_img, start_button_rect),
            "retract_button_rect": (retract_button_img, retract_button_rect),
            "quit_button_rect": (quit_button_img, quit_button_rect)
        }