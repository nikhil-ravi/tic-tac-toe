from typing import Optional
from constants import *
from dataclasses import dataclass
from pydantic import BaseModel, ValidationError, validator


class Move(BaseModel):
    move: int

    @validator("move")
    def move_square_should_be_valid(cls, v:int) -> int:
        """Check whether the move involves one of the 9 squares indexed 0...8

        Args:
            v (int): The index of the square.

        Raises:
            ValueError: The index should be in 0...8 (inclusive).

        Returns:
            int: The valid square index.
        """
        if not 0 <= v <= SQUARES - 1:
            raise ValueError(
                f"Move must be between 0 and {SQUARES - 1}. {v} was passed."
            )
        return v

    @property
    def row(self):
        return self.move // ROWS

    @property
    def col(self):
        return self.move % COLS


def rowcol_to_move(row: int, col: int) -> Move:
    """Converts row, col representation to a Move dataclass.
    
    Args:
        row (int): The row index.
        col (int): The column index.
    
    Returns:
        Move: The converted Move dataclass instance.
    """
    return Move(move=row * ROWS + col)


class Board:
    """Maintains the state of the board of the current game."""

    def __init__(self):
        self.playerState = {1: 0, -1: 0}
        self.squares = self._get_board_state()
        self.winningStates = [
            int("111000000", 2),
            int("000111000", 2),
            int("000000111", 2),
            int("100100100", 2),
            int("010010010", 2),
            int("001001001", 2),
            int("100010001", 2),
            int("001010100", 2),
        ]
        self.moveLog = []
        self.whereWin = None

    def _get_board_state(self):
        return self.playerState[1] | self.playerState[-1]

    def final_state(self) -> Optional[int]:
        """Returns the winning player's ID if there is a win. In case of a draw,
        returns 0.

        Returns:
            Optional[int]: The winning player's ID if there is a win or 0 in case
            of a draw.
        """
        if self.moveLog:  # Check for wins in rows, cols, diags
            _, player = self.moveLog[-1]
            for idx, winningState in enumerate(self.winningStates):
                if (self.playerState[player] & winningState) == winningState:
                    self.whereWin = idx
                    return player
            # If full return Draw
            if self.squares == 511:
                return 0
            else:
                return None
        else:  # Still going
            return None

    def mark_move(self, move: Move, player: int):
        """Update the state of the board upon a move.

        Args:
            move (Move): The move to be filled.
            player (int): The player's ID which needs to be added to the state
                at row and col.
        """
        if not 0 <= move.move <= SQUARES - 1:
            raise ValueError(
                f"Move must be between 0 and {SQUARES-1}. {move.move} was passed."
            )
        self.moveLog.append((move, player))
        self.playerState[player] |= 1 << SQUARES - (move.move + 1)
        self.squares = self._get_board_state()

    def undo(self):
        """Update the state of the board upon an undo."""
        move, player = self.moveLog.pop()
        self.playerState[player] &= ~(1 << SQUARES - (move.move + 1))
        self.squares = self._get_board_state()

    def is_empty_square(self, square: int) -> bool:
        """Check if a square is empty.
        Args:
            square (int): The square to be checked.
        
        Returns:
            bool: True if the square is empty, False otherwise.
        """
        return ~self.squares & (1 << SQUARES - (square + 1))

    def is_full(self) -> bool:
        """Check if all the squares on the board have been filled.
        
        Returns:
            bool: True if all the squares have been filled, False otherwise.
        """
        return self.squares == 511

    def is_empty(self) -> bool:
        """Check if none of the squares on the board have been filled.
        
        Returns:
            bool: True if none of the squares have been filled, False otherwise.
        """
        return self.squares == 0

    def get_empty_squares(self) -> list[int]:
        """Get the indices of empty squares on the board.
        
        Returns:
            list[int]: The indices of empty squares on the board.
        """
        unset_bits = []
        for i in range(SQUARES):
            if not self.squares & (1 << SQUARES - (i + 1)):
                unset_bits.append(i)
        return unset_bits
