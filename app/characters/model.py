import pygame
import os
import json

from typing import Tuple
from app.items.model import GetItem


class CreateCharacter:

    def __init__(self, character_name: str, info: dict):
        self.character_name = character_name
        self.inf = json.dumps(info)


class GetCharacter:

    def __init__(self, character_id: int, character_name: str, info: str):
        self.character_id = character_id
        self.character_name = character_name
        self.inf = json.loads(info)

    def get_name(self) -> str:
        return self.character_name

    def get_info(self) -> dict:
        return self.inf


class Character(pygame.sprite.Sprite):
    def __init__(self, character: GetCharacter, tile_width: int = 8, tile_height: int = 8,
                 speed: Tuple[float, float] = (1, 1)):
        super().__init__()
        self.character = character
        # self.emotional_health = self.character.get_info()['emotional_health']
        # self.image = pygame.image.load(os.path.join('app/view/images/', character.get_name() + '.png'))
        self.image = pygame.image.load(os.path.join('app/view/images/', character + '.png'))
        self.y = 475
        self.x = 425
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.tile_size = tile_width, tile_height
        self.rect = pygame.Rect([self.x, self.y, tile_width, tile_height])
        self.speed = speed
        # if self.character.get_info()['permissions']:
        #     self.permissions = character.inf.get('permissions')
        # else:
        #     self.permissions = {
        #         'may_move': False,
        #         'may_speak': False,
        #         'may_use_items': False,
        #         'may_have_backpack': False
        #     }
        # if self.permissions['may_have_backpack']:
        #     self.backpack = BackPack(character.inf.get('backpack_volume') or 10, self)

    def move(self, word: str):
        if word == 'up':
            self.y += self.speed[1]
            self.rect.move_ip(0, self.speed[1])
        elif word == 'down':
            self.y -= self.speed[1]
            self.rect.move_ip(0, -self.speed[1])
        elif word == 'left':
            self.x -= self.speed[0]
            self.rect.move_ip(-self.speed[0], 0)
        elif word == 'right':
            self.x += self.speed[0]
            self.rect.move_ip(self.speed[0], 0)

    def get_coors(self) -> tuple:
        return self.x, self.y

    def say(self, phrase: str):
        pass
        # if self.active:
        #     print(self.character_name + ': ' + phrase)
        # else:
        #     # здесь надо подумать над тем хотим ли дать персонаджу с которым говорили
        #     # уникальную фразу для ответа если с ним попиздели
        #     print(self.character_name + ':' + '')


class BackPack:

    def __init__(self, volume: int, character: Character):
        self.volume = volume
        self.character = character
        self.rest = [None for _ in range(self.volume)]

    def add(self, item: GetItem):
        self.rest.append(item)

    def remove(self, item: GetItem):
        self.rest.remove(item)

    def check_items(self):
        for item in self.rest:
            if item.inf.get('is_wasted') and item.inf.get('may_deleted'):
                self.remove(item)

    def get_item_by_name(self, name: str) -> GetItem:
        for item in self.rest:
            if item.item_name == name:
                return item

    def do_selected(self):
        pass
