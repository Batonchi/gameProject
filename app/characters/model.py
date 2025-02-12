import json
import pygame
import os
import sys

from typing import Tuple


class Character(pygame.sprite.Sprite):
    def __init__(self, character_name: str, info: json = None, character_id: int = None,
                 tile_width: int = 8, tile_height: int = 8, speed: Tuple[int, int] = (0, 0)):
        super().__init__()
        self.image = pygame.image.load(os.path.join('app/view/images/', character_name + '.png'))
        self.character_name = character_name
        self.info = info
        self.y = 500
        self.x = 500
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.tile_size = tile_width, tile_height
        self.rect = self.image.get_rect()
        self.speed = speed
        # self.info_from_json = json.loads(info)
        if character_id:
            self.character_id = character_id
        self.active = True

    def move(self, word: str):
        if word == 'up':
            self.y -= self.speed[1]
            self.rect.move_ip(0, self.speed[1])
        elif word == 'down':
            self.y += self.speed[1]
            self.rect.move_ip(0, -self.speed[1])
        elif word == 'left':
            self.x -= self.speed[0]
            self.rect.move_ip(0, -self.speed[0])
        elif word == 'right':
            self.x += self.speed[0]
            self.rect.move_ip(0, self.speed[0])

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