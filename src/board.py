from typing import Optional
from constants import *
import numpy as np


class Board:
    """Maintains the state of the board of the current game."""
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_squares = self.squares
        self.marked_squares = 0
        self.rows = [0] * ROWS
        self.cols = [0] * COLS
        self.diag = 0
        self.antidiag = 0
        self.moveLog = []
        self.whereWin = [None, None, None, None]

    def final_state(self) -> Optional[int]:
        """Returns the winning player's ID if there is a win. In case of a draw,
        returns 0.
        
        Returns:
            Optional[int]: The winning player's ID if there is a win or 0 in case
            of a draw. 
        """
        if self.moveLog:
            row, col, player = self.moveLog[-1]
            toCheck = (self.rows[row], self.cols[col], self.diag, self.antidiag)
            for i, line in enumerate(toCheck):
                if abs(line) == ROWS:
                    if i == 0:
                        self.whereWin[i] = row
                    elif i == 1:
                        self.whereWin[i] = col
                    else:
                        self.whereWin[i] = True
                    return player
            if self.is_full():
                return 0
            else:
                return None
        else:
            return None

    def mark_square(self, row: int, col: int, player: int):
        """Update the state of the board upon a move. 

        Args:
            row (int): The row of the state to be updated.
            col (int): The column of the state to be updated.
            player (int): The player's ID which needs to be added to the state
                at row and col.
        """
        self.moveLog.append((row, col, player))
        self.squares[row, col] = player
        self.marked_squares += 1
        self.rows[row] += player
        self.cols[col] += player
        if row == col:
            self.diag += player
        if row + col == ROWS - 1:
            self.antidiag += player
    
    def undo(self):
        """Update the state of the board upon an undo."""
        row, col, player = self.moveLog.pop()
        self.squares[row, col] = 0
        self.marked_squares -= 1
        self.rows[row] -= player
        self.cols[col] -= player
        if row == col:
            self.diag -= player
        if row + col == ROWS - 1:
            self.antidiag -= player

    def is_empty_square(self, row, col):
        """Check if a square is empty."""
        return self.squares[row, col] == 0

    def is_full(self):
        """Check if all the squares on the board have been filled."""
        return self.marked_squares == 9

    def is_empty(self):
        """Check if none of the squares on the board have been filled."""
        return self.marked_squares == 0

    def get_empty_squares(self):
        """Get the indices (row, col) of empty squares on the board."""
        return np.stack(np.where(self.squares == 0), axis=-1).tolist()
