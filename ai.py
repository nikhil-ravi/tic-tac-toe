import copy
from board import Board
import numpy as np
from random import choice


class AI:
    def __init__(self, level=1, player=-1):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_squares = board.get_empty_squares()
        return tuple(choice(empty_squares))

    def minimax(self, board, maximizing):
        case = board.final_state()
        if case == 1:
            return 1, None
        elif case == -1:
            return -1, None
        elif board.is_full():
            return 0, None

        if maximizing:
            max_eval = -2
            best_move = None
            empty_squares = board.get_empty_squares()
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, - self.player)
                eval, _ = self.minimax(temp_board, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                if max_eval == 1:
                    break
            return max_eval, best_move
        elif not maximizing:
            min_eval = 2
            best_move = None
            empty_squares = board.get_empty_squares()
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval, _ = self.minimax(temp_board, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
                if min_eval == -1:
                    break
            return min_eval, best_move

    def eval(self, main_board: Board):

        if self.level == 0:  # random choice
            move = self.rnd(main_board)
        else:  # minimax algorithm
            eval, move = self.minimax(main_board, False)
            print(f"The AI has chosen the move {move} with an evaluation of {eval}")
        return move
