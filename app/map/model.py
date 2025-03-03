from typing import Tuple

import pytmx.util_pygame
import pygame
import os
from app.texts.model import ShowTextContent, GetText
import app.characters.model


class PlayerCamera:
    def __init__(self, target, view_x_zone: int, view_y_zone: int):
        self.dx = target.x - view_x_zone * target.tile_size[0]
        self.dy = target.y - view_y_zone * target.tile_size[1]
        self.view_size = (view_x_zone * 2 * target.tile_size[0] +
                          target.rect.width, view_y_zone * 2 * target.tile_size[1] + target.rect.height)
        self.view_x = view_x_zone
        self.view_y = view_y_zone
        self.target = target

    def update(self):
        self.dx = self.target.x - self.view_x * self.target.tile_size[0]
        self.dy = self.target.y - self.view_y * self.target.tile_size[1]


class Map:
    def __init__(self, filename: str, tile_width: int = 8, tile_height: int = 8):
        self.map = pytmx.TiledMap(os.path.abspath('app/map/' + filename))
        self.width = 100
        self.height = 100
        self.top = 0
        self.left = 0
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.walls_layer = self.map.get_layer_by_name('walls')

        self.rects_doors = dict()

        # Списки нужны для взаимодействия с игроком и прочим.
        self.walls = []
        self.keys = []
        self.notes = []
        self.doors = []
        self.interactions = []

        self.width = 100
        self.height = 100

    def init_tile_object(self, x: int, y: int, item, screen: pygame.Surface, type_tile: str):  # метод, для того чтобы
        # добавлять в различные списки прямоугольники
        rect = pygame.Rect([x * self.tile_width, y * self.tile_height,
                            self.tile_width, self.tile_height])
        # смотрим куда добавляем прямоугольник
        if type_tile == 'key':
            self.keys.append(rect)
        if type_tile == 'note':
            self.notes.append(rect)
        else:
            self.interactions.append(rect)

        image = pygame.image.load(item[0])
        screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)),
                    (self.left + (x * self.tile_width), self.top + (y * self.tile_height)))

    def render(self, screen, x_i: int, y_i: int, width: int, height: int):
        for y in range(y_i, height):
            for x in range(x_i, width):
                # получаем тайл на данных координатах, после отображаем его на экране
                walls = self.map.get_tile_image(x, y, 1)
                floor = self.map.get_tile_image(x, y, 0)
                doors = self.map.get_tile_image(x, y, 2)
                interaction = self.map.get_tile_image(x, y, 3)
                key = self.map.get_tile_image(x, y, 4)
                note = self.map.get_tile_image(x, y, 5)
                if walls is None:  # тк мы проверяем все слои и все координаты,
                    # у нас могут быть тайлы с типом данных None
                    if not (doors is None):
                        image = pygame.image.load(doors[0])
                        rect = pygame.Rect([x * self.tile_width, y * self.tile_height,
                                            self.tile_width, self.tile_height])
                        self.doors.append(rect)
                        self.rects_doors[str(rect)] = [doors[0].split('/')[-1]]  # для каждого прямоугольника
                        # - имя файла тайла. Это нужно для смены картинки дверей.
                        screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)),
                                    (self.left + (x * self.tile_width), self.top + (y * self.tile_height)))

                    elif key is not None:
                        self.init_tile_object(x, y, key, screen, type_tile='key')
                    elif note is not None:
                        self.init_tile_object(x, y, note, screen, type_tile='note')
                    elif interaction is not None:
                        self.init_tile_object(x, y, key, screen, type_tile='interaction')
                    else:
                        if floor is None:
                            continue
                        image = pygame.image.load(floor[0])
                        screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)),
                                    (self.left + (x * self.tile_width), self.top + (y * self.tile_height)))

                else:
                    self.walls.append(pygame.Rect([x * self.tile_width, y * self.tile_height,
                                                   self.tile_width, self.tile_height]))
                    image = pygame.image.load(walls[0])
                    screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)),
                                (self.left + (x * self.tile_width), self.top + (y * self.tile_height)))

    def get_character_xy_by_tile_xy(self, x, y) -> Tuple[int, int]:
        return int(x * self.tile_width), int(y * self.tile_height)

    def update(self, screen, camera: PlayerCamera):
        left_top_point_camera = camera.dx, camera.dy
        right_bottom_point_camera = camera.dx + camera.view_size[0], camera.dy + camera.view_size[1]
        xy_tile_start = self.get_cell_coord(left_top_point_camera)
        if not xy_tile_start:
            xy_tile_start = (0, 0)
        if xy_tile_start[0] < 0:
            xy_tile_start = (0, xy_tile_start[1])
        if xy_tile_start[1] < 0:
            xy_tile_start = (xy_tile_start[0], 0)
        xy_tile_end = self.get_cell_coord(right_bottom_point_camera)
        if not xy_tile_end:
            xy_tile_end = (self.width, self.height)
        if xy_tile_end[0] > self.width:
            xy_tile_end = (self.width, xy_tile_end[1])
        if xy_tile_end[1] > self.height:
            xy_tile_end = (xy_tile_end[0], 0)
        self.render(screen, xy_tile_start[0], xy_tile_start[1],
                    xy_tile_end[0] - xy_tile_start[0] + xy_tile_start[0],
                    xy_tile_end[1] - xy_tile_start[1] + xy_tile_start[1])

    def get_cell_coord(self, coors: Tuple[int, int]) -> Tuple[int, int]:
        for x in range(coors[0], coors[0] + self.tile_width):
            for y in range(coors[1], coors[1] + self.tile_height):
                if x % self.tile_width == 0 and y % self.tile_height == 0:
                    return x // self.tile_width - 1, y // self.tile_height - 1

    def collide_with_walls(self, player_rect):  # коллайд со стенами
        # Здесь, мы просто проверяем есть ли какие-либо пересечения со всеми стенами, если да - возвращаем True
        if player_rect.collidelistall(self.walls):
            return True
        return False


