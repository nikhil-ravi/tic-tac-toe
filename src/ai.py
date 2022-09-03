import copy
from typing import Optional
from board import Board
import numpy as np
from random import choice


class AI:
    def __init__(self, level=1, player=-1):
        self.level = level
        self.player = player

    def rnd(self, board: Board) -> tuple[int, int]:
        """Choose a random empty square on the board for the next move.

        Returns:
            int: The row index of the chosen square.
            int: The column index of the chosen square
        """
        empty_squares = board.get_empty_squares()
        return tuple(choice(empty_squares))

    def minimax(
        self, board: Board, maximizing: bool
    ) -> tuple[int, Optional[tuple[int, int]]]:
        """Minimax algorithm to find the best move given the state of the board.

        Args:
            board (Board): The board for which to find the best move.
            maximizing (bool): Whether the AI is trying to maximize (when AI is
            player 1) or minimize (when AI is player -1) the score.

        Returns:
            int: The evaluation of the position. It is -1 when AI has a sure win,
            +1 when the player has a sure win and 0 otherwise.
            Optional[tuple[int,int]]: The row, col index of the best move.
        """
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
                temp_board.mark_square(row, col, -self.player)
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

    def eval(self, main_board: Board) -> tuple[int, int]:
        """Evaluates the best move for the given board state.
        
        Args:
            main_board: The main board state.
        
        Returns:
            int: The row index of the best move for the AI.
            int: The column index of the best move for the AI.
        """
        if self.level == 0:  # random choice
            move = self.rnd(main_board)
        else:  # minimax algorithm
            eval, move = self.minimax(main_board, False)
            print(f"The AI has chosen the move {move} with an evaluation of {eval}")
        return move
