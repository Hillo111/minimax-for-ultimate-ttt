from game import *
import numpy as np
import random


def new_minimax_ab(board, depth, player, opponent, alpha=-np.inf, beta=np.inf, maximizing=True, starting=False,
                   last_move=None):

    if board.is_finished() or depth <= 0:
        return board.calc_score(player)

    if maximizing:
        max_eval = -np.inf
        best_move = None

        for move in board.legal_moves(last_move):
            if type(board) == Game:
                board_copy = Game()
            else:
                board_copy = UltimateTicTacToe()
            board_copy.board = board.board.copy()

            board_copy.push_move(player, move)

            evaluation = new_minimax_ab(board_copy, depth - 1, player, opponent, alpha, beta, False, last_move=move)

            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move

            alpha = max(evaluation, alpha)

            if beta <= alpha:
                break

        if starting:
            print(f'maximum possible score within {depth} moves assuming optimal play:', max_eval)
            return best_move

        return max_eval

    else:
        min_eval = np.inf
        best_move = None

        for move in board.legal_moves(last_move):
            if type(board) == Game:
                board_copy = Game()
            else:
                board_copy = UltimateTicTacToe()
            board_copy.board = board.board.copy()

            board_copy.push_move(opponent, move)

            evaluation = new_minimax_ab(board_copy, depth - 1, player, opponent, alpha, beta, True, last_move=move)

            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(evaluation, beta)

            if beta <= alpha:
                break

        if starting:
            return best_move
        return min_eval


def anti_minimax_ab(board: Game, depth, player, opponent, alpha=-np.inf, beta=np.inf, maximizing=True, starting=False,
                    last_move=None):

    if board.is_finished() or depth <= 0:
        return board.calc_score(opponent)

    if maximizing:
        max_eval = -np.inf
        best_move = None

        for move in board.legal_moves(last_move):
            if type(board) == Game:
                board_copy = Game()
            else:
                board_copy = UltimateTicTacToe()
            board_copy.board = board.board.copy()

            board_copy.push_move(player, move)
            last_move = move
            evaluation = anti_minimax_ab(board_copy, depth - 1, player, opponent, alpha, beta, False, last_move=last_move)

            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move

            alpha = max(evaluation, alpha)

            if beta <= alpha:
                break

        if starting:
            return best_move

        return max_eval

    else:

        min_eval = np.inf
        best_move = None

        for move in board.legal_moves(last_move):
            if type(board) == Game:
                board_copy = Game()
            else:
                board_copy = UltimateTicTacToe()
            board_copy.board = board.board.copy()

            board_copy.push_move(opponent, move)

            last_move = move
            evaluation = anti_minimax_ab(board_copy, depth - 1, player, opponent, alpha, beta, True, last_move=last_move)

            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(evaluation, beta)

            if beta <= alpha:
                break

        if starting:
            return best_move

        return min_eval


def create_board(shape: (int, int)):
    ax = shape[0]
    ay = shape[1]

    board = []

    for y in range(ay):
        smaller = []
        for x in range(ax):
            smaller.append(' ')

        smaller = np.array(smaller)
        board.append(smaller)

    return np.array(board)


def play(board: Game, difficulty, player, computer):
    maxing = True

    steps = 5

    if difficulty == 'impossible':
        steps = 10
    if difficulty == 'baby':
        steps = 1

    if difficulty not in ('random', 'anti-impossible'):
        move = new_minimax_ab(board, steps, computer, player, starting=True)
    elif difficulty == 'random':
        move = random.choice(board.legal_moves())
    elif difficulty == 'anti-impossible':
        move = anti_minimax_ab(board, 10, computer, player, starting=True)

    return move


if __name__ == '__main__':
    game = Game()
    Game.check_length = 3

    game.board = create_board((3, 3))

    turn = 'x'
    other = 'x' if turn == 'o' else 'o'

    while not game.is_finished():
        print(game)

        m = int(input()) - 1

        move = [m % 3, m // 3]

        game.push_move(other, move)

        move = play(game, 'impossible', other, turn)

        print(turn, move)

        game.push_move(turn, move)