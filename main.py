import pygame
from database import Connection, create_database
from app.characters.model import Character
from app.map.model import Map


def start_screen(screen, w, h):
    intro_text = ["Game", "",
                  "Новая игра",
                  "Сохранения",
                  "Обучение"]


create_database()


if __name__ == '__main__':
    pygame.init()

    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    running = True
    map_game = Map('map1.tmx', size)
    # character = Character()
    if running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_w:
            #         character.move('up')
            #     if event.key == pygame.K_a:
            #         character.move('left')
            #     if event.key == pygame.K_s:
            #         character.move('down')
            #     if event.key == pygame.K_d:
            #         character.move('right')
        map_game.render(screen)
        pygame.display.update()
# получение рейтинг борда


def get_rating():
    with Connection() as conn:
        results = conn.execute('SELECT * FROM ratings ORDER BY rate_num').fetchall()
