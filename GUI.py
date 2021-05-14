import random
import sys, pygame

from MinMax import minmax
import pygame_gui

from GameEngine import *
from openpyxl.styles.colors import *

# hole_img = pygame.image.load('racecar.png')

mainClock = pygame.time.Clock()
from pygame.locals import *

human_img = pygame.image.load('user2.png')
human_img = pygame.transform.scale(human_img, (50, 50))
human_rect = human_img.get_rect()

bot_img = pygame.image.load('robot2.png')
bot_img = pygame.transform.scale(bot_img, (50, 50))
bot_rect = bot_img.get_rect()

picture = pygame.image.load('bg-wood2-holes3.jpg')
picture = pygame.transform.scale(picture, (1280, 720))
rect = picture.get_rect()
rect = rect.move((0, 0))

leaderboard_bg = pygame.image.load('bg-leaderboard.jpg')
leaderboard_bg = pygame.transform.scale(leaderboard_bg, (1280, 720))
lead_rect = leaderboard_bg.get_rect()
lead_rect = lead_rect.move((0, 0))

game_engine = Game()
pygame.init()
pygame.display.set_caption('game base')
WIDTH, HEIGHT = (1280, 720)
HOLE_RADIUS = WIDTH / 20 + 2
manager = pygame_gui.UIManager((1280, 720))
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
font = pygame.font.SysFont(None, 20)
font_names = pygame.font.SysFont(None, 40)
font_stones_in_hole = pygame.font.SysFont(None, 30)


def draw_hole(x, y, border=None, color='BLUE'):
    pygame.draw.circle(screen, color, (x, y), HOLE_RADIUS, border)  # surface, color, center, radius


def draw_text(text, font, color, surface, x, y, center=None):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center is not None:
        textrect.center = center
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False


def check_hole_click(mx, my, hole, radius=HOLE_RADIUS):
    return (mx - hole.center_x) ** 2 + (my - hole.center_y) ** 2 < radius ** 2


def coords_to_holes():
    for number, hole in game_engine.holes.items():
        if not isinstance(hole, Mancala):
            if number > 7:
                hole.center_x = (8 - hole.number) * (WIDTH / 9)
                hole.center_y = 1 * HEIGHT / 3
            else:
                hole.center_x = (1 + hole.number) * (WIDTH / 9)
                hole.center_y = 2 * HEIGHT / 3
        elif number == 7:
            print(1)
            hole.center_x = (1 + hole.number) * (WIDTH / 9)
            hole.center_y = HEIGHT / 2
        elif number == 14:
            print(14)
            hole.center_x = (8 - hole.number) * (WIDTH / 9)
            hole.center_y = HEIGHT / 2


def change_hole_color(hole, color='green'):
    draw_hole(hole.center_x, hole.center_y, 5, color=color)


def draw_holes():
    for num, hole in game_engine.holes.items():
        if not isinstance(hole, Mancala):
            draw_hole(hole.center_x, hole.center_y, 5)
            draw_text(str(hole.number), font, 'green', screen, 0, 0,
                      (hole.center_x, hole.center_y + (HOLE_RADIUS + 20 if num < 7 else -HOLE_RADIUS - 20)))
            draw_text(str(len(hole.stones)), font_stones_in_hole, 'white', screen, 0, 0,
                      (hole.center_x, hole.center_y + (-HOLE_RADIUS - 20 if num < 7 else HOLE_RADIUS + 20)))

        else:
            pygame.draw.rect(screen, 'red', (
            hole.center_x - HOLE_RADIUS, hole.center_y - (HEIGHT / 3 + 2 * HOLE_RADIUS) / 2, HOLE_RADIUS * 2,
            HEIGHT / 3 + 2 * HOLE_RADIUS), 5)
            if num == 7:
                draw_text(str(game_engine.players[0].points), font_names, 'white', screen, 0, 0,
                          (hole.center_x, hole.center_y + (HEIGHT / 3 + 2 * HOLE_RADIUS) / 2 + 50))
            if num == 14:
                draw_text(str(game_engine.players[1].points), font_names, 'white', screen, 0, 0,
                          (hole.center_x, hole.center_y - (HEIGHT / 3 + 2 * HOLE_RADIUS) / 2 - 50))
            # pygame.draw.ellipse(screen, 'red', (hole.center_x, hole.center_y, HOLE_RADIUS*2, ), 5)


