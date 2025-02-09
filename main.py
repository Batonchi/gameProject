import pygame
from database import Connection, create_database
from pygame_widgets.button import Button
from app.characters.model import Character
from app.map.model import Map


create_database()


def start_game():
    return False


def show_about_the_game(screen):
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Об игре')
    button_back = Button(screen, 150, 400, 200, 80, text='Назад',
                         fontSize=30, margin=20,
                         inactiveColour=(250, 250, 250),
                         pressedColour=(0, 255, 0), radius=0,
                         onClick=None)
    show_menu = True
    while show_menu:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                show_menu = False
                quit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if (150 < e.pos[0] and e.pos[0] < 150 + 200 and 400 < e.pos[1] and e.pos[1] < 400 + 80):
                    show_menu = False
        button_back.listen(events)
        button_back.draw()
        pygame.display.update()
    return


def show_trainig_screen(screen):
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Обучение')
    button_back = Button(screen, 150, 400, 200, 80, text='Назад',
                         fontSize=30, margin=20,
                         inactiveColour=(250, 250, 250),
                         pressedColour=(0, 255, 0), radius=0,
                         onClick=None)
    show_menu = True
    while show_menu:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                show_menu = False
                quit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if (150 < e.pos[0] and e.pos[0] < 150 + 200 and 400 < e.pos[1] and e.pos[1] < 400 + 80):
                    show_menu = False
        button_back.listen(events)
        button_back.draw()
        pygame.display.update()
    return


def main_menu(screen):
    screen.fill((0, 0, 0))
    show_main_menu = True
    pygame.display.set_caption('Меню')

    button_play = Button(screen, 10, 60, 200, 80, text='Новая игра',
                         fontSize=30, margin=20,
                         inactiveColour=(250, 250, 250),
                         pressedColour=(0, 255, 0), radius=0,
                         onClick=None)
    button_training = Button(screen, 10, 150, 200, 80, text='Обучение',
                         fontSize=30, margin=20,
                         inactiveColour=(250, 250, 250),
                         pressedColour=(0, 255, 0), radius=0,
                         onClick=None)
    button_about_the_game = Button(screen, 10, 240, 200, 80, text='Об игре',
                         fontSize=30, margin=20,
                         inactiveColour=(250, 250, 250),
                         pressedColour=(0, 255, 0), radius=0,
                         onClick=None)
    button_exit = Button(screen, 10, 330, 200, 80, text='Выход',
                         fontSize=30, margin=20,
                         inactiveColour=(250, 250, 250),
                         pressedColour=(0, 255, 0), radius=0,
                         onClick=None)
    while show_main_menu:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                show_main_menu = False
                pygame.quit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if (10 < e.pos[0] and e.pos[0] < 10 + 200 and 60 < e.pos[1] and e.pos[1] < 60 + 80):
                    show_main_menu = start_game()
                    if not show_main_menu:
                        break
                if (10 < e.pos[0] and e.pos[0] < 10 + 200 and 150 < e.pos[1] and e.pos[1] < 150 + 80):
                    show_trainig_screen(pygame.display.set_mode((500, 500)))
                if (10 < e.pos[0] and e.pos[0] < 10 + 200 and 240 < e.pos[1] and e.pos[1] < 240 + 80):
                        show_about_the_game(pygame.display.set_mode((500, 500)))
                if (10 < e.pos[0] and e.pos[0] < 10 + 200 and 330 < e.pos[1] and e.pos[1] < 330 + 80):
                    quit()
        bg_menu = pygame.image.load('app/view/images/for_menu.jpg')
        screen.blit(bg_menu, (-25, -50))
        button_play.listen(events)
        button_play.draw()
        button_training.listen(events)
        button_training.draw()
        button_about_the_game.listen(events)
        button_about_the_game.draw()
        button_exit.listen(events)
        button_exit.draw()

        pygame.display.update()


if __name__ == '__main__':
    pygame.init()

    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)

    running = True

    main_menu(screen)
    map_game = Map('map_level1.tmx', size)
    # character = Character()
    clock = pygame.time.Clock()
    coors = (100, 100)
    menu_scr = True
    up, left, down, right = False, False, False, False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    # coors = character.move('up')
                    # map_game.render(screen, coors)
                    pass
                if event.key == pygame.K_a:
                    # coors = character.move('left')
                    # map_game.render(screen, coors)
                    pass
                if event.key == pygame.K_s:
                    # coors = character.move('down')
                    # map_game.render(screen, coors)
                    pass
                if event.key == pygame.K_d:
                    # coors = character.move('right')
                    # map_game.render(screen, coors)
                    pass
        map_game.render(screen)
        pygame.display.flip()
        pygame.display.update()


# получение рейтинг борда
def get_rating():
    with Connection() as conn:
        results = conn.execute('SELECT * FROM ratings ORDER BY rate_num').fetchall()