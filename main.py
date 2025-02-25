import pygame
import pygame.camera
import pygame_widgets

from database import create_database
from typing import Tuple
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from app.characters.model import Character
from app.map.model import Map, PlayerCamera, Doors, KeysDoors, Notes
from pygame_widgets.button import Button
from app.sessions.service import SessionService


create_database()

FPS = 60


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        pygame.display.set_caption('Game')

        self.w_w, self.w_h = self.screen.get_size()

        self.render_other_window_handler = RenderingOtherWindow(self.screen, self.w_w, self.w_h, self)
        self.render_other_window_handler.render('main_menu')


class RenderingOtherWindow:
    def __init__(self, screen: pygame.surface.Surface, w_w: int, w_h: int, link: Game):
        self.screen = screen
        self.w_w = w_w
        self.w_h = w_h
        self.link = link
        self.all_buttons = []
        self.base_button_arguments = {
            'win': self.screen,
            'fontSize': 30,
            'margin': 20,
            'inactiveColour': (250, 250, 250),
            'pressedColour': (0, 0, 0),
            'radius': 50,
        }
        self.text_box_arguments = {
            'fontSize': 24,
            'borderColour': (255, 255, 255),
            'textColour': (255, 255, 255),
            'radius': 50,
            'colour': (0, 0, 0),
            'borderThickness': 5
        }
        self.arguments_for_buttons = {
            'exit-btn': {
                'text': 'выйти из игры',
                'onclick': lambda: quit()
            },
            'start_game-btn': {
                'text': 'начать игру',
                'onclick': lambda: self.render_main_game_window(self.link)
            },
            'back-btn': {
                'text': 'назад',
                'onclick': ''
            },
            'continue_game_session-btn': {
                'text': 'продолжить игру',
                'onclick': lambda: self.render_main_game_window(self.link)
            },
            'continue_game-btn': {
                'text': 'продолжить',
                'onclick': lambda: self.render_main_game_window(self.link)
            },
            'new_game_session-btn': {
                'text': 'новая игра',
                'onclick': ''
            },
            'about-btn': {
                'text': 'о игре',
                'onclick': lambda: self.show_about_the_game()
            },
            'exit_to_menu-btn': {
                'text': 'выйти в меню',
                'onclick': ''
            },
            'train-btn': {
                'text': 'обучение',
                'onclick': lambda: self.show_training_screen()
            },
            'exit_note-btn': {
                'onclick': ''
            }
        }
        self.base_window_arguments = {
            'background-position': (0, 0),
            'background-size': (self.w_w, self.w_h),
            'background-color': (0, 0, 0),
        }
        # здесь надо будет написать какие окна тееб нада
        # если что кнопки тоже можешь добавить
        self.types_of_window = {
            'main_menu': {
                'background-image': 'app/view/images/for_main_menu.jpg',
                'caption': 'Меню',
                'input_text_box': {
                    1: {
                        'xy_strat': (self.w_w / 2, self.w_h / 2),
                        'width_height': (self.w_w // 3, self.w_h // 12),
                        'placeholderText': 'ник',
                        'onsubmit': ''
                    }
                },
                'buttons_column_groups': {
                    1: {
                        'xy_start': (self.w_w // 3, self.w_h // 4),
                        'width_height': (self.w_w // 3, self.w_h // 12),
                        'gap': 10,
                        'buttons': {
                            1: ('start_game-btn', 'continue_game_session-btn'),
                            2: ('new_game_session-btn',),
                            3: ('train-btn',),
                            4: ('about-btn',),
                            5: ('exit-btn',),
                        }
                    }
                }
            },
            'pause_game': {
                'caption': 'Игра приостановлена',
                'buttons_column_groups': {
                    1: {
                        'xy_start': (self.w_w // 3, self.w_h // 4),
                        'width_height': (self.w_w // 3, self.w_h // 12),
                        'gap': 10,
                        'buttons': {
                            1: ('continue_game-btn',),
                            2: ('exit_to_menu-btn',),
                            3: ('exit-btn',)
                        }
                    }
                }
            },
            'training_menu': {
                'background-image': 'app/view/images/training.png',
                'caption': 'Обучение/управление',
                'buttons_column_groups': {
                    1: {
                        'xy_start': (self.w_w // 3, self.w_h // 1.3),
                        'width_height': (self.w_w // 3, self.w_h // 12),
                        'gap': 10,
                        'buttons': {
                            1: ('exit_to_menu-btn',)
                        }
                    }
                }
            },
            'about_the_game_menu': {
                'caption': 'О игре',
                'buttons_column_groups': {
                    1: {
                        'xy_start': (self.w_w // 3, self.w_h // 1.3),
                        'width_height': (self.w_w // 3, self.w_h // 12),
                        'gap': 10,
                        'buttons': {
                            1: ('exit_to_menu-btn',)
                        }
                    }
                }
            }
        }

    def show_training_screen(self):
        self.render('training_menu')

    def show_about_the_game(self):
        self.render('about_the_game_menu')

    def render(self, type_window: str):
        for button in self.all_buttons:
            button.hide()
        self.all_buttons.clear()

        pygame.mouse.set_visible(True)

        data = self.types_of_window.get(type_window)
        if data is None:
            return
        pygame.display.set_caption(data.get('caption', 'Просто окно'))
        self.all_buttons = []
        if data.get('buttons_column_groups'):
            for column_group in data.get('buttons_column_groups').values():
                self.all_buttons.extend(self.iterate_group_buttons(column_group, 'column'))
        if data.get('buttons_row_groups'):
            for row_group in data.get('buttons_row_groups').values():
                self.all_buttons.extend(self.iterate_group_buttons(row_group, 'row'))
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
                    quit()
            if background_image:
                self.screen.blit(background_image, self.base_window_arguments['background-position'])
            pygame_widgets.update(events)
            pygame.display.update()
            # in func we need return caption_name

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
                      onClick=(self.arguments_for_buttons[name_button]['onclick'] if name_button != 'exit_to_menu-btn'
                               else (lambda: self.render('main_menu'))) or (lambda: None),
                      inactiveColour=self.base_button_arguments['inactiveColour'],
                      pressedColour=self.base_button_arguments['pressedColour'],
                      radius=self.base_button_arguments['radius'],
                      fontSize=self.base_button_arguments['fontSize'],
                      margin=self.base_button_arguments['margin'])

    def render_main_game_window(self, game_class: Game):
        for button in self.all_buttons:
            button.hide()
        self.all_buttons.clear()

        pygame.display.set_caption('Game')
        running = True
        filename_map = 'map_level1.tmx'
        map_game = Map(filename_map, tile_width=game_class.w_w // 100, tile_height=game_class.w_h // 100)
        game_class.screen.fill((34, 35, 35))
        map_game.render(game_class.screen, 0, 0, 100, 100)
        player_start_xy = map_game.get_character_xy_by_tile_xy(30, 35)
        character = Character('character', tile_width=game_class.w_w // 125, tile_height=game_class.w_h // 110,
                              speed=(2, 2), x=player_start_xy[0], y=player_start_xy[1])
        camera = PlayerCamera(character, 10, 10)
        doors = Doors(map_game.doors, tile_width=self.w_w // 100, tile_height=self.w_h // 100,
                      pairs_doors_rects=map_game.rects_doors)
        keys_doors = KeysDoors(self.screen, keys=map_game.keys, tile_width=self.w_w // 100, tile_height=self.w_h // 100
                              )
        notes = Notes(rects=map_game.notes, tile_width=self.w_w // 100, tile_height=self.w_h // 100)
        while running:
            pygame.mouse.set_visible(False)
            events = pygame.event.get()
            clock = pygame.time.Clock()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        result_d = doors.check_rect_in_zone(character.rect)
                        result_k = keys_doors.check_rect_in_zone(character.rect)
                        result_n = notes.check_rect_in_zone(character.rect)
                        if result_d[0]:
                            doors.removing_closed_door(result_d[1])
                        if result_k[0]:
                            keys_doors.add_taken_key(result_k[1])
                            # здесь еще нужно дописать, чтобы в инвентарь ключ добавлялся

                        if result_n[0]:
                            notes.add_taken_note(result_n[1])

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_class.render_other_window_handler.render('pause_game')
            if pygame.key.get_pressed()[pygame.K_w]:
                rect = pygame.Rect([character.rect.x, character.rect.y - character.speed[1], character.rect.w,
                                    character.rect.h])
                if not map_game.collide_with_walls(rect):
                    if not doors.collide_with_doors(rect):
                        character.move('down')
            if pygame.key.get_pressed()[pygame.K_s]:
                rect = pygame.Rect([character.rect.x, character.rect.y + character.speed[1], character.rect.w,
                                    character.rect.h])
                if not map_game.collide_with_walls(rect):
                    if not doors.collide_with_doors(rect):
                        character.move('up')
            if pygame.key.get_pressed()[pygame.K_a]:
                rect = pygame.Rect([character.rect.x - character.speed[0], character.rect.y, character.rect.w,
                                    character.rect.h])
                if not map_game.collide_with_walls(rect):
                    if not doors.collide_with_doors(rect):
                        character.move('left')
            if pygame.key.get_pressed()[pygame.K_d]:
                rect = pygame.Rect([character.rect.x + character.speed[0], character.rect.y, character.rect.w,
                                    character.rect.h])
                if not map_game.collide_with_walls(rect):
                    if not doors.collide_with_doors(rect):
                        character.move('right')

            camera.update()

            map_game.update(game_class.screen, camera)
            doors.update(self.screen)
            keys_doors.update(self.screen)
            notes.update(self.screen)

            game_class.screen.blit(character.image, (character.x, character.y))
            pygame.event.pump()
            pygame.display.flip()
            pygame.display.update()
            clock.tick(FPS)


class OnClickFunctions:

    @staticmethod
    def new_game_session_start():
        pass

    @staticmethod
    def about():
        pass

    @staticmethod
    def continue_game_session():
        pass


if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.music.load("Stop Watch OST — The Binding"
                            " of Isaac_ Antibirth Journey from a Jar to the Sky (www.lightaudio.ru).mp3")
    pygame.mixer.music.play(-1, 0.0)
    game = Game()