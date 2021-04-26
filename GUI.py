import random
import sys, pygame
from GameEngine import *
from openpyxl.styles.colors import *
#hole_img = pygame.image.load('racecar.png')

mainClock = pygame.time.Clock()
from pygame.locals import *


game_engine = Game()
pygame.init()
pygame.display.set_caption('game base')
WIDTH, HEIGHT = (1280, 720)
HOLE_RADIUS = WIDTH/20
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
font = pygame.font.SysFont(None, 20)


def draw_hole(x, y, border=None, color = 'BLUE'):
    pygame.draw.circle(screen, color, (x, y), HOLE_RADIUS, border)  # surface, color, center, radius


def draw_text(text, font, color, surface, x, y, center=None):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center is not None:
        textrect.center = center
    else:
        textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


click = False


def check_hole_click(mx, my, hole, radius=HOLE_RADIUS):
    return (mx - hole.center_x) ** 2 + (my - hole.center_y) ** 2 < radius ** 2


def coords_to_holes():
    for number, hole in game_engine.holes.items():
        if not isinstance(hole, Mancala):
            if number > 7:
                hole.center_x = (1+hole.number)*(WIDTH/9)
                hole.center_y = 1*HEIGHT/3
            else:
                hole.center_x = (8-hole.number)*(WIDTH/9)
                hole.center_y = 2*HEIGHT/3
        elif number == 7:
            print(1)
            hole.center_x = (1 + hole.number) * (WIDTH / 9)
            hole.center_y = HEIGHT / 2
        elif number == 14:
            print(14)
            hole.center_x = (8 - hole.number) * (WIDTH / 9)
            hole.center_y = HEIGHT / 2


def change_hole_color(hole, color='purple'):
    draw_hole(hole.center_x, hole.center_y, 5, color=color)


def draw_holes():
    for hole in game_engine.holes.values():
        if not isinstance(hole, Mancala):
            draw_hole(hole.center_x, hole.center_y, 5)
        else:
            pygame.draw.rect(screen, 'red', (hole.center_x-HOLE_RADIUS, hole.center_y-(HEIGHT/3 + 2*HOLE_RADIUS)/2, HOLE_RADIUS*2, HEIGHT/3 + 2*HOLE_RADIUS), 5)
            #pygame.draw.ellipse(screen, 'red', (hole.center_x, hole.center_y, HOLE_RADIUS*2, ), 5)


def coords_to_stones():
    for hole in game_engine.holes.values():
        for stone in hole.stones:
            while True:
                x = random.randint(int(hole.center_x-HOLE_RADIUS), int(hole.center_x+HOLE_RADIUS))
                y = random.randint(int(hole.center_y-HOLE_RADIUS), int(hole.center_y+HOLE_RADIUS))
                if check_hole_click(x, y, hole, radius=HOLE_RADIUS-30):
                    stone.center_x = x
                    stone.center_y = y
                    break
                print("WRONG")

def draw_stones():
    for hole in game_engine.holes.values():
        for stone in hole.stones:
            stone.rect = pygame.Rect(stone.center_x, stone.center_y, 12, 12)
            pygame.draw.rect(screen, stone.color, stone.rect)

def main_menu():
    global game_engine
    game_engine = Game()
    players = game_engine.get_players(2)
    game_engine.initialize_game(players)
    coords_to_holes()
    coords_to_stones()
    while True:
        screen.fill((0,0,0))
        draw_text('main menu', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game()

        if button_2.collidepoint((mx, my)):
            if click:
                options()

        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        draw_text('Game', pygame.font.Font("freesansbold.ttf", 20), (255, 230, 215), screen, 20, 20,
                  (50 + (200 / 2), 100 + (50 / 2)))

        draw_text('Options', pygame.font.Font("freesansbold.ttf", 20), (255, 230, 215), screen, 20, 20,
                  (50 + (200 / 2), 200 + (50 / 2)))

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

            pygame.display.update()
            mainClock.tick(60)

def game():
    running = True
    click = False
    game_engine.turn = 0
    while running:
        screen.fill((0,0,0))
        draw_text('game', font, (255, 255, 255), screen, 20, 20)
        draw_text(f"{game_engine.players[game_engine.turn].name}'s turn", font, (255, 255, 255), screen, 20, 40)
        draw_text(f"{game_engine.players[1].name}", font, (255, 255, 255), screen, 0, 0, (WIDTH/2, 1*HEIGHT/3 - HOLE_RADIUS - 30))
        draw_text(f"{game_engine.players[0].name}", font, (255, 255, 255), screen, 0, 0, (WIDTH/2, 2*HEIGHT/3 + HOLE_RADIUS + 30))
        if not click:  # test
            draw_holes()
            draw_stones()

        mx, my = pygame.mouse.get_pos()

        for hole in game_engine.holes.values():
            if check_hole_click(mx, my, hole):
                if hole.number in game_engine.get_possible_moves(game_engine.turn) and hole.player.id == game_engine.turn:
                    change_hole_color(hole)
                    if click:
                        game_engine.move(game_engine.turn, hole.number)
                        coords_to_stones()

                else:
                    change_hole_color(hole, 'red')

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
        mainClock.tick(60)

def options():
    running = True
    while running:
        screen.fill((0,0,0))
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