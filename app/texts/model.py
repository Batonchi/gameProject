import json
from typing import Tuple

import pygame


class CreateText:

    def __init__(self, content: dict):
        self.content = json.dumps(content)


class GetText:

    def __init__(self, text_id: int, content: str):
        self.text_id = text_id
        self.content = json.loads(content)


class ShowTextContent:

    def __init__(self, text: GetText, color: Tuple[int, int, int], font_size: int,
                 background_color: Tuple[int, int, int], xy_start: Tuple[int, int]):
        self.text = text
        self.color = color
        self.font_size = font_size
        self.background_color = background_color
        self.xy_start = xy_start

    def render(self, screen: pygame.Surface, width: int, horiz_padding: int):
        font = pygame.font.SysFont(None, 80)
        image = font.render('huiiiiii', True, self.background_color)
        screen.blit(image, (self.xy_start[0], self.xy_start[1]))
        pygame.display.update()

