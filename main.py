import json
import os
import random
import pygame
import pygame.camera
import pygame_widgets

from app.characters.service import CharacterService, npc_inform
from random import randint
from database import create_database, reset_bd
from typing import Tuple
from pygame_widgets.textbox import TextBox
from app.characters.model import Character, GetCharacter, CreateCharacter, BackPack, Item
from app.map.model import Map, PlayerCamera, Doors, KeysDoors, Notes, Interactions
from pygame_widgets.button import Button
from app.sessions.service import SessionService, LevelService, GetSession, Level, base_levels
from app.texts.model import ShowTextContent
from app.texts.service import GetText, TextService, CreateText, all_dicts, mind_gg_id, author_words_id

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


class Cross:
    def __init__(self):
        self.replicas = ['ТвоюБогаДушуМать!!',  'Боже, дай мне сил',
                         'Бог видит и слышит, но, похоже, не всегда отвечает.', 'Боже, где я?',
                         'Скучно каждый раз к Богу обращаться: Андрей, дай мне сил!!',
                         'В нашем культе не принято теряться',
                         'С крестом в кармане — куда угодно! Хоть в ад, хоть в рай!',
                         'Заблудился в жизни? Крестик в руках — компас не потеряешь!']  # фразы. Типо прикольно

    def show_text(self, screen, alpha):  # показывает текст в верхем левом углу
        font = pygame.font.SysFont('Arial-black', 20)
        text_surface = font.render(random.choice(self.replicas), True, (255, 0, 0))
        text_surface.set_alpha(alpha)  # Устанавливаем уровень прозрачности
        screen.blit(text_surface, (0, 5))


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
        self.mind_rects = None
        self.for_second_level_mind_hero = None
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
            'reset_bd-btn': {
                'text': 'сброс прогресса',
                'onclick': lambda: self.reset_btn_func()
            }
        }
        self.base_window_arguments = {
            'background-position': (0, 0),
            'background-size': (self.w_w, self.w_h),
            'background-color': (0, 0, 0),
        }
        # здесь надо будет написать какие окна тыеб нада
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
                            5: ('reset_bd-btn',),
                            6: ('exit-btn',)
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
                        'width_height': (self.w_w // 3, self.w_h // 14),
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
                        'width_height': (self.w_w // 3, self.w_h // 14),
                        'gap': 10,
                        'buttons': {
                            1: ('exit_to_menu-btn',)
                        }
                    }
                }
            },
            'final_window': {
                'caption': 'The end',
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

    def reset_btn_func(self):
        reset_bd()
        cell = self.types_of_window['main_menu']['buttons_column_groups'][1]['buttons'][1]
        self.types_of_window['main_menu']['buttons_column_groups'][1]['buttons'][1] = (cell[0], False)
        self.return_to_menu()

    def show_training_screen(self):
        self.render('training_menu')

    def show_about_the_game(self):
        self.render('about_the_game_menu')

    def draw_text(self, text: str, alpha, y: int = 0):
        size = 64 if text == 'The End' else 30
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_surface.set_alpha(alpha)  # Устанавливаем уровень прозрачности
        center = (self.w_w // 2, self.w_h // 6) if text == 'The End' else (self.w_w // 2, self.w_h // 4 + y)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect)

    def show_final_window(self):
        self.render('final_window')

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
        clock = pygame.time.Clock()
        alpha, y = 0, 0
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
            if type_window == 'final_window':
                if alpha < 255:
                    alpha += 2  # Увеличиваем на 2 каждый кадр
                else:
                    alpha = 255
                self.draw_text(f'The End', alpha)
                for el in SessionService.get_name_player_and_date()[:10]:
                    y += 30
                    self.draw_text(f'nickname: {el[0]} - start: {el[1]}', alpha, y)
            y = 0
            self.particles.update()
            self.particles.render((255, 0, 0) if type_window != 'pause_game' and type_window != 'final_window'
                                  else (255, 255, 255))
            pygame_widgets.update(events)
            pygame.display.update()
            pygame.display.flip()
            clock.tick(60)

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

    def render_level_map_with_param(self, game_class: Game, params: Tuple[GetSession, Level, GetCharacter]):
        if params[1].level_id == 1:
            self.for_second_level_mind_hero = [ShowTextContent(TextService.get_text_by_id(text_id), (255, 255, 255),
                                                               16, (0, 0, 0),
                                                               (0, int(self.w_h // 1.3)),
                                                               (10, 10, 10, 10)) for text_id in mind_gg_id]
            self.mind_rects = {}
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
        doors = Doors(level_map=int(filename_map[9]), doors_rects=map_game.doors,
                      tile_width=game_class.w_w // self.w_and_h_for_map[last_name_sim][0],
                      tile_height=game_class.w_h // self.w_and_h_for_map[last_name_sim][1],
                      pairs_doors_rects=map_game.rects_doors)
        keys_doors = KeysDoors(keys=map_game.keys, tile_width=self.player_w_and_h[last_name_sim][0],
                               tile_height=self.player_w_and_h[last_name_sim][1])
        notes = Notes(rects=map_game.notes, tile_width=self.player_w_and_h[last_name_sim][0],
                      tile_height=self.player_w_and_h[last_name_sim][0])
        if params[1].level_id == 0:
            SessionService.update_inf({'no_use_notes': [i for i in range(33, 33 + len(notes.rects_notes))]},
                                      params[0].player_name)
        elif params[1].level_id == 1:
            SessionService.update_inf({'no_use_notes': [i for i in range(37, 37 + len(notes.rects_notes))]},
                                      params[0].player_name)
        else:
            SessionService.update_inf({'no_use_notes': [i for i in range(40, 40 + len(notes.rects_notes))]},
                                      params[0].player_name)
        note_text_id = {}
        notes_text_ids = json.loads(SessionService.get_last_session().inf)['no_use_notes']
        for rect in notes.zone_rects_notes:
            note_text_id[(rect.x, rect.y)] = notes_text_ids[notes.zone_rects_notes.index(rect)]
        interactions = Interactions(rects=map_game.interactions,
                                    tile_width=self.player_w_and_h[last_name_sim][0],
                                    tile_height=self.player_w_and_h[last_name_sim][1])
        cross = Cross()
        if self.mind_rects is not None:
            for rect in interactions.rects_interaction:
                self.mind_rects[(rect.x, rect.y)] = (self.for_second_level_mind_hero
                                                     .pop(randint(0, len(self.for_second_level_mind_hero) - 1)))
        backpack.render(self.screen, self.w_w, self.w_h)
        npc = []
        npc_xy = []
        npc_rects = []
        characters = CharacterService.get_all_npc_characters()
        for data_character in characters:
            npc_on_map = data_character.get_characters_by_level_num(params[1].level_id + 1)
            for one_npc in npc_on_map:
                npc.append(Character(one_npc, tile_width=self.player_w_and_h[last_name_sim][0],
                                     tile_height=self.player_w_and_h[last_name_sim][1], speed=(0, 0)))
                npc_xy.append((npc[-1].x, npc[-1].y))
                npc_rect = npc[-1].rect
                npc_rects.append(pygame.Rect(npc_rect[0] * map_game.tile_width - 6,
                                             npc_rect[1] * map_game.tile_height - 6,
                                             npc_rect[2] + 10, npc_rect[3] + 10))
        map_game.npc_xy = npc_xy
        map_game.npc_rects = npc_rects
        draw_dialog = True
        author_words_text = TextService.get_text_by_id(author_words_id[params[1].level_id])
        draw_dialog_text = [ShowTextContent(author_words_text, (255, 255, 255),
                                            16, (0, 0, 0),
                                            (0, int(self.w_h // 1.3)),
                                            (10, 10, 10, 10))]
        ready_to_transport = False
        num_of_join_dialogs = 0
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
                    if event.key == pygame.K_u:
                        if backpack.active_cell_id == backpack.volume - 1:
                            map_game.render(self.screen, 0, 0, 30, 10)
                            cross.show_text(self.screen, 255)
                        else:
                            backpack_elem = backpack.rest[backpack.active_cell_id]
                            if backpack_elem is not None and backpack_elem.item_name == 'note':
                                get_text = backpack_elem.inf['text_note']
                                text = get_text.content['text'].split()
                                len_text = len(get_text.content['text'].split())
                                if len_text > 8:
                                    res_text = []
                                    full_del = len_text // 8
                                    for i in range(0, full_del):
                                        res_text.append(' '.join(text[i * 8:i * 8 + 8]))
                                    res_text.append(' '.join(text[full_del * 8:]))
                                    backpack_elem.inf['text_note'].content['text'] = '\n'.join(res_text)
                                draw_dialog_text.append(ShowTextContent(get_text, (255, 255, 255),
                                                                        16, (0, 0, 0),
                                                                        (0, int(self.w_h // 1.35)),
                                                                        (10, 10, 10, 10), add_repeat=5))
                                draw_dialog = True
                    if event.key == pygame.K_f:
                        result_i = interactions.check_rect_in_zone(game_model_character.rect)
                        result_npc = map_game.collide_with_npc(game_model_character.rect)
                        if result_i[0]:
                            get_dialog = self.mind_rects.get((result_i[2].x, result_i[2].y))
                            draw_dialog_text.append(get_dialog)
                            draw_dialog = True
                        if result_npc[0]:
                            npc_model = None
                            for one_npc in npc:
                                if (one_npc.x == (result_npc[1].x + 6) // map_game.tile_width and
                                        one_npc.y == (result_npc[1].y + 6) // map_game.tile_height):
                                    npc_model = one_npc
                                    break
                            if npc_model is not None:
                                if npc_model.character.get_info().get('dialog_ids'):
                                    res_data = []
                                    for dialog_id in npc_model.character.get_info().get('dialog_ids'):
                                        get_text = TextService.get_text_by_id(dialog_id)
                                        res_data.append(ShowTextContent(get_text, (255, 255, 255),
                                                                        16, (0, 0, 0),
                                                                        (0, int(self.w_h // 1.3)),
                                                                        (10, 10, 10, 10)))
                                    if len(res_data) == 2:
                                        draw_dialog = True
                                        num_of_join_dialogs = 2
                                        SessionService.update_level(params[1].level_id + 1, params[0].player_name)
                                    else:
                                        num_of_join_dialogs = len(res_data)
                                        get_text = TextService.get_text_by_id(author_words_id[3])
                                        res_data.append(ShowTextContent(get_text, (255, 255, 255),
                                                                        16, (0, 0, 0),
                                                                        (0, int(self.w_h // 1.3)),
                                                                        (10, 10, 10, 10)))
                                        SessionService.update_level(params[1].level_id + 1, params[0].player_name)
                                        draw_dialog = True
                                    draw_dialog_text.append(res_data)
                                else:
                                    if npc_model.character.get_info()['dialog_id'] == 8:
                                        SessionService.update_level(params[1].level_id + 1, params[0].player_name)
                                    get_text = (TextService
                                                .get_text_by_id(int(npc_model.character.inf['dialog_id'])))
                                    dialog_class = ShowTextContent(get_text, (255, 255, 255),
                                                                   16, (0, 0, 0),
                                                                   (0, int(self.w_h // 1.3)),
                                                                   (10, 10, 10, 10))
                                    draw_dialog_text.append(dialog_class)
                                    draw_dialog = True
                    if event.key == pygame.K_e:
                        # локальные переменные, проверяем находится ли игрок в какой-либо зоне
                        result_d = doors.check_rect_in_zone(game_model_character.rect)
                        result_k = keys_doors.check_rect_in_zone(game_model_character.rect)
                        result_n = notes.check_rect_in_zone(game_model_character.rect)
                        if result_d[0]:
                            # подаем в метод removing closed door ячейки рюкзака и активную ячейку
                            if doors.removing_closed_door(result_d[1], backpack.items, backpack.active_cell_id):
                                # если все окей, то удаляем использованный ключ из рюкзака
                                backpack.remove_item(backpack.active_cell_id)
                            # если True, удаляем дверь
                        if result_k[0]:
                            # проверяем что ключ подобран и при этом его нет в списке подобранных (это нужно для того,
                            # чтобы не было дубляжа ключей в инвентаре
                            if keys_doors.add_taken_key(result_k[1]) and result_k[1] not in keys_doors.keys_taken:
                                free_cell = backpack.get_last_free_cell()
                                if free_cell is not None:
                                    backpack.take(free_cell, Item(f'{keys_doors.names[-1]}',
                                                                  {'image': 'key'},
                                                                  lambda: print('hi')))
                        if result_n[0]:
                            if notes.add_taken_note(result_n[1]) and result_n[1] not in notes.notes_taken:
                                free_cell = backpack.get_last_free_cell()
                                if free_cell is not None:
                                    data_for_note = note_text_id[(result_n[1].x, result_n[1].y)]
                                    data_for_note = TextService.get_text_by_id(data_for_note)
                                    # здесь поолучаем текст из БД для записки
                                    backpack.take(free_cell, Item('note',
                                                                  {'image': 'note', 'text_note': data_for_note},
                                                                  lambda: print('hi')))
                    # при нажатие на стрелки лево/право меняем активную ячейку рюкзака
                    if event.key == pygame.K_LEFT:
                        backpack.do_unselected(backpack.active_cell_id)
                        backpack.previous_item()
                        backpack.do_selected(backpack.active_cell_id)
                    if event.key == pygame.K_RIGHT:
                        backpack.do_unselected(backpack.active_cell_id)
                        backpack.next_item()
                        backpack.do_selected(backpack.active_cell_id)
                    # меню паузы, здесь мы скрываем также рюкзак, что логично)
                    if event.key == pygame.K_ESCAPE:  # Для меню паузы
                        backpack.close_backpack()
                        game_class.render_other_window_handler.render('pause_game')  # отрисовка меню паузы

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
            for one_npc in npc:
                self.screen.blit(one_npc.image, (one_npc.x * map_game.tile_width, one_npc.y * map_game.tile_height))
            if draw_dialog:
                if isinstance(draw_dialog_text[-1], list):
                    alist = list(reversed(draw_dialog_text[-1]))
                    if not alist[num_of_join_dialogs - 1].show_dialog_window(self.screen,
                                                                             map_game.tile_width,
                                                                             map_game.tile_height,
                                                                             10):
                        map_game.render(game_class.screen, 0, 0, 70, 70)
                        num_of_join_dialogs -= 1
                    if num_of_join_dialogs == 0:
                        draw_dialog = False
                        ready_to_transport = True
                else:
                    if not draw_dialog_text[-1].show_dialog_window(self.screen, map_game.tile_width,
                                                                   map_game.tile_height,
                                                                   10):
                        draw_dialog = False
                        map_game.render(game_class.screen, 0, 0, 70, 70)
                        if params[0].level_id - SessionService.get_last_session().level_id != 0:
                            ready_to_transport = True
            if ready_to_transport:
                backpack.close_backpack()
                try:
                    self.render_level_map_with_param(game_class, params=(SessionService.get_last_session(),
                                                                         LevelService
                                                                         .get_level_by_id(SessionService
                                                                                          .get_last_session().
                                                                                          level_id), params[2]))
                except Exception as e:
                    print(e)
                    SessionService.update_level(0, params[0].player_name)
                    self.show_final_window()
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


# класс для вызова нажатием на кнопку функций
class OnClickFunctions:

    # начать новую игру
    @staticmethod
    def new_game_session_init(player_name: str) -> Tuple[GetSession, Level, GetCharacter] or ErrorWidget:
        if not CharacterService.check_characters():
            for level_inf in base_levels:
                LevelService.create(Level(level_inf[0], level_inf[1], level_inf[2], level_inf[3]))
            for npc in npc_inform:
                CharacterService.create(CreateCharacter(npc[0], npc[1]))
            for el in all_dicts:
                TextService.save(CreateText(el[0]), el[1])
            with open('notes_text.txt', 'r', encoding='utf-8') as f:
                for text in f.readlines():
                    if text != '\n':
                        TextService.save(CreateText({'text': text, 'next': None}), TextService.get_last_id() + 1)
        create_session = SessionService.create(player_name)
        SessionService.update_inf({'no_use_notes': [i for i in range(33, 45)]}, player_name)
        if create_session is not None:
            return ErrorWidget(create_session[1], 1000, 100, (0, 0))
        CharacterService.create(CreateCharacter(character_name=player_name, info={
            'image_name': 'character',
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

    # продолжить игру
    @staticmethod
    def continue_game_session(player_name: str) -> Tuple[GetSession, Level, GetCharacter] or ErrorWidget:
        get_session = SessionService.get_session_by_player_name(player_name)
        SessionService.update_inf({'no_use_notes': [i for i in range(33, 45)]}, player_name)
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
    game = Game('Absolutely Depressive Live')
