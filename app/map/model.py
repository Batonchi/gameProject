from typing import Tuple

import pytmx.util_pygame
import pygame
import os
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

        self.walls = []
        self.keys = []
        self.notes = []
        self.doors = []

        self.width = 100
        self.height = 100

    def init_tile_object(self, x: int, y: int, item, screen: pygame.Surface, type_tile: str):
        rect = pygame.Rect([x * self.tile_width, y * self.tile_height,
                            self.tile_width, self.tile_height])
        if type_tile == 'key':
            self.keys.append(rect)
        else:
            self.notes.append(rect)
        image = pygame.image.load(item[0])
        screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)),
                    (self.left + (x * self.tile_width), self.top + (y * self.tile_height)))

    def render(self, screen, x_i: int, y_i: int, width: int, height: int):
        for y in range(y_i, height):
            for x in range(x_i, width):
                walls = self.map.get_tile_image(x, y, 1)
                floor = self.map.get_tile_image(x, y, 0)
                doors = self.map.get_tile_image(x, y, 2)
                key = self.map.get_tile_image(x, y, 3)
                note = self.map.get_tile_image(x, y, 4)
                if walls is None:
                    if not (doors is None):
                        image = pygame.image.load(doors[0])
                        rect = pygame.Rect([x * self.tile_width, y * self.tile_height,
                                            self.tile_width, self.tile_height])
                        self.doors.append(rect)
                        self.rects_doors[str(rect)] = [doors[0].split('/')[-1]]
                        screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)),
                                    (self.left + (x * self.tile_width), self.top + (y * self.tile_height)))

                    elif key is not None:
                        self.init_tile_object(x, y, key, screen, type_tile='key')
                    elif note is not None:
                        self.init_tile_object(x, y, note, screen, type_tile='note')
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

    def collide_with_walls(self, player_rect):
        if player_rect.collidelistall(self.walls):
            return True
        return False


class Doors(pygame.sprite.Sprite):
    def __init__(self, doors_rects: list, tile_width: int, tile_height: int, pairs_doors_rects: dict):
        super().__init__()

        self.tile_width, self.tile_height = tile_width, tile_height

        self.pair_doors_rects = pairs_doors_rects
        self.rectangles_doors = doors_rects.copy()
        self.zone_doors_rects = []

        for rect in self.rectangles_doors:
            self.zone_doors_rects.append(pygame.Rect([rect.x - 6, rect.y - 6, rect.w + 10, rect.h + 10]))

        self.open_doors = []
        self.pair_doors = {
            'tile_0076.png': 'tile_0034.png',
            'tile_0075.png': 'tile_0034.png',
            'tile_0036.png': 'tile_0034.png',
            'tile_0060.png': 'tile_0076.png',
            'tile_0059.png': 'tile_0075.png'
        }

    def collide_with_doors(self, player_rect):
        if player_rect.collidelistall(self.rectangles_doors):
            return True
        return False

    def removing_closed_door(self, door_zone):
        for door in self.rectangles_doors:
            if door.colliderect(door_zone):
                self.open_doors.append([door, *self.pair_doors_rects[(str(door))]])
                self.rectangles_doors.remove(door)

    def update(self, screen):
        for el in self.open_doors:
            image = pygame.image.load(os.path.join('app/view/images/', self.pair_doors[el[1]]))
            screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)), (el[0].x, el[0].y))

    def check_rect_in_zone(self, player_rect: pygame.Rect):
        for zone_door in self.zone_doors_rects:
            if player_rect.colliderect(zone_door):
                return [True, zone_door]
        return [False]


class KeysDoors:
    def __init__(self, screen, keys: list, tile_width: int, tile_height: int):
        self.tile_width, self.tile_height = tile_width, tile_height

        self.rects_keys = keys.copy()
        self.zone_keys_rects = []

        for rect in self.rects_keys:
            self.zone_keys_rects.append(pygame.Rect([rect.x - 6, rect.y - 6, rect.w + 10, rect.h + 10]))
        self.keys_taken = []

    def add_taken_key(self, key_zone):
        for key in self.rects_keys:
            if key.colliderect(key_zone):
                self.keys_taken.append(key)

    def update(self, screen):
        for el in self.keys_taken:
            image = pygame.image.load(os.path.join('app/view/images/', 'tile_0017.png'))
            screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)), (el.x, el.y))

    def check_rect_in_zone(self, player_rect: pygame.Rect):
        for zone_key in self.zone_keys_rects:
            if player_rect.colliderect(zone_key):
                return [True, zone_key]
        return [False]


class Notes:
    def __init__(self, rects: list, tile_width: int, tile_height: int):
        self.tile_width, self.tile_height = tile_width, tile_height

        self.rects_notes = rects.copy()
        self.zone_rects_notes = []

        for rect in self.rects_notes:
            self.zone_rects_notes.append(pygame.Rect([rect.x - 6, rect.y - 6, rect.w + 10, rect.h + 10]))
        self.notes_taken = []

    def update(self, screen):
        for el in self.notes_taken:
            image = pygame.image.load(os.path.join('app/view/images/', 'tile_0017.png'))
            screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)), (el.x, el.y))

    def check_rect_in_zone(self, player_rect: pygame.Rect):
        for zone_note in self.zone_rects_notes:
            if player_rect.colliderect(zone_note):
                return [True, zone_note]
        return [False]

    def add_taken_note(self, rect_zone):
        for note in self.rects_notes:
            if note.colliderect(rect_zone):
                self.notes_taken.append(note)
