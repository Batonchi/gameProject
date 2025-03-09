import json
import pygame
import pytmx
import os

from typing import Tuple, List


class CreateText:

    def __init__(self, content: dict):
        self.content = json.dumps(content)


class GetText:

    def __init__(self, text_id: int, content: str):
        self.text_id = text_id
        self.content = json.loads(content)


class ShowTextContent:

    def __init__(self, text: GetText, color: Tuple[int, int, int], font_size: int,
                 background_color: Tuple[int, int, int] | Tuple[int, int, int, int],
                 xy_start: Tuple[int, int] | Tuple[float, int],
                 padding: Tuple[int, int, int, int],
                 border_radius: int = 0, font_weight: int = 700,add_repeat: int = 0):
        self.view_text_background = pytmx.TiledMap(os.path.abspath('app/map/for_dialog.tmx'))
        self.text = text
        self.dialog_link = text.content
        self.color = color
        self.font_size = font_size
        self.background_color = pygame.Color(*background_color)
        self.xy_start = xy_start
        self.x_start, self.y_start = self.xy_start[0], self.xy_start[1]
        self.font = pygame.font.SysFont('Arial-black', font_size, font_weight)
        self.image = self.font.render(self.text.content['text'], True, self.color)
        self.padding = padding
        self.rect = self.image.get_rect()
        self.rect.height += self.padding[0] + self.padding[2]
        self.rect.width += self.padding[1] + self.padding[3]
        self.rect.x = self.xy_start[0] - self.padding[0]
        self.rect.y = self.xy_start[1] - self.padding[1]
        self.border_radius = border_radius
        self.add_repeat = add_repeat
        self.now_text = self.dialog_link.get('text', None)

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.background_color, self.rect, border_radius=self.border_radius)
        screen.blit(self.image, self.xy_start)

    def draw_rect_frame_in_full_line(self, screen: pygame.Surface, v_padding: int, x_end: int):
        pygame.draw.rect(screen, self.background_color, pygame.rect.Rect(0, self.rect.y - v_padding // 2,
                                                                         x_end,
                                                                         self.rect.height + v_padding),
                         border_radius=5)

    def restart_dialog(self):
        self.dialog_link = self.text.content
        self.now_text = self.dialog_link.get('text', None)

    def show_dialog_window(self, screen: pygame.Surface, tile_width: int, tile_height: int, repeat_count: int):
        repeat = repeat_count
        image = pygame.image.load(os.path.abspath('app/map/white.png'))
        image = pygame.transform.scale(image, (tile_width, tile_height))
        image.set_alpha(100)
        for y in range(0, repeat + self.add_repeat):
            for x in range(0, 100):
                screen.blit(image, (tile_width * x + self.x_start, tile_height * y + self.y_start))
        if '\n' in self.now_text:
            now_text = self.now_text.split('\n')
            i = 0
            for text in now_text:
                text_image = self.font.render(text, True, self.background_color)
                screen.blit(text_image, (pygame.display.get_window_size()[0] // 2 - text_image.get_width() // 2,
                                         self.y_start + (repeat // 2
                                                         * tile_height + (text_image.get_height() + 5) * i) // 2))
                i += 1
        else:
            text_image = self.font.render(self.now_text, True, self.background_color)
            screen.blit(text_image, (pygame.display.get_window_size()[0] // 2 - text_image.get_width() // 2,
                                     self.y_start + (repeat // 2
                                                     * tile_height + (text_image.get_height() + 5)) // 2))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.now_text = self.next_rep()
                    if not self.now_text:
                        self.restart_dialog()
                        return False
        return True

    def next_rep(self):
        words = self.dialog_link['text']
        self.dialog_link = self.dialog_link.get('next', None)
        if self.dialog_link is None:
            return False
        return words
