import pygame as pg
import numpy as np

pg.init()
pg.font.init()


class Game:
    check_length = 3

    def __init__(self):
        self.board = np.array([
            np.array([' ', ' ', ' ']),
            np.array([' ', ' ', ' ']),
            np.array([' ', ' ', ' ']),
        ])

        self.computer = 'x'
        self.player = 'o'

    def display(self, pixels: int, x: pg.Surface, o: pg.Surface, bg: pg.Surface = None):
        if bg is None:
            bg = pg.Surface((pixels, pixels))
            bg.fill((255, 255, 255))

        bg = pg.transform.scale(bg, (pixels, pixels))

        cellSize = pixels // 3

        x_img = pg.transform.scale(x, (cellSize, cellSize))
        o_img = pg.transform.scale(o, (cellSize, cellSize))

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                pos_x, pos_y = x * cellSize, y * cellSize
                if self.board[y][x] == 'x':
                    bg.blit(x_img, [pos_x, pos_y])
                if self.board[y][x] == 'o':
                    bg.blit(o_img, [pos_x, pos_y])

        for i in range(1, 3):
            pg.draw.line(bg, (0, 0, 0), [0, i * cellSize], [pixels, i * cellSize], 2)
            pg.draw.line(bg, (0, 0, 0), [i * cellSize, 0], [i * cellSize, pixels], 2)

        return bg

    def legal_moves(self, last_move=None):
        moves = []
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == ' ':
                    moves.append([x, y])

        return moves

    def push_move(self, char: str, pos: [int, int]):
        self.board[pos[1]][pos[0]] = char

    def __repr__(self):
        ch = ''
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                ch += ' ' + self.board[y][x]
                ch += ' |' if x < len(self.board[y]) - 1 else ''
            ch += '\n' + '----' * len(self.board[y]) + '\n' if y < len(self.board) - 1 else ''
        return ch

    def winner(self, neither=None):
        dirs = [[1, 0], [0, 1], [1, 1], [-1, 1]]

        check_length = Game.check_length

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                original = self.board[y][x]

                if original == ' ':
                    continue

                for d in dirs:
                    if not (0 <= x + (check_length - 1) * d[0] < len(self.board[y]) and 0 <= y + (check_length - 1) * d[1] < len(self.board)):
                        continue

                    equal = True
                    for i in range(check_length):
                        if self.board[y + d[1] * i][x + d[0] * i] != original:
                            equal = False
                            break

                    if equal:
                        if original != neither:
                            return original
        return None

    def is_finished(self):
        if self.winner() is not None:
            return True

        if len(self.legal_moves()) <= 0:
            return True

        return False

    def calc_score(self, piece):
        if self.winner() is not None:
            if self.winner() == piece:
                return len(self.legal_moves()) + 1
            else:
                return -len(self.legal_moves()) - 1
        else:
            return 0


