import pygame
from database import Connection, create_database
from app.characters.model import Character
from app.map.model import Map


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(pygame.load_image('app/view/images/fon.jpg'), (400, 400))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


create_database()


if __name__ == '__main__':
    pygame.init()

    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    running = True
    map_game = Map('map1.tmx', size)
    # character = Character()
    start_scr = True
    while running:
        # if start_scr:
        #     start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN and start_scr:
                start_scr = False
        map_game.render(screen)
        # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_w:
            #         character.move('up')
            #     if event.key == pygame.K_a:
            #         character.move('left')
            #     if event.key == pygame.K_s:
            #         character.move('down')
            #     if event.key == pygame.K_d:
            #         character.move('right')
        pygame.display.flip()
        pygame.display.update()
# получение рейтинг борда


def get_rating():
    with Connection() as conn:
        results = conn.execute('SELECT * FROM ratings ORDER BY rate_num').fetchall()