class Doors(pygame.sprite.Sprite):  # класс дверей. Здесь прописаны все или почти все функции для взаимодействия с ними
    def __init__(self, doors_rects: list, tile_width: int, tile_height: int, pairs_doors_rects: dict):
        super().__init__()

        self.tile_width, self.tile_height = tile_width, tile_height

        self.pair_doors_rects = pairs_doors_rects
        self.rectangles_doors = doors_rects.copy()
        self.zone_doors_rects = []  # Этот список - список зон дверей. Зона двери - это просто прямоугольник побольше,
        # Он нужен для того, чтобы проще делать открытие дверей. Не нужно подходить вплотную к двери, достаточно войти
        # в это зону и нажатием кнопки открыть дверь

        for rect in self.rectangles_doors:
            self.zone_doors_rects.append(pygame.Rect([rect.x - 6, rect.y - 6, rect.w + 10, rect.h + 10]))

        self.open_doors = []
        self.pair_doors = {
            'tile_0076.png': 'tile_0034.png',
            'tile_0075.png': 'tile_0034.png',
            'tile_0036.png': 'tile_0034.png',
            'tile_0060.png': 'tile_0076.png',
            'tile_0059.png': 'tile_0075.png'
        }  # словарь нужен для смены картинки дверей после их открывания

    def collide_with_doors(self, player_rect):  # коллайд с дверьми. Аналогичен коллайду со стенами
        if player_rect.collidelistall(self.rectangles_doors):
            return True
        return False

    def removing_closed_door(self, door_zone):  # Этот метод нужен для того, чтобы удалять из списка обычных дверей
        # - открытые, следовательно, во время проверки столкновений с дверьми, открытые двери мы проверять не будем,
        # тк они будут удалены
        for door in self.rectangles_doors:
            if door.colliderect(door_zone):
                self.open_doors.append([door, *self.pair_doors_rects[(str(door))]])  # добавляем открытую дверь в список
                # этот список используется в update
                self.rectangles_doors.remove(door)

    def update(self, screen):
        # отрисовываем все открытые двери

        for el in self.open_doors:
            image = pygame.image.load(os.path.join('app/view/images/', self.pair_doors[el[1]]))
            screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)), (el[0].x, el[0].y))

    def check_rect_in_zone(self, player_rect: pygame.Rect):
        # перед тем как открыть дверь, мы должны проверить, находитсья ли игрок рядом с дверью, если да - True
        for zone_door in self.zone_doors_rects:
            if player_rect.colliderect(zone_door):  # По сути коллайд, но используется по-другому
                return [True, zone_door]
        return [False]


