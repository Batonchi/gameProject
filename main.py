import pygame
import pygame.camera

from database import Connection, create_database
from app.characters.model import Character
from app.map.model import Map, PlayerCamera
from pygame_widgets.button import Button

pygame.init()
create_database()

FPS = 60


from typing import Tuple

import pygame
import os
import pygame.camera

from database import create_database
from app.characters.model import Character
from app.map.model import Map, PlayerCamera
from pygame_widgets.button import Button

pygame.init()
create_database()

FPS = 60


class Game:
    def init(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        pygame.display.set_caption('Game')

        w_w, w_h = self.screen.get_size()

        render_other_window_handler = self.RenderingOtherWindow(self.screen, w_w, w_h)
        render_other_window_handler.render('Меню')

        running = True

        filename_map = 'map_level1.tmx'
        map_game = Map(filename_map, tile_width=w_w // 100, tile_height=w_h // 100)
        self.screen.fill((34, 35, 35))
        map_game.render(self.screen, 0, 0, 100, 100)
        character = Character('character', tile_width=w_w // 150, tile_height=w_h // 75,
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
                        render_other_window_handler.render('pause_game')
            if pygame.key.get_pressed()[pygame.K_w]:
                rect = pygame.Rect([character.rect.x, character.rect.y - character.speed[1], character.rect.w,
                                    character.rect.h])
                if not map_game.check_tiles(rect):
                    character.move('down')
            if pygame.key.get_pressed()[pygame.K_s]:
                rect = pygame.Rect([character.rect.x, character.rect.y + character.speed[1], character.rect.w,
                                    character.rect.h])
                if not map_game.check_tiles(rect):
                    character.move('up')
            if pygame.key.get_pressed()[pygame.K_a]:
                rect = pygame.Rect([character.rect.x - character.speed[0], character.rect.y, character.rect.w,
                                    character.rect.h])
                if not map_game.check_tiles(rect):
                    character.move('left')
            if pygame.key.get_pressed()[pygame.K_d]:
                rect = pygame.Rect([character.rect.x + character.speed[0], character.rect.y, character.rect.w,
                                    character.rect.h])
                if not map_game.check_tiles(rect):
                    character.move('right')
            camera.update()
            map_game.update(self.screen, camera)
            self.screen.blit(character.image, (character.x, character.y))
            camera.update()
            pygame.event.pump()
            pygame.display.flip()
            pygame.display.update()
            clock.tick(FPS)


class RenderingOtherWindow:
    def init(self, screen: pygame.surface.Surface, w_w: int, w_h: int):
        self.screen = screen
        self.w_w = w_w
        self.w_h = w_h
        self.base_button_arguments = {
            'win': self.screen,
            'fontSize': 30,
            'margin': 20,
            'inactiveColour': (250, 250, 250),
            'pressedColour': (0, 255, 0),
            'radius': 50
        }
        self.arguments_for_buttons = {
            'exit-btn': {
                'text': 'выйти из игры',
                'onclick': ''
            },
            'start_game-btn': {
                'text': 'начать игру',
                'onclick': ''
            },
            'back-btn': {
                'text': 'назад',
                'onclick': ''
            },
            'continue_game_session-btn': {
                'text': 'продолжить игру',
                'onclick': ''
            },
            'continue_game-btn': {
                'text': 'продолжить',
                'onclick': ''
            },
            'new_game_session-btn': {
                'text': 'новая игра',
                'onclick': ''
            },
            'about-btn': {
                'text': 'о игре',
                'onclick': ''
            },
            'exit_to_menu-btn': {
                'text': 'вытии в меню',
                'onclick': ''
            },
            'train-btn': {
                'text': 'обучение',
                'onclick': ''
            },
            'exit_note-btn': {
                'onclick': ''
            }
        }
        self.base_window_arguments = {
            'background-position': (0, 0),
            'background-size': (self.w_w, self.w_h),
            'background-color': (255, 255, 255),
        }
        # здесь надо будет написать какие окна тебе нужны
        # если что кнопки тоже можешь добавить
        self.types_of_window = {
            'main_menu': {
                'background-image': 'app/view/images/for_main_menu.jpg',
                'caption': 'Меню',
                'buttons_column_groups': {
                    1: {
                        'xy_start': (self.w_w // 3, self.w_h // 6),
                        'width_height': (self.w_w // 10, self.w_h // 15),
                        'gap': 10,
                        'buttons': {
                            1: ('start_game-btn', 'continue_game_session-btn'),
                            2: ('new_game_session-btn',),
                            3: ('about-btn',),
                            4: ('exit-btn',),
                        }
                    }
                }
            },
            'pause_game': {
                'caption': 'Игра приостановлена',
                'buttons_column_groups': {
                    1: {
                        'xy_start': (self.w_w // 3, self.w_h // 6),
                        'width_height': (self.w_w // 10, self.w_h // 15),
                        'gap': 10,
                        'buttons': {
                            1: ('continue_game-btn',),
                            2: ('exit_to_menu-btn',),
                            3: ('exit-btn',)
                        }
                    }
                }
            },
        }

    def render(self, type_window: str):
        data = self.types_of_window.get(type_window)
        if data is None:
            return
        pygame.display.set_caption(data.get('caption', 'Просто окно'))
        all_buttons = []
        if data.get('buttons_column_groups'):
            for column_group in data.get('buttons_column_groups').values():
                all_buttons.extend(self.iterate_group_buttons(column_group, 'column'))
        if data.get('buttons_row_groups'):
            for row_group in data.get('buttons_row_groups').values():
                all_buttons.extend(self.iterate_group_buttons(row_group, 'row'))
        background_color = self.base_window_arguments['background-color']
        background_image = False
        if data.get('background-image'):
            background_image = pygame.image.load(data['background-image'])
            background_image = pygame.transform.scale(background_image,
                                                      self.base_window_arguments['background-size'])
            self.screen.blit(background_image, self.base_window_arguments['background-position'])
        show = True
        while show:
            self.screen.fill(background_color)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    show = False
                    quit()
            if background_image:
                self.screen.blit(background_image, self.base_window_arguments['background-position'])
            for button in all_buttons:
                button.listen(events)
                button.draw()
            pygame.display.update()

    def iterate_group_buttons(self, group: dict, type_group: str) -> list:
        res_buttons = []
        for position, button in group.get('buttons', {}).items():
            width, height = group.get('width_height', (100, 20))
            gap = group.get('gap', 10)
            x_y_start = group.get('xy_start', (0, 0))
            if type_group == 'column':
                res_buttons.append(self.create_button(position, button[0], width, height, gap, x_y_start, 'y'))
            else:
                res_buttons.append(self.create_button(position, button[0], width, height, gap, x_y_start, 'x'))
        return res_buttons

    def create_button(self, position: int, name_button: str, width: int, height: int,
                      gap: int, x_y_start: Tuple[int, int], x_or_y: str) -> Button:
        x = x_y_start[0]
        y = x_y_start[1]
        if x_or_y == 'x':
            x += position * (width + gap)
        else:
            y += position * (height + gap)
        return Button(self.screen, x, y, width, height,
                      text=self.arguments_for_buttons[name_button]['text'],
                      onClick=self.arguments_for_buttons[name_button]['onclick'],
                      inactiveColour=self.base_button_arguments[name_button]['inactiveColour'],
                      pressedColour=self.base_button_arguments[name_button]['pressedColour'],
                      radius=self.base_button_arguments[name_button]['radius'],
                      fontSize=self.base_button_arguments[name_button]['fontSize'],
                      margin=self.base_button_arguments[name_button]['margin'])

class ButtonsOnClickFunctions:
    # этот класс где методы все со @staticmethods,
    # то есть вызываються без иницилизации класса
    pass


if __name__ == '__main__':
    game = Game()