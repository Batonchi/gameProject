import pygame
import os
import json

from typing import Tuple
from app.items.model import GetItem
from pygame_widgets.button import Button


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
                 speed: Tuple[float, float] = (1, 1), y: int = 0, x: int = 0):
        super().__init__()
        self.character = character
        self.emotional_health = self.character.get_info()['emotional_health']
        self.image = pygame.image.load(os.path.join('app/view/images/character.png'))
        self.y = y
        self.x = x
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        image2 = pygame.image.load(os.path.join('app/view/images/' + 'tile_0004(2).png'))
        image2 = pygame.transform.scale(image2, (tile_width, tile_height))
        image3 = pygame.image.load(os.path.join('app/view/images/' + 'tile_0010(4).png'))
        image3 = pygame.transform.scale(image3, (tile_width, tile_height))
        self.images = [self.image, image2, image3]
        self.index = 0
        self.tile_size = tile_width, tile_height
        self.rect = pygame.Rect([self.x, self.y, tile_width, tile_height])
        self.speed = speed
        if self.character.get_info()['permissions']:
            self.permissions = character.inf.get('permissions')
        else:
            self.permissions = {
                'may_move': False,
                'may_speak': False,
                'may_use_items': False,
                'may_have_backpack': False
            }
        if self.permissions['may_have_backpack']:
            self.backpack = BackPack(character.inf.get('backpack_volume') or 10, self)
        self.is_npc = character.inf.get('_is_npc') or True
        if self.is_npc:
            self.dialog = character.inf.get('dialog')
            self.dialog_link = self.dialog

    def move(self, word: str):
        if word == 'up':
            self.y += self.speed[1]
            self.rect.move_ip(0, self.speed[1])
            self.index = 0
        elif word == 'down':
            self.y -= self.speed[1]
            self.rect.move_ip(0, -self.speed[1])
            self.index = 0
        elif word == 'left':
            self.x -= self.speed[0]
            self.rect.move_ip(-self.speed[0], 0)
            self.index = 2
        elif word == 'right':
            self.x += self.speed[0]
            self.rect.move_ip(self.speed[0], 0)
            self.index = 1
        self.image = self.images[self.index]

    def get_coors(self) -> tuple:
        return self.x, self.y

    def say(self):
        words = self.dialog_link['text']
        self.dialog_link = self.dialog_link.get('next', None)
        if self.dialog_link is None:
            self.start_dialog()
        return words

    def start_dialog(self):
        self.dialog_link = self.dialog


class BackPack:

    def __init__(self, volume: int, character: Character):
        self.volume = volume
        self.character = character
        self.rest = [None for _ in range(self.volume)]
        self.cells = []

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

    def render(self, screen: pygame.Surface, w_width: int, w_height: int):
        gap = 10
        width_cell, height_cell = (w_width - (self.volume * 10) // self.volume, w_height // 20)
        for i in range(0, self.volume):
            self.cells.append(Button(screen, i * width_cell + gap, w_height - height_cell, width_cell,
                                     height_cell, colour=(0, 0, 0), borderColour=(255, 255, 255), radius=10,
                                     borderThickness=10))

