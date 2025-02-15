import pygame
import pygame.camera

from database import Connection, create_database
from app.characters.model import Character
from app.map.model import Map, PlayerCamera
from pygame_widgets.button import Button

pygame.init()
create_database()

FPS = 60


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        pygame.display.set_caption('Game')

        w_w, w_h = self.screen.get_size()

        menu = Menu(self.screen, w_w, w_h)
        menu_in_game = MenuInGame(self.screen, w_w, w_h)
        menu.main_menu(self.screen)

        running = True

        filename_map = 'map_level1.tmx'
        map_game = Map(filename_map, tile_width=w_w // 100, tile_height=w_h // 100)
        self.screen.fill((34, 35, 35))
        map_game.render(self.screen, 0, 0, 100, 100)
        character = Character('character', tile_width=w_w // 100, tile_height=w_h // 100,
                              speed=(1, 1))
        camera = PlayerCamera(character, 10, 10)
        while running:
            events = pygame.event.get()
            clock = pygame.time.Clock()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu_in_game.game_menu()
            if pygame.key.get_pressed()[pygame.K_w]:
                if not map_game.check_tiles(character.rect):
                    character.move('up')
            if pygame.key.get_pressed()[pygame.K_a]:
                character.move('left')
            if pygame.key.get_pressed()[pygame.K_s]:
                character.move('down')
            if pygame.key.get_pressed()[pygame.K_d]:
                character.move('right')
            camera.update()
            map_game.update(self.screen, camera)
            self.screen.blit(character.image, (character.x, character.y))

            camera.update()
            pygame.event.pump()
            pygame.display.flip()
            pygame.display.update()
            clock.tick(FPS)

    def start(self):
        pass

    def end(self):
        pass


class Menu:
    def __init__(self, screen, w, h):
        self.screen = screen
        self.w = w
        self.h = h

    def show_about_the_game(self, screen):
        screen.fill((0, 0, 0))
        pygame.display.set_caption('Об игре')
        button_back = Button(screen, self.w // 12, self.h - 120, 100, 80, text='Назад',
                             fontSize=30, margin=20,
                             inactiveColour=(250, 250, 250),
                             pressedColour=(0, 255, 0), radius=50,
                             onClick=None, textVAlign='center', textHAlign='center')
        show_menu = True
        while show_menu:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    show_menu = False
                    quit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if (self.w // 12 < e.pos[0] < self.w // 12
                            + 200 and self.h - 120 < e.pos[1] < self.h - 120 + 80):
                        show_menu = False
            button_back.listen(events)
            button_back.draw()
            pygame.display.update()
        return

    def show_trainig_screen(self, screen):
        screen.fill((0, 0, 0))
        pygame.display.set_caption('Обучение')
        button_back = Button(screen, self.w // 12, self.h - 120, 100, 80, text='Назад',
                             fontSize=30, margin=20,
                             inactiveColour=(250, 250, 250),
                             pressedColour=(0, 255, 0), radius=0,
                             onClick=None, textVAlign='center', textHAlign='center')
        show_menu = True
        while show_menu:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    show_menu = False
                    quit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if (self.w // 12 < e.pos[0] < self.w // 12
                            + 200 and self.h - 120 < e.pos[1] < self.h - 120 + 80):
                        show_menu = False
            button_back.listen(events)
            button_back.draw()
            pygame.display.update()
        return

    def main_menu(self, screen):
        screen.fill((0, 0, 0))
        show_main_menu = True
        pygame.display.set_caption('Меню')

        button_play = Button(screen, self.w // 1.5, 150, self.w // 5, self.h // 15, text='Новая игра',
                             fontSize=30,
                             inactiveColour=(250, 250, 250),
                             pressedColour=(0, 255, 0), radius=50,
                             onClick=None, textVAlign='center', textHAlign='center')
        button_training = Button(screen, self.w // 1.5, 260, self.w // 5, self.h // 15, text='Обучение',
                                 fontSize=30, margin=20,
                                 inactiveColour=(250, 250, 250),
                                 pressedColour=(0, 255, 0), radius=50,
                                 onClick=None, textVAlign='center', textHAlign='center')
        button_about_the_game = Button(screen, self.w // 1.5, 370, self.w // 5, self.h // 15, text='Об игре',
                                       fontSize=30, margin=20,
                                       inactiveColour=(250, 250, 250),
                                       pressedColour=(0, 255, 0), radius=50,
                                       onClick=None, textVAlign='center', textHAlign='center')
        button_exit = Button(screen, self.w // 1.5, 480, self.w // 5, self.h // 15, text='Выход',
                             fontSize=30, margin=20,
                             inactiveColour=(250, 250, 250),
                             pressedColour=(0, 255, 0), radius=50,
                             onClick=None, textVAlign='center', textHAlign='center')
        bg_menu = pygame.image.load('app/view/images/for_main_menu.jpg')
        bg_menu = pygame.transform.scale(bg_menu, (self.w, self.h))
        while show_main_menu:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    show_main_menu = False
                    pygame.quit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if (self.w // 1.5 < e.pos[0] < (self.w // 1.5 + self.w // 5)
                            and 150 < e.pos[1] < 150 + self.h // 7):
                        show_main_menu = False
                    if (self.w // 1.5 < e.pos[0] < (self.w // 1.5 + self.w // 5)
                            and 260 < e.pos[1] < 260 + self.h // 7):
                        self.show_trainig_screen(screen)
                    if (self.w // 1.5 < e.pos[0] < (self.w // 1.5 + self.w // 5)
                            and 370 < e.pos[1] < 370 + self.h // 7):
                        self.show_about_the_game(screen)
                    if (self.w // 1.5 < e.pos[0] < (self.w // 1.5 + self.w // 5)
                            and 480 < e.pos[1] < 460 + self.h // 7):
                        quit()
            screen.blit(bg_menu, (0, 0))
            button_play.listen(events)
            button_play.draw()
            button_training.listen(events)
            button_training.draw()
            button_about_the_game.listen(events)
            button_about_the_game.draw()
            button_exit.listen(events)
            button_exit.draw()

            pygame.display.update()


class MenuInGame:
    def __init__(self, screen, w, h):
        self.screen = screen
        self.w, self.h = w, h

    def game_menu(self):
        self.screen.fill((0, 0, 0))
        show_game_menu = True
        button_play = Button(self.screen, self.w // 1.5, 150, self.w // 5, self.h // 7, text='Продолжить',
                             fontSize=30, margin=20,
                             inactiveColour=(250, 250, 250),
                             pressedColour=(0, 255, 0), radius=0,
                             onClick=None)
        button_exit = Button(self.screen, self.w // 1.5, 260, self.w // 5, self.h // 7, text='Выход',
                             fontSize=30, margin=20,
                             inactiveColour=(250, 250, 250),
                             pressedColour=(0, 255, 0), radius=0,
                             onClick=None)
        bg_menu = pygame.image.load('app/view/images/for_main_menu.jpg')
        bg_menu = pygame.transform.scale(bg_menu, (self.w, self.h))
        while show_game_menu:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    show_game_menu = False
                    pygame.quit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if (self.w // 1.5 < e.pos[0] < (self.w // 1.5 + self.w // 5)
                            and 150 < e.pos[1] < 150 + self.h // 7):
                        print('IN')
                        show_game_menu = False
                    if (self.w // 1.5 < e.pos[0] < (self.w // 1.5 + self.w // 5)
                            and 260 < e.pos[1] < 260 + self.h // 7):
                        quit()

            self.screen.blit(bg_menu, (0, 0))
            button_play.listen(events)
            button_play.draw()
            button_exit.listen(events)
            button_exit.draw()

            pygame.display.update()


class EndWindow:
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
