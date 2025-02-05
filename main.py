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

    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    running = True
    map_game = Map('map_level1.tmx', size)
    character = Character()
    clock = pygame.time.Clock()
    coors = (100, 100)
    start_scr = True
    up, left, down, right = False, False, False, False
    while running:
        # if start_scr:
        #     start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    coors = character.move('up')
                    map_game.render(screen, coors)
                if event.key == pygame.K_a:
                    coors = character.move('left')
                    map_game.render(screen, coors)
                if event.key == pygame.K_s:
                    coors = character.move('down')
                    map_game.render(screen, coors)
                if event.key == pygame.K_d:
                    coors = character.move('right')
                    map_game.render(screen, coors)
        pygame.display.flip()
        pygame.display.update()

# получение рейтинг борда
def get_rating():
    with Connection() as conn:
        results = conn.execute('SELECT * FROM ratings ORDER BY rate_num').fetchall()


# '''if event.key == pygame.K_w:
#     up = True
# if event.key == pygame.K_a:
#     left = True
# if event.key == pygame.K_s:
#     down = True
# if event.key == pygame.K_d:
#     right = True
# if event.type == pygame.KEYUP:
#     if event.key == pygame.K_w:
#         up = False
#     if event.key == pygame.K_a:
#         left = False
#     if event.key == pygame.K_s:
#         down = False
#     if event.key == pygame.K_d:
#         right = False
#
# if up:
#     coors = character.move('up')
#     map_game.render(screen, coors)
# if left:
#     coors = character.move('left')
#     map_game.render(screen, coors)
# if right:
#     coors = character.move('right')
#     map_game.render(screen, coors)
# if down:
#     coors = character.move('down')
#     map_game.render(screen, coors)
# map_game.render(screen, coors)'''