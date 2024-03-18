# 音效类
import pygame
pygame.init()


class Audio:
    def __init__(self) -> None:
        self.audios_dict = {}
        # 加载音频文件

        start_sound = pygame.mixer.Sound("music\ks.mp3")
        pause_sound = pygame.mixer.Sound("music\zt.mp3")
        finish_sound = pygame.mixer.Sound("music\js.mp3")
        retract_sound = pygame.mixer.Sound("music\hq.mp3")
        drop_piece_sound = pygame.mixer.Sound("music\lz.wav")  

        self.audios_dict["start_sound"] = start_sound
        self.audios_dict["pause_sound"] = pause_sound
        self.audios_dict["finish_sound"] = finish_sound
        self.audios_dict["retract_sound"] = retract_sound
        self.audios_dict["drop_piece_sound"] = drop_piece_sound
        #self.audios_dict["background_sound"] = 
