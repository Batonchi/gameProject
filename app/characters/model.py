import json
import pygame
import os
import sys


class Character:
    def __init__(self, character_name: str = None, info: str = None, character_id: int = None):
        self.character_name = character_name
        self.info = info
        self.coors = (100, 100)
        self.speed = 5
        # self.info_from_json = json.loads(info)
        if character_id:
            self.character_id = character_id
        self.active = True

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('app/view/images', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            print(f"Файл с изображением '{fullname}' не найден")
            raise sys.exit()
        image = image.convert_alpha()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        return image

    def move(self, word: str):
        match_word = {'left': lambda x=None: (self.coors[0] - self.speed, self.coors[1]),
                      'right': lambda x=None: (self.coors[0] + self.speed, self.coors[1]),
                      'down': lambda x=None: (self.coors[0], self.coors[1] + self.speed),
                      'up': lambda x=None: (self.coors[0], self.coors[1] - self.speed)
                      }
        self.coors = match_word[word]()
        return self.coors

    def get_coors(self):
        print(self.coors)
        return self.coors

    def get_info(self):
        return self.info

    def get_name(self):
        return self.character_name

    def say(self, phrase: str):
        if self.active:
            print(self.character_name + ': ' + phrase)
        else:
            # здесь надо подумать над тем хотим ли дать персонаджу с которым говорили
            # уникальную фразу для ответа если с ним попиздели
            print(self.character_name + ':' + '')