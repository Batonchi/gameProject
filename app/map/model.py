import pytmx
import pygame
import os
import sys

import app.characters.model

CHARACTER_CLASS = app.characters.model.Character()


class Map:
    def __init__(self, filename, window_size):
        self.map = pytmx.TiledMap(os.path.join('app/map/files_tmx', filename))

        self.width = self.map.width
        self.height = self.map.height

        self.tile_size = self.map.tilewidth
        self.window_size = window_size

        self.collision = self.map.get_layer_by_name('walls')
        self.tiles = []
        for x, y, tile in self.collision.tiles():
            if tile:
                 self.tiles.append(pygame.Rect([(x * self.tile_size), (y * self.tile_size),
                                                self.tile_size, self.tile_size]))

        self.doors = pygame.sprite.Group()

    def load_image_player(self, name, colorkey=None):
        fullname = os.path.join('app/view/images/', name)
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

    def render(self, screen, coors):
        player_coors = coors
        for layer in self.map.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile in layer.tiles():
                    screen.blit(pygame.image.load(f'app/view/images/{list(tile)[0].split("/")[-1]}'),
                                [(x * self.tile_size),
                                 (y * self.tile_size)])
            if isinstance(layer, pytmx.TiledObjectGroup):
                for object in layer:
                    if object.name == 'Player':
                        x_player, y_player = self.map.get_object_by_name('Player').x, self.map.get_object_by_name(
                            'Player').y
                        new_x_player, new_y_player = player_coors[0], player_coors[1]
                        player_rect = pygame.Rect(new_x_player, new_y_player,
                                                  self.map.get_object_by_name('Player').width,
                                                  self.map.get_object_by_name('Player').height)
                        if self.checktiles(player_rect):
                            new_x_player, new_y_player = x_player, y_player
                        self.map.get_object_by_name('Player').x, self.map.get_object_by_name('Player').y =\
                            new_x_player, new_y_player
                        screen.blit(self.load_image_player('tile_0010.png'),
                                    (self.map.get_object_by_name('Player').x,
                                     self.map.get_object_by_name('Player').y))
        pygame.display.update()

    def checktiles(self, player_rect):
        check = False
        if player_rect.collidelistall(self.tiles):
            check = True
        return check

    def check_coins(self, player_rect):  # здесь будем проверять ключи и прочие предметы, которые можно будет поднять.
        pass