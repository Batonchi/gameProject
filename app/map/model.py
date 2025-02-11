import pytmx.util_pygame
import pygame
import os
import app.characters.model


# CHARACTER_CLASS = app.characters.model.Character()


class Map:
    def __init__(self, filename: str):
        self.map = pytmx.TiledMap(os.path.abspath('app/map/' + filename))
        self.top = 0
        self.left = 0
        self.height = self.map.height
        self.width = self.map.width
        self.tile_width = self.map.tilewidth
        self.walls = self.map.get_layer_by_name('walls')
        self.doors = self.map.get_layer_by_name('close_doors')
        self.floor = self.map.get_layer_by_name('floor')
        self.walls = [pygame.Rect([(x * self.tile_width), (y * self.tile_width),
                                   self.tile_width, self.tile_width]) for x, y, tile in self.walls.tiles()
                      if tile]
        self.floor = [pygame.Rect([(x * self.tile_width), (y * self.tile_width),
                                   self.tile_width, self.tile_width]) for x, y, tile in self.floor.tiles()
                      if tile]
        self.doors = [pygame.Rect([(x * self.tile_width), (y * self.tile_width),
                                   self.tile_width, self.tile_width]) for x, y, tile in self.doors.tiles()
                      if tile]

    def render(self, screen, x_i: int, y_i: int, width: int, height: int):
        for y in range(y_i, height):
            for x in range(x_i, width):
                walls = self.map.get_tile_image(x, y, 1)
                floor = self.map.get_tile_image(x, y, 0)
                doors = self.map.get_tile_image(x, y, 2)
                if walls is None:
                    if not (doors is None):
                        screen.blit(pygame.image.load(doors[0]), (x * self.tile_width, y * self.tile_width))
                    else:
                        if floor is None:
                            continue
                        screen.blit(pygame.image.load(floor[0]), (x * self.tile_width, y * self.tile_width))
                else:
                    screen.blit(pygame.image.load(walls[0]), (x * self.tile_width, y * self.tile_width))

    # def check_coord(self, coors):
    #     if (self.top > coors[1] or self.top + (len(self.board) * self.tile_width) < coors[1] or self.left > coors[0]
    #             or self.left + (len(self.board[0]) * self.tile_width) < coors[0]):
    #         return None
    #     for y in range(0, len(self.board)):
    #         for x in range(0, len(self.board[0])):
    #             if (self.top + y * self.tile_width <= coors[1] <= self.top + y * self.tile_width + self.tile_width and
    #                     self.left + x * self.tile_width <= coors[0] <= self.left + x * self.tile_width + self.tile_width):
    #                 return x, y
    #     pygame.display.update()

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def check_tiles(self, player_rect):
        check = False
        if not player_rect.collidelistall(self.walls):
            check = True
        return check

    def check_coins(self, player_rect):  # здесь будем проверять ключи и прочие предметы, которые можно будет поднять.
        pass


class Camera:
    pass