def coords_to_stones():
    for hole in game_engine.holes.values():
        for stone in hole.stones:
            stone.moved = False
            while True:
                x = random.randint(int(hole.center_x - HOLE_RADIUS), int(hole.center_x + HOLE_RADIUS))
                y = random.randint(int(hole.center_y - HOLE_RADIUS), int(hole.center_y + HOLE_RADIUS))
                if check_hole_click(x, y, hole, radius=HOLE_RADIUS - 30):
                    stone.center_x = x
                    stone.center_y = y
                    break


def draw_stones():
    for hole in game_engine.holes.values():
        for stone in hole.stones:
            stone.rect = pygame.Rect(stone.center_x, stone.center_y, 14, 14)
            pygame.draw.rect(screen, stone.color, stone.rect)


def recoord_stones():
    for hole in game_engine.holes.values():
        for stone in hole.stones:
            if stone.moved:
                while True:
                    x = random.randint(int(hole.center_x - HOLE_RADIUS), int(hole.center_x + HOLE_RADIUS))
                    y = random.randint(int(hole.center_y - HOLE_RADIUS), int(hole.center_y + HOLE_RADIUS))
                    if check_hole_click(x, y, hole, radius=HOLE_RADIUS - 30):
                        stone.center_x = x
                        stone.center_y = y
                        break
                stone.moved = False


def move(hole):
    for stone in game_engine.holes[game_engine.global_hole_number(hole)].stones:
        stone.moved = True
    return game_engine.move(game_engine.turn, hole.number)


def choose_players():
    global human_rect, bot_rect
    click = False
    players = (Player(0), Player(1))
    entry = pygame.Rect(WIDTH / 2 - 215, HEIGHT / 2 - 50, 400, 50)
    entry2 = pygame.Rect(WIDTH / 2 - 215, HEIGHT / 2 + 50, 400, 50)
    level_entry = pygame.Rect(WIDTH / 2 + 100, HEIGHT / 2 + 150, 40, 50)

    text_input_1 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=entry, manager=manager)
    print("fonts", pygame.font.get_fonts())
    text_input_1.font = pygame.font.SysFont('consolas', 40)
    text_input_1.text_colour = 'red'
    text_input_1.rebuild()

    text_input_2 = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=entry2, manager=manager)
    text_input_2.font = pygame.font.SysFont('consolas', 40)
    text_input_2.text_colour = 'green'
    text_input_2.rebuild()

    level_input = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=level_entry, manager=manager)
    print("fonts", pygame.font.get_fonts())
    level_input.font = pygame.font.SysFont('consolas', 40)
    level_input.text_colour = 'white'
    level_input.rebuild()

    while True:
        screen.fill((155, 155, 155))
        draw_text('Choose players', font, (255, 255, 255), screen, 20, 20)

        draw_text('Player1', pygame.font.SysFont('consolas', 40), (255, 255, 255), screen, WIDTH / 2 - 390,
                  HEIGHT / 2 - 40)

        draw_text('Player2', pygame.font.SysFont('consolas', 40), (255, 255, 255), screen, WIDTH / 2 - 390,
                  HEIGHT / 2 + 60)

        draw_text('AI Level (2-5)', pygame.font.SysFont('consolas', 40), (255, 255, 255), screen, WIDTH / 2 - 250,
                  HEIGHT / 2 + 160)

        mx, my = pygame.mouse.get_pos()

        human1 = pygame.Rect(WIDTH / 2 + 235, HEIGHT / 2 - 50, 50, 50)
        bot1 = pygame.Rect(WIDTH / 2 + 295, HEIGHT / 2 - 50, 50, 50)
        if human1.collidepoint((mx, my)):
            if click:
                players[0].type = "Human"
        pygame.draw.rect(screen, (255, 0, 0) if players[0].type == "Human" else (255, 255, 255), human1)
        if bot1.collidepoint((mx, my)):
            if click:
                players[0].type = "AI"
        pygame.draw.rect(screen, (255, 0, 0) if players[0].type == "AI" else (255, 255, 255), bot1)

        screen.blit(human_img, human1)

        screen.blit(bot_img, bot1)

        human2 = pygame.Rect(WIDTH / 2 + 235, HEIGHT / 2 + 50, 50, 50)
        bot2 = pygame.Rect(WIDTH / 2 + 295, HEIGHT / 2 + 50, 50, 50)
        if human2.collidepoint((mx, my)):
            if click:
                players[1].type = "Human"
        pygame.draw.rect(screen, (0, 255, 0) if players[1].type == "Human" else (255, 255, 255), human2)
        if bot2.collidepoint((mx, my)):
            if click:
                players[1].type = "AI"
        pygame.draw.rect(screen, (0, 255, 0) if players[1].type == "AI" else (255, 255, 255), bot2)
        screen.blit(human_img, human2)

        screen.blit(bot_img, bot2)
        # screen.blit(bot, rect)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_RETURN:
                    players[0].name = text_input_1.get_text()
                    players[1].name = text_input_2.get_text()
                    for player in players:
                        if player.type == "AI":
                            player.name += " (AI)"
                    game_engine.initialize_game(players)
                    coords_to_holes()
                    coords_to_stones()
                    game_engine.set_turn(0)
                    game(int(level_input.get_text()))
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            manager.process_events(event)
            time_delta = mainClock.tick(60) / 1000.0
            manager.update(time_delta)

            # screen.blit(background, (0, 0))
            manager.draw_ui(screen)

            pygame.display.update()


