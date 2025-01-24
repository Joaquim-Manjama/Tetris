import pygame, sys
import random as r
import copy
import os

pygame.init()

WIDTH = 710
HEIGHT = 765
CELL = 50
LINE = 1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JmD's Tetris Game")
current_path = os.path.dirname(os.path.abspath(__file__))

#FRAMES
clock = pygame.time.Clock()
frame_count = 0
block_speed = 20
score = 0

p1 = [[0, 0], [1, 0], [1, 1], [2, 1], ['red']]
p2 = [[0, 1], [1, 1], [1, 0], [2, 0], ['green']]
p3 = [[0, 1], [1, 0], [1, 1], [2, 1], ['purple']]
p4 = [[0, 1], [1, 1], [2, 1], [2, 0], ['orange']]
p5 = [[0, 0], [1, 0], [2, 0], [3, 0], ['light blue']]
p6 = [[0, 0], [0, 1], [1, 0], [1, 1], ['yellow']]
p7 = [[0, 0], [0, 1], [1, 1], [2, 1], ['dark blue']]

pieces = [p1, p2, p3, p4, p5, p6, p7]

game = []
next_piece = []
movement = [0, 0]
moving = False
rotation = 0
inc = 0

f = open(current_path+"\\HighScore.txt", "r")
highest_score = int(f.read())
f.close()

board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

def draw_board(surface):
    surface.fill('black')
    for i in range(1, 11):
        #Vertical lines
        pygame.draw.line(surface, 'white', (i*CELL + ((i-1)*LINE), 0), (i*CELL + ((i-1)*LINE), HEIGHT), LINE)
    for i in range(1, 15):
        #Horizontal lines
        pygame.draw.line(surface, 'white', (0, i*CELL + ((i-1)*LINE)), (WIDTH - 200 , i*CELL + ((i-1)*LINE)), LINE)

def generate_next_piece(p):
    x = copy.deepcopy(p[r.randint(0, 6)])
    return x

def insert_piece(p):
    global next_piece
    next_piece.append(generate_next_piece(p))
    return next_piece[len(next_piece) - 2]
    

def draw_piece(surface, g):
    for piece in g:
        for block in range(0, len(piece) - 1):
            x = (piece[block][0] * CELL) + (piece[block][0] * LINE)
            y = (piece[block][1] * CELL) + (piece[block][1] * LINE)
            colour = piece[len(piece) - 1][0]
            b = pygame.Rect(x, y, CELL, CELL)
            pygame.draw.rect(surface, colour, b)

def gravity(g, b, p):
    global rotation
    global inc
    global next_piece
    vel = [0, 1]
    piece = g[len(g) - 1]
    print(piece)
    if piece[0][1] == 14 or piece[1][1] == 14 or piece[2][1] == 14 or piece[3][1] == 14 or b[piece[0][1] + 1][piece[0][0]] == 1 or b[piece[1][1] + 1][piece[1][0]] == 1 or b[piece[2][1] + 1][piece[2][0]] == 1 or b[piece[3][1] + 1][piece[3][0]] == 1:
        for block in range(0, len(piece) - 1):
            b[piece[block][1]][piece[block][0]] = 1
        inc = 0
        g.append(insert_piece(p))
        randomise_pos(g)
        rotation = 0
        return
    else:
        for block in range(0, len(piece) - 1):
            piece[block][1] += vel[1]

def move(g, b, p, m=[0, 0]):
    piece = g[len(g) - 1]
    if not (piece[0][1] == 14 or piece[1][1] == 14 or piece[2][1] == 14 or piece[3][1] == 14 or b[piece[0][1] + 1][piece[0][0]] == 1 or b[piece[1][1] + 1][piece[1][0]] == 1 or b[piece[2][1] + 1][piece[2][0]] == 1 or b[piece[3][1] + 1][piece[3][0]] == 1):
        if m[0] == -1:
            if piece[0][0] > 0 and piece[1][0] > 0 and piece[2][0] > 0 and piece[3][0] > 0 and b[piece[0][1]][piece[0][0] - 1] != 1 and b[piece[1][1]][piece[1][0] - 1] != 1 and b[piece[2][1]][piece[2][0] - 1] != 1 and b[piece[3][1]][piece[3][0] - 1] != 1:
                for block in range(0, len(piece) - 1):
                    piece[block][0] += m[0]
                    piece[block][1] += m[1]
        elif m[0] == 1:
            if piece[0][0] < 9 and piece[1][0] < 9 and piece[2][0] < 9 and piece[3][0] < 9 and b[piece[0][1]][piece[0][0] + 1] != 1 and b[piece[1][1]][piece[1][0] + 1] != 1 and b[piece[2][1]][piece[2][0] + 1] != 1 and b[piece[3][1]][piece[3][0] + 1] != 1:
                for block in range(0, len(piece) - 1):
                    piece[block][0] += m[0]
                    piece[block][1] += m[1]
        else:
            for block in range(0, len(piece) - 1):
                piece[block][1] += movement[1]

