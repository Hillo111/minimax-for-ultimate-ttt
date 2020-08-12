from game import *
import numpy as np


def new_minimax_ab(board, depth, player, opponent, alpha=-np.inf, beta=np.inf, maximizing=True, starting=False,
                   last_move=None, initial_depth=81):

    if board.is_finished() or depth <= 0:
        return board.calc_score(player, turn_amount=initial_depth - depth)

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

            evaluation = new_minimax_ab(board_copy, depth - 1, player, opponent, alpha, beta, False, last_move=move,
                                        initial_depth=initial_depth)

            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move

            alpha = max(evaluation, alpha)

            if beta <= alpha:
                break

        if starting:
            return best_move, max_eval

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

            evaluation = new_minimax_ab(board_copy, depth - 1, player, opponent, alpha, beta, True, last_move=move,
                                        initial_depth=initial_depth)

            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(evaluation, beta)

            if beta <= alpha:
                break

        if starting:
            return best_move, min_eval
        return min_eval