def main_menu():
    global game_engine
    click = False
    game_engine = Game()

    while True:
        screen.fill((155, 155, 155))
        draw_text('main menu', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 125, 200, 50)
        button_2 = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 25, 200, 50)
        button_3 = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 75, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                choose_players()

        if button_2.collidepoint((mx, my)):
            if click:
                options()

        if button_3.collidepoint((mx, my)):
            if click:
                pass
                # choose_players()

        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        pygame.draw.rect(screen, (15, 15, 15), button_3)
        draw_text('Game', pygame.font.Font("freesansbold.ttf", 20), (255, 230, 215), screen, 20, 20,
                  button_1.center)

        draw_text('Options', pygame.font.Font("freesansbold.ttf", 20), (255, 230, 215), screen, 20, 20,
                  button_2.center)

        draw_text('Players', pygame.font.Font("freesansbold.ttf", 20), (255, 230, 215), screen, 20, 20,
                  button_3.center)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            # if event.type == pygame.USEREVENT:
            #     if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            #         if event.ui_element == text_input:
            #             entered_text = event.text
            #             print(entered_text)

            # manager.process_events(event)
            # time_delta = mainClock.tick(60) / 1000.0
            # manager.update(time_delta)
            #
            # #screen.blit(background, (0, 0))
            # manager.draw_ui(screen)
            #
            # pygame.display.update()

            pygame.display.update()
            mainClock.tick(60)


def best_move(ai_depth, hole_number):
    root = GameNode(game_engine, hole_number, game_engine.turn)
    make_decision_tree(root, ai_depth)  # 2
    minmax(root, ai_depth, -math.inf, math.inf, heuristic_points_diff, is_finished, root.player_id, is_alfa_beta=False) # True
    if len(root.children) > 0:
        print("Next move options:")
        for child in root.children:  # Print options
            print("Hole:", child.number, child.value)
        next_best_move = max(root.children, key=lambda n: n.value).number
        pprint_tree(root)
        print("Next best move:", next_best_move)
        return next_best_move


