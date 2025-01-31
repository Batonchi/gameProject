import pytmx
import pygame
import os

from app.characters.model import Character


class Map:
    def __init__(self, filename, window_size):
        self.map = pytmx.TiledMap(os.path.join('app\map', filename))
        self.width = self.map.width
        self.height = self.map.height
        self.tile_size = self.map.tilewidth
        self.window_size = window_size
        self.collision = self.map.get_layer_by_name('walls')
        # self.CAMERA = self.map.get_object_by_name("Player")
        self.tiles = []
        for x, y, tile in self.collision.tiles():
            if tile:
                 self.tiles.append(pygame.Rect([(x * self.tile_size), (y * self.tile_size),
                                                self.tile_size, self.tile_size]))

    def render(self, screen, player=None):  # <- надо будет поменять
        try:
            for layer in self.map.layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, tile in layer.tiles():
                        screen.blit(pygame.image.load(f'app/view/images/{list(tile)[0].split("/")[-1]}'),
                                    [x * self.tile_size,y * self.tile_size])

                elif isinstance(layer, pytmx.TiledObjectGroup):
                    for object in layer:
                        if object.type == 'Player':
                            screen.blit(player,
                                        [object.x + (self.window_size[0] / 2),
                                         object.y + (self.window_size[1] / 2)])
                pygame.display.update()
        except Exception as e:
            print(e)

    def checktiles(self, player_rect):
        check = False
        if player_rect.collidelistall(self.tiles):
            check = True
        return check

    def check_coins(self, player_rect):  # здесь будем проверять ключи и прочие предметы, которые можно будет поднять.
        pass