def randomise_pos(g):
    buffer = r.randint(0, 6)
    piece = g[len(g) - 1]
    for block in range(0, len(piece) - 1):
        piece[block][0] += buffer 

def rotate(g, r, b):
    piece = g[len(g) - 1]
    if piece[0][1] == 14 or piece[1][1] == 14 or piece[2][1] == 14 or piece[3][1] == 14 or b[piece[0][1] + 1][piece[0][0]] == 1 or b[piece[1][1] + 1][piece[1][0]] == 1 or b[piece[2][1] + 1][piece[2][0]] == 1 or b[piece[3][1] + 1][piece[3][0]] == 1:
        return
    else:
        if piece[4] == ['red']:
            if r % 2 == 0:
                piece[0][0] += 1
                piece[1][1] += 1
                piece[2][0] -= 1
                piece[3][0] -= 2
                piece[3][1] += 1 
            else:
                piece[0][0] -= 1
                piece[1][1] -= 1
                piece[2][0] += 1
                piece[3][0] += 2
                piece[3][1] -= 1

        if piece[4] == ['green']: 
            if r % 2 == 0:
                piece[0][1] -= 1
                piece[1][0] -= 1
                piece[2][1] += 1
                piece[3][0] -= 1
                piece[3][1] += 2 
            else:
                piece[0][1] += 1
                piece[1][0] += 1
                piece[2][1] -= 1
                piece[3][0] += 1
                piece[3][1] -= 2 

        if piece[4] == ['purple']: 
            if r == 0:
                piece[0][1] -= 1
                piece[1][1] += 1
                piece[2][0] -= 1
                piece[3][0] -= 2
                piece[3][1] += 1 
            
            elif r == 1:
                piece[0][0] += 2
                piece[2][0] += 1
                piece[2][1] -= 1
                piece[3][1] -= 2 

            elif r == 2:
                piece[0][1] += 1
                piece[1][1] -= 1
                piece[2][0] += 1
                piece[3][0] += 2
                piece[3][1] -= 1
            
            elif r == 3:
                piece[0][0] -= 2
                piece[2][0] -= 1
                piece[2][1] += 1
                piece[3][1] += 2

        if piece[4] == ['orange']:
            if r == 0:
                piece[0][1] -= 2
                piece[1][0] -= 1
                piece[1][1] -= 1
                piece[2][0] -= 2
                piece[3][0] -= 1
                piece[3][1] += 1
            if r == 1:
                piece[0][0] += 2
                piece[1][0] += 1
                piece[1][1] -= 1
                piece[2][1] -= 2
                piece[3][0] -= 1
                piece[3][1] -= 1

            if r == 2:
                piece[0][0] -= 1
                piece[0][1] += 2
                piece[1][1] += 1
                piece[2][0] += 1
                piece[3][1] -= 1

            if r == 3:
                piece[0][0] -= 1#
                piece[1][1] += 1#
                piece[2][0] += 1
                piece[2][1] += 2
                piece[3][0] += 2
                piece[3][1] += 1

        if piece[4] == ['light blue']:
            if r % 2 == 0:
                piece[1][0] -= 1
                piece[1][1] += 1
                piece[2][0] -= 2
                piece[2][1] += 2
                piece[3][0] -= 3
                piece[3][1] += 3

                for block in range(0, len(piece) - 1):
                    piece[block][1] -= 1
            
            else:
                piece[1][0] += 1
                piece[1][1] -= 1
                piece[2][0] += 2
                piece[2][1] -= 2
                piece[3][0] += 3
                piece[3][1] -= 3

                for block in range(0, len(piece) - 1):
                    piece[block][1] += 1

        if piece[4] == ['dark blue']:
            if r == 0:
                piece[0][0] += 1
                piece[0][1] -= 1
                piece[1][1] -= 2
                piece[2][0] -= 1
                piece[2][1] -= 1
                piece[3][0] -= 2

            if r == 1:
                piece[0][0] += 1
                piece[0][1] += 1
                piece[1][0] += 2
                piece[2][0] += 1
                piece[2][1] -= 1
                piece[3][1] -= 2

            if r == 2:
                piece[0][0] -= 1
                piece[0][1] += 1
                piece[1][1] += 2
                piece[2][0] += 1
                piece[2][1] += 1
                piece[3][0] += 2
                
            if r == 3:
                piece[0][0] -= 1
                piece[0][1] -= 1
                piece[1][0] -= 2
                piece[2][0] -= 1
                piece[2][1] += 1
                piece[3][1] += 2

