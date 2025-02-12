import os.path
import pygame
import pygame.camera

from database import Connection, create_database
from app.characters.model import Character
from app.map.model import Map, PlayerCamera
from pygame_widgets.button import Button


create_database()


FPS = 60


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        pygame.display.set_caption('Game')
        # zoom = 2
        # wnd_w, wnd_h = self.screen.get_size()
        # zoom_size = (round(wnd_w / zoom), round(wnd_h / zoom))
        # zoom_area = pygame.Rect(0, 0, *zoom_size)
        # zoom_area.center = (100, 100)
        # zoom_surf = pygame.Surface(zoom_area.size)
        # zoom_surf.blit(self.screen, (0, 0), zoom_area)
        # zoom_surf = pygame.transform.scale(zoom_surf, (wnd_w, wnd_h))
        w_w, w_h = self.screen.get_size()
        running = True
        map_game = Map('map_level1.tmx', tile_width=w_w // 100, tile_height=w_h // 100)
        map_game.render(self.screen, 0, 0, 100, 100)
        character = Character('character', tile_width=w_w // 150, tile_height=w_h // 75,
                              speed=((w_w // 200) // 4, (w_h // 200) // 4))
        camera = PlayerCamera(character, 10, 10)
        while running:
            # self.screen.blit(zoom_surf, (0, 0))
            events = pygame.event.get()
            clock = pygame.time.Clock()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        character.move('left')
                    if event.key == pygame.K_w:
                        character.move('up')
                    if event.key == pygame.K_s:
                        character.move('down')
                    if event.key == pygame.K_d:
                        character.move('right')
                camera.update()
                map_game.update(self.screen, camera)
                self.screen.blit(character.image, (character.x, character.y))
            if pygame.key.get_pressed()[pygame.K_w]:
                character.move('up')
            if pygame.key.get_pressed()[pygame.K_a]:
                character.move('left')
            if pygame.key.get_pressed()[pygame.K_s]:
                character.move('down')
            if pygame.key.get_pressed()[pygame.K_d]:
                character.move('right')
            camera.update()
            pygame.event.pump()
            pygame.display.flip()
            pygame.display.update()
            clock.tick(FPS)

    def start(self):
        pass

    def end(self):
        pass


if __name__ == '__main__':
    game = Game()




# if event.key == pygame.K_w:
#     coors = character.move('up')
#     map_game.render(screen, coors)
# elif event.key == pygame.K_a:
#     coors = character.move('left')
#     map_game.render(screen, coors)
# elif event.key == pygame.K_s:
#     coors = character.move('down')
#     map_game.render(screen, coors)
# elif event.key == pygame.K_d:
#     coors = character.move('right')
#     map_game.render(screen, coors)