def game(ai_depth=2):
    running = True
    click = False
    finished = False
    next_best_move = 0
    ai_depth = ai_depth
    while running:
        screen.blit(picture, rect)
        # screen.fill((0,0,0))
        draw_text('game', font, (255, 255, 255), screen, 20, 20)
        draw_text(f"{game_engine.players[game_engine.turn].name}'s turn", font, (255, 255, 255), screen, 20, 40)
        draw_text(f"{game_engine.players[1].name}", font_names, (255, 255, 255), screen, 0, 0,
                  (WIDTH / 2, 1 * HEIGHT / 3 - HOLE_RADIUS - 60))
        draw_text(f"{game_engine.players[0].name}", font_names, (255, 255, 255), screen, 0, 0,
                  (WIDTH / 2, 2 * HEIGHT / 3 + HOLE_RADIUS + 60))
        # if not click:  # test
        draw_holes()
        draw_stones()

        # Draw tips
        draw_text(f"Next best move: {next_best_move}", font_names, (255, 255, 255), screen, 0, 0,
                  (WIDTH / 2, 2 * HEIGHT / 3 + HOLE_RADIUS + 140) if game_engine.turn == 0 else (
                  WIDTH / 2, 1 * HEIGHT / 3 - HOLE_RADIUS - 140))

        mx, my = pygame.mouse.get_pos()
        if not finished:
            if not game_engine.is_finished():
                if game_engine.players[game_engine.turn].type == "AI":  # AI player
                    pygame.display.update()
                    # Get best move
                    hole_number = next_best_move

                    pygame.time.wait(3000)
                    if hole_number != 0:
                        move(game_engine.get_hole(hole_number, game_engine.turn))
                        print(f"{game_engine.players[game_engine.turn].name} picked hole no.{hole_number}!")
                    else:  # If first move then random
                        print("Random AI move")
                        hole_number = random.choice(list(game_engine.get_possible_moves(game_engine.turn)))
                        move(game_engine.get_hole(hole_number, game_engine.turn))
                        print(f"{game_engine.players[game_engine.turn].name} picked hole no.{hole_number}!")
                    recoord_stones()
                    game_engine.calculate_result()
                    #  coords_to_stones()
                    if not game_engine.additional_move:
                        game_engine.change_turn()
                    game_engine.additional_move = False

                    next_best_move = best_move(ai_depth, hole_number)  # Calculate next best move

                else:  # Human player
                    for hole in game_engine.holes.values():
                        if check_hole_click(mx, my, hole):
                            if hole.number in game_engine.get_possible_moves(
                                    game_engine.turn) and hole.player.id == game_engine.turn:
                                change_hole_color(hole)
                                if click:
                                    move(hole)
                                    recoord_stones()
                                    print(f"{game_engine.players[game_engine.turn].name} picked hole no.{hole.number}!")
                                    game_engine.calculate_result()
                                    #  coords_to_stones()
                                    if not game_engine.additional_move:
                                        game_engine.change_turn()
                                    game_engine.additional_move = False

                                    next_best_move = best_move(ai_depth, hole.number)
                            else:
                                if not isinstance(hole, Mancala):
                                    change_hole_color(hole, 'red')
            else:
                # Finish game and show leaderboard

                game_engine.finish_game()
                recoord_stones()
                finished = True
                # Print board
                game_engine.print_game_state("numbers")
                finished_screen()
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(120)


def finished_screen():
    running = True
    while running:
        screen.blit(leaderboard_bg, lead_rect)
        # screen.fill((0, 0, 0))
        draw_text('Leaderboard', font, (255, 255, 255), screen, 20, 20)
        leaderboard = pygame.Rect(WIDTH / 6, 1 * HEIGHT / 5, 4 * WIDTH / 6, 3 * HEIGHT / 5)
        pygame.draw.rect(screen, "white", leaderboard)

        try_again = pygame.Rect(WIDTH / 2 - 50, 4 * HEIGHT / 5 - 50, 100, 30)
        pygame.draw.rect(screen, "black", try_again, 2)

        results = game_engine.calculate_result()

        draw_text(results[1], pygame.font.Font(None, 40), 'black', screen, WIDTH / 6 + 50, 1 * HEIGHT / 5 + 50)
        draw_text(results[2], pygame.font.Font(None, 30), 'black', screen, WIDTH / 6 + 50, 1 * HEIGHT / 5 + 150)

        draw_text('TRY AGAIN', font, 'black', screen, 0, 0, (WIDTH / 2, 4 * HEIGHT / 5 - 35))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


def options():
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_text('options', font, (255, 255, 255), screen, 20, 20)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


main_menu()