class KeysDoors:
    def __init__(self, screen, keys: list, tile_width: int, tile_height: int):
        self.tile_width, self.tile_height = tile_width, tile_height

        self.rects_keys = keys.copy()
        self.zone_keys_rects = []  # зона для подбора ключей

        for rect in self.rects_keys:
            self.zone_keys_rects.append(pygame.Rect([rect.x - 6, rect.y - 6, rect.w + 10, rect.h + 10]))
        self.keys_taken = []  # подобранные ключи

    def add_taken_key(self, key_zone):  # Просто добавляем подобранный ключ в список
        for key in self.rects_keys:
            if key.colliderect(key_zone):
                self.keys_taken.append(key)

    def update(self, screen):
        # вместо всех подобранных ключей - отрисовываем тайл пола
        for el in self.keys_taken:
            image = pygame.image.load(os.path.join('app/view/images/', 'tile_0017.png'))
            screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)), (el.x, el.y))

    def check_rect_in_zone(self, player_rect: pygame.Rect):  # поверяем находится ли игрок в зоне ключа, если да - True,
        # следовательно, игрок может подобрать ключ
        for zone_key in self.zone_keys_rects:
            if player_rect.colliderect(zone_key):
                return [True, zone_key]
        return [False]


class Notes:
    def __init__(self, text: GetText, rects: list, tile_width: int, tile_height: int):
        self.text = text
        self.tile_width, self.tile_height = tile_width, tile_height

        self.rects_notes = rects.copy()
        self.zone_rects_notes = []  # список зон записок (зоны прямоугольник тайла)

        for rect in self.rects_notes:
            self.zone_rects_notes.append(pygame.Rect([rect.x - 6, rect.y - 6, rect.w + 10, rect.h + 10]))
        self.notes_taken = []  # подобранные записки

    def update(self, screen):
        #  отрисовываем вместо подобранных записок тайл пола
        for el in self.notes_taken:
            image = pygame.image.load(os.path.join('app/view/images/', 'tile_0017.png'))
            screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)), (el.x, el.y))

    def check_rect_in_zone(self, player_rect: pygame.Rect):
        #  проверяем находится ли игрок в зоне прямоугольника (записки), если да - True, следовательно, можно подобрать
        for zone_note in self.zone_rects_notes:
            if player_rect.colliderect(zone_note):
                return [True, zone_note]
        return [False]

    def add_taken_note(self, rect_zone):
        # подобранные записки добавляем в список
        for note in self.rects_notes:
            if note.colliderect(rect_zone):
                self.notes_taken.append(note)


class Interactions:  # это класс особых "событий", которые нужны для того, чтобы начать комментарий игрока (ГГ), тобишь
    # диалог
    def __init__(self, rects: list, tile_width: int, tile_height: int):
        self.tile_width, self.tile_height = tile_width, tile_height

        self.rects_interaction = rects.copy()
        self.zone_rects_interaction = []  # список, зона прямоугольников (взаимодействий/событий)
        for rect in self.rects_interaction:
            self.zone_rects_interaction.append(pygame.Rect([rect[1].x - 11, rect[1].y - 11,
                                                            rect[1].w + 20, rect[1].h + 20]))
        self.active = []

    def update(self, screen):
        # если игрок зашел в зону "события" (я просто не знаю как это еще можно назвать), отрисовываем её на карте.
        for el in self.active:
            image = pygame.image.load(os.path.join('app/view/images/', 'tile_0116.png'))
            screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)), (el.x, el.y))

    def check_rect_in_zone(self, player_rect: pygame.Rect):  # проверяем, находится ли игрок в зоне прямугольников,
        # если да - True
        for zone_interaction in self.zone_rects_interaction:
            if player_rect.colliderect(zone_interaction):
                return [True, zone_interaction]
        return [False]

    def add_active(self, rect_zone):  # если игрок хотя бы один раз зашел в зону "события", добавляем в список
        for rect in self.rects_interaction:
            if rect[1].colliderect(rect_zone):
                if rect[1] not in self.active:
                    self.active.append(rect[1])