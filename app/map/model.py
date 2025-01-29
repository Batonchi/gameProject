import pytmx
import pygame
from app.characters.model import Character
FILE_DIR = 'map'


class Map:
    def __init__(self, filename, window_size):
        self.map = pytmx.load_pygame(f'{FILE_DIR}/{filename}')
        self.width = self.map.width
        self.height = self.map.height
        self.tile_size = self.map.tilewidth
        self.window_size = window_size
        self.collision = self.map.get_layer_by_name('walls')
        self.CAMERA = self.map.get_object_by_name("Player")
        self.tiles = []
        for x, y, tile in self.collision.tiles():
            if tile:
                 self.tiles.append(pygame.Rect([(x * self.tile_size), (y * self.tile_size),
                                                self.tile_size, self.tile_size]))

    def render(self, screen, player):  # <- надо будет поменять
        for layer in self.map.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, tile in layer.tiles():
                    if tile:
                        screen.blit(tile, [(x * self.tile_size) - self.CAMERA.x + (self.window_size[0] / 2),
                                           (y * self.tile_size) - self.CAMERA.y + (self.window_size[1] / 2)])

            elif isinstance(layer, pytmx.TiledObjectGroup):
                for object in layer:
                    if object.type == 'Player':
                        screen.blit(player,
                                    [object.x - self.CAMERA.x + (self.window_size[0] / 2),
                                     object.y - self.CAMERA.y + (self.window_size[1] / 2)])

    def update(self):
        pass