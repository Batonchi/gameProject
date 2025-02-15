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
        self.top = 0
        self.left = 0
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.walls_layer = self.map.get_layer_by_name('walls')
        # self.doors = self.map.get_layer_by_name('close_doors')
        # self.floor = self.map.get_layer_by_name('floor')

        self.walls = [(pygame.Rect([(x * self.tile_width), (y * self.tile_width),
                                    self.tile_width, self.tile_width]), tile)
                      for x, y, tile in self.walls_layer.tiles() if tile]
        # self.floor = [(pygame.Rect([(x * self.tile_width), (y * self.tile_width),
        #                            self.tile_width, self.tile_width]), tile) for x, y, tile in self.floor.tiles()
        #               if tile]
        # self.doors = [(pygame.Rect([(x * self.tile_width), (y * self.tile_width),
        #                            self.tile_width, self.tile_width]), tile) for x, y, tile in self.doors.tiles()
        #               if tile]
        self.width = 100
        self.height = 100

    def render(self, screen, x_i: int, y_i: int, width: int, height: int):
        for y in range(y_i, height):
            for x in range(x_i, width):
                walls = self.map.get_tile_image(x, y, 1)
                floor = self.map.get_tile_image(x, y, 0)
                doors = self.map.get_tile_image(x, y, 2)
                if walls is None:
                    if not (doors is None):
                        image = pygame.image.load(doors[0])
                        screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)),
                                    (self.left + (x * self.tile_width), self.top + (y * self.tile_height)))
                    else:
                        if floor is None:
                            continue
                        image = pygame.image.load(floor[0])
                        screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)),
                                    (self.left + (x * self.tile_width), self.top + (y * self.tile_height)))
                else:
                    image = pygame.image.load(walls[0])
                    screen.blit(pygame.transform.scale(image, (self.tile_width, self.tile_height)),
                                (self.left + (x * self.tile_width), self.top + (y * self.tile_height)))

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

    def get_cell_coord(self, coors: Tuple[int, int]):
        for x in range(coors[0], coors[0] + self.tile_width):
            for y in range(coors[1], coors[1] + self.tile_height):
                if x % self.tile_width == 0 and y % self.tile_height == 0:
                    return x // self.tile_width - 1, y // self.tile_height - 1

    def check_tiles(self, player_rect):
        check = False
        if not player_rect.collidelistall(self.walls):
            check = True
        return check

    def check_coins(self, player_rect):  # здесь будем проверять ключи и прочие предметы, которые можно будет поднять.
        pass