def clear_lines(surface, g, b):
    global score
    global highest_score
    global inc
    c = []
    line = 0
    increment = 0
    for i in b:
        if i == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:
            inc += 10
            increment += 10
            for piece in g:
                for block in range(0, len(piece) - 1):
                    if piece[block][1] == line:
                        piece[block][1] += 1000
            
            c = copy.deepcopy(b)
            for j in range(0, line + 1):
                b[j] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            
            for piece in g:
                for block in range(0, len(piece) - 1):
                    if piece[block][1] < line:
                        piece[block][1] += 1

            for j in range(line, 0, -1):
                b[j] = c[j - 1]
        line += 1
    score += increment
    show_increment(surface, inc)
    store_high_score(score, highest_score)
            
def display_score(surface):
    global score
    global highest_score
    if highest_score >= score:
        f = pygame.font.SysFont('Comis Sans MS', 30)
        text = f.render(f"Score: {score}", False, 'white')
        surface.blit(text, (400, 50))

def show_increment(surface, i):
    f = pygame.font.SysFont('Comis Sans MS', 30)
    text = f.render(f"+ {i}", False, 'white')
    surface.blit(text, (420, 100))

def store_high_score(scr, hscr):
    if scr > hscr:
        f = open("C:\\Users\\melor\\Desktop\\Pygame\\Tetris\\HighScore.txt", "w")
        f.write(str(scr))
        f.close()

def highest_score_render(surface, scr, hscr):
        if scr < hscr:
            x = hscr
        else:
            x = scr
        f = pygame.font.SysFont('Comis Sans MS', 30)
        text = f.render(f"Highest Score: {x}", False, 'white')
        surface.blit(text, (20, 50))

def draw_next_piece(surface):
    f = pygame.font.SysFont('Comis Sans MS', 30)
    text = f.render(f"Next Piece:", False, 'white')
    surface.blit(text, (550, 150))
    global next_piece
    piece = next_piece[len(next_piece) - 1]
    for block in range(0, len(piece) - 1):
        x = ((piece[block][0] + 21) * CELL/2) + ((piece[block][0] + 21) * LINE) 
        y = ((piece[block][1] + 4) * CELL/2) + ((piece[block][1] + 4) * LINE) + 100
        colour = piece[len(piece) - 1][0]
        b = pygame.Rect(x, y, CELL/2, CELL/2)
        pygame.draw.rect(surface, colour, b)

next_piece.append(generate_next_piece(pieces))
game.append(insert_piece(pieces))
randomise_pos(game)

while True:

    draw_board(screen)
    draw_piece(screen, game)
    display_score(screen)
    highest_score_render(screen, score, highest_score)
    draw_next_piece(screen)

    if frame_count % block_speed == 5 and not moving:
        gravity(game, board, pieces)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                movement = [-1, 0]

            if event.key == pygame.K_RIGHT:
                movement = [1, 0]

            if event.key == pygame.K_DOWN:
                movement = [0, 1]

            if event.key == pygame.K_SPACE:
                rotate(game, rotation, board)
                rotation += 1
                if rotation == 4:
                    rotation = 0

            moving = True
            frame_count -= 1
            move(game, board, pieces, movement)

        if event.type == pygame.KEYUP:
            movement = [0, 0]
            moving = False

    frame_count += 1
    clear_lines(screen, game, board)
    clock.tick(60)
    pygame.display.update()