import pygame as pg
from game import UltimateTicTacToe
from other_minimax import new_minimax_ab
import numpy as np
import json
from threading import Thread

pg.init()

font = pg.font.SysFont('Sans', 20)


def play_game(screen: pg.Surface, going_first, autoplay, difficulty, x_img, o_img, tie_img, cellSize, threaded=False):
    largerCellSize = cellSize * 3

    game = UltimateTicTacToe()

    turn = 'x'
    other = 'o'

    last_move = None

    if not autoplay:
        is_thinking = going_first
        is_player = not going_first
    else:
        is_thinking, is_player = False, False

    run = True
    clock = pg.time.Clock()

    def blit_img():
        n = game.picture(x_img, o_img, tie_img, 450, font, None, last_move, is_thinking, is_player)

        try:
            screen.blit(n, (0, 0))
        except:
            return

        pg.display.flip()

    def display_image():
        while run:
            blit_img()

            try:
                pg.display.flip()
            except pg.error:
                break
            clock.tick(60)

    first_display = True

    cpu = False

    def get_input():
        x, y = map(int, pg.mouse.get_pos())
        larger_x = x // largerCellSize
        larger_y = y // largerCellSize

        smaller_x = (x - larger_x * largerCellSize) // cellSize
        smaller_y = (y - larger_y * largerCellSize) // cellSize

        move = [[larger_x, larger_y], [smaller_x, smaller_y]]
        return move

    def cpu_play():
        nonlocal turn, other, is_player, is_thinking, last_move, cpu
        move, soon_score = new_minimax_ab(game, difficulty, turn, other, starting=True, last_move=last_move)
        game.push_move(turn, move)

        turn, other = other, turn
        is_player, is_thinking = is_thinking, is_player
        last_move = move

        cpu = False

    while run:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False
                pg.display.quit()
                break

            if e.type == pg.MOUSEBUTTONDOWN:
                if game.is_finished():
                    break

                move = get_input()
                if move in game.legal_moves(last_move) and is_player:
                    game.push_move(turn, move)
                    last_move = move
                    is_player, is_thinking = False, True
                    turn, other = other, turn

                    if threaded:
                        Thread(target=cpu_play).start()
                    else:
                        cpu_play()

        if first_display:
            Thread(target=display_image).start()
            first_display = False

        if autoplay and not game.is_finished() and not cpu:
            cpu = True
            if threaded:
                Thread(target=cpu_play).start()
            else:
                cpu_play()

        if going_first:
            going_first = False
            if threaded:
                Thread(target=cpu_play).start()
            else:
                cpu_play()


if __name__ == '__main__':
    screen = pg.display.set_mode((450, 450))

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

    play_game(screen, True, False, 4, cx, co, tie, 50)