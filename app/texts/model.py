import json
import pygame
import pytmx

from typing import Tuple


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
                 border_radius: int = None):
        self.text = text
        self.color = color
        self.font_size = font_size
        self.background_color = pygame.Color(*background_color)
        self.xy_start = xy_start
        self.font = pygame.font.SysFont(None, font_size)
        self.image = self.font.render(self.text.content['text'], True, self.color)
        self.padding = padding
        self.rect = self.image.get_rect()
        self.rect.height += self.padding[0] + self.padding[2]
        self.rect.width += self.padding[1] + self.padding[3]
        self.rect.x = self.xy_start[0] - self.padding[0]
        self.rect.y = self.xy_start[1] - self.padding[1]
        if border_radius:
            self.border_radius = border_radius

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.background_color, self.rect, border_radius=self.border_radius)
        screen.blit(self.image, self.xy_start)

    def draw_rect_frame_in_full_line(self, screen: pygame.Surface, v_padding: int, x_end: int):
        pygame.draw.rect(screen, self.background_color, pygame.rect.Rect(0, self.rect.y - v_padding // 2,
                                                                         x_end,
                                                                         self.rect.height + v_padding),
                         border_radius=5)

    # def draw_tile_adapt_frame(self, screen: pygame.Surface):
    #     tile_map = pytmx.TiledMap('for_dialog')
    #     for y in range(0, 3):
    #         for x in range(0, 100):


    def get_text_width(self) -> int:
        return self.padding[0] + self.rect.width + self.padding[2]
