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


class Menu(Game):
    def __init__(self):
        super().__init__()

    def start_game(self):
        return False

    def show_about_the_game(self, screen):
        screen.fill((0, 0, 0))
        pygame.display.set_caption('Об игре')
        button_back = Button(screen, 150, 300, 200, 80, text='Назад',
                             fontSize=30, margin=20,
                             inactiveColour=(250, 250, 250),
                             pressedColour=(0, 255, 0), radius=0,
                             onClick=None)
        show_menu = True
        while show_menu:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    show_menu = False
                    quit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if (150 < e.pos[0] and e.pos[0] < 150 + 200 and 400 < e.pos[1] and e.pos[1] < 400 + 80):
                        show_menu = False
            button_back.listen(events)
            button_back.draw()
            pygame.display.update()
        return

    def show_trainig_screen(self, screen):
        screen.fill((0, 0, 0))
        pygame.display.set_caption('Обучение')
        button_back = Button(screen, 300, 700, 200, 80, text='Назад',
                             fontSize=30, margin=20,
                             inactiveColour=(250, 250, 250),
                             pressedColour=(0, 255, 0), radius=0,
                             onClick=None)
        show_menu = True
        while show_menu:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    show_menu = False
                    quit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if (500 < e.pos[0] and e.pos[0] < 500 + 200 and 400 < e.pos[1] and e.pos[1] < 400 + 80):
                        show_menu = False
            button_back.listen(events)
            button_back.draw()
            pygame.display.update()
        return

    def main_menu(self, screen):
        screen.fill((0, 0, 0))
        show_main_menu = True
        pygame.display.set_caption('Меню')

        button_play = Button(screen, 500, 150, 200, 100, text='Новая игра',
                             fontSize=30, margin=20,
                             inactiveColour=(250, 250, 250),
                             pressedColour=(0, 255, 0), radius=0,
                             onClick=None)
        button_training = Button(screen, 500, 260, 200, 100, text='Обучение',
                                 fontSize=30, margin=20,
                                 inactiveColour=(250, 250, 250),
                                 pressedColour=(0, 255, 0), radius=0,
                                 onClick=None)
        button_about_the_game = Button(screen, 500, 370, 200, 100, text='Об игре',
                                       fontSize=30, margin=20,
                                       inactiveColour=(250, 250, 250),
                                       pressedColour=(0, 255, 0), radius=0,
                                       onClick=None)
        button_exit = Button(screen, 500, 480, 200, 100, text='Выход',
                             fontSize=30, margin=20,
                             inactiveColour=(250, 250, 250),
                             pressedColour=(0, 255, 0), radius=0,
                             onClick=None)
        while show_main_menu:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    show_main_menu = False
                    pygame.quit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if (500 < e.pos[0] and e.pos[0] < 700 and 150 < e.pos[1] and e.pos[1] < 250):
                        show_main_menu = self.start_game()
                        if not show_main_menu:
                            break
                    if (500 < e.pos[0] and e.pos[0] < 700 and 260 < e.pos[1] and e.pos[1] < 360):
                        self.show_trainig_screen(pygame.display.set_mode((800, 800)))
                    if (500 < e.pos[0] and e.pos[0] < 700 and 370 < e.pos[1] and e.pos[1] < 440):
                        self.show_about_the_game(pygame.display.set_mode((800, 800)))
                    if (500 < e.pos[0] and e.pos[0] < 700 and 480 < e.pos[1] and e.pos[1] < 580):
                        quit()
            bg_menu = pygame.image.load('app/view/images/for_main_menu.jpg')
            screen.blit(bg_menu, (-25, -50))
            button_play.listen(events)
            button_play.draw()
            button_training.listen(events)
            button_training.draw()
            button_about_the_game.listen(events)
            button_about_the_game.draw()
            button_exit.listen(events)
            button_exit.draw()

            pygame.display.update()


if __name__ == '__main__':
    game = Game()