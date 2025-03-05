import pygame
import os
import json

from typing import Tuple
from pygame_widgets.animations.animation import Recolour
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
        images_path = {}
        self.image = pygame.image.load(os.path.
                                       join(f'app/view/images/character.png'))
        self.y = y
        self.x = x
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.is_npc = self.character.inf.get('is_npc', True)
        if self.is_npc:
            self.dialog = character.inf.get('dialog')
            self.dialog_link = self.dialog
        else:
            self.emotional_health = self.character.get_info().get('emotional_health', 100)
            image2 = pygame.image.load(os.path.join('app/view/images/' + 'tile_0004(2).png'))
            image2 = pygame.transform.scale(image2, (tile_width, tile_height))
            image3 = pygame.image.load(os.path.join('app/view/images/' + 'tile_0010(4).png'))
            image3 = pygame.transform.scale(image3, (tile_width, tile_height))
            self.images = [self.image, image2, image3]
            self.speed = speed
        self.index = 0
        self.tile_size = tile_width, tile_height

        self.rect = pygame.Rect([self.x, self.y, tile_width, tile_height])
        self.zone_rect = pygame.Rect([self.x - 6, self.y - 6, tile_width + 10, tile_height + 10])

        self.speed = speed
        if self.character.get_info().get('permissions'):
            self.permissions = character.inf.get('permissions')
        else:
            self.permissions = {
                'may_move': False,
                'may_speak': True,
                'may_use_items': False,
                'may_have_backpack': False
            }
        if self.permissions['may_have_backpack']:
            self.backpack = BackPack(character.inf.get('backpack_volume') or 10, self)

    def check_rect_in_zone(self, player_rect: pygame.Rect, zone_rect: list):
        for rect in zone_rect:
            if player_rect.colliderect(rect):
                return [True]
        return [False]

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


class Item:

    def __init__(self, item_name: str, inf: dict, func, harmless: int = 10):
        self.item_name = item_name
        self.inf = inf
        self.use_func = func
        self.harmless = harmless

    def use_item(self):
        self.use_func()

    def do_affect(self, character: Character):
        character.emotional_health += self.harmless


class BackPack:

    def __init__(self, volume: int, character: Character):
        self.active_cell_id = 0
        self.height_cell = None
        self.width_cell = None
        self.gap = 10
        self.volume = volume
        self.character = character
        self.is_show = True
        self.rest = [0 for _ in range(self.volume)]
        self.cells = []

    def take(self, i: int, item: Item):
        self.remove_item(i)
        self.rest[i] = item
        # self.cells[i].image = pygame.transform.scale(
        #     pygame.image.load(os.path.abspath(f'app\\map\\icons\\{item.inf.get('image')}.png')),
        #     (self.width_cell // 3, self.height_cell // 2))
        self.cells[i].setText(item.item_name)
        self.cells[i].font = pygame.font.SysFont('Arial-black', 30, bold=500)

    def get_last_free_cell(self) -> int | None:
        for cell in range(0, self.volume):
            if self.rest[cell] == 0:
                return cell

    def do_selected(self, cell_i: int):
        button = self.cells[cell_i]
        animation = Recolour(widget=button, colour=(50, 0, 0), timeout=0)
        animation.start()

    def do_unselected(self, cell_i: int):
        button = self.cells[cell_i]
        animation = Recolour(widget=button, colour=(30, 30, 30), timeout=0)
        animation.start()

    def render(self, screen: pygame.Surface, w_width: int, w_height: int):
        gap = 20
        self.width_cell, self.height_cell = ((w_width // self.volume) - gap, w_height // 20)
        for i in range(0, self.volume):
            self.cells.append(Button(screen, i * (self.width_cell + gap), w_height - self.height_cell, self.width_cell,
                                     self.height_cell, colour=(30, 30, 30), borderColour=(155, 155, 155), radius=10,
                                     borderThickness=1, textColour=(255, 255, 255)))
            if self.cells[-1].image is None:
                self.cells[-1].setText('пусто')
        self.do_selected(self.active_cell_id)

    def show_buttons(self):
        for cell in self.cells:
            cell.show()
        self.is_show = True

    def close_backpack(self):
        for cell in self.cells:
            cell.hide()
        self.is_show = False

    def next_item(self):
        self.active_cell_id += 1
        if self.active_cell_id == len(self.cells):
            self.active_cell_id = 0

    def previous_item(self):
        self.active_cell_id -= 1
        if self.active_cell_id == -1:
            self.active_cell_id = len(self.cells) - 1

    def remove_item(self, cell_i: int):
        self.rest[cell_i] = None
        self.cells[cell_i].setText('пусто')
        self.cells[cell_i].image = None
        self.cells[cell_i].font_size = 20
