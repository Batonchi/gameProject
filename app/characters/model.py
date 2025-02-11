import json
import pygame
import os
import sys


class Character(pygame.sprite.Sprite):
    def __init__(self, character_name: str, info: json = None, character_id: int = None):
        super().__init__()
        self.image = pygame.image.load(os.path.join('app/view/images/', character_name + '.png'))
        self.character_name = character_name
        self.info = info
        self.y = 100
        self.x = 100
        self.rect = self.image.get_rect()
        self.speed = 2
        # self.info_from_json = json.loads(info)
        if character_id:
            self.character_id = character_id
        self.active = True

    def move(self, word: str):
        if word == 'up':
            self.y -= self.speed
            self.rect.move_ip(0, self.speed)
        elif word == 'down':
            self.y += self.speed
            self.rect.move_ip(0, -self.speed)
        elif word == 'left':
            self.x -= self.speed
            self.rect.move_ip(0, -self.speed)
        elif word == 'right':
            self.x += self.speed
            self.rect.move_ip(0, self.speed)

    def get_coors(self):
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