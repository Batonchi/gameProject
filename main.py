import json
import os
import time
import random
import pygame
import pygame.camera
import pygame_widgets

from app.characters.service import CharacterService
from app.sessions.model import GetSession, GetLevel
from database import create_database
from typing import Tuple
from pygame_widgets.textbox import TextBox
from app.characters.model import Character, GetCharacter, CreateCharacter, BackPack, Item
from app.map.model import Map, PlayerCamera, Doors, KeysDoors, Notes, Interactions
from pygame_widgets.button import Button
from app.sessions.service import SessionService, LevelService
from app.texts.model import ShowTextContent
from app.texts.service import GetText, TextService, CreateText, all_dicts

create_database()

FPS = 60


class ErrorWidget:

    def __init__(self, message: str, width: int, height: int, pos: Tuple[int, int] = (0, 0)):
        self.message = str(message)
        self.width = width
        self.height = height
        self.pos = pos
        self.background_color = (255, 0, 0)

    def show(self, screen: pygame.Surface):
        font = pygame.font.SysFont('Arial', 20)
        image = font.render(self.message, True, self.background_color)
        screen.blit(image, (self.pos[0], self.pos[1]))


class Game:
    def __init__(self, name: str):
        self.name = name

        pygame.init()

        pygame.mixer.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE, pygame.SRCALPHA)
        pygame.display.set_caption(name)

        self.w_w, self.w_h = self.screen.get_size()

        self.render_other_window_handler = RenderingOtherWindow(self.screen, int(self.w_w * 1), int(self.w_h * 1), self)
        game_session = SessionService.get_last_session()

        pygame.mixer.music.load(os.path.abspath(os.path.join('app\\music', 'melody_1.mp3')))
        pygame.mixer.music.play(-1, 0.0)

        if game_session is not None:
            (self.render_other_window_handler.types_of_window['main_menu']
            ['buttons_column_groups'][1]['buttons'][1]) = ('continue_game_session-btn', True)
            self.render_other_window_handler.render('main_menu',
                                                    param={'player_name': game_session.player_name,
                                                           'title': self.name})
        else:
            self.render_other_window_handler.render('main_menu',
                                                    param={'title': self.name})