class UltimateTicTacToe:
    def __init__(self):
        region = np.array([
            np.array([' ', ' ', ' ']),
            np.array([' ', ' ', ' ']),
            np.array([' ', ' ', ' ']),
        ])

        self.board = np.array([
            np.array([region, region, region]),
            np.array([region, region, region]),
            np.array([region, region, region]),
        ])

        self.won_boards = np.array([
            np.array([' ', ' ', ' ']),
            np.array([' ', ' ', ' ']),
            np.array([' ', ' ', ' '])
        ])

        self.full = 'f'

    def picture(self, xs: pg.Surface, os: pg.Surface, tie: pg.Surface, pixels: int, background: pg.Surface = None,
                last_move=None, is_computer=False, is_player=False):
        print('entered getting picture')

        def blit_alpha(target, source, location, opacity):
            x = location[0]
            y = location[1]
            temp = pg.Surface((source.get_width(), source.get_height())).convert()
            temp.blit(target, (-x, -y))
            temp.blit(source, (0, 0))
            temp.set_alpha(opacity)
            target.blit(temp, location)

        print('defined blit alpha')

        smaller_cell_size = pixels // 9
        larger_cell_size = pixels // 3

        large_x = pg.transform.scale(xs, (larger_cell_size, larger_cell_size))
        small_x = pg.transform.scale(xs, (smaller_cell_size, smaller_cell_size))
        large_o = pg.transform.scale(os, (larger_cell_size, larger_cell_size))
        small_o = pg.transform.scale(os, (smaller_cell_size, smaller_cell_size))

        tie = pg.transform.scale(tie, (larger_cell_size, larger_cell_size))

        print('defined images')

        opacity = 255

        if background is None:
            background = pg.Surface((pixels, pixels))
            background.fill((255, 255, 255))
        else:
            background = pg.transform.scale(background, (pixels, pixels))

        print('set background')

        if last_move is not None:
            surface = pg.Surface((smaller_cell_size, smaller_cell_size))
            surface.fill((0, 255, 0))
            surface.set_alpha(255)

            move = last_move
            pos_x, pos_y = move[0][0] * larger_cell_size + move[1][0] * smaller_cell_size, move[0][1] * larger_cell_size + move[1][1] * smaller_cell_size
            background.blit(surface, (pos_x, pos_y))

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):

                local = self.board[y][x]
                pos_x, pos_y = x * larger_cell_size, y * larger_cell_size

                for sub_y in range(len(local)):
                    for sub_x in range(len(local[sub_y])):
                        sub_pos_x, sub_pos_y = pos_x + sub_x * smaller_cell_size, pos_y + sub_y * smaller_cell_size

                        if local[sub_y][sub_x] == 'x':
                            background.blit(small_x, (sub_pos_x, sub_pos_y))
                        if local[sub_y][sub_x] == 'o':
                            background.blit(small_o, (sub_pos_x, sub_pos_y))

                        print('blitted smaller images')

                if self.won_boards[y][x] == 'x':
                    # background.blit(large_x, (pos_x, pos_y))
                    blit_alpha(background, large_x, (pos_x, pos_y), opacity)
                if self.won_boards[y][x] == 'o':
                    blit_alpha(background, large_o, (pos_x, pos_y), opacity)
                if self.won_boards[y][x] == self.full:
                    blit_alpha(background, tie, (pos_x, pos_y), opacity)

                print('blitted larger images')

        surface = pg.Surface((smaller_cell_size, smaller_cell_size))
        surface.fill((255, 255, 0))
        surface.set_alpha(255 if is_player else 0)

        print('defined surface')

        if not self.is_finished():
            for move in self.legal_moves(last_move):
                pos_x, pos_y = move[0][0] * larger_cell_size + move[1][0] * smaller_cell_size, move[0][1] * larger_cell_size + move[1][1] * smaller_cell_size
                background.blit(surface, (pos_x, pos_y))

        print('placed surfaces')

        for i in range(1, 9):
            width = 5 if i % 3 == 0 else 2
            pg.draw.line(background, (0, 0, 0), [0, i * smaller_cell_size], [pixels, i * smaller_cell_size], width)
            pg.draw.line(background, (0, 0, 0), [i * smaller_cell_size, 0], [i * smaller_cell_size, pixels], width)

        print('drew lines')

        try:
            font = pg.font.SysFont('Sans', 20)
        except:
            print('could not create font')
            print('returning background')
            return background
        print('created font')
        text = ''
        print(is_player, is_computer)
        if is_computer:
            text = "CPU's turn"  # 'Ход компьютера'
        if is_player:
            text = "Player's turn"  # 'Ход игрока'
        text = font.render(text, 20, (0, 0, 0))
        background.blit(text, (5, pixels - 37))
        print('blited text')

        print('returning background')
        return background

    def legal_moves(self, last_move: [[int, int], [int, int]] = None):
        moves = []
        if last_move is None:
            for ny in range(len(self.board)):
                for nx in range(len(self.board[ny])):
                    if self.won_boards[ny][nx] != ' ':
                        continue

                    local_board = self.board[ny][nx]

                    for sub_ny in range(len(local_board)):
                        for sub_nx in range(len(local_board[sub_ny])):
                            if local_board[sub_ny][sub_nx] == ' ':
                                moves.append([[nx, ny], [sub_nx, sub_ny]])

        else:
            x, y = last_move[0][0], last_move[0][1]
            sub_x, sub_y = last_move[1][0], last_move[1][1]

            if self.won_boards[sub_y][sub_x] != ' ':
                for ny in range(len(self.board)):
                    for nx in range(len(self.board[ny])):
                        if self.won_boards[ny][nx] != ' ':
                            continue

                        local_board = self.board[ny][nx]

                        for sub_ny in range(len(local_board)):
                            for sub_nx in range(len(local_board[sub_ny])):
                                if local_board[sub_ny][sub_nx] == ' ':
                                    moves.append([[nx, ny], [sub_nx, sub_ny]])
            else:
                board = self.board[sub_y][sub_x]
                for ny in range(len(board)):
                    for nx in range(len(board[ny])):
                        if board[ny][nx] == ' ':
                            moves.append([[sub_x, sub_y], [nx, ny]])

        return moves

    def update_won_boards(self, cell: [int, int] = None):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.won_boards[y][x] != ' ':
                    continue

                custom_game = Game()
                custom_game.board = self.board[y][x]

                if custom_game.is_finished():
                    if custom_game.winner() is not None:
                        self.won_boards[y][x] = custom_game.winner()
                    else:
                        self.won_boards[y][x] = self.full

    def push_move(self, piece: str, move: [[int, int], [int, int]]):
        x, y = move[0][0], move[0][1]
        sub_x, sub_y = move[1][0], move[1][1]

        self.board[y][x][sub_y][sub_x] = piece

        self.update_won_boards(move[0])

    def winner(self):
        dirs = [[1, 0], [0, 1], [1, 1], [-1, 1]]

        check_length = 3

        for y in range(len(self.won_boards)):
            for x in range(len(self.won_boards[y])):
                original = self.won_boards[y][x]

                if original in (' ', self.full):
                    continue

                for d in dirs:
                    if not (0 <= x + (check_length - 1) * d[0] < len(self.won_boards[y]) and 0 <= y + (check_length - 1) * d[1] < len(self.won_boards)):
                        continue

                    equal = True
                    for i in range(check_length):
                        if self.won_boards[y + d[1] * i][x + d[0] * i] != original:
                            equal = False
                            break

                    if equal:
                        return original
        return None

    def is_finished(self):
        if self.winner() is not None:
            return True
        full = True
        for y in range(len(self.won_boards)):
            for x in range(len(self.won_boards[y])):
                if self.won_boards[y][x] == ' ':
                    full = False
                    break

        if full:
            return True

        return False

    @staticmethod
    def calc_twos(local_board, value: int, player, opponent):
        change = 0

        for y in range(len(local_board)):
            to_change = 0

            if local_board[y][0] == local_board[y][1] and local_board[y][2] == ' ':
                to_change = value

            if local_board[y][0] == local_board[y][2] and local_board[y][1] == ' ':
                to_change = value

            if local_board[y][1] == local_board[y][2] and local_board[y][0] == ' ':
                to_change = value

            if player in (local_board[y][1], local_board[y][2]):
                change += to_change

            if opponent in (local_board[y][1], local_board[y][2]):
                change -= to_change

        for x in range(len(local_board[0])):
            to_change = 0

            if local_board[0][x] == local_board[1][x] and local_board[2][x] == ' ':
                to_change = value

            if local_board[0][x] == local_board[2][x] and local_board[1][x] == ' ':
                to_change = value

            if local_board[1][x] == local_board[2][x] and local_board[0][x] == ' ':
                to_change = value

            if player in (local_board[1][x], local_board[2][x]):
                change += to_change

            if opponent in (local_board[1][x], local_board[2][x]):
                change -= to_change

        to_change = 0

        if local_board[0][0] == local_board[1][1] and local_board[2][2] == ' ':
            to_change = value

        if local_board[0][0] == local_board[2][2] and local_board[1][1] == ' ':
            to_change = value

        if player in (local_board[0][0], local_board[2][2]):
            change += to_change

        if opponent in (local_board[0][0], local_board[2][2]):
            change -= to_change

        if local_board[2][0] == local_board[1][1] and local_board[0][2] == ' ':
            to_change = value

        if local_board[2][0] == local_board[0][2] and local_board[1][1] == ' ':
            to_change = value

        if player in (local_board[2][0], local_board[0][2]):
            change += to_change

        if opponent in (local_board[2][0], local_board[0][2]):
            change -= to_change

        return change

    @staticmethod
    def calc_block(local_board, value, player, opponent):
        change = 0

        for y in range(len(local_board)):
            to_change = 0

            if local_board[y][0] == local_board[y][1] == opponent and local_board[y][2] == player:
                to_change = value

            if local_board[y][0] == local_board[y][2] == opponent and local_board[y][1] == player:
                to_change = value

            if local_board[y][1] == local_board[y][2] == opponent and local_board[y][0] == player:
                to_change = value

            change += to_change

        for x in range(len(local_board[0])):
            to_change = 0

            if local_board[0][x] == local_board[1][x] == opponent and local_board[2][x] == player:
                to_change = value

            if local_board[0][x] == local_board[2][x] == opponent and local_board[1][x] == player:
                to_change = value

            if local_board[1][x] == local_board[2][x] == opponent and local_board[0][x] == player:
                to_change = value

            change += to_change

        to_change = 0

        if local_board[0][0] == local_board[1][1] == opponent and local_board[2][2] == player:
            to_change = value

        if local_board[0][0] == local_board[2][2] == opponent and local_board[1][1] == player:
            to_change = value

        change += to_change

        if local_board[2][0] == local_board[1][1] == opponent and local_board[0][2] == player:
            to_change = value

        if local_board[2][0] == local_board[0][2] == opponent and local_board[1][1] == player:
            to_change = value

        change += to_change

        return change

    def calc_score(self, player, value_board=None):
        if value_board is None:
            value_board = {'won 1': 100, 'won 2 in a row': 200, 'won game': 9999999999, '2 in a row': 5,
                           'blocked 2': 12, 'won block 2': 120}

        opponent = 'o' if player == 'x' else 'x'

        score = 0

        # Calculate score for individual boards based on the amount of "useful twos" they have

        for large_y in range(len(self.board)):
            for large_x in range(len(self.board[large_y])):
                local_board = self.board[large_y][large_x]
                if self.won_boards[large_y][large_x] != ' ':
                    continue

                score += self.calc_twos(local_board, value_board['2 in a row'], player, opponent)

        # Checking for single won boards

        for y in range(len(self.won_boards)):
            for x in range(len(self.won_boards[y])):
                if self.won_boards[y][x] == player:
                    score += value_board['won 1']

                if self.won_boards[y][x] == opponent:
                    score -= value_board['won 1']

        # Same algorithm as with the boards but now for whole game

        score += self.calc_twos(self.won_boards, value_board['won 2 in a row'], player, opponent)

        # If they win they get infinity points

        if self.winner() == player:
            score += value_board['won game']
        if self.winner() == opponent:
            score -= value_board['won game']

        # Smaller board blocking score
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                score += self.calc_block(self.board[y][x], value_board['blocked 2'], player, opponent)
                score -= self.calc_block(self.board[y][x], value_board['blocked 2'], opponent, player)

        # Won boards blocking score
        score += self.calc_block(self.won_boards, value_board['won block 2'], player, opponent)
        score -= self.calc_block(self.won_boards, value_board['won block 2'], opponent, player)

        return score
