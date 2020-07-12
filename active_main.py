import pygame as pg
from game import UltimateTicTacToe
from game import Game
from other_minimax import new_minimax_ab
import numpy as np
import json
from threading import Thread

local_friendly = True

init_result = pg.init()
print('result of initialization:', init_result)

id = 0

game = UltimateTicTacToe()
print('created game')


def dump_info():
    global id
    as_list = []
    for ly in range(len(game.board)):
        as_list.append([])
        for lx in range(len(game.board[ly])):
            as_list[ly].append([])
            for sy in range(len(game.board[ly][lx])):
                as_list[ly][lx].append([])
                for sx in range(len(game.board[ly][lx][sy])):
                    as_list[ly][lx][sy].append(game.board[ly][lx][sy][sx])

    with open(f'{id}.txt', 'w') as document:
        document.write(json.dumps(as_list))

    id += 1


going_first = False

turn = 'x'
other = 'o'

loading = False
autoplay = False
difficulty = 4

if loading and not local_friendly:

    last_move = [[1, 1], [2, 0]]

    with open('24.txt', 'r') as read:
        as_list = json.loads(read.read())

    print(as_list)

    as_array = []
    for ly in range(len(as_list)):
        as_array.append([])
        for lx in range(len(as_list[ly])):
            as_array[ly].append([])
            for sy in range(len(as_list[ly][lx])):
                as_array[ly][lx].append([])
                for sx in range(len(as_list[ly][lx][sy])):
                    as_array[ly][lx][sy].append(as_list[ly][lx][sy][sx])
                as_array[ly][lx][sy] = np.array(as_array[ly][lx][sy])
            as_array[ly][lx] = np.array(as_array[ly][lx])
        as_array[ly] = np.array(as_array[ly])
    as_array = np.array(as_array)

    game.board = as_array
    game.board[2][2][0][0] = 'x'
    game.update_won_boards()

else:
    last_move = None

exe_version = True

if going_first:
    move = new_minimax_ab(board=game, depth=difficulty, player=turn, opponent=other, starting=True,
                          last_move=last_move)

    game.push_move(turn, move)
    print('cpu played', move)
    last_move = move

    turn, other = other, turn


cellSize = 50
largerCellSize = cellSize * 3

screen = pg.display.set_mode((450, 450))

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (125, 125, 125)

run = True

clock = pg.time.Clock()

if not local_friendly:
    cx = pg.image.load('regular_x.png')
    co = pg.image.load('regular_o.png')
    tie = pg.image.load('tie.png')
else:
    thickness = 40
    initial_color = (255, 255, 255, 0)

    cx = pg.Surface((200, 200), pg.SRCALPHA, 32)
    cx = cx.convert_alpha(cx)
    pg.draw.line(cx, (255, 0, 0), [0, 0], [200, 200], thickness)
    pg.draw.line(cx, (255, 0, 0), [200, 0], [0, 200], thickness)

    co = pg.Surface((200, 200), pg.SRCALPHA, 32)
    co = co.convert_alpha(co)
    pg.draw.circle(co, (0, 0, 255), [100, 100], 100, thickness)

    tie = pg.Surface((200, 200), pg.SRCALPHA, 32)
    tie = tie.convert_alpha(tie)
    pg.draw.circle(tie, (255, 0, 255), [100, 100], 100, thickness)
    pg.draw.line(tie, (255, 0, 255), [0, 0], [200, 200], thickness)
    pg.draw.line(tie, (255, 0, 255), [200, 0], [0, 200], thickness)


n = None

if not autoplay:
    is_thinking = going_first
    is_player = not going_first
else:
    is_thinking, is_player = False, False


def display_image():
    global n
    while run:
        try:
            n = game.picture(cx, co, tie, 450, None, last_move, is_thinking, is_player)
        except:
            break

        try:
            screen.blit(n, (0, 0))
        except:
            break
        pg.display.flip()
        clock.tick(60)


first_exposure = True
print('displaying image')

while run:
    for e in pg.event.get():
        if e.type == pg.VIDEORESIZE:
            print('resizing video')

        if e.type == pg.VIDEOEXPOSE:
            print('exposing video')
        print('after "exposing video"')

        if e.type == pg.QUIT:
            run = False
        print('checking for input', e)
        if e.type == pg.MOUSEBUTTONDOWN and is_player:
            # print('pressing mouse')
            if game.is_finished():
                break
            x, y = map(int, pg.mouse.get_pos())
            larger_x = x // largerCellSize
            larger_y = y // largerCellSize

            smaller_x = (x - larger_x * largerCellSize) // cellSize
            smaller_y = (y - larger_y * largerCellSize) // cellSize

            move = [[larger_x, larger_y], [smaller_x, smaller_y]]

            if move in game.legal_moves(last_move):
                print('player played', move)
                game.push_move(turn, move)
                last_move = move

                turn, other = other, turn
                is_thinking, is_player = is_player, is_thinking

                # in between

                if game.is_finished():
                    break

                move = new_minimax_ab(board=game, depth=difficulty, player=turn, opponent=other, starting=True,
                                      last_move=last_move)

                game.push_move(turn, move)
                print('cpu played', move)
                last_move = move

                turn, other = other, turn
                is_thinking, is_player = is_player, is_thinking

                if not local_friendly:
                    dump_info()

        print('finished checking for mouse')

    print('finished checking for input')

    if autoplay:
        if not game.is_finished():
            move = new_minimax_ab(board=game, depth=difficulty, player=turn, opponent=other, starting=True,
                                  last_move=last_move)

            game.push_move(turn, move)

            print(f'{turn} played', move)
            last_move = move

            turn, other = other, turn

    if first_exposure:
        Thread(target=display_image).start()
        first_exposure = False

pg.quit()
print('winner:', game.winner())
print(game.calc_score(game.winner()))
pg.image.save(n, 'finished game.png')