class RenderingOtherWindow:
    def __init__(self, screen: pygame.surface.Surface, w_w: int, w_h: int, link: Game):
        self.player_w_and_h = None
        self.w_and_h_for_map = None
        self.screen = screen
        self.w_w = w_w
        self.w_h = w_h
        self.link = link
        self.all_buttons = []
        self.all_inputs = []
        self.texts = []
        self.returned_errors = []
        self.active_dialogs = []
        self.show = True
        self.base_button_arguments = {
            'win': self.screen,
            'fontSize': 30,
            'margin': 20,
            'inactiveColour': (250, 250, 250),
            'pressedColour': (0, 0, 0),
            'radius': 10,
        }
        self.base_text_box_arguments = {
            'fontSize': 24,
            'borderColour': (255, 255, 255, 0.5),
            'textColour': (255, 255, 255),
            'radius': 10,
            'colour': (0, 0, 0),
            'borderThickness': 1
        }
        self.arguments_for_buttons = {
            'exit-btn': {
                'text': 'выйти из игры',
                'onclick': lambda: quit()
            },
            'back-btn': {
                'text': 'назад',
                'onclick': ''
            },
            'continue_game_session-btn': {
                'text': 'продолжить игру',
                'onclick': lambda: self.starting_game(2)
            },
            'continue_game-btn': {
                'text': 'продолжить',
                'onclick': lambda: self.continue_game_show()
            },
            'new_game_session-btn': {
                'text': 'новая игра',
                'onclick': lambda: self.starting_game(1)
            },
            'about-btn': {
                'text': 'об игре',
                'onclick': lambda: self.show_about_the_game()
            },
            'exit_to_menu-btn': {
                'text': 'выйти в меню',
                'onclick': lambda: self.return_to_menu()
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
                'background-image': 'app/view/images/for_main_menu.jpeg',
                'caption': 'Меню',
                'input_text_box': {
                    1: {
                        'xy_start': (self.w_w // 4, int(self.w_h * 0.95)),
                        'width_height': (self.w_w // 2, self.w_h // 18),
                        'placeholderText': 'ник',
                        'onsubmit': None
                    }
                },
                'buttons_column_groups': {
                    1: {
                        'xy_start': (self.w_w // 3, self.w_h // 4),
                        'width_height': (self.w_w // 3, self.w_h // 12),
                        'gap': 10,
                        'buttons': {
                            1: ('continue_game_session-btn', False),
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
                'background-image': 'app/view/images/training.jpg',
                'caption': 'Обучение/управление',
                'buttons_column_groups': {
                    1: {
                        'xy_start': (self.w_w // 3, self.w_h // 1.2),
                        'width_height': (self.w_w // 3, self.w_h // 12),
                        'gap': 10,
                        'buttons': {
                            1: ('exit_to_menu-btn', True)
                        }
                    }
                }
            },
            'about_the_game_menu': {
                'background-image': 'app/view/images/about_the_game.jpg',
                'caption': 'О игре',
                'buttons_column_groups': {
                    1: {
                        'xy_start': (self.w_w // 3, self.w_h // 1.2),
                        'width_height': (self.w_w // 3, self.w_h // 12),
                        'gap': 10,
                        'buttons': {
                            1: ('exit_to_menu-btn',)
                        }
                    }
                }
            }
        }

        self.particles = Particles(screen, width=w_w, height=w_h)

    def show_training_screen(self):
        self.render('training_menu')

    def show_about_the_game(self):
        self.render('about_the_game_menu')

    def check_errors(self):
        if self.returned_errors:
            for error in self.returned_errors:
                error[0].show(self.screen)

    def render(self, type_window: str, param: dict = None):
        self.show = True
        if self.all_inputs:
            for el in self.all_inputs:
                el.hide()
        if self.all_buttons:
            for el in self.all_buttons:
                el.hide()
        self.texts.clear()
        self.all_inputs.clear()
        self.all_buttons.clear()
        pygame.mouse.set_visible(True)
        data = self.types_of_window.get(type_window)
        if data is None:
            return
        pygame.display.set_caption(data.get('caption', 'Просто окно'))
        if data.get('buttons_column_groups'):
            for column_group in data.get('buttons_column_groups').values():
                self.all_buttons.extend(self.iterate_group_buttons(column_group, 'column'))
        if data.get('buttons_row_groups'):
            for row_group in data.get('buttons_row_groups').values():
                self.all_buttons.extend(self.iterate_group_buttons(row_group, 'row'))
        if data.get('input_text_box'):
            for input_text_box_parameter in data.get('input_text_box').values():
                self.all_inputs.append(self.create_input_box(input_text_box_parameter['xy_start'],
                                                             input_text_box_parameter['width_height'],
                                                             input_text_box_parameter['onsubmit'],
                                                             input_text_box_parameter['placeholderText']))
        if type_window == 'pause_game':
            self.all_buttons[1].onClick = lambda: self.return_to_menu(from_pause=True)
        background_color = self.base_window_arguments['background-color']
        background_image = False
        if data.get('background-image'):
            background_image = pygame.image.load(data['background-image'])
            background_image = pygame.transform.scale(background_image,
                                                      self.base_window_arguments['background-size'])
            self.screen.blit(background_image, self.base_window_arguments['background-position'])
        if param:
            if param.get('player_name'):
                self.all_inputs[0].setText(param.get('player_name'))
            if param.get('title'):
                pygame.display.set_caption(param.get('title')[0])
                self.texts.append((ShowTextContent(GetText(0, json.dumps({'text': param.get('title')})),
                                                   (0, 0, 0), self.w_h // 14,
                                                   (200, 200, 200), (self.w_w // 4.9, self.w_h // 6),
                                                   padding=(10, 10, 10, 10), border_radius=10), 'inline'))
        if self.texts:
            self.texts[-1][0].image.set_alpha(100)
        while self.show:
            self.returned_errors = [error for error in self.returned_errors if error[1] > 0]
            if self.returned_errors:
                for i in range(0, len(self.returned_errors)):
                    self.returned_errors[i] = (self.returned_errors[i][0], self.returned_errors[i][1] - 1)
                    if self.returned_errors[i][1] - 1 == -1:
                        continue
                    self.returned_errors[i][0].show(self.screen)
            self.screen.fill(background_color)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
            if background_image:
                self.screen.blit(background_image, self.base_window_arguments['background-position'])
                self.check_errors()
            if self.texts:
                for text in self.texts:
                    if text[1] == 'inline':
                        text[0].draw_rect_frame_in_full_line(self.screen, 50, self.w_w)
                    text[0].render(self.screen)
            self.particles.update()
            self.particles.render((255, 0, 0) if type_window != 'pause_game' else (255, 255, 255))
            pygame_widgets.update(events)
            pygame.display.update()

    def iterate_group_buttons(self, group: dict, type_group: str) -> list:
        res_buttons = []
        pos_decrease = 0
        for position, button in group.get('buttons', {}).items():
            width, height = group.get('width_height', (100, 20))
            gap = group.get('gap', 10)
            x_y_start = group.get('xy_start', (0, 0))
            if len(button) > 1 and not button[1]:
                pos_decrease += 1
                continue
            if type_group == 'column':
                button = self.create_button(position - pos_decrease, button[0],
                                            width, height, gap, x_y_start, 'y')
                res_buttons.append(button)
            else:
                button = self.create_button(position - pos_decrease, button[0],
                                            width, height, gap, x_y_start, 'x')
                res_buttons.append(button)
        return res_buttons

    def create_button(self, position: int, name_button: str, width: int, height: int,
                      gap: int, x_y_start: Tuple[int, int], x_or_y: str) -> Button:
        x = x_y_start[0]
        y = x_y_start[1]
        if x_or_y == 'x':
            x += position * (width + gap)
        else:
            y += position * (height + gap)
        onclick_func = {
            'exit_to_menu-btn': lambda: self.return_to_menu()
        }
        return Button(self.screen, x, y, width, height,
                      text=self.arguments_for_buttons[name_button]['text'],
                      onClick=(onclick_func.get(name_button)) or (self.arguments_for_buttons[name_button]['onclick']) or
                              (lambda: None),
                      inactiveColour=self.base_button_arguments['inactiveColour'],
                      pressedColour=self.base_button_arguments['pressedColour'],
                      radius=self.base_button_arguments['radius'],
                      fontSize=self.base_button_arguments['fontSize'],
                      margin=self.base_button_arguments['margin'], borderColour=(155, 155, 155), borderThickness=5,
                      font=pygame.font.SysFont('Arial-black', self.base_text_box_arguments['fontSize'], 700))

    def create_input_box(self, xy_start: Tuple[int, int], width_height: Tuple[int, int], placeholder_text: str,
                         onsubmit: object) -> TextBox:
        return TextBox(self.screen, x=xy_start[0] or 0, y=xy_start[1] or 0,
                       width=width_height[0] or 100, height=width_height[1] or 100,
                       placeholderText=placeholder_text or '', onSubmit=onsubmit or None,
                       fontSize=self.base_text_box_arguments['fontSize'],
                       borderColour=self.base_text_box_arguments['borderColour'],
                       textColour=self.base_text_box_arguments['textColour'],
                       radius=self.base_text_box_arguments['radius'],
                       colour=self.base_text_box_arguments['colour'],
                       borderThickness=self.base_text_box_arguments['borderThickness'],
                       font=pygame.font.SysFont('Arial-black', self.base_text_box_arguments['fontSize'], 700))

    def render_level_map_with_param(self, game_class: Game, params: Tuple[GetSession, GetLevel, GetCharacter]):
        pygame.mixer.music.load(os.path.abspath(os.path.join('app\\music', 'melody_4.mp3')))
        pygame.mixer.music.play(-1, 0.0)
        for button in self.all_buttons:
            button.hide()
        for input_box in self.all_inputs:
            input_box.hide()
        self.all_buttons.clear()
        self.all_inputs.clear()
        pygame.display.set_caption('Absolutely Depressive Live')
        running = True
        filename_map = params[1].level_map
        last_name_sim = filename_map.split('.')[0][-1]
        self.w_and_h_for_map = {
            '1': (63, 60),
            '2': (67, 70),
            '3': (64, 70),
        }
        self.player_w_and_h = {
            '1': (game_class.w_w // 80, game_class.w_h // 70),
            '2': (game_class.w_w // 80, game_class.w_h // 70),
            '3': (game_class.w_w // 80, game_class.w_h // 70)
        }
        map_game = Map(filename_map, tile_width=game_class.w_w // self.w_and_h_for_map[last_name_sim][0],
                       tile_height=game_class.w_h // self.w_and_h_for_map[last_name_sim][1])
        game_class.screen.fill((34, 35, 35))
        map_game.render(game_class.screen, 0, 0, 70, 70)
        player_start_xy = map_game.get_character_xy_by_tile_xy(params[1].player_start_x, params[1].player_start_y)
        game_model_character = Character(character=params[2], speed=(self.w_w // 450, self.w_h // 450),
                                         x=player_start_xy[0],
                                         y=player_start_xy[1], tile_width=self.player_w_and_h[last_name_sim][0],
                                         tile_height=self.player_w_and_h[last_name_sim][1])
        backpack = BackPack(15, game_model_character)
        camera = PlayerCamera(game_model_character, 10, 10)
        doors = Doors(map_game.doors, tile_width=self.player_w_and_h[last_name_sim][0],
                      tile_height=self.player_w_and_h[last_name_sim][1],
                      pairs_doors_rects=map_game.rects_doors)
        keys_doors = KeysDoors(self.screen, keys=map_game.keys, tile_width=self.player_w_and_h[last_name_sim][0],
                               tile_height=self.player_w_and_h[last_name_sim][1]
                               )
        notes = Notes(rects=map_game.notes, tile_width=self.player_w_and_h[last_name_sim][0],
                      tile_height=self.player_w_and_h[last_name_sim][0])
        interactions = Interactions(rects=map_game.interactions,
                                    tile_width=self.player_w_and_h[last_name_sim][0],
                                    tile_height=self.player_w_and_h[last_name_sim][1])
        backpack.render(self.screen, self.w_w, self.w_h)
        text = ShowTextContent(GetText(0, json.dumps({'text': 'hfbk,bdfk,bkbnddkbdfdkjb'})),
                               (0, 0, 0), 20,
                               (200, 200, 200), (self.w_w // 4.9, self.w_h // 6),
                               padding=(10, 10, 10, 10), border_radius=10)
        while running:
            pygame.mouse.set_visible(False)
            if not backpack.is_show:
                backpack.show_buttons()
            events = pygame.event.get()
            clock = pygame.time.Clock()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYUP:
                    game_model_character.image = game_model_character.images[0]
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        # локальные переменные, проверяем находится ли игрок в какой-либо зоне
                        result_d = doors.check_rect_in_zone(game_model_character.rect)
                        result_k = keys_doors.check_rect_in_zone(game_model_character.rect)
                        result_n = notes.check_rect_in_zone(game_model_character.rect)
                        if result_d[0]:
                            doors.removing_closed_door(result_d[1])  # если True, удаляем дверь
                        if result_k[0]:
                            if keys_doors.add_taken_key(result_k[1]):
                                free_cell = backpack.get_last_free_cell()
                                if free_cell is not None:
                                    backpack.take(free_cell, Item('hi',
                                                                  {'image': 'key'},
                                                                  lambda: print('hi')))
                        if result_n[0]:
                            if notes.add_taken_note(result_n[1]):
                                free_cell = backpack.get_last_free_cell()
                                if free_cell is not None:
                                    data_for_note = ''  # здесь поолучаем текст из БД для записки
                                    backpack.take(free_cell, Item('hгi',
                                                                  {'image': 'note'},
                                                                  lambda: print('hi')))
                    if event.key == pygame.K_LEFT:
                        backpack.do_unselected(backpack.active_cell_id)
                        backpack.previous_item()
                        backpack.do_selected(backpack.active_cell_id)
                    if event.key == pygame.K_RIGHT:
                        backpack.do_unselected(backpack.active_cell_id)
                        backpack.next_item()
                        backpack.do_selected(backpack.active_cell_id)
                    if event.key == pygame.K_ESCAPE:  # Для меню паузы
                        backpack.close_backpack()
                        game_class.render_other_window_handler.render('pause_game')

            #     if event.type == pygame.K_f:
            #         result_i = interactions.check_rect_in_zone(game_model_character.rect)
            #         if result_i[0]:
            #             # вот здесь мы начинаем диалог с нпс или комментарий ГГ
            #             pass
            #
            result_i = interactions.check_rect_in_zone(game_model_character.rect)  # если игрок заходит в зону "события"
            # Добавляем это событие/взаимодействие в список активных. После обновляем
            if result_i[0]:
                interactions.add_active(result_i[1])

            # Движение игрока нажатием клавиш WASD
            # Получаем прямоугольник на +-скорость, чтобы проверить коллайд со стенами или дверьми, если игрок сталкива-
            # ется с чем либо, он не перемещается на определенное направление (WASD)

            # скорость игрока = (1, 1) (скорость для x и для y)
            if pygame.key.get_pressed()[pygame.K_w]:
                rect = pygame.Rect([game_model_character.rect.x,
                                    game_model_character.rect.y - game_model_character.speed[1],
                                    game_model_character.rect.w,
                                    game_model_character.rect.h])
                if not map_game.collide_with_walls(rect):  # проверяем на столкновения со стенами
                    if not doors.collide_with_doors(rect):  # проверяем на столкновения с дверьми
                        game_model_character.move('down')
            if pygame.key.get_pressed()[pygame.K_s]:
                rect = pygame.Rect([game_model_character.rect.x,
                                    game_model_character.rect.y + game_model_character.speed[1],
                                    game_model_character.rect.w,
                                    game_model_character.rect.h])
                if not map_game.collide_with_walls(rect):  # проверяем на столкновения со стенами
                    if not doors.collide_with_doors(rect):  # проверяем на столкновения с дверьми
                        game_model_character.move('up')
            if pygame.key.get_pressed()[pygame.K_a]:
                rect = pygame.Rect([game_model_character.rect.x - game_model_character.speed[0],
                                    game_model_character.rect.y, game_model_character.rect.w,
                                    game_model_character.rect.h])
                if not map_game.collide_with_walls(rect):  # проверяем на столкновения со стенами
                    if not doors.collide_with_doors(rect):  # проверяем на столкновения с дверьми
                        game_model_character.move('left')
            if pygame.key.get_pressed()[pygame.K_d]:
                rect = pygame.Rect([game_model_character.rect.x + game_model_character.speed[0],
                                    game_model_character.rect.y, game_model_character.rect.w,
                                    game_model_character.rect.h])
                if not map_game.collide_with_walls(rect):  # проверяем на столкновения со стенами
                    if not doors.collide_with_doors(rect):  # проверяем на столкновения с дверьми
                        game_model_character.move('right')

            # различные апдейты, по названию все понятно
            camera.update()

            map_game.update(game_class.screen, camera)
            doors.update(self.screen)
            keys_doors.update(self.screen)
            notes.update(self.screen)
            interactions.update(self.screen)

            # notes.update(self.screen)
            pygame_widgets.update(events)
            game_class.screen.blit(game_model_character.image, (game_model_character.x, game_model_character.y))
            pygame.event.pump()
            pygame.display.flip()
            pygame.display.update()
            clock.tick(FPS)

    def starting_game(self, scene: int):
        if scene == 1:
            result = OnClickFunctions.new_game_session_init(self.all_inputs[0].getText() or 'Sam_Naprosilsy_Cvetochek')
            if isinstance(result, ErrorWidget):
                self.returned_errors.append((result, 40))
                return
        else:
            result = OnClickFunctions.continue_game_session(self.all_inputs[0].getText() or 'Sam_Naprosilsy_Cvetochek')
            if isinstance(result, ErrorWidget):
                self.returned_errors.append((result, 40))
                return
        self.render_level_map_with_param(self.link, result)

    def return_to_menu(self, from_pause: bool = False):
        game_session = SessionService.get_last_session()
        if pygame.mixer.music.get_busy() and from_pause:
            pygame.mixer.music.load(os.path.abspath(os.path.join('app\\music', 'melody_3.mp3')))
            pygame.mixer.music.play(-1, 0.0)
        if game_session is not None:
            (self.types_of_window['main_menu']
            ['buttons_column_groups'][1]['buttons'][1]) = ('continue_game_session-btn', True)
            self.render('main_menu', param={'player_name': game_session.player_name,
                                            'title': 'Absolutely Depressive Live'})
        self.render(type_window='main_menu', param={'title': 'Absolutely Depressive Live'})

    def continue_game_show(self):
        self.show = False
        game_class = self.link
        for button in self.all_buttons:
            button.hide()
        self.all_buttons.clear()
        last_session = SessionService.get_last_session()
        map_path = LevelService.get_level_by_id(last_session.level_id).level_map
        last_name_sim = map_path.split('\\')[-1].split('.')[0][-1]
        map_game = Map(map_path, tile_width=game_class.w_w // self.w_and_h_for_map[last_name_sim][0],
                       tile_height=game_class.w_h // self.w_and_h_for_map[last_name_sim][1])
        self.screen.fill((34, 35, 35))
        map_game.render(self.screen, 0, 0, 70, 70)


class OnClickFunctions:

    @staticmethod
    def new_game_session_init(player_name: str) -> Tuple[GetSession, GetLevel, GetCharacter] or ErrorWidget:
        create_session = SessionService.create(player_name)
        if create_session is not None:
            return ErrorWidget(create_session[1], 1000, 100, (0, 0))
        CharacterService.create(CreateCharacter(character_name=player_name, info={
            'emotional_health': 100,
            'is_npc': False,
            'permissions': {
                'may_move': True,
                'may_speak': True,
                'may_use_items': True,
                'may_have_backpack': True,
                'may_heal': True,
                'may_see': True
            }
        }))
        get_character = CharacterService.get_character_by_name(player_name)
        get_session = SessionService.get_session_by_player_name(player_name)
        level_id = get_session.level_id
        get_level = LevelService.get_level_by_id(level_id)
        return get_session, get_level, get_character

    @staticmethod
    def continue_game_session(player_name: str) -> Tuple[GetSession, GetLevel, GetCharacter] or ErrorWidget:
        get_session = SessionService.get_session_by_player_name(player_name)
        if get_session is None:
            return ErrorWidget(get_session[1], 1000, 100, (0, 0))
        get_character = CharacterService.get_character_by_name(player_name)
        get_level = LevelService.get_level_by_id(get_session.level_id)
        return get_session, get_level, get_character


class Particles:  # класс частиц
    def __init__(self, screen, width: int, height: int):
        self.width, self.height = width, height
        self.screen = screen
        self.particles = []  # список всех живых частиц, которые будут отрисовываться

    def update(self):
        # создаем частицу, которая имеет свою позицию (рандомную), скорость и жизнь (жизнь нужна для затухания частицы)
        particle = {
            'pos': [
                random.randint(0, self.width),
                random.randint(0, self.height)
            ],
            'velocity': [
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            ],
            'life': 128

        }
        self.particles.append(particle)  # добавляем в список частиц

        for p in self.particles:
            # меняем позицию с помощью скорости и уменьшаем жизнь частицы
            p['pos'][0] += p['velocity'][0]
            p['pos'][1] += p['velocity'][1]
            p['life'] -= 1

            if p['life'] <= 0:
                self.particles.remove(p)

    def render(self, color):  # отрисовка
        for p in self.particles:
            k = p['life'] / 128  # коэффициент, для того чтобы менять цвет.
            pygame.draw.circle(self.screen, (color[0] * k, color[1] * k, color[2] * k), p['pos'], 2)


if __name__ == '__main__':
    # for el in all_dicts:
    #     TextService.save(CreateText(el))
    # with open('notes_text.txt', 'r', encoding='utf-8') as f:
    #     for text in f.readlines():
    #         TextService.save(CreateText({'text': text, 'next': None}))

    game = Game('Absolutely Depressive Live')
